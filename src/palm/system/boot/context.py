"""Boot walk context — shared fields for phase handlers (0.59.2+ / seat DI)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BootContext:
    """
    Mutable bag passed to phase handlers during a schedule walk.

    **Seats (prefer over digging the shell):**

    | Field | After phase |
    |-------|-------------|
    | ``shell`` | always (system instance) |
    | ``install`` | ``system.install.bind`` |
    | ``planes`` | ``system.planes.attach`` |
    | ``supervisor`` | ``system.supervisor.wire`` |

    Keep free of product types so ``palm.system.boot`` stays pure.
    Host-side handlers may hang collaborators on ``extras``.
    """

    schedule: str
    mode: str | None = None
    runtime: str | None = None
    """Log / identity name of the runtime (string), not the shell object."""
    shell: Any = None
    """System instance that owns seats (assembly target)."""
    install: Any = None
    """InstallInterface after bind phase."""
    planes: Any = None
    """Planes subsystem after attach phase."""
    supervisor: Any = None
    """Supervisor subsystem after wire phase."""
    extras: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.extras.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.extras[key] = value


__all__ = ["BootContext"]
