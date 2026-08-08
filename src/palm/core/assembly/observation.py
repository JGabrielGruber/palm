"""Observations — facts folded into the assembly engine (closed set)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ObservationKind(StrEnum):
    """Closed set of structure facts. Grow by theme."""

    PLACE_READY = "place_ready"
    PLACE_FAILED = "place_failed"
    PLACE_GONE = "place_gone"
    TRUTH_HOME_UP = "truth_home_up"
    TRUTH_HOME_DOWN = "truth_home_down"
    PROJECTION_LOADED = "projection_loaded"
    PROJECTION_FAILED = "projection_failed"
    STRUCTURE_SEED_FINISHED = "structure_seed_finished"
    STRUCTURE_SEED_FAILED = "structure_seed_failed"
    SEAT_BOUND = "seat_bound"
    #: Membership violates DNA refuse — target is reason code (refuse:…).
    STRUCTURE_POLICY_VIOLATION = "structure_policy_violation"
    #: Clear a prior policy violation reason (target = reason code).
    STRUCTURE_POLICY_CLEARED = "structure_policy_cleared"


@dataclass(frozen=True, slots=True)
class Observation:
    """One fact from system hands (or tests) into the pure engine."""

    kind: ObservationKind
    target: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": str(self.kind),
            "target": self.target,
            "payload": dict(self.payload),
        }


__all__ = [
    "Observation",
    "ObservationKind",
]
