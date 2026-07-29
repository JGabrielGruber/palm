"""
RuntimeHost — thin legacy contract for definition-driven job submission.

Prefer :class:`~palm.system.instance.SystemInstance` + ports for new code (0.57+).
This protocol remains so :class:`~palm.common.executions.executor.DefinitionExecutor`
stays decoupled from a single runtime class during cutover (SD-003).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from palm.core.event import EventEngine
    from palm.core.orchestration import OrchestrationEngine
    from palm.core.resource import ResourceEngine


@runtime_checkable
class RuntimeHost(Protocol):
    """
    Minimal structural subset for the executions layer (legacy).

    Prefer :class:`~palm.system.instance.SystemInstance` and
    :class:`~palm.system.ports.execution.ExecutionPort` for effects.
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
