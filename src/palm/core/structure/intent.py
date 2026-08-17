"""Effect intents — structure actions the pure engine requests (closed set)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4


class EffectIntentKind(StrEnum):
    """Closed set of structure effects. Grow by theme, not free strings."""

    ENSURE_PLACE = "ensure_place"
    RELEASE_PLACE = "release_place"
    INVALIDATE_PROJECTION = "invalidate_projection"
    REFRESH_PROJECTION = "refresh_projection"
    APPLY_STRUCTURE_POLICY = "apply_structure_policy"
    REQUEST_STRUCTURE_SEED = "request_structure_seed"


@dataclass(frozen=True, slots=True)
class EffectIntent:
    """One structure action for the system structure effect port to apply."""

    kind: EffectIntentKind
    target: str = ""
    """Place key, projection name, or policy id — meaning depends on kind."""

    intent_id: str = field(default_factory=lambda: uuid4().hex)
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "kind": str(self.kind),
            "target": self.target,
            "payload": dict(self.payload),
        }


__all__ = [
    "EffectIntent",
    "EffectIntentKind",
]
