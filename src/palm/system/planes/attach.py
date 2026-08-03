"""
Attach / detach system planes from the roster (0.61).

**Roster** = what. **This module** = how (constructors differ per plane).
Schedule and shutdown call these; they must not re-list plane names.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from palm.system.planes.roster import SYSTEM_PLANES, SystemPlaneSpec, missing_roster_planes
from palm.system.planes.session.plane import SessionPlaneService
from palm.system.planes.wait.plane import WaitPlaneService
from palm.system.planes.work.plane import WorkPlaneService

# plane_id → (runtime, options, boot_ctx) -> plane instance (already attached)
PlaneAttacher = Callable[[Any, Mapping[str, Any], Any], Any]


def get_attached_plane(runtime: Any, plane_id_or_attr: str) -> Any | None:
    """Resolve a roster plane on *runtime* (public property, then private field)."""
    from palm.system.planes.roster import get_system_plane

    spec = get_system_plane(plane_id_or_attr)
    if spec is None:
        return None
    plane = getattr(runtime, spec.attr, None)
    if plane is not None:
        return plane
    return getattr(runtime, spec.private_attr, None)


def set_attached_plane(runtime: Any, spec: SystemPlaneSpec, plane: Any | None) -> None:
    """Write the private backing field for *spec* (public property reads it)."""
    setattr(runtime, spec.private_attr, plane)


def _attach_wait(runtime: Any, options: Mapping[str, Any], ctx: Any) -> Any:
    plane = WaitPlaneService()
    plane.attach(runtime)
    return plane


def _attach_session(runtime: Any, options: Mapping[str, Any], ctx: Any) -> Any:
    plane = SessionPlaneService(storage=runtime.storage)
    plane.attach(runtime)
    try:
        plane.ensure_host_session()
    except Exception as exc:
        # BI-014 — still swallowed; honesty later.
        try:
            from palm.system.log import get_system_log

            get_system_log().system(
                "plane.session.host_session",
                f"ensure_host_session swallowed: {type(exc).__name__}",
                runtime=getattr(ctx, "runtime", None),
                reason=str(exc),
            )
        except Exception:
            pass
    return plane


def _attach_work(runtime: Any, options: Mapping[str, Any], ctx: Any) -> Any:
    max_depth = int(options.get("work_drain_max_depth", 8) or 8)
    batch_size = int(options.get("work_drain_batch_size", 10) or 10)
    poll_interval = float(options.get("work_drain_poll_interval", 1.0) or 1.0)
    plane = WorkPlaneService()
    plane.attach(
        runtime,
        max_depth=max_depth,
        batch_size=batch_size,
        poll_interval=poll_interval,
        able=lambda: bool(getattr(runtime, "is_started", False)),
    )
    return plane


# Must cover every SYSTEM_PLANES.plane_id — attach_all asserts completeness.
_ATTACHERS: dict[str, PlaneAttacher] = {
    "wait": _attach_wait,
    "session": _attach_session,
    "work": _attach_work,
}


def _require_attachers_match_roster() -> None:
    roster_ids = {p.plane_id for p in SYSTEM_PLANES}
    attacher_ids = set(_ATTACHERS)
    if roster_ids != attacher_ids:
        raise RuntimeError(
            "plane attachers out of sync with SYSTEM_PLANES roster: "
            f"roster={sorted(roster_ids)} attachers={sorted(attacher_ids)}"
        )


def attach_system_planes(
    runtime: Any,
    *,
    options: Mapping[str, Any] | None = None,
    ctx: Any = None,
) -> list[SystemPlaneSpec]:
    """
    Attach every plane in :data:`SYSTEM_PLANES` in roster order.

    Returns the specs that were attached. Raises if an attacher is missing.
    """
    _require_attachers_match_roster()
    opts = dict(options or {})
    attached: list[SystemPlaneSpec] = []
    for spec in SYSTEM_PLANES:
        attacher = _ATTACHERS[spec.plane_id]
        plane = attacher(runtime, opts, ctx)
        set_attached_plane(runtime, spec, plane)
        attached.append(spec)
    return attached


def detach_system_planes(runtime: Any) -> None:
    """Detach roster planes in **reverse** order; clear private fields."""
    for spec in reversed(SYSTEM_PLANES):
        plane = get_attached_plane(runtime, spec.attr)
        if plane is None:
            set_attached_plane(runtime, spec, None)
            continue
        detach = getattr(plane, "detach", None)
        if callable(detach):
            try:
                detach()
            except Exception:
                pass
        set_attached_plane(runtime, spec, None)


def log_roster_attach_result(runtime: Any, ctx: Any) -> None:
    """SystemLog summary after attach (schedule observation)."""
    from palm.system.log import get_system_log

    slog = get_system_log()
    missing = missing_roster_planes(runtime)
    runtime_name = getattr(ctx, "runtime", None)
    if missing:
        slog.system(
            "plane.roster.incomplete",
            f"roster planes missing after attach: {','.join(missing)}",
            schedule="system",
            runtime=runtime_name,
            missing=list(missing),
        )
    else:
        slog.info(
            "plane.roster.attached",
            "system planes attached per roster",
            schedule="system",
            runtime=runtime_name,
            planes=[p.plane_id for p in SYSTEM_PLANES],
        )


__all__ = [
    "PlaneAttacher",
    "attach_system_planes",
    "detach_system_planes",
    "get_attached_plane",
    "log_roster_attach_result",
    "set_attached_plane",
]
