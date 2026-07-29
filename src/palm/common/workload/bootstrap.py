"""Shim (SD-012) — canonical: :mod:`palm.system.planes.workload.bootstrap`."""

from palm.system.planes.workload.bootstrap import *  # noqa: F403
from palm.system.planes.workload import bootstrap as _mod

__all__ = getattr(_mod, "__all__", [n for n in dir(_mod) if not n.startswith("_")])
