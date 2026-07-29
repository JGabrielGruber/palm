"""Shim (SD-012) — canonical: :mod:`palm.system.planes.workload`."""

from palm.system.planes.workload import *  # noqa: F403
from palm.system.planes import workload as _mod

__all__ = getattr(_mod, "__all__", [])
