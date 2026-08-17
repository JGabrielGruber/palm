"""Effect port — apply structure effect intents (system hands).

Floor: no place-registry spawn yet. ENSURE_PLACE is recorded and can be
auto-satisfied for tests via ``auto_ack_places`` (default off in production;
on for pure loop dogfood when no place registry is wired).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from palm.core.assembly import EffectIntent, EffectIntentKind, Observation, ObservationKind


@runtime_checkable
class EffectPort(Protocol):
    """Apply one structure intent; return observations to fold back."""

    def apply(self, intent: EffectIntent) -> tuple[Observation, ...]: ...


@dataclass
class RecordingEffectPort:
    """Records intents; optional auto-ack for ensure_place (floor / tests)."""

    auto_ack_places: bool = False
    applied: list[EffectIntent] = field(default_factory=list)
    on_apply: Callable[[EffectIntent], tuple[Observation, ...]] | None = None

    def apply(self, intent: EffectIntent) -> tuple[Observation, ...]:
        self.applied.append(intent)
        if self.on_apply is not None:
            return self.on_apply(intent)
        if (
            intent.kind is EffectIntentKind.ENSURE_PLACE
            and self.auto_ack_places
            and intent.target
        ):
            return (
                Observation(
                    kind=ObservationKind.PLACE_READY,
                    target=intent.target,
                ),
            )
        return ()


__all__ = [
    "EffectPort",
    "RecordingEffectPort",
]
