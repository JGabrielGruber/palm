"""
RuntimeHost — structural contract for definition-driven job submission.

Prefer :class:`~palm.system.instance.SystemInstance` + ports for **effects**
(product edges, graphs). Submission still needs orchestration/event engines
to materialize patterns and drive jobs — that is this protocol's purpose.

Not an edge bypass: :class:`~palm.system.executions.executor.DefinitionExecutor`
is system-internal and types against this subset (SD-003).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from palm.core.event import EventEngine
    from palm.core.orchestration import OrchestrationEngine
    from palm.core.resource import ResourceEngine
    from palm.system.interfaces.execution import ExecutionPort


@runtime_checkable
class RuntimeHost(Protocol):
    """
    Engines the definition executor needs to submit and resume jobs.

    Live system instances also expose :attr:`execution` (preferred for effects).
    New product code should not type only this protocol when calling effects.
    """

    @property
    def orchestration(self) -> OrchestrationEngine:
        """Job lifecycle coordinator."""

    @property
    def event(self) -> EventEngine:
        """Observability bus used when materializing patterns."""

    @property
    def resource(self) -> ResourceEngine | None:
        """Optional external provider coordinator."""

    @property
    def is_started(self) -> bool:
        """Whether the host has completed startup and accepts submissions."""

    @property
    def execution(self) -> ExecutionPort:
        """Effect/inspect port (same surface as SystemInstance.execution)."""
