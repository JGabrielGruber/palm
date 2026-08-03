"""0.61.1 — seat report protocol + dynamic walk + raw sampling."""

from __future__ import annotations

from typing import Any

from palm.system.log import reset_system_log_for_tests
from palm.system.runtime.base import BaseRuntime
from palm.system.supervisor import CallableSystemService, SystemSupervisor
from palm.system.vitality import (
    KIND_OTHER,
    KIND_PLANE,
    LINEAGE_NATIVE,
    LINEAGE_SAMPLED,
    SEAT_BOOT_MEMBERSHIP,
    SEAT_EXECUTION,
    SEAT_REPORT_SCHEMA,
    SEAT_SESSION_PLANE,
    SEAT_SUPERVISOR,
    SEAT_SYSTEM_LOG,
    SEAT_WAIT_PLANE,
    SEAT_WORK_PLANE,
    STATE_ABSENT,
    STATE_OK,
    ProbeCatalog,
    SeatProbe,
    SeatReport,
    WalkOptions,
    coerce_report,
    default_probe_catalog,
    discover_seats,
    index_by_seat_id,
    seat_walk,
    supervisor_service_seat_id,
    walk_result,
)


# ── unit: SeatReport ─────────────────────────────────────────────────────────


def test_seat_report_roundtrip_and_schema() -> None:
    r = SeatReport.ok(
        "wait_plane",
        KIND_PLANE,
        load={},
        lineage=LINEAGE_SAMPLED,
        meta={"sample_source": "doctor_snapshot", "raw": {"open_wait_owners": 2}},
    )
    d = r.to_dict()
    assert d["schema"] == SEAT_REPORT_SCHEMA
    assert d["seat_id"] == "wait_plane"
    assert d["present"] is True
    assert d["state"] == STATE_OK
    assert d["lineage"] == LINEAGE_SAMPLED
    assert d["meta"]["raw"]["open_wait_owners"] == 2
    back = SeatReport.from_dict(d)
    assert back.seat_id == r.seat_id
    assert back.meta["raw"] == r.meta["raw"]


def test_seat_report_absent_never_present() -> None:
    r = SeatReport.absent("work_plane", KIND_PLANE, reason="not_attached")
    assert r.present is False
    assert r.state == STATE_ABSENT
    assert "not_attached" in r.notes


def test_seat_report_coerces_false_present_ok() -> None:
    r = SeatReport(
        seat_id="x",
        kind=KIND_OTHER,
        present=False,
        state=STATE_OK,
    )
    assert r.state == STATE_ABSENT


def test_coerce_report_fills_defaults() -> None:
    r = coerce_report({"state": "ok", "load": {"n": 1}}, default_seat_id="s1")
    assert r.seat_id == "s1"
    assert r.present is True
    assert r.load["n"] == 1


# ── unit: probe catalog ──────────────────────────────────────────────────────


def test_probe_catalog_register_clone_extend() -> None:
    cat = ProbeCatalog()
    cat.register(
        SeatProbe(
            seat_id="alpha",
            kind=KIND_OTHER,
            resolve=lambda inst: getattr(inst, "alpha", None),
            order=1,
        )
    )
    clone = cat.clone()
    clone.register(
        SeatProbe(
            seat_id="beta",
            kind=KIND_OTHER,
            resolve=lambda inst: None,
            order=2,
        )
    )
    assert "alpha" in cat
    assert "beta" not in cat
    assert clone.seat_ids() == ["alpha", "beta"]


def test_default_probe_catalog_has_core_seeds() -> None:
    ids = set(default_probe_catalog().seat_ids())
    for sid in (
        SEAT_WAIT_PLANE,
        SEAT_SESSION_PLANE,
        SEAT_WORK_PLANE,
        SEAT_SUPERVISOR,
        SEAT_EXECUTION,
        SEAT_SYSTEM_LOG,
        SEAT_BOOT_MEMBERSHIP,
    ):
        assert sid in ids


# ── lean shell: honest absent ────────────────────────────────────────────────


class _LeanShell:
    """Minimal duck-typed instance with no planes attached."""

    is_started = False


def test_walk_lean_shell_honest_absent() -> None:
    reset_system_log_for_tests()
    reports = discover_seats(_LeanShell(), expand_supervisor_services="never")
    by_id = index_by_seat_id(reports)

    assert by_id[SEAT_WAIT_PLANE].state == STATE_ABSENT
    assert by_id[SEAT_WAIT_PLANE].present is False
    assert by_id[SEAT_SESSION_PLANE].state == STATE_ABSENT
    assert by_id[SEAT_WORK_PLANE].state == STATE_ABSENT
    assert by_id[SEAT_SUPERVISOR].state == STATE_ABSENT
    assert by_id[SEAT_BOOT_MEMBERSHIP].state == STATE_ABSENT

    # Process log still present (process-wide seat); raw-sampled public API.
    assert by_id[SEAT_SYSTEM_LOG].present is True
    assert by_id[SEAT_SYSTEM_LOG].lineage == LINEAGE_SAMPLED
    assert "raw" in by_id[SEAT_SYSTEM_LOG].meta

    # Execution absent: lean shell has no port methods.
    assert by_id[SEAT_EXECUTION].state == STATE_ABSENT


