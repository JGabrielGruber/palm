"""NeonRoot provider app manifest (0.53)."""

from __future__ import annotations

from typing import Any

from palm.common.providers.app import ProviderApp
from palm.common.runtimes.doctor_contributors import register_doctor_contributor


def _neonroot_doctor_contributor(runtime: Any) -> dict[str, Any]:
    """Register-downward doctor section (avoids common → providers import)."""
    from palm.providers.neonroot.doctor import (
        neonroot_doctor_issues,
        neonroot_doctor_section,
    )

    composition_has_neonroot: bool | None = None
    for attr in ("application_host", "host_bridge", "_host_bridge", "host"):
        host = getattr(runtime, attr, None)
        if host is None:
            continue
        composition = getattr(host, "composition", None)
        if composition is not None and hasattr(composition, "has"):
            try:
                composition_has_neonroot = bool(composition.has("neonroot"))
            except Exception:
                composition_has_neonroot = None
            break
    try:
        section = neonroot_doctor_section(
            composition_has_neonroot=composition_has_neonroot,
        )
        return {
            "section": {"neonroot": section},
            "issues": neonroot_doctor_issues(section),
        }
    except Exception as exc:
        return {
            "section": {
                "neonroot": {
                    "available": False,
                    "error": f"neonroot doctor probe failed: {exc}",
                }
            },
            "issues": [],
        }


class NeonrootApp(ProviderApp):
    name = "neonroot"
    label = "NeonRoot hermetic runners (sandbox spawn / tool images)"
    palm_layers = ("core.resource",)
    actions = (
        "health",
        "spawn",  # hermetic job
        "run_script",  # Assist run-code: stage payload + spawn
        "list_images",  # later
    )
    registry_hooks = ("provider_registry",)

    def ready(self) -> None:
        register_doctor_contributor(_neonroot_doctor_contributor)


neonroot_app = NeonrootApp()

__all__ = ["NeonrootApp", "neonroot_app"]

