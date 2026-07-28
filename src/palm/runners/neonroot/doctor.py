"""NeonRoot WorkloadRuntime doctor section (was provider; now runner-only)."""

from __future__ import annotations

from typing import Any

from palm.core.workload.registry import workload_runtime_registry
from palm.runners.neonroot.cli import probe_neonroot


def neonroot_doctor_section(
    *,
    composition_has_neonroot: bool | None = None,
) -> dict[str, Any]:
    """Probe CLI + workload runtime registry (no ResourceEngine provider)."""
    registered = "neonroot" in set(workload_runtime_registry.names())
    probe = probe_neonroot()
    issues: list[str] = []
    if composition_has_neonroot and not probe.available:
        issues.append(
            "composition declares capability 'neonroot' but neonroot CLI is not available "
            f"({probe.error or 'not on PATH'})"
        )

    return {
        "registered": registered,
        "available": probe.available,
        "path": probe.path,
        "version": probe.version,
        "error": probe.error,
        "composition_declares": composition_has_neonroot,
        "role": "workload_runtime",
        "kinds": ("run",),
        "images_hint": ("palm-ci", "palm-docs"),
        "issues": issues,
        "note": (
            "NeonRoot is a WorkloadRuntime (hermetic spawn). "
            "Start via WorkloadEngine / step_kind=workload / execution.workloads — "
            "not ResourceEngine.provider neonroot (removed 0.56)."
        ),
    }


def neonroot_doctor_issues(section: dict[str, Any]) -> list[str]:
    raw = section.get("issues") if isinstance(section, dict) else None
    if not isinstance(raw, list):
        return []
    return [str(x) for x in raw]


__all__ = ["neonroot_doctor_issues", "neonroot_doctor_section"]