def test_walk_no_fake_green_for_missing_planes() -> None:
    reports = discover_seats(_LeanShell())
    for r in reports:
        if r.seat_id in (SEAT_WAIT_PLANE, SEAT_SESSION_PLANE, SEAT_WORK_PLANE):
            assert r.present is False
            assert r.state == STATE_ABSENT


# ── full BaseRuntime attach ──────────────────────────────────────────────────


def test_walk_started_base_runtime_seats_present() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=True)
    try:
        result = walk_result(rt)
        by_id = result.by_id()

        for sid in (
            SEAT_WAIT_PLANE,
            SEAT_SESSION_PLANE,
            SEAT_WORK_PLANE,
            SEAT_SUPERVISOR,
            SEAT_EXECUTION,
            SEAT_SYSTEM_LOG,
            SEAT_BOOT_MEMBERSHIP,
        ):
            assert sid in by_id, f"missing seat {sid}"
            assert by_id[sid].present is True, f"{sid} should be present"
            assert by_id[sid].state == STATE_OK, f"{sid} state={by_id[sid].state}"

        # Boot membership saw phases (raw under meta).
        boot = by_id[SEAT_BOOT_MEMBERSHIP]
        assert boot.lineage == LINEAGE_SAMPLED
        assert boot.meta.get("raw", {}).get("count", 0) > 0

        # Planes / supervisor / log: raw public APIs — product presents.
        assert by_id[SEAT_WAIT_PLANE].lineage == LINEAGE_SAMPLED
        assert by_id[SEAT_WAIT_PLANE].meta.get("sample_source") == "doctor_snapshot"
        assert "raw" in by_id[SEAT_WAIT_PLANE].meta
        assert by_id[SEAT_SESSION_PLANE].lineage == LINEAGE_SAMPLED
        assert by_id[SEAT_WORK_PLANE].lineage == LINEAGE_SAMPLED
        assert by_id[SEAT_WORK_PLANE].meta.get("sample_source") == "status"
        assert by_id[SEAT_SUPERVISOR].lineage == LINEAGE_SAMPLED
        assert by_id[SEAT_SYSTEM_LOG].lineage == LINEAGE_SAMPLED
        assert "capacity" in (by_id[SEAT_SYSTEM_LOG].meta.get("raw") or {})

        # Dynamic supervisor services (work_drain, outbox with outbox flag).
        service_ids = [
            r.seat_id for r in result.reports if r.seat_id.startswith("supervisor.")
        ]
        assert supervisor_service_seat_id("work_drain") in service_ids
        assert supervisor_service_seat_id("outbox") in service_ids
        for sid in service_ids:
            assert by_id[sid].present is True
            assert by_id[sid].lineage == LINEAGE_SAMPLED
            assert "raw" in by_id[sid].meta

        assert result.present_count >= 7
        assert result.error_count == 0
    finally:
        rt.stop()


def test_seat_walk_dicts_schema() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        rows = seat_walk(rt)
        assert all(row["schema"] == SEAT_REPORT_SCHEMA for row in rows)
        assert any(row["seat_id"] == SEAT_WAIT_PLANE for row in rows)
    finally:
        rt.stop()


def test_public_last_boot_walk_property() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    assert rt.last_boot_walk is None
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        assert rt.last_boot_walk is not None
        assert len(rt.last_boot_walk) > 0
    finally:
        rt.stop()


# ── detach / dynamics ────────────────────────────────────────────────────────


def test_detach_wait_plane_becomes_absent() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        before = index_by_seat_id(discover_seats(rt))
        assert before[SEAT_WAIT_PLANE].present is True

        # Detach without full stop — simulate composition change.
        if rt.wait_plane is not None:
            rt.wait_plane.detach()
        rt._wait_plane = None

        after = index_by_seat_id(discover_seats(rt))
        assert after[SEAT_WAIT_PLANE].state == STATE_ABSENT
        assert after[SEAT_WAIT_PLANE].present is False
        # Others still present.
        assert after[SEAT_SESSION_PLANE].present is True
    finally:
        rt.stop()


def test_supervisor_service_discovered_dynamically() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        assert rt.supervisor is not None
        custom = CallableSystemService("custom_loop", status=lambda: {"ticks": 3})
        rt.supervisor.register(custom)

        by_id = index_by_seat_id(discover_seats(rt))
        sid = supervisor_service_seat_id("custom_loop")
        assert sid in by_id
        assert by_id[sid].present is True
        assert by_id[sid].meta.get("raw", {}).get("ticks") == 3
    finally:
        rt.stop()


