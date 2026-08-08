"""0.63.7 — vitality eyes on assembly admission."""

from __future__ import annotations

from palm.system.log import reset_system_log_for_tests
from palm.system.runtime.base import BaseRuntime
from palm.system.vitality import (
    SEAT_ASSEMBLY,
    STATE_DEGRADED,
    STATE_OK,
    project,
    walk_result,
)
from palm.system.vitality.seats import reset_default_probe_catalog_for_tests


def test_assembly_seat_in_default_probes() -> None:
    from palm.system.vitality.seats import build_default_probes

    reset_default_probe_catalog_for_tests()
    assert any(p.seat_id == SEAT_ASSEMBLY for p in build_default_probes())


def test_started_runtime_assembly_seat_ok() -> None:
    reset_system_log_for_tests()
    reset_default_probe_catalog_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        result = walk_result(rt)
        by_id = result.by_id()
        assert SEAT_ASSEMBLY in by_id
        report = by_id[SEAT_ASSEMBLY]
        assert report.present is True
        assert report.state == STATE_OK
        assert report.load.get("may_run_business") is True
        assert report.load.get("definition_id") == "local.embedded"

        snap = project(rt)
        assert snap is not None
    finally:
        rt.stop()


def test_assembly_skip_seat_absent_or_degraded() -> None:
    reset_system_log_for_tests()
    reset_default_probe_catalog_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=False,
        assembly_skip=True,
    )
    try:
        result = walk_result(rt)
        report = result.by_id().get(SEAT_ASSEMBLY)
        # No seat object → absent report (when_absent=report)
        if report is not None and report.present:
            assert report.state == STATE_DEGRADED
            assert report.load.get("may_run_business") is not True
        else:
            assert report is None or report.present is False
    finally:
        rt.stop()
