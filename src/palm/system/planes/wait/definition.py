"""Wait plane definition — install law at the edge (SD-015)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.system.planes.definition import InstallContext, PlaneDefinition
from palm.system.planes.wait.plane import WaitPlaneService

if TYPE_CHECKING:
    from palm.system.planes.hub import SystemPlanes


def install_wait_plane(
    hub: SystemPlanes,
    runtime: Any,
    ctx: InstallContext,
) -> WaitPlaneService:
    """Construct wait plane, wire orchestration/event, put as ``wait``."""
    orch = getattr(runtime, "orchestration", None)
    if orch is None:
        raise RuntimeError("runtime has no orchestration for wait plane")
    plane = WaitPlaneService()
    plane.attach(
        orchestration=orch,
        event=getattr(runtime, "event", None),
    )
    hub.put(WAIT_PLANE.name, plane, aliases=WAIT_PLANE.aliases)
    return plane


WAIT_PLANE = PlaneDefinition(
    name="wait",
    aliases=("wait_plane",),
    order=10,
    install=install_wait_plane,
)


__all__ = [
    "WAIT_PLANE",
    "install_wait_plane",
]
