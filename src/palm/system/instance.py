"""
SystemInstance — one started running Palm.

Today the concrete type is :class:`~palm.system.runtime.base.BaseRuntime`.
Later slices move that type under ``palm.system.runtime``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from palm.system.ports.execution import ExecutionPort
from palm.system.ports.wire import WirePort


@runtime_checkable
class SystemInstance(Protocol):
    """
    Contract for one running Palm machine (engines + ports + planes).

    Supersedes the thin :class:`~palm.system.runtime.host.RuntimeHost` for new
    code. Product and graphs resolve a system instance and call **ports**, not
    engine fields on the edge.
    """

    @property
    def is_started(self) -> bool:
        """Whether the instance accepts work."""
        ...

    @property
    def execution(self) -> ExecutionPort:
        """Resource and workload effect port (and later job drive as chosen)."""
        ...

    @property
    def wire(self) -> WirePort:
        """Collaborator wire port for install (peer of execution)."""
        ...
