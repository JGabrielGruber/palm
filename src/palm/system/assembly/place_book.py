"""In-process place book — assembly effect hands for ENSURE/RELEASE place (0.63.11+).

Ledger of places the place-book can mark ready so a definition with places_required can
converge. **0.63.14:** optional :class:`PlaceSpawnPort` grows bodies (OS /
workload strategies); default remains in-process success. Not Grove.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from palm.core.assembly import EffectIntent, EffectIntentKind, Observation, ObservationKind
from palm.system.assembly.place_spawn import InProcessPlaceSpawn, PlaceSpawnPort

PlaceState = Literal["ready", "failed", "gone"]


@dataclass
class InProcessPlaceBook:
    """Local place ledger for one process (structure only)."""

    places: dict[str, PlaceState] = field(default_factory=dict)

    def ensure(self, place_id: str) -> PlaceState:
        key = str(place_id or "").strip()
        if not key:
            return "failed"
        # Floor: ensure = present and ready (no external body yet).
        self.places[key] = "ready"
        return "ready"

    def mark(self, place_id: str, state: PlaceState) -> None:
        key = str(place_id or "").strip()
        if not key:
            return
        if state == "gone":
            self.places.pop(key, None)
        else:
            self.places[key] = state

    def release(self, place_id: str) -> PlaceState:
        key = str(place_id or "").strip()
        if not key:
            return "gone"
        self.places.pop(key, None)
        return "gone"

    def status(self) -> dict[str, str]:
        return dict(self.places)


@dataclass
class PlaceBookEffectPort:
    """Apply structure intents against ledger + optional spawn port (0.63.14)."""

    book: InProcessPlaceBook = field(default_factory=InProcessPlaceBook)
    spawn: PlaceSpawnPort = field(default_factory=InProcessPlaceSpawn)
    applied: list[EffectIntent] = field(default_factory=list)

    def apply(self, intent: EffectIntent) -> tuple[Observation, ...]:
        self.applied.append(intent)
        kind = intent.kind
        target = str(intent.target or "").strip()

        if kind is EffectIntentKind.ENSURE_PLACE:
            if not target:
                return (
                    Observation(
                        kind=ObservationKind.PLACE_FAILED,
                        target="",
                        payload={"reason": "empty_place_id"},
                    ),
                )
            # Spawn hands first (structure body); ledger records the outcome.
            result = self.spawn.ensure(target, payload=dict(intent.payload or {}))
            if result.state == "ready":
                self.book.mark(target, "ready")
                return (
                    Observation(
                        kind=ObservationKind.PLACE_READY,
                        target=target,
                        payload={"spawn": result.reason, **dict(result.payload)},
                    ),
                )
            self.book.mark(target, "failed")
            return (
                Observation(
                    kind=ObservationKind.PLACE_FAILED,
                    target=target,
                    payload={
                        "reason": result.reason or result.state,
                        **dict(result.payload),
                    },
                ),
            )

        if kind is EffectIntentKind.RELEASE_PLACE:
            if target:
                result = self.spawn.release(target)
                self.book.release(target)
                return (
                    Observation(
                        kind=ObservationKind.PLACE_GONE,
                        target=target,
                        payload={"spawn": result.reason},
                    ),
                )
            return ()

        # Other structure intents: recorded, no observation yet (growth).
        return ()


__all__ = [
    "InProcessPlaceBook",
    "PlaceBookEffectPort",
    "PlaceState",
]
