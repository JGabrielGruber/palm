"""0.63.8 — admission inventory: gated map + packaging admission pointer."""

from __future__ import annotations

from palm.app.host.application_host import ApplicationHost
from palm.app.settings import PalmSettings
from palm.system.assembly import (
    GATED_CITIZENS,
    PRETENDER_EDGES,
    kingdom_map,
    kingdom_snapshot,
)
from palm.system.log import reset_system_log_for_tests
from palm.system.runtime.base import BaseRuntime


def test_kingdom_map_has_walls() -> None:
    m = kingdom_map()
    assert m["gated_count"] >= 8
    assert m["pretender_count"] >= 1
    ids = {g["id"] for g in GATED_CITIZENS}
    assert "work_plane.tick" in ids
    assert "executor.submit_flow" in ids
    assert "dna.refuse" in ids
    assert "vitality.assembly" in ids
    pret = {p["id"] for p in PRETENDER_EDGES}
    assert "env.structure_toggles" in pret


def test_kingdom_snapshot_live() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        snap = kingdom_snapshot(rt)
        assert snap["live"]["is_started"] is True
        assert snap["live"]["admission"]["may_run_business"] is True
        assert snap["live"]["definition_id"] == "local.embedded"
    finally:
        rt.stop()


def test_host_packaging_nests_assembly() -> None:
    reset_system_log_for_tests()
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost.for_mode("safe", settings=settings)
    host.start()
    try:
        bag = host.packaging_status()
        assert "assembly" in bag
        assert bag["assembly"]["role"] == "admission_pointer"
        assert bag["assembly"]["may_run_business"] is True
        assert bag["assembly"]["definition_id"] == "local.embedded"
        # Host surface
        assert host.admission.may_run_business is True
    finally:
        host.shutdown()


def test_host_admission_empty_before_start() -> None:
    host = ApplicationHost.for_mode("safe")
    assert host.admission.may_run_business is False
