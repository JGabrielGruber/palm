"""Structure status phase and admission snapshot (pure)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Self


class StructurePhase(StrEnum):
    """Local readiness phase under the current definition."""

    EMPTY = "empty"
    """No definition loaded."""

    RECEIVED = "received"
    """Definition held; not yet reconciled."""

    ASSEMBLING = "assembling"
    """Reconciling toward desired structure."""

    READY = "ready"
    """Definition-ready — business that needs ground may run (if admission says so)."""

    BLOCKED = "blocked"
    """Cannot reach ready; reasons on the snapshot."""

    INVALIDATED = "invalidated"
    """Prior ready is void (e.g. new definition); reassemble required."""


@dataclass(frozen=True, slots=True)
class AdmissionSnapshot:
    """Published gate for clients and planes — may business that needs ground run?

    Fail closed: ``may_run_business`` is True only when phase is READY and
    no blocking reasons remain.
    """

    may_run_business: bool
    phase: StructurePhase
    definition_id: str | None = None
    definition_version: str | None = None
    reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "may_run_business": self.may_run_business,
            "phase": str(self.phase),
            "definition_id": self.definition_id,
            "definition_version": self.definition_version,
            "reasons": list(self.reasons),
        }

    @classmethod
    def empty(cls) -> Self:
        return cls(
            may_run_business=False,
            phase=StructurePhase.EMPTY,
            reasons=("no_definition",),
        )


@dataclass(frozen=True, slots=True)
class StructureStatus:
    """In-engine status of readiness under the current definition."""

    phase: StructurePhase
    definition_id: str | None = None
    definition_version: str | None = None
    places_ready: frozenset[str] = frozenset()
    places_missing: tuple[str, ...] = ()
    block_reasons: tuple[str, ...] = ()
    truth_home_up: bool = True

    def admission(self) -> AdmissionSnapshot:
        reasons: list[str] = []
        if self.phase is StructurePhase.EMPTY:
            reasons.append("no_definition")
        elif self.phase is StructurePhase.RECEIVED:
            reasons.append("definition_not_assembled")
        elif self.phase is StructurePhase.ASSEMBLING:
            reasons.append("assembling")
            reasons.extend(f"place_missing:{p}" for p in self.places_missing)
        elif self.phase is StructurePhase.BLOCKED:
            reasons.extend(self.block_reasons or ("blocked",))
        elif self.phase is StructurePhase.INVALIDATED:
            reasons.append("invalidated")
        elif self.phase is StructurePhase.READY:
            if not self.truth_home_up:
                reasons.append("truth_home_down")
            reasons.extend(self.block_reasons)

        may = self.phase is StructurePhase.READY and not reasons and self.truth_home_up
        if may:
            reason_tuple: tuple[str, ...] = ()
        else:
            reason_tuple = tuple(reasons) if reasons else ("not_ready",)

        return AdmissionSnapshot(
            may_run_business=may,
            phase=self.phase,
            definition_id=self.definition_id,
            definition_version=self.definition_version,
            reasons=reason_tuple,
        )


__all__ = [
    "AdmissionSnapshot",
    "StructurePhase",
    "StructureStatus",
]
