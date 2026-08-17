"""0.44.1 — server host profile enables background work drain by default."""

from __future__ import annotations

from palm.app import ApplicationHost, PalmSettings
from palm.app.host.roles import DeploymentProfile


def test_server_profile_starts_work_drain_without_env() -> None:
    """Server DNA lists work_drain; settings flag is not required to start it."""
    settings = PalmSettings(
        load_example_definitions=False,
        storage_backend="memory",
        enable_work_drain_service=False,
        rebuild_projections_on_startup=False,
        reconcile_instances_on_startup=False,
        enable_compensation=False,
        enable_outbox_service=False,
        enable_event_outbox=False,
    )
    host = ApplicationHost(
        settings=settings,
        profile=DeploymentProfile.server_only(port=0),
    )
    host.start()
    try:
        assert host.admission.definition_id == "local.server"
        assert host._work_drain_background_enabled() is True
        assert host.work_drain is not None
        assert host.work_drain.is_running is True
    finally:
        host.shutdown()


def test_all_in_one_profile_starts_drain_from_dna() -> None:
    """all_in_one DNA lists work_drain; settings flag / composition are not kings."""
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost(
        settings=settings,
        profile=DeploymentProfile.all_in_one(),
    )
    host.start()
    try:
        assert host.admission.definition_id == "local.all_in_one"
        assert host._work_drain_background_enabled() is True
        assert host.work_drain is not None
        assert host.work_drain.is_running is True
    finally:
        host.shutdown()