"""
Resolve graph effect surfaces from PatternBuildContext (0.57.4).

Prefer ExecutionPort when present so production builds share the same port
as product. Fall back to engine fields for unit tests that inject engines only.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from palm.core.resource.invoker import ResourceInvoker
from palm.core.workload.driver import WorkloadDriver

if TYPE_CHECKING:
    from palm.common.patterns.build_context import PatternBuildContext


def resolve_resource_invoker(context: PatternBuildContext) -> ResourceInvoker | None:
    """
    Resource effect for pattern materialization.

    Order: ``execution`` port bridge, then ``resource_engine``.
    """
    execution = getattr(context, "execution", None)
    if execution is not None:
        from palm.system.effects import resource_invoker_from_port

        return resource_invoker_from_port(execution)
    return getattr(context, "resource_engine", None)


def resolve_workload_driver(context: PatternBuildContext) -> WorkloadDriver | None:
    """
    Workload effect for pattern materialization.

    Order: ``execution`` port bridge, then ``workload_engine``.
    """
    execution = getattr(context, "execution", None)
    if execution is not None:
        from palm.system.effects import workload_driver_from_port

        return workload_driver_from_port(execution)
    return getattr(context, "workload_engine", None)
