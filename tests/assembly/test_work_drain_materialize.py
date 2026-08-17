"""work_drain materialize — DNA capabilities are the install king."""

from __future__ import annotations

from dataclasses import replace

from palm.app.host.application_host import ApplicationHost
from palm.app.host.boot.modes import BootMode
from palm.app.host.composition import CompositionProfile as CP
from palm.app.settings import PalmSettings
from palm.core.assembly import (
    CAPABILITY_WORK_DRAIN,
    LOCAL_CLI_ID,
    LOCAL_EMBEDDED_ID,
    LOCAL_MCP_ID,
    LOCAL_SERVER_ID,
    local_all_in_one,
    local_cli,
    local_embedded,
    local_mcp,
    local_server,
    local_worker,
    resolve_builtin_dna,
)
from palm.system.assembly import (
    apply_local_capabilities,
    definition_lists_work_drain,
    dna_lists_work_drain,
)
from palm.system.log import reset_system_log_for_tests
from palm.system.subsystems.supervisor import SystemSupervisor
from palm.system.subsystems.supervisor.definition import (
    ContinuousWireContext,
    register_work_drain,
)


def test_builtin_dna_lists_work_drain_on_drain_phenotypes() -> None:
    assert CAPABILITY_WORK_DRAIN not in local_embedded().capabilities
    assert CAPABILITY_WORK_DRAIN not in local_mcp().capabilities
    assert local_cli().has_capability(CAPABILITY_WORK_DRAIN)
    assert local_server().has_capability(CAPABILITY_WORK_DRAIN)
    assert local_all_in_one().has_capability(CAPABILITY_WORK_DRAIN)
    assert local_worker().has_capability(CAPABILITY_WORK_DRAIN)
    roundtrip = local_cli().from_dict(local_cli().to_dict())
    assert CAPABILITY_WORK_DRAIN in roundtrip.capabilities
    unknown = resolve_builtin_dna("local.unknown")
    assert not unknown.has_capability(CAPABILITY_WORK_DRAIN)


def test_definition_lists_work_drain_helper() -> None:
    assert definition_lists_work_drain(local_cli()) is True
    assert definition_lists_work_drain(local_embedded()) is False
    assert definition_lists_work_drain(None) is False
    assert dna_lists_work_drain(local_server()) is True


class _FakePlane:
    def start_background(self) -> None:
        return None

    def stop_background(self) -> None:
        return None

    def status(self) -> dict[str, object]:
        return {"name": "work_drain", "running": False}


class _FakeShell:
    def __init__(self, *, plane: object | None, supervisor: SystemSupervisor) -> None:
        self.work_plane = plane
        self.supervisor = supervisor


def test_materialize_registers_work_drain_only_when_listed() -> None:
    sup = SystemSupervisor(definitions=())
    shell = _FakeShell(plane=_FakePlane(), supervisor=sup)
    applied = apply_local_capabilities(local_cli(), shell)
    assert CAPABILITY_WORK_DRAIN in applied
    assert "work_drain" in sup.names()

    dropped = apply_local_capabilities(local_embedded(), shell)
    assert dropped == frozenset()
    assert "work_drain" not in sup.names()


def test_materialize_unregisters_freelance_work_drain() -> None:
    sup = SystemSupervisor(definitions=())
    plane = _FakePlane()
    register_work_drain(sup, ContinuousWireContext(work_plane=plane))
    assert "work_drain" in sup.names()
    shell = _FakeShell(plane=plane, supervisor=sup)
    apply_local_capabilities(local_embedded(), shell)
    assert "work_drain" not in sup.names()


def _lean() -> PalmSettings:
    return PalmSettings.for_tests(load_examples=False)


def test_embedded_host_does_not_start_drain() -> None:
    reset_system_log_for_tests()
    host = ApplicationHost.for_mode(BootMode.safe(), settings=_lean())
    host.start()
    try:
        assert host.admission.definition_id == LOCAL_EMBEDDED_ID
        assert host._work_drain_background_enabled() is False
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].outcome == "skip"
        assert by_id["host.background.work_drain"].reason == "structure_off:work_drain"
        assert host.work_drain is None or host.work_drain.is_running is False
        rt = host.runtime()
        assert rt.assembly is not None
        assert CAPABILITY_WORK_DRAIN not in rt.assembly.materialized_capabilities
        assert rt.supervisor is None or "work_drain" not in rt.supervisor.names()
    finally:
        host.shutdown()


def test_cli_host_starts_drain_even_when_composition_omits_it() -> None:
    reset_system_log_for_tests()
    host = ApplicationHost.for_mode(
        BootMode.cli(),
        settings=_lean(),
        composition=replace(CP.cli(), capabilities=frozenset()),
    )
    assert not host.composition.has("work_drain")
    host.start()
    try:
        assert host.admission.definition_id == LOCAL_CLI_ID
        assert host.admission.may_run_business is True
        assert host._work_drain_background_enabled() is True
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].outcome == "ok"
        assert host.work_drain is not None
        assert host.work_drain.is_running is True
        rt = host.runtime()
        assert rt.assembly is not None
        assert CAPABILITY_WORK_DRAIN in rt.assembly.materialized_capabilities
        assert "work_drain" in rt.supervisor.names()
    finally:
        host.shutdown()


def test_server_dna_starts_drain() -> None:
    reset_system_log_for_tests()
    host = ApplicationHost.for_mode("server", settings=_lean(), server_port=0)
    host.start()
    try:
        assert host.admission.definition_id == LOCAL_SERVER_ID
        assert host._work_drain_background_enabled() is True
        assert host.work_drain is not None
        assert host.work_drain.is_running is True
    finally:
        host.shutdown()


def test_boot_mode_cannot_forbid_drain_when_dna_lists_it() -> None:
    """allow_background_drain is not a peer OR after DNA load."""
    reset_system_log_for_tests()
    host = ApplicationHost.for_mode(BootMode.test(), settings=_lean())
    host.start(assembly_dna_id=LOCAL_CLI_ID)
    try:
        assert host.boot_mode is not None
        assert host.boot_mode.allow_background_drain is False
        assert host.admission.definition_id == LOCAL_CLI_ID
        assert host._work_drain_background_enabled() is True
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].outcome == "ok"
        assert host.work_drain is not None
        assert host.work_drain.is_running is True
    finally:
        host.shutdown()


def test_mcp_dna_does_not_list_or_start_drain() -> None:
    reset_system_log_for_tests()
    host = ApplicationHost.for_mode("mcp", settings=_lean())
    host.start()
    try:
        assert host.admission.definition_id == LOCAL_MCP_ID
        assert host._work_drain_background_enabled() is False
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].reason == "structure_off:work_drain"
    finally:
        host.shutdown()