def test_expand_supervisor_services_never() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=True)
    try:
        reports = discover_seats(
            rt, WalkOptions(expand_supervisor_services="never")
        )
        assert all(not r.seat_id.startswith("supervisor.") for r in reports)
        assert any(r.seat_id == SEAT_SUPERVISOR for r in reports)
    finally:
        rt.stop()


# ── native vs raw lineage ────────────────────────────────────────────────────


def test_native_seat_report_preferred_over_raw() -> None:
    class _NativePlane:
        def doctor_snapshot(self) -> dict[str, Any]:
            return {"wait_plane_attached": True, "open_wait_owners": 99}

        def seat_report(self) -> dict[str, Any]:
            return {
                "schema": SEAT_REPORT_SCHEMA,
                "seat_id": SEAT_WAIT_PLANE,
                "kind": KIND_PLANE,
                "present": True,
                "state": STATE_OK,
                "load": {"open_wait_owners": 1, "native": True},
                "notes": ["from_native"],
                "lineage": LINEAGE_NATIVE,
            }

    class _Shell:
        is_started = True
        wait_plane = _NativePlane()
        session_plane = None
        work_plane = None
        supervisor = None
        execution = None
        last_boot_walk = None

    # Only wait_plane + process log (+ execution absent)
    cat = default_probe_catalog()
    reports = discover_seats(
        _Shell(),
        WalkOptions(
            catalog=cat,
            expand_supervisor_services="never",
            skip_seat_ids=frozenset(
                {
                    SEAT_SESSION_PLANE,
                    SEAT_WORK_PLANE,
                    SEAT_SUPERVISOR,
                    SEAT_EXECUTION,
                    SEAT_BOOT_MEMBERSHIP,
                    SEAT_SYSTEM_LOG,
                }
            ),
        ),
    )
    by_id = index_by_seat_id(reports)
    wait = by_id[SEAT_WAIT_PLANE]
    assert wait.lineage == LINEAGE_NATIVE
    assert wait.load.get("native") is True
    assert wait.load.get("open_wait_owners") == 1
    assert "from_native" in wait.notes


def test_system_log_and_supervisor_have_no_seat_report() -> None:
    """Seats expose public API; vitality samples raw — product presents."""
    reset_system_log_for_tests()
    from palm.system.log import get_system_log

    log = get_system_log()
    assert not hasattr(log, "seat_report") or not callable(
        getattr(type(log), "seat_report", None)
    )
    assert log.capacity >= 10
    assert isinstance(log.record_count, int)

    sup = SystemSupervisor()
    sup.register(CallableSystemService("x"))
    assert not hasattr(SystemSupervisor, "seat_report")
    assert "x" in sup.status()["registered"]


# ── custom probe extension ───────────────────────────────────────────────────


def test_custom_probe_extends_discovery() -> None:
    class _Shell:
        is_started = True
        custom_seat = object()

    cat = ProbeCatalog()
    cat.register(
        SeatProbe(
            seat_id="custom_seat",
            kind=KIND_OTHER,
            resolve=lambda inst: getattr(inst, "custom_seat", None),
            report=lambda inst, seat: SeatReport.ok(
                "custom_seat",
                KIND_OTHER,
                load={"found": True},
                lineage=LINEAGE_NATIVE,
            ),
            order=1,
        )
    )
    reports = discover_seats(
        _Shell(),
        WalkOptions(catalog=cat, expand_supervisor_services="never"),
    )
    assert len(reports) == 1
    assert reports[0].seat_id == "custom_seat"
    assert reports[0].load["found"] is True


def test_probe_error_becomes_error_report() -> None:
    def _bad_resolve(inst: Any) -> Any:
        raise RuntimeError("boom")

    cat = ProbeCatalog()
    cat.register(
        SeatProbe(
            seat_id="bad",
            kind=KIND_OTHER,
            resolve=_bad_resolve,
            order=1,
        )
    )
    reports = discover_seats(
        object(),
        WalkOptions(catalog=cat, expand_supervisor_services="never"),
    )
    assert len(reports) == 1
    assert reports[0].state == "error"
    assert "boom" in reports[0].notes[0]


# ── observation purity ───────────────────────────────────────────────────────


def test_walk_does_not_start_supervisor_services() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=True)
    try:
        assert rt.supervisor is not None
        assert rt.supervisor.status()["running_count"] == 0
        discover_seats(rt)
        assert rt.supervisor.status()["running_count"] == 0
    finally:
        rt.stop()


def test_system_package_exports_vitality_importable() -> None:
    import palm.system.vitality as vit

    assert vit.SEAT_REPORT_SCHEMA == "palm.seat_report/1"
    assert callable(vit.discover_seats)
