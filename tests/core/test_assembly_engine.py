"""0.63.1 — pure AssemblyEngine (embedded DNA · admission · fail closed)."""

from __future__ import annotations

import pytest

from palm.core.assembly import (
    LOCAL_EMBEDDED_ID,
    AdmissionSnapshot,
    AssemblyDefinition,
    AssemblyEngine,
    AssemblyEngineError,
    AssemblyPhase,
    EffectIntentKind,
    Observation,
    ObservationKind,
    local_embedded,
)


@pytest.fixture
def engine() -> AssemblyEngine:
    eng = AssemblyEngine()
    eng.initialize()
    return eng


def test_empty_admission_fail_closed(engine: AssemblyEngine) -> None:
    snap = engine.admission()
    assert snap.may_run_business is False
    assert snap.phase is AssemblyPhase.EMPTY
    assert "no_definition" in snap.reasons


def test_local_embedded_builtin() -> None:
    dna = local_embedded()
    assert dna.id == LOCAL_EMBEDDED_ID
    assert dna.role_intent == "embedded"
    assert "server_surfaces" in dna.refuse
    assert dna.capabilities == frozenset()
    assert dna.places_required == ()
    assert AssemblyDefinition.from_dict(dna.to_dict()).id == dna.id


def test_receive_definition_not_ready_until_tick(engine: AssemblyEngine) -> None:
    snap = engine.receive_definition(local_embedded())
    assert snap.may_run_business is False
    assert snap.definition_id == LOCAL_EMBEDDED_ID
    assert snap.phase in (AssemblyPhase.RECEIVED, AssemblyPhase.INVALIDATED)


def test_embedded_tick_becomes_ready(engine: AssemblyEngine) -> None:
    engine.receive_definition(local_embedded(version="1"))
    result = engine.tick()
    assert result.admission.may_run_business is True
    assert result.admission.phase is AssemblyPhase.READY
    assert result.status.phase is AssemblyPhase.READY
    assert result.intents == ()
    assert result.changed is True
    assert "definition_ready" in result.notes


def test_idempotent_same_definition_while_ready(engine: AssemblyEngine) -> None:
    dna = local_embedded(version="1")
    engine.receive_definition(dna)
    engine.tick()
    snap = engine.receive_definition(dna)
    assert snap.may_run_business is True
    assert snap.phase is AssemblyPhase.READY


def test_new_definition_invalidates_readiness(engine: AssemblyEngine) -> None:
    engine.receive_definition(local_embedded(version="1"))
    engine.tick()
    assert engine.admission().may_run_business is True

    snap = engine.receive_definition(local_embedded(version="2"))
    assert snap.may_run_business is False
    assert snap.phase is AssemblyPhase.INVALIDATED
    assert snap.definition_version == "2"

    result = engine.tick()
    assert result.admission.may_run_business is True
    assert result.admission.definition_version == "2"


def test_truth_home_down_blocks(engine: AssemblyEngine) -> None:
    engine.receive_definition(local_embedded())
    engine.tick()
    assert engine.admission().may_run_business is True

    engine.observe(Observation(kind=ObservationKind.TRUTH_HOME_DOWN))
    snap = engine.admission()
    assert snap.may_run_business is False
    assert snap.phase is AssemblyPhase.BLOCKED
    assert "truth_home_down" in snap.reasons

    engine.observe(Observation(kind=ObservationKind.TRUTH_HOME_UP))
    result = engine.tick()
    assert result.admission.may_run_business is True
    assert result.admission.phase is AssemblyPhase.READY


def test_places_required_emits_ensure_and_waits(
    engine: AssemblyEngine,
) -> None:
    dna = AssemblyDefinition(
        id="local.with_place",
        version="1",
        role_intent="support",
        places_required=("support_home",),
    )
    engine.receive_definition(dna)
    result = engine.tick()
    assert result.admission.may_run_business is False
    assert result.admission.phase is AssemblyPhase.ASSEMBLING
    assert len(result.intents) == 1
    assert result.intents[0].kind is EffectIntentKind.ENSURE_PLACE
    assert result.intents[0].target == "support_home"

    # Second tick does not re-emit while still pending
    result2 = engine.tick()
    assert result2.intents == ()
    assert result2.admission.may_run_business is False

    engine.observe(
        Observation(kind=ObservationKind.PLACE_READY, target="support_home")
    )
    result3 = engine.tick()
    assert result3.admission.may_run_business is True
    assert result3.status.places_ready == frozenset({"support_home"})


def test_place_failed_blocks(engine: AssemblyEngine) -> None:
    dna = AssemblyDefinition(
        id="local.with_place",
        version="1",
        places_required=("support_home",),
    )
    engine.receive_definition(dna)
    engine.tick()
    engine.observe(
        Observation(kind=ObservationKind.PLACE_FAILED, target="support_home")
    )
    snap = engine.admission()
    assert snap.may_run_business is False
    assert snap.phase is AssemblyPhase.BLOCKED
    assert any("place_failed" in r for r in snap.reasons)


def test_empty_definition_id_rejected(engine: AssemblyEngine) -> None:
    with pytest.raises(AssemblyEngineError):
        engine.receive_definition(AssemblyDefinition(id=""))


def test_admission_snapshot_to_dict(engine: AssemblyEngine) -> None:
    engine.receive_definition(local_embedded())
    engine.tick()
    d = engine.admission().to_dict()
    assert d["may_run_business"] is True
    assert d["definition_id"] == LOCAL_EMBEDDED_ID
    assert d["phase"] == "ready"


def test_shutdown_clears(engine: AssemblyEngine) -> None:
    engine.receive_definition(local_embedded())
    engine.tick()
    engine.shutdown()
    engine.initialize()
    assert engine.admission().phase is AssemblyPhase.EMPTY
    assert engine.admission().may_run_business is False


def test_admission_empty_factory() -> None:
    snap = AdmissionSnapshot.empty()
    assert snap.may_run_business is False
    assert snap.phase is AssemblyPhase.EMPTY
