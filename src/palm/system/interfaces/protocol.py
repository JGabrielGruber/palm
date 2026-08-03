"""
System interface protocol — thin DIP surface for shell seats that supply contracts.

Implementations: :class:`~palm.system.interfaces.execution.ExecutionPort`,
:class:`~palm.system.interfaces.install.InstallInterface`.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SystemInterface(Protocol):
    """
    Optional umbrella for named contracts on the system shell.

    Individual interfaces define their own methods. This protocol only
    requires a public :meth:`status` when useful for vitality / doctor.
    """

    def status(self) -> dict[str, Any]:
        """Public snapshot for observation."""
        ...


__all__ = ["SystemInterface"]
