"""Boot walk context — shared fields for phase handlers (0.59.2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BootContext:
    """Mutable bag passed to phase handlers during a schedule walk.

    Keep this free of product types so ``palm.system.boot`` stays pure.
    Host-side handlers may hang collaborators on ``extras``.
    """

    schedule: str
    mode: str | None = None
    runtime: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.extras.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.extras[key] = value


__all__ = ["BootContext"]
