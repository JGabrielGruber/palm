"""Library provider registration."""

from palm.core.registry import provider_registry
from palm.providers.library.app import library_app
from palm.providers.library.provider import LibraryProvider

provider_registry.register("library", LibraryProvider)
library_app.register()
