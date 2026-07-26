"""NeonRoot provider app manifest (0.53)."""

from __future__ import annotations

from palm.common.providers.app import ProviderApp


class NeonrootApp(ProviderApp):
    name = "neonroot"
    label = "NeonRoot hermetic runners (sandbox spawn / tool images)"
    palm_layers = ("core.resource",)
    actions = (
        "health",
        "spawn",  # 0.53.2 — git-archive | path seed + command
        "list_images",  # later
    )
    registry_hooks = ("provider_registry",)


neonroot_app = NeonrootApp()

__all__ = ["NeonrootApp", "neonroot_app"]
