"""Session plane definition — install law at the edge (SD-015)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.system.planes.definition import InstallContext, PlaneDefinition
from palm.system.planes.session.plane import (
    SessionPlaneError,
    SessionPlaneService,
    session_get_job_from_runtime,
)

if TYPE_CHECKING:
    from palm.system.planes.hub import SystemPlanes


def install_session_plane(
    hub: SystemPlanes,
    runtime: Any,
    ctx: InstallContext,
) -> SessionPlaneService:
    """
    Construct (or re-wire) session plane, put as ``session``.

    Uses storage + instance_manager + get_job + wait plane from runtime/hub.
    """
    wait = hub.get("wait")
    if wait is None:
        wait = getattr(runtime, "wait_plane", None)
    im = getattr(runtime, "instance_manager", None)
    get_job = session_get_job_from_runtime(runtime)

    existing = hub.get("session")
    if existing is None:
        existing = getattr(runtime, "session_plane", None)
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
        storage = getattr(runtime, "storage", None)
        if storage is None:
            raise SessionPlaneError("runtime has no storage for session plane")
        plane = SessionPlaneService(storage=storage)
        plane.attach(
            instance_manager=im,
            get_job=get_job,
            wait_plane=wait,
        )
        hub.put(SESSION_PLANE.name, plane, aliases=SESSION_PLANE.aliases)

    try:
        plane.ensure_host_session()
    except Exception as exc:
        if ctx.on_host_session_error is not None:
            ctx.on_host_session_error(exc)
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
