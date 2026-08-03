"""
Subsystem protocol — membership + lifecycle region on the system shell.

Implementations: :class:`~palm.system.subsystems.planes.hub.SystemPlanes`,
:class:`~palm.system.subsystems.supervisor.supervisor.SystemSupervisor`.

**DI law:** inject a subsystem when you need membership/lifecycle — not the
whole system instance.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Subsystem(Protocol):
    """
    Living membership region: list, get, status.

    Install/register APIs stay family-specific (planes vs continuous services)
    so this protocol stays thin and honest.
    """

    def names(self) -> list[str]:
        """Canonical member names in stable order (or sorted)."""
        ...

    def get(self, name: str) -> Any | None:
        """Member by name, or ``None``."""
        ...

    def status(self) -> dict[str, Any]:
        """Public snapshot for vitality / doctor / boot."""
        ...


__all__ = ["Subsystem"]
