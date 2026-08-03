"""
Bridge ExecutionPort to core graph protocols (ResourceInvoker, WorkloadDriver).

Patterns and leaves stay on core protocols. Product and system expose ExecutionPort.
These adapters are the only place that maps port method names onto engine shapes.
"""

from __future__ import annotations

from typing import Any

from palm.core.resource.invoker import ResourceInvoker
from palm.core.resource.result import ProviderResult
from palm.core.workload.driver import WorkloadDriver
from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.record import Workload
from palm.core.workload.spec import WorkloadSpec
from palm.system.interfaces.execution import ExecutionPort


class PortResourceInvoker:
    """Adapt :class:`~palm.system.interfaces.execution.ExecutionPort` to ResourceInvoker."""

    __slots__ = ("_port",)

    def __init__(self, port: ExecutionPort) -> None:
        self._port = port

    @property
    def is_initialized(self) -> bool:
        return True

    def initialize(self, **options: Any) -> None:
        del options

    def invoke(
        self,
        resource_ref: str | None = None,
        *,
        provider: str | None = None,
        action: str | None = None,
        params: dict[str, Any] | None = None,
        state: Any = None,
        resource_id: str | None = None,
        correlation: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ProviderResult:
        del kwargs
        result = self._port.invoke_resource(
            resource_ref,
            provider=provider,
            action=action,
            params=params,
            state=state,
            resource_id=resource_id,
            correlation=correlation,
        )
        if isinstance(result, ProviderResult):
            return result
        raise TypeError(
            f"ExecutionPort.invoke_resource must return ProviderResult, got {type(result)!r}"
        )


class PortWorkloadDriver:
    """Adapt :class:`~palm.system.interfaces.execution.ExecutionPort` to WorkloadDriver."""

    __slots__ = ("_port",)

    def __init__(self, port: ExecutionPort) -> None:
        self._port = port

    @property
    def is_initialized(self) -> bool:
        return True

    def initialize(self, **options: Any) -> None:
        del options

    def start(
        self,
        spec: WorkloadSpec,
        *,
        owner: WorkloadOwner | None = None,
        workload_id: str | None = None,
        idempotency_key: str | None = None,
        host_id: str | None = None,
    ) -> Workload:
        result = self._port.start_workload(
            spec,
            owner=owner,
            workload_id=workload_id,
            idempotency_key=idempotency_key,
            host_id=host_id,
        )
        return _as_workload(result)

    def status(self, workload_id: str, *, refresh: bool = False) -> Workload:
        return _as_workload(
            self._port.workload_status(str(workload_id), refresh=refresh)
        )

    def stop(self, workload_id: str) -> Workload:
        return _as_workload(self._port.stop_workload(str(workload_id)))


def resource_invoker_from_port(port: ExecutionPort) -> ResourceInvoker:
    """Return a ResourceInvoker backed by the execution port."""
    return PortResourceInvoker(port)


def workload_driver_from_port(port: ExecutionPort) -> WorkloadDriver:
    """Return a WorkloadDriver backed by the execution port."""
    return PortWorkloadDriver(port)


def _as_workload(value: Any) -> Workload:
    if isinstance(value, Workload):
        return value
    raise TypeError(f"ExecutionPort workload methods must return Workload, got {type(value)!r}")
