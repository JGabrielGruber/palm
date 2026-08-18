"""NeonRoot WorkloadRuntime doctor — aligns with RuntimeHealth."""

from __future__ import annotations

from typing import Any

from palm.core.workload.registry import workload_runtime_registry
from palm.runners.neonroot.cli import probe_neonroot
from palm.runners.neonroot.runtime import NeonrootWorkloadRuntime


def neonroot_doctor_section(
    *,
    runtime: Any = None,
) -> dict[str, Any]:
    """Probe CLI + registry; prefer live bound runtime.health() when present."""
    registered = "neonroot" in set(workload_runtime_registry.names())
    health: dict[str, Any] | None = None
    engine = getattr(runtime, "workload", None) if runtime is not None else None
    if engine is not None and getattr(engine, "is_initialized", False):
        try:
            for row in engine.runtimes():
                if row.get("name") == "neonroot" and isinstance(row.get("health"), dict):
                    health = dict(row["health"])
                    break
        except Exception:
            health = None

    if health is None:
        # Standalone probe (same shape as RuntimeHealth.to_dict)
        probe = probe_neonroot()
        health = NeonrootWorkloadRuntime().health().to_dict()
        # refresh from probe in case of drift
        health = {
            "name": "neonroot",
            "available": probe.available,
            "enabled": True,
            "message": probe.version or probe.error or ("ready" if probe.available else "missing"),
            "detail": {
                "path": probe.path,
                "version": probe.version,
                "error": probe.error,
            },
        }

    return {
        "registered": registered,
        "available": bool(health.get("available")),
        "enabled": bool(health.get("enabled", True)),
        "path": (health.get("detail") or {}).get("path"),
        "version": (health.get("detail") or {}).get("version"),
        "error": (health.get("detail") or {}).get("error"),
        "health": health,
        "role": "workload_runtime",
        "trust": "hermetic",
        "kinds": ("run",),
        "images_hint": ("palm-ci", "palm-docs"),
        "issues": [],
        "note": (
            "NeonRoot is a WorkloadRuntime. Map WorkloadSpec via spec_map; "
            "start via WorkloadEngine / step_kind=workload / execution.workloads."
        ),
    }


def neonroot_doctor_issues(section: dict[str, Any]) -> list[str]:
    raw = section.get("issues") if isinstance(section, dict) else None
    if not isinstance(raw, list):
        return []
    return [str(x) for x in raw]


__all__ = ["neonroot_doctor_issues", "neonroot_doctor_section"]
