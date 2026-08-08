"""0.63.5 — DNA seed map from mode / composition (not dual structure king)."""

from __future__ import annotations

from palm.app.host.application_host import ApplicationHost
from palm.app.host.boot.modes import BootMode
from palm.app.settings import PalmSettings
from palm.core.assembly import (
    LOCAL_ALL_IN_ONE_ID,
    LOCAL_CLI_ID,
    LOCAL_EMBEDDED_ID,
    LOCAL_SERVER_ID,
    LOCAL_WORKER_ID,
    resolve_builtin_dna,
)
from palm.system.assembly.seed import (
    dna_id_for_boot_mode,
    dna_id_for_composition,
    resolve_seed_dna,
)
from palm.system.log import reset_system_log_for_tests


def test_mode_to_dna_ids() -> None:
    assert dna_id_for_boot_mode("safe") == LOCAL_EMBEDDED_ID
    assert dna_id_for_boot_mode("test") == LOCAL_EMBEDDED_ID
    assert dna_id_for_boot_mode("cli") == LOCAL_CLI_ID
    assert dna_id_for_boot_mode("server") == LOCAL_SERVER_ID
    assert dna_id_for_boot_mode("prod") == LOCAL_SERVER_ID
    assert dna_id_for_boot_mode("worker") == LOCAL_WORKER_ID
    assert dna_id_for_boot_mode("dev") == LOCAL_ALL_IN_ONE_ID
    assert dna_id_for_boot_mode(None) is None


def test_composition_inference() -> None:
    assert (
        dna_id_for_composition(services=("execution",), surfaces=(), capabilities=())
        == LOCAL_WORKER_ID
    )
    assert (
        dna_id_for_composition(
            services=("execution", "definitions"),
            surfaces=(),
            capabilities=frozenset({"work_drain"}),
        )
        == LOCAL_CLI_ID
    )
    assert (
        dna_id_for_composition(
            services=("execution",),
            surfaces=("rest",),
            capabilities=frozenset({"work_drain"}),
        )
        == LOCAL_SERVER_ID
    )
    assert (
        dna_id_for_composition(services=(), surfaces=(), capabilities=())
        == LOCAL_EMBEDDED_ID
    )


def test_resolve_seed_explicit_wins() -> None:
    dna = resolve_seed_dna(mode_name="server", explicit_dna_id="local.cli")
    assert dna.id == LOCAL_CLI_ID


def test_builtin_refuse_differs() -> None:
    emb = resolve_builtin_dna(LOCAL_EMBEDDED_ID)
    cli = resolve_builtin_dna(LOCAL_CLI_ID)
    assert "background_drain" in emb.refuse
    assert "background_drain" not in cli.refuse
    assert "server_surfaces" in cli.refuse


def test_host_for_mode_cli_seeds_cli_dna() -> None:
    reset_system_log_for_tests()
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost.for_mode(BootMode.cli(), settings=settings)
    host.start()
    try:
        rt = host.runtime()
        assert rt.admission.may_run_business is True
        assert rt.admission.definition_id == LOCAL_CLI_ID
        assert rt.assembly is not None
        assert rt.assembly.definition is not None
        assert "server_surfaces" in rt.assembly.definition.refuse
    finally:
        host.shutdown()


def test_host_for_mode_safe_seeds_embedded() -> None:
    reset_system_log_for_tests()
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost.for_mode("safe", settings=settings)
    host.start()
    try:
        rt = host.runtime()
        assert rt.admission.definition_id == LOCAL_EMBEDDED_ID
    finally:
        host.shutdown()


def test_host_explicit_dna_override() -> None:
    reset_system_log_for_tests()
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost.for_mode("cli", settings=settings)
    host.start(assembly_dna_id="local.embedded")
    try:
        rt = host.runtime()
        assert rt.admission.definition_id == LOCAL_EMBEDDED_ID
    finally:
        host.shutdown()
