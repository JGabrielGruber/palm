"""Doctor section for host WorkloadRuntime."""

from __future__ import annotations

from typing import Any

from palm.core.workload.registry import workload_runtime_registry


def host_workload_doctor_section(
    *,
    enabled: bool | None = None,
    runtime: Any = None,
) -> dict[str, Any]:
    """Report host runner registration and enablement (warn when ON)."""
    registered = "host" in set(workload_runtime_registry.names())
    bound_enabled = enabled
    if bound_enabled is None and runtime is not None:
        wl = getattr(runtime, "workload", None)
        if wl is not None and getattr(wl, "is_initialized", False):
            try:
                for row in wl.runtimes():
                    if row.get("name") == "host":
                        # capabilities default_enabled is False; live enabled via is_enabled
                        bound = wl._runtimes.get("host")  # doctor introspection
                        if bound is not None:
                            bound_enabled = bool(bound.is_enabled())
                        break
            except Exception:
                bound_enabled = None

    issues: list[str] = []
    if bound_enabled:
        issues.append(
            "host WorkloadRuntime is ENABLED — not multi-tenant safe; "
            "disable unless local dogfood (PALM_WORKLOAD_HOST_ENABLED)"
        )

    return {
        "registered": registered,
        "enabled": bound_enabled,
        "default_enabled": False,
        "isolation_modes": ["host", "best_effort"],
        "kinds": ["run"],
        "issues": issues,
        "note": (
            "Host runtime runs argv via subprocess on the Palm machine. "
            "Default OFF. Hermetic isolation cannot select host."
        ),
    }


def host_workload_doctor_issues(section: dict[str, Any]) -> list[str]:
    raw = section.get("issues") if isinstance(section, dict) else None
    if not isinstance(raw, list):
        return []
    return [str(x) for x in raw]


__all__ = ["host_workload_doctor_issues", "host_workload_doctor_section"]
