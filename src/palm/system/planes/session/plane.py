"""SessionPlaneService — system **session** plane (0.58).

Outside subject on :class:`SessionStore` (:class:`~palm.core.storage.StorageEngine`).

* Lifecycle: open / get / close / list
* Multi-attach (0.58.2): attach/detach instances; reverse index
* **Bind law (0.58.3):** surfaces call :meth:`bind` / :meth:`require_open`
  before driving work — no silent instance-only subject

Does **not** resume jobs. Continue remains the wait plane.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.system.planes.session.store import SessionStore
from palm.system.planes.session.types import (
    SessionBind,
    SessionRecord,
    SessionStatus,
    new_session_id,
)

if TYPE_CHECKING:
    from palm.core.storage import StorageEngine


class SessionPlaneError(RuntimeError):
    """Session plane operation failed."""


class SessionNotFoundError(SessionPlaneError):
    """No session for the given id."""


class SessionClosedError(SessionPlaneError):
    """Session is closed and cannot accept mutations."""


class InstanceAlreadyAttachedError(SessionPlaneError):
    """Instance is already attached to a different session."""


class SessionPlaneService:
    """Session plane: lifecycle + multi-attach + surface bind law.

    Lifecycle:
    * construct with :class:`SessionStore` (or storage engine)
    * :meth:`attach` / :meth:`detach` — plane↔runtime link (not instances)
    * :meth:`open` / :meth:`get` / :meth:`close` / :meth:`list_sessions`
    * :meth:`attach_instance` / :meth:`detach_instance` — multi-attach (0.58.2)
    * :meth:`session_for_instance` — reverse lookup
    * :meth:`bind` / :meth:`require_open` — surface entry law (0.58.3)
    """

    def __init__(
        self,
        store: SessionStore | None = None,
        *,
        storage: StorageEngine | None = None,
    ) -> None:
        if store is not None:
            self._store = store
        elif storage is not None:
            self._store = SessionStore(storage)
        else:
            raise TypeError("SessionPlaneService requires store= or storage=")
        self._runtime: Any | None = None

    @property
    def store(self) -> SessionStore:
        return self._store

    @property
    def is_attached(self) -> bool:
        return self._runtime is not None

    def attach(self, runtime: Any) -> None:
        """Bind plane to a system instance (BaseRuntime)."""
        self._runtime = runtime

    def detach(self) -> None:
        """Unbind from runtime. Session records stay in StorageEngine."""
        self._runtime = None

    def open(
        self,
        *,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> SessionRecord:
        """Create an OPEN session. Id is generated when omitted."""
        sid = (session_id or "").strip() or new_session_id()
        existing = self._store.get(sid)
        if existing is not None:
            if existing.status == SessionStatus.CLOSED:
                raise SessionPlaneError(f"session {sid!r} exists and is closed")
            return existing
        record = SessionRecord(
            session_id=sid,
            status=SessionStatus.OPEN,
            metadata=dict(metadata or {}),
        )
        return self._store.put(record)

    def bind(
        self,
        session_id: str | None = None,
        *,
        create: bool = True,
        metadata: dict[str, Any] | None = None,
        surface: str | None = None,
    ) -> SessionBind:
        """Surface entry: resolve or create a system session (bind law).

        * No ``session_id`` + ``create=True`` → open a new session.
        * Known open/active id → rebind (touch surface metadata).
        * Unknown id + ``create=True`` → open with that id.
        * Unknown id + ``create=False`` → :class:`SessionNotFoundError`.
        * Closed id → :class:`SessionClosedError` (never silently reopen).

        Returns :class:`SessionBind` proof. Does **not** attach instances
        and does **not** resume jobs.
        """
        meta = dict(metadata or {})
        surf = (surface or "").strip() or None
        if surf:
            meta.setdefault("surface", surf)
            meta["last_surface"] = surf

        sid = (session_id or "").strip() or None
        if sid is None:
            if not create:
                raise SessionPlaneError(
                    "bind requires session_id when create=False (no outside subject)"
                )
            rec = self.open(metadata=meta or None)
            return SessionBind.from_record(rec, created=True, surface=surf)

        existing = self._store.get(sid)
        if existing is None:
            if not create:
                raise SessionNotFoundError(f"session not found: {sid!r}")
            rec = self.open(session_id=sid, metadata=meta or None)
            return SessionBind.from_record(rec, created=True, surface=surf)

        if existing.status == SessionStatus.CLOSED:
            raise SessionClosedError(
                f"session {sid!r} is closed; bind refused (create a new session)"
            )

        touched = False
        if meta:
            for key, value in meta.items():
                if existing.metadata.get(key) != value:
                    existing.metadata[key] = value
                    touched = True
        if touched:
            existing.touch()
            existing = self._store.put(existing)
        return SessionBind.from_record(existing, created=False, surface=surf)

    def require_open(self, session_id: str) -> SessionRecord:
        """Require an existing non-closed session (continue / inspect paths)."""
        rec = self.require(session_id)
        if rec.status == SessionStatus.CLOSED:
            raise SessionClosedError(f"session {session_id!r} is closed")
        return rec

    def get(self, session_id: str) -> SessionRecord | None:
        return self._store.get(session_id)

    def require(self, session_id: str) -> SessionRecord:
        rec = self._store.get(session_id)
        if rec is None:
            raise SessionNotFoundError(f"session not found: {session_id!r}")
        return rec

    def close(self, session_id: str) -> SessionRecord:
        """Mark session CLOSED. Idempotent if already closed.

        Does not detach instances from the record (history stays).
        Reverse index remains until instances are detached or session deleted.
        """
        rec = self.require(session_id)
        if rec.status == SessionStatus.CLOSED:
            return rec
        rec.status = SessionStatus.CLOSED
        rec.touch()
        return self._store.put(rec)

    def list_sessions(
        self,
        *,
        status: SessionStatus | None = None,
        include_closed: bool = True,
    ) -> list[SessionRecord]:
        return self._store.list(status=status, include_closed=include_closed)

    def attach_instance(self, session_id: str, instance_id: str) -> SessionRecord:
        """Attach an instance to a session (multi-attach; 0..N).

        Idempotent if already on this session. Refuses if another session
        already owns the instance. Promotes OPEN → ACTIVE on first attach.
        """
        iid = (instance_id or "").strip()
        if not iid:
            raise SessionPlaneError("instance_id is required")
        rec = self.require(session_id)
        if rec.status == SessionStatus.CLOSED:
            raise SessionClosedError(
                f"session {session_id!r} is closed; cannot attach instances"
            )
        owner = self._store.session_id_for_instance(iid)
        if owner is not None and owner != rec.session_id:
            raise InstanceAlreadyAttachedError(
                f"instance {iid!r} already attached to session {owner!r}"
            )
        if iid in rec.instance_ids:
            return rec
        rec.instance_ids.append(iid)
        if rec.status == SessionStatus.OPEN:
            rec.status = SessionStatus.ACTIVE
        rec.touch()
        return self._store.put(rec)

    def detach_instance(self, session_id: str, instance_id: str) -> SessionRecord:
        """Remove an instance from a session. Idempotent if not attached.

        Closed sessions may still detach (cleanup). Does not reopen closed.
        """
        iid = (instance_id or "").strip()
        if not iid:
            raise SessionPlaneError("instance_id is required")
        rec = self.require(session_id)
        if iid not in rec.instance_ids:
            return rec
        rec.instance_ids = [x for x in rec.instance_ids if x != iid]
        rec.touch()
        return self._store.put(rec)

    def list_instances(self, session_id: str) -> list[str]:
        """Return attached instance ids for a session (ordered)."""
        return list(self.require(session_id).instance_ids)

    def session_for_instance(self, instance_id: str) -> SessionRecord | None:
        """Reverse lookup: session that owns this instance, if any."""
        return self._store.get_by_instance(instance_id)

    def doctor_snapshot(self) -> dict[str, Any]:
        """Small inspect payload for doctor / system diagnostics."""
        open_n = len(self._store.list(status=SessionStatus.OPEN, include_closed=False))
        active_n = len(
            self._store.list(status=SessionStatus.ACTIVE, include_closed=False)
        )
        closed_n = len(self._store.list(status=SessionStatus.CLOSED))
        attached_instances = 0
        for rec in self._store.list(include_closed=True):
            attached_instances += len(rec.instance_ids)
        backend = getattr(self._store.storage, "backend_name", None)
        return {
            "plane": "session",
            "session_plane_attached": self.is_attached,
            "verbs": [
                "bind",
                "require_open",
                "open",
                "get",
                "close",
                "list",
                "attach_instance",
                "detach_instance",
                "session_for_instance",
            ],
            "store": "storage_engine",
            "storage_backend": backend,
            "multi_attach": True,
            "bind_law": True,
            "counts": {
                "open": open_n,
                "active": active_n,
                "closed": closed_n,
                "total": len(self._store),
                "attached_instances": attached_instances,
            },
        }


def bind_session_plane_to_runtime(runtime: Any) -> SessionPlaneService:
    """Attach a new (or existing) session plane on ``runtime`` and return it."""
    existing = getattr(runtime, "session_plane", None)
    if isinstance(existing, SessionPlaneService):
        existing.attach(runtime)
        return existing
    storage = getattr(runtime, "storage", None)
    if storage is None:
        raise SessionPlaneError("runtime has no storage for session plane")
    plane = SessionPlaneService(storage=storage)
    plane.attach(runtime)
    if hasattr(runtime, "_session_plane"):
        runtime._session_plane = plane
    return plane


__all__ = [
    "InstanceAlreadyAttachedError",
    "SessionClosedError",
    "SessionNotFoundError",
    "SessionPlaneError",
    "SessionPlaneService",
    "bind_session_plane_to_runtime",
    "require_session_plane",
]


def require_session_plane(runtime: Any) -> SessionPlaneService:
    """Return the runtime's session plane or raise (bind law helper)."""
    plane = getattr(runtime, "session_plane", None)
    if isinstance(plane, SessionPlaneService):
        return plane
    raise SessionPlaneError(
        "runtime has no session plane; start the system instance first"
    )
