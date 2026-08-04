"""Work plane definition — install law at the edge (SD-015)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from palm.system.subsystems.planes.definition import PlaneDefinition
from palm.system.subsystems.planes.install_context import InstallContext
from palm.system.subsystems.planes.work.plane import WorkPlaneService

if TYPE_CHECKING:
    from palm.system.subsystems.planes.hub import SystemPlanes


def install_work_plane(
    hub: SystemPlanes,
    ctx: InstallContext,
) -> WorkPlaneService:
    """Construct work plane from *ctx* ports, put as ``work``."""
    opts = dict(ctx.options or {})
    storage = ctx.storage
    if storage is None:
        raise RuntimeError("runtime has no storage for work plane")
    submit_flow = ctx.submit_flow
    if submit_flow is None:
        raise RuntimeError("no submit_flow port for work plane")
    able = ctx.able if ctx.able is not None else (lambda: True)
    max_depth = int(opts.get("work_drain_max_depth", 8) or 8)
    batch_size = int(opts.get("work_drain_batch_size", 10) or 10)
    poll_interval = float(opts.get("work_drain_poll_interval", 1.0) or 1.0)
    workers = int(opts.get("work_drain_workers", 1) or 1)
    lease_seconds = float(opts.get("work_drain_lease_seconds", 60.0) or 60.0)
    claimer_id = str(opts.get("work_drain_claimer_id") or "default")
    plane = WorkPlaneService()
    plane.attach(
        storage=storage,
        submit_flow=submit_flow,
        able=able,
        event=ctx.event,
        max_depth=max_depth,
        batch_size=batch_size,
        poll_interval=poll_interval,
        workers=workers,
        lease_seconds=lease_seconds,
        claimer_id=claimer_id,
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
