"""NeonRoot section for doctor / Assist health reports (0.53.6)."""

from __future__ import annotations

from typing import Any

from palm.core.registry import provider_registry
from palm.providers.neonroot.cli import probe_neonroot


def neonroot_doctor_section(
    *,
    composition_has_neonroot: bool | None = None,
) -> dict[str, Any]:
    """Probe CLI + registry for the Sovereign Runners surface.

    Does **not** spawn containers — health only. Soft issues when the composition
    declares ``neonroot`` but the host binary is missing.
    """
    registered = "neonroot" in set(provider_registry.names())
    probe = probe_neonroot()
    issues: list[str] = []
    if composition_has_neonroot and not probe.available:
        issues.append(
            "composition declares capability 'neonroot' but neonroot CLI is not available "
            f"({probe.error or 'not on PATH'})"
        )
    if registered and not probe.available:
        # Informational — provider is honest when CLI missing (not a hard doctor fail alone).
        pass

    return {
        "registered": registered,
        "available": probe.available,
        "path": probe.path,
        "version": probe.version,
        "error": probe.error,
        "composition_declares": composition_has_neonroot,
        "actions": ("health", "spawn", "list_images"),
        "images_hint": ("palm-ci", "palm-docs"),
        "issues": issues,
        "note": (
            "Hermetic runners: palm resource invoke neonroot-health | "
            "just ci-sandbox / docs-css-sandbox. "
            "Spawn does not load Palm into the container — only seed + command."
        ),
    }


def neonroot_doctor_issues(section: dict[str, Any]) -> list[str]:
    """Issues that should degrade doctor status (soft: composition vs CLI mismatch)."""
    raw = section.get("issues") if isinstance(section, dict) else None
    if not isinstance(raw, list):
        return []
    return [str(x) for x in raw]


__all__ = ["neonroot_doctor_issues", "neonroot_doctor_section"]
