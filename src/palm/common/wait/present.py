"""Shim (SD-012) — canonical: :mod:`palm.system.planes.wait.present`."""

from palm.system.planes.wait.present import *  # noqa: F403
from palm.system.planes.wait import present as _mod

# Re-export public names from the canonical module.
__all__ = getattr(_mod, "__all__", [n for n in dir(_mod) if not n.startswith("_")])
