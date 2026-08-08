"""In-process place book — assembly effect hands for ENSURE/RELEASE place (0.63.11).

Not OS spawn. Not Grove. A **ledger of places** the household can mark ready
so DNA with places_required can converge. Growth wires real place-book spawn.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from palm.core.assembly import EffectIntent, EffectIntentKind, Observation, ObservationKind

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
    """Apply structure intents against an :class:`InProcessPlaceBook`."""

    book: InProcessPlaceBook = field(default_factory=InProcessPlaceBook)
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
            state = self.book.ensure(target)
            if state == "ready":
                return (
                    Observation(kind=ObservationKind.PLACE_READY, target=target),
                )
            return (
                Observation(
                    kind=ObservationKind.PLACE_FAILED,
                    target=target,
                    payload={"reason": state},
                ),
            )

        if kind is EffectIntentKind.RELEASE_PLACE:
            if target:
                self.book.release(target)
                return (Observation(kind=ObservationKind.PLACE_GONE, target=target),)
            return ()

        # Other structure intents: recorded, no observation yet (growth).
        return ()


__all__ = [
    "InProcessPlaceBook",
    "PlaceBookEffectPort",
    "PlaceState",
]
