"""
Core host service providers (T2 / 0.48.2).

Core services and their construction, declared as dependency-ordered
``ServiceProvider`` entries. The host builds them via
``HostServiceRegistry.build_all(ctx)``.

Construction order encoded by ``depends_on``:
``inspect`` → ``session`` → ``definitions`` → ``execution`` →
``assist``/``design``/``analytics``.
The ``assist.bind_analytics(analytics)`` cross-wire stays an explicit host
post-build step (a mutual link, not a construction dependency).

**0.58.12:** product ``session`` is the surface door over the system session plane.
**0.61.4 / SD-007:** product inspect door is ``inspect`` (was ``system``).
"""

from __future__ import annotations

from typing import Any

from palm.app.host.services.registry import HostServiceContext, HostServiceRegistry, ServiceProvider
from palm.services.analytics import AnalyticsService
from palm.services.assist import AssistService
from palm.services.definitions import DefinitionService
from palm.services.design import DesignService
from palm.services.design.factory import create_proposal_repository
from palm.services.execution import ExecutionService
from palm.services.execution.flows import FlowExecutionService
from palm.services.execution.processes import ProcessExecutionService
from palm.services.execution.providers import ProviderExecutionService
from palm.services.execution.workloads import WorkloadExecutionService
from palm.services.inspect import InspectService
from palm.services.session import SessionService


def _build_inspect(ctx: HostServiceContext, built: dict[str, Any]) -> Any:
    return InspectService(**ctx.bus_kwargs)


def _build_session(ctx: HostServiceContext, built: dict[str, Any]) -> Any:
    return SessionService(
        **ctx.bus_kwargs,
        inspect=built["inspect"],
        runtime_resolver=ctx.resolve_execution_runtime,
        strict_attribution=bool(
            getattr(ctx.settings, "session_strict_attribution", True)
        ),
    )


def _build_definitions(ctx: HostServiceContext, built: dict[str, Any]) -> Any:
    return DefinitionService(**ctx.bus_kwargs, repository=ctx.app.repository())


def _build_execution(ctx: HostServiceContext, built: dict[str, Any]) -> Any:
    flows = FlowExecutionService(
        **ctx.bus_kwargs,
        inspect=built["inspect"],
        session=built.get("session"),
        runtime_resolver=ctx.resolve_execution_runtime,
    )
    providers = ProviderExecutionService(
        **ctx.bus_kwargs,
        runtime_resolver=ctx.resolve_execution_runtime,
        definitions=built["definitions"],
        event_engine=ctx.event,
    )
    processes = ProcessExecutionService(
        **ctx.bus_kwargs,
        runtime_resolver=ctx.resolve_execution_runtime,
    )
    workloads = WorkloadExecutionService(
        **ctx.bus_kwargs,
        runtime_resolver=ctx.resolve_execution_runtime,
    )
    return ExecutionService(
        flows=flows,
        providers=providers,
        processes=processes,
        workloads=workloads,
    )


def _build_assist(ctx: HostServiceContext, built: dict[str, Any]) -> Any:
    return AssistService(
        **ctx.bus_kwargs,
        definitions=built["definitions"],
        execution=built["execution"],
        inspect=built["inspect"],
        session=built.get("session"),
        runtime_resolver=ctx.resolve_execution_runtime,
    )


def _build_design(ctx: HostServiceContext, built: dict[str, Any]) -> Any:
    return DesignService(
        **ctx.bus_kwargs,
        definitions=built["definitions"],
        proposals=create_proposal_repository(ctx.app.storage),
        runtime_resolver=ctx.resolve_execution_runtime,
    )


def _build_analytics(ctx: HostServiceContext, built: dict[str, Any]) -> Any:
    settings = ctx.settings
    allow_unpub = bool(settings.analytics_allow_unpublished)
    if settings.analytics_allow_unpublished_with_server:
        allow_unpub = True
    return AnalyticsService(
        definitions=built["definitions"],
        providers=built["execution"].providers,
        commands=ctx.command_bus,
        queries=ctx.query_bus,
        schemas=ctx.schemas,
        allow_unpublished=allow_unpub,
        default_limit=int(settings.analytics_default_limit),
        max_limit=int(settings.analytics_max_limit),
        max_response_bytes=int(settings.analytics_max_response_bytes),
        enabled=bool(settings.analytics_enabled),
    )


CORE_SERVICE_PROVIDERS: tuple[ServiceProvider, ...] = (
    ServiceProvider("inspect", _build_inspect),
    ServiceProvider("session", _build_session, depends_on=("inspect",)),
    ServiceProvider("definitions", _build_definitions),
    ServiceProvider(
        "execution",
        _build_execution,
        depends_on=("inspect", "definitions", "session"),
    ),
    ServiceProvider(
        "assist",
        _build_assist,
        depends_on=("definitions", "execution", "inspect", "session"),
    ),
    ServiceProvider("design", _build_design, depends_on=("definitions",)),
    ServiceProvider("analytics", _build_analytics, depends_on=("definitions", "execution")),
)


def core_service_registry() -> HostServiceRegistry:
    """A fresh registry pre-loaded with the core host service providers."""
    registry = HostServiceRegistry()
    for provider in CORE_SERVICE_PROVIDERS:
        registry.register(provider)
    return registry


__all__ = ["CORE_SERVICE_PROVIDERS", "core_service_registry"]
