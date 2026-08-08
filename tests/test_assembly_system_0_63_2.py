"""0.63.2 — system assembly seat + household assemble phase."""

from __future__ import annotations

from palm.core.assembly import (
    LOCAL_EMBEDDED_ID,
    AssemblyDefinition,
    AssemblyPhase,
    local_embedded,
)
from palm.system.assembly import (
    AssemblySeat,
    RecordingEffectPort,
    assemble_until_steady,
    load_and_assemble,
)
from palm.system.boot import system_phase_ids
from palm.system.log import reset_system_log_for_tests
from palm.system.runtime.base import BaseRuntime


def test_system_phase_table_includes_assembly() -> None:
    ids = system_phase_ids()
    assert "system.assembly.assemble" in ids
    assert ids.index("system.ready") < ids.index("system.assembly.assemble")
    assert ids.index("system.assembly.assemble") < ids.index(
        "system.background.start"
    )


def test_load_and_assemble_embedded_ready() -> None:
    seat = AssemblySeat()
    loop = seat.assemble(local_embedded())
    assert loop.steady is True
    assert loop.last.admission.may_run_business is True
    assert loop.last.admission.definition_id == LOCAL_EMBEDDED_ID
    assert seat.admission().phase is AssemblyPhase.READY


def test_assemble_with_places_auto_ack() -> None:
    seat = AssemblySeat(effects=RecordingEffectPort(auto_ack_places=True))
    dna = AssemblyDefinition(
        id="local.with_place",
        version="1",
        places_required=("support_home",),
    )
    loop = seat.assemble(dna)
    assert loop.steady is True
    assert seat.admission().may_run_business is True
    assert any(
        i.target == "support_home" for i in seat.effects.applied  # type: ignore[attr-defined]
    )


def test_runtime_start_publishes_admission() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(storage_backend="memory", enable_event_outbox=False)
    try:
        assert rt.is_started
        by_id = {w.phase: w for w in (rt._last_boot_walk or [])}
        assert by_id["system.assembly.assemble"].outcome == "ok"
        assert rt.assembly is not None
        snap = rt.admission
        assert snap.may_run_business is True
        assert snap.definition_id == LOCAL_EMBEDDED_ID
        assert snap.phase is AssemblyPhase.READY
    finally:
        rt.stop()
        assert rt.assembly is None
        assert rt.admission.may_run_business is False


def test_runtime_assembly_skip_fail_closed() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=False,
        assembly_skip=True,
    )
    try:
        by_id = {w.phase: w for w in (rt._last_boot_walk or [])}
        assert by_id["system.assembly.assemble"].outcome == "skip"
        assert by_id["system.assembly.assemble"].reason == "assembly_skip"
        assert rt.assembly is None
        assert rt.admission.may_run_business is False
        assert rt.admission.phase is AssemblyPhase.EMPTY
    finally:
        rt.stop()


def test_runtime_custom_dna_id() -> None:
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=False,
        assembly_dna_id="local.embedded",
        assembly_dna_version="9",
    )
    try:
        assert rt.admission.definition_version == "9"
        assert rt.admission.may_run_business is True
    finally:
        rt.stop()


def test_loop_module_export() -> None:
    engine = AssemblySeat().engine
    effects = RecordingEffectPort()
    result = load_and_assemble(engine, effects, local_embedded())
    assert result.last.admission.may_run_business is True
    again = assemble_until_steady(engine, effects)
    assert again.last.admission.may_run_business is True
