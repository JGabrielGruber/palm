"""0.63.18 — reassemble edges (new DNA · membership · force invalidate)."""

from __future__ import annotations

from palm.core.structure import (
    Observation,
    ObservationKind,
    StructureDefinition,
    StructurePhase,
    local_embedded,
)
from palm.system.structure import RecordingEffectPort, StructureSeat


def test_reassemble_new_version_invalidates_then_ready() -> None:
    seat = StructureSeat()
    seat.assemble(local_embedded(version="1"))
    assert seat.admission().may_run_business is True

    loop = seat.reassemble(local_embedded(version="2"))
    assert loop.steady is True
    assert seat.admission().may_run_business is True
    assert seat.admission().definition_version == "2"
    assert seat.admission().phase is StructurePhase.READY


def test_reassemble_membership_worse_blocks() -> None:
    seat = StructureSeat()
    seat.assemble(local_embedded(), surfaces=())
    assert seat.admission().may_run_business is True

    seat.reassemble(local_embedded(), surfaces=("rest",))
    assert seat.admission().may_run_business is False
    assert seat.admission().phase is StructurePhase.BLOCKED
    assert any("server_surfaces" in r for r in seat.admission().reasons)


def test_reassemble_membership_heals_without_soft_dual() -> None:
    seat = StructureSeat()
    seat.assemble(local_embedded(), surfaces=("rest",))
    assert seat.admission().may_run_business is False

    seat.reassemble(local_embedded(), surfaces=())
    assert seat.admission().may_run_business is True
    assert seat.admission().phase is StructurePhase.READY
    assert not any(r.startswith("refuse:") for r in seat.admission().reasons)


def test_reassemble_force_same_dna_voids_ready() -> None:
    seat = StructureSeat(effects=RecordingEffectPort(auto_ack_places=True))
    dna = StructureDefinition(
        id="local.with_place",
        version="1",
        places_required=("support_home",),
    )
    seat.assemble(dna)
    assert seat.admission().may_run_business is True
    assert "support_home" in seat.status().places_ready

    # force: wipe places ledger; recording port re-acks on re-ensure
    seat.reassemble(dna, force=True)
    assert seat.admission().may_run_business is True
    assert seat.admission().phase is StructurePhase.READY
    # intents re-fired for place
    assert any(
        i.target == "support_home" for i in seat.effects.applied  # type: ignore[attr-defined]
    )


def test_reassemble_omitted_definition_uses_seat_dna() -> None:
    seat = StructureSeat()
    seat.assemble(local_embedded(version="7"))
    seat.reassemble()  # keep definition
    assert seat.admission().definition_version == "7"
    assert seat.admission().may_run_business is True


def test_engine_invalidate_blocks_until_reassemble() -> None:
    seat = StructureSeat()
    seat.assemble(local_embedded())
    assert seat.admission().may_run_business is True

    snap = seat.engine.invalidate()
    assert snap.may_run_business is False
    assert snap.phase is StructurePhase.INVALIDATED

    # business paths that need admission fail closed while invalidated
    assert seat.admission().may_run_business is False

    seat.reassemble()
    assert seat.admission().may_run_business is True


def test_place_gone_then_reassemble_recovers() -> None:
    seat = StructureSeat(effects=RecordingEffectPort(auto_ack_places=True))
    dna = StructureDefinition(
        id="local.place",
        places_required=("yard",),
    )
    seat.assemble(dna)
    assert seat.admission().may_run_business is True

    seat.engine.observe(
        Observation(kind=ObservationKind.PLACE_GONE, target="yard")
    )
    assert seat.admission().phase is StructurePhase.INVALIDATED
    assert seat.admission().may_run_business is False

    seat.reassemble(dna)
    assert seat.admission().may_run_business is True
