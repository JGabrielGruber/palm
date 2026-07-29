"""
ExecutionPort — first effect contract for a running Palm system.

Graphs and product must share this port for resource and workload effects.
See docs/SYSTEM-LOW-LEVEL.md §3 and docs/PALM.md.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ExecutionPort(Protocol):
    """
    Effects a started system instance may perform for graphs and product.

    Implementations: live system runtime (:class:`~palm.system.runtime.base.BaseRuntime`)
    and test doubles. Do not treat CQRS or product services as the only truth of effects.
    """

    def invoke_resource(
        self,
        resource_ref: str | None = None,
        *,
        provider: str | None = None,
        action: str | None = None,
        params: dict[str, Any] | None = None,
        state: Any = None,
        resource_id: str | None = None,
        correlation: dict[str, Any] | None = None,
    ) -> Any:
        """Invoke a resource definition or direct provider action."""
        ...

    def start_workload(
        self,
        spec: Any,
        *,
        owner: Any = None,
        workload_id: str | None = None,
        idempotency_key: str | None = None,
        host_id: str | None = None,
    ) -> Any:
        """Start a workload from Spec; return a live snapshot."""
        ...

    def exec_workload(
        self,
        workload_id: str,
        command: list[str] | tuple[str, ...],
        *,
        timeout_s: float | None = None,
        env: dict[str, str] | None = None,
    ) -> Any:
        """Execute argv on a READY workspace/service workload."""
        ...

    def stop_workload(self, workload_id: str, **kwargs: Any) -> Any:
        """Idempotent stop of a workload."""
        ...

    def workload_status(self, workload_id: str, *, refresh: bool = False) -> Any:
        """Return workload snapshot; optionally poll the runtime."""
        ...

    def resume_job(self, job_id: str) -> Any:
        """Re-drive a registered orchestration job (job-drive on the same port)."""
        ...
