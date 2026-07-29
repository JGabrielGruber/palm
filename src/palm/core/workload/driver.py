"""
WorkloadDriver — narrow effect protocol for graphs (0.57.4 / P2).

WorkloadLeaf and patterns call this instead of requiring concrete WorkloadEngine.
WorkloadEngine implements it. System adapters map ExecutionPort onto it.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.record import Workload
from palm.core.workload.spec import WorkloadSpec


@runtime_checkable
class WorkloadDriver(Protocol):
    """Minimal workload effect surface for WorkloadLeaf and pattern ticks."""

    @property
    def is_initialized(self) -> bool:
        """Whether the driver is ready for start/status/stop."""
        ...

    def initialize(self, **options: Any) -> None:
        """Initialize if needed (may be a no-op for adapters)."""
        ...

    def start(
        self,
        spec: WorkloadSpec,
        *,
        owner: WorkloadOwner | None = None,
        workload_id: str | None = None,
        idempotency_key: str | None = None,
        host_id: str | None = None,
    ) -> Workload:
        """Start a workload; return a live snapshot."""
        ...

    def status(self, workload_id: str, *, refresh: bool = False) -> Workload:
        """Return workload snapshot; optionally poll the runtime."""
        ...

    def stop(self, workload_id: str) -> Workload:
        """Idempotent stop."""
        ...
