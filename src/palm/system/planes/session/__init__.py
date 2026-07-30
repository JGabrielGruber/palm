"""Session plane — outside subject lifecycle (0.58 Session plane).

**Public door (0.58.3)** — seat + multi-attach + **bind law**:

* :class:`SessionPlaneService` / :func:`bind_session_plane_to_runtime`
* :class:`SessionRecord` / :class:`SessionStatus` / :class:`SessionBind`
* :meth:`SessionPlaneService.bind` / :meth:`~SessionPlaneService.require_open`
* :meth:`SessionPlaneService.attach_instance` / reverse lookup
* :meth:`SessionPlaneService.event_matches` / :meth:`~SessionPlaneService.make_event_filter` (0.58.8)
* :meth:`SessionPlaneService.resolve_continue_instance` (active → waiting → last)
* :attr:`SessionRecord.active_instance_id` / :meth:`SessionPlaneService.set_active_instance` (0.58.10)
* :func:`require_session_plane`

**Ownership:** one instance → one session (exclusive).  
**Active:** focus inside that attach list only — not a foreign-session pass.  
Docs: ``docs/VISION-0.58.md`` §4.1 · ADR-027 D9–D11 · residual SI-015.

Store uses :class:`~palm.core.storage.StorageEngine` (like work plane).
Surfaces (host, CLI, …) **bind** before driving work.
Continue/resume remains :mod:`palm.system.planes.wait`.
Watches filter events by system session; they do not resume.
"""

from palm.system.planes.session.plane import (
    InstanceAlreadyAttachedError,
    SessionClosedError,
    SessionNotFoundError,
    SessionPlaneError,
    SessionPlaneService,
    bind_session_plane_to_runtime,
    require_session_plane,
)
from palm.system.planes.session.store import SessionStore
from palm.system.planes.session.types import (
    SessionBind,
    SessionRecord,
    SessionStatus,
    looks_like_system_session_id,
    new_session_id,
)

__all__ = [
    "InstanceAlreadyAttachedError",
    "SessionBind",
    "SessionClosedError",
    "SessionNotFoundError",
    "SessionPlaneError",
    "SessionPlaneService",
    "SessionRecord",
    "SessionStatus",
    "SessionStore",
    "bind_session_plane_to_runtime",
    "looks_like_system_session_id",
    "new_session_id",
    "require_session_plane",
]
