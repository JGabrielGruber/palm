"""Session plane definition — install law at the edge (SD-015)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from palm.system.subsystems.planes.definition import PlaneDefinition
from palm.system.subsystems.planes.install_context import InstallContext
from palm.system.subsystems.planes.session.plane import SessionPlaneError, SessionPlaneService

if TYPE_CHECKING:
    from palm.system.subsystems.planes.hub import SystemPlanes


def install_session_plane(
    hub: SystemPlanes,
    ctx: InstallContext,
) -> SessionPlaneService:
    """Construct (or re-wire) session plane from *ctx* ports, put as ``session``."""
    wait = hub.get("wait")
    im = ctx.instance_manager
    get_job = ctx.get_job

    existing = hub.get("session")
    if ctx.reuse_existing and isinstance(existing, SessionPlaneService):
        plane = existing
        plane.attach(
            instance_manager=im,
            get_job=get_job,
            wait_plane=wait,
        )
        if hub.get("session") is not plane:
            hub.put(SESSION_PLANE.name, plane, aliases=SESSION_PLANE.aliases)
    else:
        storage = ctx.storage
        if storage is None:
            raise SessionPlaneError("runtime has no storage for session plane")
        plane = SessionPlaneService(storage=storage)
        plane.attach(
            instance_manager=im,
            get_job=get_job,
            wait_plane=wait,
        )
        hub.put(SESSION_PLANE.name, plane, aliases=SESSION_PLANE.aliases)

    # BI-014: host service session is required when the session plane installs.
    # Fail closed — do not swallow storage / plane errors at system start.
    plane.ensure_host_session()
    return plane


SESSION_PLANE = PlaneDefinition(
    name="session",
    aliases=("session_plane",),
    order=20,
    after=("wait",),
    install=install_session_plane,
)


__all__ = [
    "SESSION_PLANE",
    "install_session_plane",
]
