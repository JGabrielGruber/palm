"""Session plane — outside subject lifecycle (0.58 Session plane).

**Public door (0.58.3)** — seat + multi-attach + **bind law**:

* :class:`SessionPlaneService` / :func:`bind_session_plane_to_runtime`
* :class:`SessionRecord` / :class:`SessionStatus` / :class:`SessionBind`
* :meth:`SessionPlaneService.bind` / :meth:`~SessionPlaneService.require_open`
* :meth:`SessionPlaneService.attach_instance` / reverse lookup
* :func:`require_session_plane`

Store uses :class:`~palm.core.storage.StorageEngine` (like work plane).
Surfaces (host, CLI, …) **bind** before driving work.
Continue/resume remains :mod:`palm.system.planes.wait`.
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
    "new_session_id",
    "require_session_plane",
]
