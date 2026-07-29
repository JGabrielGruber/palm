"""Shim (SD-012) — canonical: :mod:`palm.system.planes.wait.plane`."""

from palm.system.planes.wait.plane import (
    WaitPlaneService,
    bind_wait_plane_to_runtime,
)

__all__ = [
    "WaitPlaneService",
    "bind_wait_plane_to_runtime",
]
