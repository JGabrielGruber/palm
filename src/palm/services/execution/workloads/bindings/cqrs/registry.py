"""Workload CQRS command/query type catalog."""

from __future__ import annotations

from palm.services.execution.workloads.bindings.cqrs.commands import (
    CancelWorkloadCommand,
    ExecWorkloadCommand,
    StartWorkloadCommand,
    StopWorkloadCommand,
)
from palm.services.execution.workloads.bindings.cqrs.queries import (
    GetWorkloadQuery,
    ListWorkloadHostsQuery,
    ListWorkloadRuntimesQuery,
    ListWorkloadsQuery,
)

WORKLOAD_COMMAND_TYPES: tuple[type, ...] = (
    StartWorkloadCommand,
    ExecWorkloadCommand,
    StopWorkloadCommand,
    CancelWorkloadCommand,
)

WORKLOAD_QUERY_TYPES: tuple[type, ...] = (
    GetWorkloadQuery,
    ListWorkloadsQuery,
    ListWorkloadHostsQuery,
    ListWorkloadRuntimesQuery,
)

__all__ = ["WORKLOAD_COMMAND_TYPES", "WORKLOAD_QUERY_TYPES"]
