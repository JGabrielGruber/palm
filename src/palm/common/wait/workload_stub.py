"""Shim (SD-012) — canonical: :mod:`palm.system.planes.wait.workload_stub`."""

from palm.system.planes.wait.workload_stub import *  # noqa: F403
from palm.system.planes.wait import workload_stub as _mod

# Re-export public names from the canonical module.
__all__ = getattr(_mod, "__all__", [n for n in dir(_mod) if not n.startswith("_")])
