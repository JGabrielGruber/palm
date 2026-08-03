"""0.60.2 — WorkPlaneService on system (enqueue / tick / attach)."""

from __future__ import annotations

from palm.core.work import WorkIntent
from palm.system.log import reset_system_log_for_tests
from palm.system.subsystems.planes.work.plane import WorkPlaneService
from palm.system.runtime.base import BaseRuntime


def test_work_plane_attach_enqueue_tick_hostless() -> None:
    reset_system_log_for_tests()
    submitted: list[tuple[str, dict]] = []

    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        plane = rt.work_plane
        assert isinstance(plane, WorkPlaneService)
        assert plane.is_attached
        assert plane.status()["attached"] is True

        # Override submit so we do not need a catalog flow definition.
        plane._submit_flow = lambda fid, payload: submitted.append((fid, dict(payload)))

        intent_id = plane.enqueue(
            WorkIntent(kind="run_flow", target="demo-flow", payload={"k": 1})
        )
        assert intent_id
        assert plane.store.pending_count() >= 1

        n = plane.tick(limit=10)
        assert n == 1
        assert submitted == [("demo-flow", {"k": 1})]
        assert plane.store.pending_count() == 0
    finally:
        rt.stop()
        assert rt.work_plane is None


def test_work_plane_depth_guard() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        plane = rt.work_plane
        assert plane is not None
        plane._max_depth = 2
        ok = plane.enqueue(WorkIntent(kind="run_flow", target="a", depth=2))
        drop = plane.enqueue(WorkIntent(kind="run_flow", target="b", depth=3))
        assert ok != ""
        assert drop == ""
        assert plane.dropped_depth_count == 1
    finally:
        rt.stop()


def test_system_schedule_attaches_work_plane() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        assert rt.work_plane is not None
        assert rt.wait_plane is not None
        assert rt.session_plane is not None
        assert rt.supervisor is not None
        assert "work_drain" in rt.supervisor.names()
        by_id = {w.phase: w for w in (rt._last_boot_walk or [])}
        assert by_id["system.background.start"].outcome == "skip"
        assert by_id["system.background.start"].reason == "no_background_services_enabled"
    finally:
        rt.stop()


def test_supervised_work_drain_background_when_enabled() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=False,
        enable_work_drain_service=True,
    )
    try:
        assert rt.supervisor is not None
        by_id = {w.phase: w for w in (rt._last_boot_walk or [])}
        assert by_id["system.background.start"].outcome == "ok"
        assert rt.work_plane is not None
        assert rt.work_plane.is_running is True
        assert rt.supervisor.status()["running"] == ["work_drain"]
    finally:
        rt.stop()
        assert rt.work_plane is None
