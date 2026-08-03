"""Work plane definition — install law at the edge (SD-015)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.system.planes.definition import InstallContext, PlaneDefinition
from palm.system.planes.work.plane import WorkPlaneService, default_submit_flow

if TYPE_CHECKING:
    from palm.system.planes.hub import SystemPlanes


def install_work_plane(
    hub: SystemPlanes,
    runtime: Any,
    ctx: InstallContext,
) -> WorkPlaneService:
    """Construct work plane, wire storage/submit/able/event, put as ``work``."""
    opts = dict(ctx.options or {})
    storage = getattr(runtime, "storage", None)
    if storage is None:
        raise RuntimeError("runtime has no storage for work plane")
    max_depth = int(opts.get("work_drain_max_depth", 8) or 8)
    batch_size = int(opts.get("work_drain_batch_size", 10) or 10)
    poll_interval = float(opts.get("work_drain_poll_interval", 1.0) or 1.0)
    plane = WorkPlaneService()
    plane.attach(
        storage=storage,
        submit_flow=default_submit_flow(runtime),
        able=lambda: bool(getattr(runtime, "is_started", False)),
        event=getattr(runtime, "event", None),
        max_depth=max_depth,
        batch_size=batch_size,
        poll_interval=poll_interval,
    )
    hub.put(WORK_PLANE.name, plane, aliases=WORK_PLANE.aliases)
    return plane


WORK_PLANE = PlaneDefinition(
    name="work",
    aliases=("work_plane",),
    order=30,
    after=("session",),
    install=install_work_plane,
)


__all__ = [
    "WORK_PLANE",
    "install_work_plane",
]
