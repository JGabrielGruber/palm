"""0.63.13 — env structure seed (SD-021): DNA from settings; drain DNA king."""

from __future__ import annotations

from palm.app.host.application_host import ApplicationHost
from palm.app.host.boot.modes import BootMode
from palm.app.settings import PalmSettings
from palm.core.assembly import LOCAL_CLI_ID, LOCAL_EMBEDDED_ID
from palm.system.assembly import (
    STRUCTURE_SEED_ENV,
    dna_id_from_settings,
    dna_refuses_background_drain,
    resolve_seed_dna,
    seed_assembly_options_from_host,
)
from palm.core.assembly import resolve_builtin_dna
from palm.system.log import reset_system_log_for_tests


def test_structure_seed_env_catalog() -> None:
    envs = {row["env"] for row in STRUCTURE_SEED_ENV}
    assert "PALM_ASSEMBLY_DNA_ID" in envs
    assert "PALM_ENABLE_WORK_DRAIN_SERVICE" in envs


def test_dna_id_from_settings() -> None:
    assert dna_id_from_settings(None) is None
    s = PalmSettings.for_tests(load_examples=False)
    assert dna_id_from_settings(s) is None
    s3 = PalmSettings(
        load_example_definitions=False,
        storage_backend="memory",
        assembly_dna_id="local.cli",
        rebuild_projections_on_startup=False,
        enable_compensation=False,
        enable_outbox_service=False,
        enable_event_outbox=False,
        reconcile_instances_on_startup=False,
    )
    assert dna_id_from_settings(s3) == LOCAL_CLI_ID


def test_settings_dna_wins_over_mode_in_seed() -> None:
    settings = PalmSettings(
        load_example_definitions=False,
        storage_backend="memory",
        assembly_dna_id="local.cli",
        rebuild_projections_on_startup=False,
        enable_compensation=False,
        enable_outbox_service=False,
        enable_event_outbox=False,
        reconcile_instances_on_startup=False,
    )
    host = ApplicationHost.for_mode(BootMode.safe(), settings=settings)
    seed = seed_assembly_options_from_host(host)
    assert seed["assembly_dna_id"] == LOCAL_CLI_ID
    assert seed["assembly_definition"].id == LOCAL_CLI_ID


def test_host_settings_dna_id_loads() -> None:
    reset_system_log_for_tests()
    settings = PalmSettings(
        load_example_definitions=False,
        storage_backend="memory",
        assembly_dna_id="local.cli",
        rebuild_projections_on_startup=False,
        enable_compensation=False,
        enable_outbox_service=False,
        enable_event_outbox=False,
        reconcile_instances_on_startup=False,
    )
    # safe mode composition is embedded (no surfaces); DNA from settings → cli
    host = ApplicationHost.for_mode("safe", settings=settings)
    host.start()
    try:
        assert host.admission.definition_id == LOCAL_CLI_ID
        assert host.admission.may_run_business is True
    finally:
        host.shutdown()


def test_dna_override_still_checks_composition_membership() -> None:
    """Caller DNA override + cli composition with work_drain → refuse on embedded."""
    reset_system_log_for_tests()
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost.for_mode("cli", settings=settings)
    assert host.composition.has("work_drain")
    host.start(assembly_dna_id="local.embedded")
    try:
        assert host.admission.definition_id == LOCAL_EMBEDDED_ID
        assert host.admission.may_run_business is False
        reasons = host.admission.reasons
        assert any("refuse:background_drain" in str(r) for r in reasons)
        # Continuous drain must not peer-law under DNA refuse
        assert host._work_drain_listed() is False
    finally:
        host.shutdown()


def test_dna_refuses_background_drain_helper() -> None:
    emb = resolve_builtin_dna(LOCAL_EMBEDDED_ID)
    cli = resolve_builtin_dna(LOCAL_CLI_ID)
    assert dna_refuses_background_drain(emb) is True
    assert dna_refuses_background_drain(cli) is False
    assert dna_refuses_background_drain(None) is False


def test_resolve_seed_explicit_from_settings_path() -> None:
    dna = resolve_seed_dna(mode_name="server", explicit_dna_id="local.embedded")
    assert dna.id == LOCAL_EMBEDDED_ID
