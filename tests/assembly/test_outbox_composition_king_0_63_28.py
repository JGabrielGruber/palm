"""0.63.28 — host outbox store wire follows composition membership (not settings peer)."""

from __future__ import annotations

from palm.app.host.application_host import ApplicationHost
from palm.app.host.composition import CompositionProfile
from palm.app.settings import PalmSettings
from palm.system.assembly.inventory import READINESS_EDGES, admission_inventory
from palm.system.log import reset_system_log_for_tests


def _lean(**overrides: object) -> PalmSettings:
    base: dict[str, object] = {
        "load_example_definitions": False,
        "storage_backend": "memory",
        "rebuild_projections_on_startup": False,
        "reconcile_instances_on_startup": False,
        "enable_compensation": False,
        "enable_outbox_service": False,
        "enable_event_outbox": True,  # settings want outbox seed
        "enable_webhook_dispatcher": False,
        "enable_neonroot_runners": False,
        "analytics_enabled": False,
    }
    base.update(overrides)
    return PalmSettings(**base)  # type: ignore[arg-type]


def test_host_outbox_wire_follows_composition_not_settings_flag() -> None:
    """Settings enable_event_outbox=True but composition omits outbox → no store."""
    reset_system_log_for_tests()
    composition = CompositionProfile(
        services=("inspect", "session", "definitions", "execution"),
        surfaces=(),
        capabilities=frozenset({"journal", "projections", "workloads"}),
    )
    assert not composition.has("outbox")
    host = ApplicationHost(settings=_lean(enable_event_outbox=True), composition=composition)
    host.start()
    try:
        rt = host.runtime()
        assert rt.outbox_store is None
        assert rt.outbox_processor is None
    finally:
        host.shutdown()


def test_host_outbox_wire_when_composition_has_outbox() -> None:
    reset_system_log_for_tests()
    composition = CompositionProfile(
        services=("inspect", "session", "definitions", "execution"),
        surfaces=(),
        capabilities=frozenset({"outbox", "journal", "projections", "workloads"}),
    )
    host = ApplicationHost(
        settings=_lean(enable_event_outbox=False),  # settings off, composition on
        composition=composition,
    )
    host.start()
    try:
        rt = host.runtime()
        assert rt.outbox_store is not None
        assert rt.outbox_processor is not None
    finally:
        host.shutdown()


def test_explicit_start_option_still_overrides_composition() -> None:
    """Named residual: host.start(enable_event_outbox=…) wins over composition."""
    reset_system_log_for_tests()
    composition = CompositionProfile(
        services=("inspect", "session", "definitions", "execution"),
        surfaces=(),
        capabilities=frozenset({"outbox", "journal", "projections", "workloads"}),
    )
    host = ApplicationHost(settings=_lean(), composition=composition)
    host.start(enable_event_outbox=False)
    try:
        rt = host.runtime()
        assert rt.outbox_store is None
    finally:
        host.shutdown()


def test_inventory_outbox_host_paid() -> None:
    pretenders = {row["id"]: row["status"] for row in READINESS_EDGES}
    assert pretenders["outbox.start_option_seed"] == "paid_host_0_63_28"
    assert pretenders["runtime.enable_event_outbox_bare"] == "named_0_63_28"
    assert admission_inventory()["readiness_edge_count"] >= 2
