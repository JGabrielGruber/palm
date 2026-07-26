"""NeonRoot provider registration."""

from palm.core.registry import provider_registry
from palm.providers.neonroot.app import neonroot_app
from palm.providers.neonroot.provider import NeonrootProvider

provider_registry.register("neonroot", NeonrootProvider)
neonroot_app.register()
