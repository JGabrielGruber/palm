"""Library provider app manifest (0.54.4)."""

from __future__ import annotations

from palm.common.providers.app import ProviderApp


class LibraryApp(ProviderApp):
    name = "library"
    label = "Living Library corpus publish / status (storage-backed)"
    palm_layers = ("core.resource", "core.storage", "common.library")
    actions = (
        "publish_wiki",
        "status",
        "get",
        "list_paths",
    )
    registry_hooks = ("provider_registry",)


library_app = LibraryApp()

__all__ = ["LibraryApp", "library_app"]
