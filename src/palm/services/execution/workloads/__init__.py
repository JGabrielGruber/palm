"""Workload product API under the execution domain."""

from palm.services.execution.workloads.bindings.cqrs import contributor as _cqrs  # noqa: F401
from palm.services.execution.workloads.service import WorkloadExecutionService

__all__ = ["WorkloadExecutionService"]
