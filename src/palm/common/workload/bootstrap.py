"""Wire WorkloadEngine with bound runner instances (host OFF by default)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from palm.core.workload.engine import WorkloadEngine
from palm.core.workload.protocol import WorkloadRuntime

EventPublisher = Callable[[str, dict[str, Any]], None]


def build_bound_runtimes(
    *,
    host_enabled: bool = False,
    work_root: Path | str | None = None,
) -> dict[str, WorkloadRuntime]:
    """Construct live runtime instances for engine.initialize(runtimes=…)."""
    # Ensure registry classes are registered (side-effect import).
    import palm.runners  # noqa: F401
    from palm.runners.host.runtime import HostWorkloadRuntime
    from palm.runners.neonroot.runtime import NeonrootWorkloadRuntime

    return {
        "host": HostWorkloadRuntime(enabled=host_enabled, work_root=work_root),
        "neonroot": NeonrootWorkloadRuntime(),
    }


def initialize_workload_engine(
    engine: WorkloadEngine,
    *,
    host_enabled: bool = False,
    work_root: Path | str | None = None,
    default_runtime: str | None = None,
    publish_event: EventPublisher | None = None,
) -> WorkloadEngine:
    """Initialize engine with host + neonroot instances."""
    runtimes = build_bound_runtimes(host_enabled=host_enabled, work_root=work_root)
    engine.initialize(
        runtimes=runtimes,
        default_runtime=default_runtime,
        publish_event=publish_event,
    )
    return engine


def workload_doctor_section(runtime: Any = None) -> dict[str, Any]:
    """Aggregate workload plane doctor view."""
    import palm.runners  # noqa: F401
    from palm.core.workload.registry import workload_runtime_registry
    from palm.runners.host.doctor import host_workload_doctor_section

    registered = sorted(workload_runtime_registry.names())
    host_section = host_workload_doctor_section(runtime=runtime)

    engine = getattr(runtime, "workload", None) if runtime is not None else None
    engine_ready = bool(
        engine is not None and getattr(engine, "is_initialized", False)
    )
    runtime_rows: list[dict[str, Any]] = []
    if engine_ready:
        try:
            runtime_rows = list(engine.runtimes())
        except Exception as exc:
            runtime_rows = [{"error": str(exc)}]

    issues: list[str] = list(host_section.get("issues") or [])
    return {
        "engine_initialized": engine_ready,
        "registered_runtimes": registered,
        "runtimes": runtime_rows,
        "host": host_section,
        "issues": issues,
        "note": (
            "Workload plane: allocate via WorkloadEngine; host default OFF; "
            "neonroot is hermetic isolation runtime (provider façade still for dogfood)."
        ),
    }


__all__ = [
    "build_bound_runtimes",
    "initialize_workload_engine",
    "workload_doctor_section",
]
