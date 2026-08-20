"""0.66.1 — AdmissionSnapshot publishes installed capability names."""

from __future__ import annotations

from palm.core.structure import (
    AdmissionSnapshot,
    StructureEngine,
    StructurePhase,
    local_cli,
)


def test_snapshot_capabilities_default_empty() -> None:
    snap = AdmissionSnapshot(
        may_run_business=True,
        phase=StructurePhase.READY,
    )
    assert snap.capabilities == frozenset()
    assert snap.has_capability("work_drain") is False


def test_snapshot_has_capability_and_to_dict_sorted() -> None:
    snap = AdmissionSnapshot(
        may_run_business=True,
        phase=StructurePhase.READY,
        capabilities=frozenset({"outbox", "work_drain"}),
    )
    assert snap.has_capability("work_drain") is True
    assert snap.has_capability("journal") is False
    assert snap.to_dict()["capabilities"] == ["outbox", "work_drain"]


def test_empty_factory_has_no_capabilities() -> None:
    snap = AdmissionSnapshot.empty()
    assert snap.capabilities == frozenset()
    assert snap.to_dict()["capabilities"] == []


def test_engine_admission_does_not_walk_dna() -> None:
    engine = StructureEngine()
    engine.initialize()
    engine.receive_definition(local_cli())
    engine.tick()
    snap = engine.admission()
    assert snap.may_run_business is True
    assert snap.capabilities == frozenset()
    assert snap.has_capability("work_drain") is False
