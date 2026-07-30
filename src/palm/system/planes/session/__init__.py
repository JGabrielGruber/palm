"""Session plane — outside subject lifecycle (0.58 Session plane).

**Public door (0.58.1)** — system seat only:

* :class:`SessionPlaneService` / :func:`bind_session_plane_to_runtime`
* :class:`SessionRecord` / :class:`SessionStatus`

Store uses :class:`~palm.core.storage.StorageEngine` (like work plane).
Multi-attach and surface bind: later 0.58 slices.
Continue/resume remains :mod:`palm.system.planes.wait`.
"""

from palm.system.planes.session.plane import (
    SessionClosedError,
    SessionNotFoundError,
    SessionPlaneError,
    SessionPlaneService,
    bind_session_plane_to_runtime,
)
from palm.system.planes.session.store import SessionStore
from palm.system.planes.session.types import SessionRecord, SessionStatus, new_session_id

__all__ = [
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
