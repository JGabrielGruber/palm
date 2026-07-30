"""Session plane — outside subject lifecycle (0.58 Session plane).

**Public door (0.58.2)** — system seat + multi-attach:

* :class:`SessionPlaneService` / :func:`bind_session_plane_to_runtime`
* :class:`SessionRecord` / :class:`SessionStatus`
* :meth:`SessionPlaneService.attach_instance` / :meth:`~SessionPlaneService.detach_instance`
* Reverse lookup :meth:`SessionPlaneService.session_for_instance`

Store uses :class:`~palm.core.storage.StorageEngine` (like work plane).
Surface bind: later 0.58 slices.
Continue/resume remains :mod:`palm.system.planes.wait`.
"""

from palm.system.planes.session.plane import (
    InstanceAlreadyAttachedError,
    SessionClosedError,
    SessionNotFoundError,
    SessionPlaneError,
    SessionPlaneService,
    bind_session_plane_to_runtime,
)
from palm.system.planes.session.store import SessionStore
from palm.system.planes.session.types import SessionRecord, SessionStatus, new_session_id

__all__ = [
    "InstanceAlreadyAttachedError",
    "SessionClosedError",
    "SessionNotFoundError",
    "SessionPlaneError",
    "SessionPlaneService",
    "SessionRecord",
    "SessionStatus",
    "SessionStore",
    "bind_session_plane_to_runtime",
    "new_session_id",
]
