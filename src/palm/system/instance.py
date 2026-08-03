"""
SystemInstance — one started running Palm.

Today the concrete type is :class:`~palm.system.runtime.base.BaseRuntime`.
Later slices move that type under ``palm.system.runtime``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from palm.system.ports.execution import ExecutionPort
from palm.system.ports.install import InstallInterface


@runtime_checkable
class SystemInstance(Protocol):
    """
    Contract for one running Palm machine (shell of interfaces + subsystems).

    Supersedes the thin :class:`~palm.system.runtime.host.RuntimeHost` for new
    code. Product and graphs resolve a system instance and call **interfaces**,
    not engine fields on the edge.

    **DI law:** inject :attr:`execution` / :attr:`install` (and subsystems),
    not the whole shell, when a call only needs those seats.
    """

    @property
    def is_started(self) -> bool:
        """Whether the instance accepts work."""
        ...

    @property
    def execution(self) -> ExecutionPort:
        """Resource and workload effect interface (and later job drive as chosen)."""
        ...

    @property
    def install(self) -> InstallInterface:
        """Collaborator install interface (peer of execution)."""
        ...
