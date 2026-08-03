"""
Seat-report adapters — transitional bridge from status / doctor_snapshot (0.61.1).

**Architecture stance (0.61 plan):** adapters are **not** the vitality foundation.
Forward work (projection, registry, inspect present) implements as if they were
absent — discover + native reports + presence truth. Interpretation of doctor
fields belongs in product present, not system eyes law.

Until seats grow native ``seat_report``, these bridges remain **honest residue**
with ``lineage: adapter`` and ``meta.adapter_source``. Prefer native when present.
Do not deepen adapter smarts here.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from palm.system.vitality.protocol import try_native_report
from palm.system.vitality.report import SeatReport, coerce_report
from palm.system.vitality.schema import (
    KIND_BOOT,
    KIND_LOG,
    KIND_PLANE,
    KIND_PORT,
    KIND_SUPERVISOR,
    KIND_SUPERVISOR_SERVICE,
    LINEAGE_ADAPTER,
    LINEAGE_NATIVE,
    SEAT_BOOT_MEMBERSHIP,
    SEAT_EXECUTION,
    SEAT_SESSION_PLANE,
    SEAT_SUPERVISOR,
    SEAT_SYSTEM_LOG,
    SEAT_WAIT_PLANE,
    SEAT_WORK_PLANE,
    STATE_DEGRADED,
    STATE_OK,
    supervisor_service_seat_id,
)


def _adapter_meta(source: str, **extra: Any) -> dict[str, Any]:
    meta: dict[str, Any] = {"adapter_source": source}
    meta.update({k: v for k, v in extra.items() if v is not None})
    return meta


def _pick(mapping: Mapping[str, Any], *keys: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in keys:
        if key in mapping and mapping[key] is not None:
            out[key] = mapping[key]
    return out


def prefer_native(
    seat: Any,
    *,
    seat_id: str,
    kind: str,
    adapter: Callable[[], SeatReport],
) -> SeatReport:
    """Use native ``seat_report`` when present; otherwise run *adapter*."""
    native = try_native_report(seat)
    if native is not None:
        report = coerce_report(
            native,
            default_seat_id=seat_id,
            default_kind=kind,
            default_lineage=LINEAGE_NATIVE,
        )
        # Native must not claim adapter lineage by accident.
        if report.lineage != LINEAGE_NATIVE:
            report = SeatReport(
                seat_id=report.seat_id or seat_id,
                kind=report.kind or kind,
                present=report.present,
                state=report.state,
                load=dict(report.load),
                notes=list(report.notes),
                lineage=LINEAGE_NATIVE,
                schema=report.schema,
                meta={**report.meta, "lineage_forced": "native"},
                sample_ts=report.sample_ts,
            )
        if report.seat_id != seat_id:
            report = SeatReport(
                seat_id=seat_id,
                kind=report.kind or kind,
                present=report.present,
                state=report.state,
                load=dict(report.load),
                notes=list(report.notes) + [f"native_seat_id_was:{report.seat_id}"],
                lineage=LINEAGE_NATIVE,
                schema=report.schema,
                meta=dict(report.meta),
                sample_ts=report.sample_ts,
            )
        return report
    return adapter()


# ── plane adapters ───────────────────────────────────────────────────────────


def adapt_wait_plane(instance: Any, plane: Any) -> SeatReport:
    def _adapter() -> SeatReport:
        try:
            snap = plane.doctor_snapshot()
            if not isinstance(snap, Mapping):
                snap = {}
        except Exception as exc:
            return SeatReport.error(
                SEAT_WAIT_PLANE,
                KIND_PLANE,
                reason=f"doctor_snapshot:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_ADAPTER,
                meta=_adapter_meta("doctor_snapshot"),
            )
        load = _pick(
            snap,
            "open_wait_owners",
            "open_wait_interests",
            "wait_kinds",
            "index_size",
            "wait_plane_attached",
            "wait_matcher_wired",
        )
        attached = bool(snap.get("wait_plane_attached") or snap.get("wait_matcher_wired"))
        state = STATE_OK if attached else STATE_DEGRADED
        notes = []
        if not attached:
            notes.append("matcher_not_wired")
        note = snap.get("note")
        if note:
            notes.append(str(note))
        return SeatReport(
            seat_id=SEAT_WAIT_PLANE,
            kind=KIND_PLANE,
            present=True,
            state=state,
            load=load,
            notes=notes,
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("doctor_snapshot"),
        )

    return prefer_native(
        plane, seat_id=SEAT_WAIT_PLANE, kind=KIND_PLANE, adapter=_adapter
    )


def adapt_session_plane(instance: Any, plane: Any) -> SeatReport:
    def _adapter() -> SeatReport:
        try:
            snap = plane.doctor_snapshot()
            if not isinstance(snap, Mapping):
                snap = {}
        except Exception as exc:
            return SeatReport.error(
                SEAT_SESSION_PLANE,
                KIND_PLANE,
                reason=f"doctor_snapshot:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_ADAPTER,
                meta=_adapter_meta("doctor_snapshot"),
            )
        counts = snap.get("counts") if isinstance(snap.get("counts"), Mapping) else {}
        load: dict[str, Any] = {
            "session_plane_attached": snap.get("session_plane_attached"),
            "storage_backend": snap.get("storage_backend"),
            "multi_attach": snap.get("multi_attach"),
            "strict_attribution": snap.get("strict_attribution"),
        }
        if counts:
            load["counts"] = dict(counts)
        attached = bool(snap.get("session_plane_attached", True))
        state = STATE_OK if attached else STATE_DEGRADED
        return SeatReport(
            seat_id=SEAT_SESSION_PLANE,
            kind=KIND_PLANE,
            present=True,
            state=state,
            load={k: v for k, v in load.items() if v is not None},
            notes=[] if attached else ["session_plane_not_attached"],
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("doctor_snapshot"),
        )

    return prefer_native(
        plane, seat_id=SEAT_SESSION_PLANE, kind=KIND_PLANE, adapter=_adapter
    )


def adapt_work_plane(instance: Any, plane: Any) -> SeatReport:
    def _adapter() -> SeatReport:
        try:
            snap = plane.status() if callable(getattr(plane, "status", None)) else {}
            if not isinstance(snap, Mapping):
                snap = {}
        except Exception as exc:
            return SeatReport.error(
                SEAT_WORK_PLANE,
                KIND_PLANE,
                reason=f"status:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_ADAPTER,
                meta=_adapter_meta("status"),
            )
        load = _pick(
            snap,
            "attached",
            "pending",
            "dropped_depth",
            "max_depth",
            "batch_size",
            "background",
            "trigger_count",
        )
        attached = bool(snap.get("attached", True))
        state = STATE_OK if attached else STATE_DEGRADED
        notes = []
        if snap.get("pending") == -1:
            notes.append("pending_unreadable")
            state = STATE_DEGRADED
        return SeatReport(
            seat_id=SEAT_WORK_PLANE,
            kind=KIND_PLANE,
            present=True,
            state=state,
            load=load,
            notes=notes,
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("status"),
        )

    return prefer_native(
        plane, seat_id=SEAT_WORK_PLANE, kind=KIND_PLANE, adapter=_adapter
    )


# ── supervisor ───────────────────────────────────────────────────────────────


def adapt_supervisor(instance: Any, supervisor: Any) -> SeatReport:
    def _adapter() -> SeatReport:
        try:
            snap = (
                supervisor.status()
                if callable(getattr(supervisor, "status", None))
                else {}
            )
            if not isinstance(snap, Mapping):
                snap = {}
        except Exception as exc:
            return SeatReport.error(
                SEAT_SUPERVISOR,
                KIND_SUPERVISOR,
                reason=f"status:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_ADAPTER,
                meta=_adapter_meta("status"),
            )
        load = _pick(
            snap,
            "service_count",
            "running_count",
            "running",
            "registered",
        )
        return SeatReport.ok(
            SEAT_SUPERVISOR,
            KIND_SUPERVISOR,
            load=load,
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("status"),
        )

    return prefer_native(
        supervisor, seat_id=SEAT_SUPERVISOR, kind=KIND_SUPERVISOR, adapter=_adapter
    )


def adapt_supervisor_service(
    instance: Any,
    service: Any,
    *,
    service_name: str,
    running: bool | None = None,
) -> SeatReport:
    seat_id = supervisor_service_seat_id(service_name)

    def _adapter() -> SeatReport:
        try:
            snap = service.status() if callable(getattr(service, "status", None)) else {}
            if not isinstance(snap, Mapping):
                snap = {}
        except Exception as exc:
            return SeatReport.error(
                seat_id,
                KIND_SUPERVISOR_SERVICE,
                reason=f"status:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_ADAPTER,
                meta=_adapter_meta("status", service_name=service_name),
            )
        load = {k: v for k, v in dict(snap).items() if k not in ("name",)}
        if running is not None:
            load["running"] = running
        is_running = bool(load.get("running", running))
        notes = [] if is_running else ["registered_not_running"]
        # Registered but idle is still ok — continuous services need not run.
        return SeatReport.ok(
            seat_id,
            KIND_SUPERVISOR_SERVICE,
            load=load,
            notes=notes,
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("status", service_name=service_name),
        )

    return prefer_native(
        service,
        seat_id=seat_id,
        kind=KIND_SUPERVISOR_SERVICE,
        adapter=_adapter,
    )


# ── execution port ───────────────────────────────────────────────────────────


def adapt_execution(instance: Any, port: Any) -> SeatReport:
    def _adapter() -> SeatReport:
        started = bool(getattr(instance, "is_started", False))
        has_invoke = callable(getattr(port, "invoke_resource", None))
        has_workload = callable(getattr(port, "start_workload", None))
        load = {
            "instance_started": started,
            "has_invoke_resource": has_invoke,
            "has_start_workload": has_workload,
        }
        # Port object present; not started is degraded (attached shell, not live).
        state = STATE_OK if (started and has_invoke) else STATE_DEGRADED
        notes = []
        if not started:
            notes.append("instance_not_started")
        if not has_invoke:
            notes.append("missing_invoke_resource")
        return SeatReport(
            seat_id=SEAT_EXECUTION,
            kind=KIND_PORT,
            present=True,
            state=state,
            load=load,
            notes=notes,
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("execution_port_probe"),
        )

    return prefer_native(
        port, seat_id=SEAT_EXECUTION, kind=KIND_PORT, adapter=_adapter
    )


# ── system log ───────────────────────────────────────────────────────────────


def adapt_system_log(instance: Any, log: Any) -> SeatReport:
    def _adapter() -> SeatReport:
        try:
            records = log.recent() if callable(getattr(log, "recent", None)) else []
            n = len(records) if records is not None else 0
        except Exception as exc:
            return SeatReport.error(
                SEAT_SYSTEM_LOG,
                KIND_LOG,
                reason=f"recent:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_ADAPTER,
                meta=_adapter_meta("system_log_probe"),
            )
        capacity = getattr(log, "capacity", None)
        if capacity is None:
            capacity = getattr(log, "_capacity", None)
        level = getattr(log, "level", None)
        load: dict[str, Any] = {"records": n}
        if capacity is not None:
            load["capacity"] = int(capacity)
        if level is not None:
            load["level"] = int(level) if isinstance(level, int) else level
        return SeatReport.ok(
            SEAT_SYSTEM_LOG,
            KIND_LOG,
            load=load,
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("system_log_probe"),
        )

    return prefer_native(
        log, seat_id=SEAT_SYSTEM_LOG, kind=KIND_LOG, adapter=_adapter
    )


# ── boot membership ──────────────────────────────────────────────────────────


def adapt_boot_membership(instance: Any, walk: Any) -> SeatReport:
    def _adapter() -> SeatReport:
        rows: list[Any]
        if walk is None:
            rows = []
        elif isinstance(walk, (list, tuple)):
            rows = list(walk)
        else:
            rows = [walk]
        phases: list[dict[str, Any]] = []
        ok_n = skip_n = fail_n = 0
        for row in rows:
            if hasattr(row, "to_dict") and callable(row.to_dict):
                d = row.to_dict()
            elif isinstance(row, Mapping):
                d = dict(row)
            else:
                d = {"repr": repr(row)}
            phases.append(d)
            outcome = str(d.get("outcome") or "")
            if outcome == "ok":
                ok_n += 1
            elif outcome == "skip":
                skip_n += 1
            elif outcome == "fail":
                fail_n += 1
        load: dict[str, Any] = {
            "phase_count": len(phases),
            "ok": ok_n,
            "skip": skip_n,
            "fail": fail_n,
            "phases": [p.get("phase") for p in phases if p.get("phase")],
        }
        state = STATE_OK if fail_n == 0 else STATE_DEGRADED
        notes = []
        if fail_n:
            notes.append(f"boot_fail_count:{fail_n}")
        if not phases:
            notes.append("empty_walk")
            state = STATE_DEGRADED
        return SeatReport(
            seat_id=SEAT_BOOT_MEMBERSHIP,
            kind=KIND_BOOT,
            present=True,
            state=state,
            load=load,
            notes=notes,
            lineage=LINEAGE_ADAPTER,
            meta=_adapter_meta("last_boot_walk"),
        )

    # Walk list itself is not SeatReportable; still use prefer_native on
    # instance if it grows a membership report later.
    native = try_native_report(instance)
    if native is not None:
        try:
            report = coerce_report(
                native,
                default_seat_id=SEAT_BOOT_MEMBERSHIP,
                default_kind=KIND_BOOT,
                default_lineage=LINEAGE_NATIVE,
            )
            if report.seat_id == SEAT_BOOT_MEMBERSHIP:
                return report
        except Exception:
            pass
    return _adapter()


__all__ = [
    "adapt_boot_membership",
    "adapt_execution",
    "adapt_session_plane",
    "adapt_supervisor",
    "adapt_supervisor_service",
    "adapt_system_log",
    "adapt_wait_plane",
    "adapt_work_plane",
    "prefer_native",
]
