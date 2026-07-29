"""Shim (SD-012) — canonical: :mod:`palm.system.planes.workload.run_python`."""

from palm.system.planes.workload.run_python import *  # noqa: F403
from palm.system.planes.workload import run_python as _mod

__all__ = getattr(_mod, "__all__", [n for n in dir(_mod) if not n.startswith("_")])
