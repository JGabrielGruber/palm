"""0.60.6 — outbox continuous service on SystemSupervisor."""

from __future__ import annotations

from palm.system.log import reset_system_log_for_tests
from palm.system.runtime.base import BaseRuntime
from palm.system.subsystems.supervisor import OutboxLoopService


def test_outbox_registered_when_outbox_wired() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=True)
    try:
        assert rt.outbox_processor is not None
        assert rt.supervisor is not None
        assert "outbox" in rt.supervisor.names()
        assert "work_drain" not in rt.supervisor.names()
        assert rt.supervisor.status()["running_count"] == 0
        by_id = {w.phase: w for w in (rt._last_boot_walk or [])}
        assert by_id["system.background.start"].outcome == "skip"
    finally:
        rt.stop()


def test_outbox_background_starts_when_enabled() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=True,
        enable_outbox_background=True,
    )
    try:
        by_id = {w.phase: w for w in (rt._last_boot_walk or [])}
        assert by_id["system.background.start"].outcome == "ok"
        assert rt.supervisor is not None
        assert "outbox" in rt.supervisor.status()["running"]
        svc = rt.supervisor.get("outbox")
        assert isinstance(svc, OutboxLoopService)
        assert svc.is_running is True
    finally:
        rt.stop()


def test_outbox_and_work_drain_both_start() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=True,
        enable_outbox_background=True,
        structure_definition_id="local.cli",
    )
    try:
        assert rt.supervisor is not None
        running = set(rt.supervisor.status()["running"])
        assert running == {"outbox", "work_drain"}
    finally:
        rt.stop()
