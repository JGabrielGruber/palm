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

    def resolve_continue_instance(self, session_id: str) -> str | None:
        """Pick an instance under the session for continue (0.58.8).

        Prefers an instance that currently has open waits; otherwise the
        last attached instance. Does **not** resume — only selects the
        product continue handle from the attach list (truth for multi-instance).
        """
        rec = self.require_open(session_id)
        if not rec.instance_ids:
            return None
        waiting = self.list_waiting(session_id)
        if waiting:
            for w in reversed(waiting):
                if not isinstance(w, dict):
                    continue
                iid = w.get("instance_id")
                if iid and str(iid) in rec.instance_ids:
                    return str(iid)
        return str(rec.instance_ids[-1])

    def attributed_session_id(
        self,
        *,
        event: Any = None,
        payload: dict[str, Any] | None = None,
        context: Any = None,
    ) -> str | None:
        """Best-effort system session id for an event (0.58.8 watches).

        Order: EventContext.session_id → payload system keys → payload
        session_id when system-shaped → reverse index on instance_id.
        """
        ctx = context
        if event is not None and ctx is None:
            ctx = getattr(event, "context", None)
        pay = payload
        if event is not None and pay is None:
            raw = getattr(event, "payload", None)
            pay = dict(raw) if isinstance(raw, dict) else {}
        pay = pay or {}

        if ctx is not None:
            if hasattr(ctx, "session_id") and ctx.session_id:
                return str(ctx.session_id).strip() or None
            if isinstance(ctx, dict) and ctx.get("session_id"):
                return str(ctx["session_id"]).strip() or None

        # 0.58.9: payload session_id is system subject when system-shaped;
        # instance-shaped → reverse index (legacy product payloads).
        raw_sid = pay.get("session_id")
        if raw_sid is not None and str(raw_sid).strip():
            text = str(raw_sid).strip()
            if text.startswith("sess-"):
                return text
            owner = self.session_for_instance(text)
            if owner is not None:
                return owner.session_id

        for key in ("instance_id", "instance"):
            raw = pay.get(key)
            if raw is not None and str(raw).strip():
                owner = self.session_for_instance(str(raw).strip())
                if owner is not None:
                    return owner.session_id

        if ctx is not None:
            iid = getattr(ctx, "instance_id", None) if not isinstance(ctx, dict) else ctx.get("instance_id")
            if iid:
                owner = self.session_for_instance(str(iid).strip())
                if owner is not None:
                    return owner.session_id
        return None

    def event_matches(
        self,
        session_id: str,
        *,
        event: Any = None,
        payload: dict[str, Any] | None = None,
        context: Any = None,
    ) -> bool:
        """True when the event belongs to this system session (fan-in filter)."""
        sid = (session_id or "").strip()
        if not sid:
            return False
        attributed = self.attributed_session_id(
            event=event, payload=payload, context=context
        )
        if attributed == sid:
            return True
        # Instance on attach list even without reverse hit on attribution
        pay = payload
        if event is not None and pay is None:
            raw = getattr(event, "payload", None)
            pay = dict(raw) if isinstance(raw, dict) else {}
        pay = pay or {}
        rec = self.get(sid)
        if rec is None:
            return False
        attached = set(rec.instance_ids)
        for key in ("instance_id", "instance", "session_id"):
            raw = pay.get(key)
            if raw is not None and str(raw).strip() in attached:
                return True
        if context is not None:
            iid = (
                getattr(context, "instance_id", None)
                if not isinstance(context, dict)
                else context.get("instance_id")
            )
            if iid and str(iid).strip() in attached:
                return True
        return False

    def make_event_filter(self, session_id: str) -> Any:
        """Return a predicate ``(event) -> bool`` for subscribe wrappers / WS."""

        def _filter(event: Any) -> bool:
            return self.event_matches(session_id, event=event)

        return _filter

    def inspect(self, session_id: str) -> dict[str, Any]:
        """Journey view for a session: instances + open waits (0.58.5).

        **Inspect only.** Does not resume, input, or cancel jobs. Continue
        remains the wait plane.
        """
        rec = self.require(session_id)
        instances: list[dict[str, Any]] = []
        waiting: list[dict[str, Any]] = []
        for iid in rec.instance_ids:
            row = self._instance_inspect_row(iid, session_id=rec.session_id)
            instances.append(row)
            for w in row.get("waiting_on") or []:
                if isinstance(w, dict):
                    waiting.append(
                        {
                            **w,
                            "instance_id": iid,
                            "job_id": row.get("job_id"),
                            "session_id": rec.session_id,
                        }
                    )
        return {
            "kind": "session_inspect",
            "session_id": rec.session_id,
            "status": rec.status.value,
            "metadata": dict(rec.metadata),
            "created_at": rec.created_at,
            "updated_at": rec.updated_at,
            "instance_ids": list(rec.instance_ids),
            "instances": instances,
            "waiting_on": waiting,
            "counts": {
                "instances": len(rec.instance_ids),
                "open_waits": len(waiting),
            },
            "note": "inspect only; continue via wait plane (not session resume)",
        }

    def list_waiting(self, session_id: str) -> list[dict[str, Any]]:
        """Open wait interests across all instances attached to the session."""
        return list(self.inspect(session_id).get("waiting_on") or [])

    def _instance_inspect_row(
        self, instance_id: str, *, session_id: str
    ) -> dict[str, Any]:
        row: dict[str, Any] = {
            "instance_id": instance_id,
            "session_id": session_id,
        }
        rt = self._runtime
        if rt is None:
            return row
        inst = None
        try:
            manager = getattr(rt, "instance_manager", None)
            if manager is not None:
                inst = manager.get(instance_id)
        except Exception:
            inst = None
        if inst is None:
            row["status"] = "unknown"
            return row
        row["status"] = getattr(inst, "status", None)
        row["job_id"] = getattr(inst, "job_id", None)
        row["flow_id"] = getattr(inst, "flow_id", None) or getattr(
            inst, "flow_name", None
        )
        row["pattern"] = getattr(inst, "pattern", None)
        resolved = None
        if hasattr(inst, "resolved_session_id"):
            try:
                resolved = inst.resolved_session_id()
            except Exception:
                resolved = getattr(inst, "session_id", None)
        else:
            resolved = getattr(inst, "session_id", None)
        if resolved:
            row["session_id"] = resolved
        job = self._resolve_job(rt, getattr(inst, "job_id", None))
        waits: list[dict[str, Any]] = []
        if job is not None:
            waits = self._waiting_on_for_job(rt, job)
        if not waits:
            # Fallback: interests on durable instance state (resume-shaped).
            waits = self._waiting_on_from_instance(inst)
        if waits:
            row["waiting_on"] = waits
            try:
                from palm.system.planes.wait.present import summarize_waiting_on

                summary = summarize_waiting_on(waits)
            except Exception:
                summary = None
            if summary:
                row["waiting_summary"] = summary
        return row

    def _waiting_on_from_instance(self, inst: Any) -> list[dict[str, Any]]:
        try:
            from palm.system.planes.wait.present import waiting_on_from_state
            from palm.common.persistence.state_snapshot import state_from_snapshot

            snap = getattr(inst, "state_snapshot", None)
            if not snap:
                return []
            state = state_from_snapshot(snap)
            return list(waiting_on_from_state(state) or [])
        except Exception:
            return []

    def _resolve_job(self, runtime: Any, job_id: str | None) -> Any | None:
        if not job_id:
            return None
        try:
            get_job = getattr(runtime, "get_job", None)
            if callable(get_job):
                return get_job(str(job_id))
        except Exception:
            pass
        orch = getattr(runtime, "orchestration", None)
        if orch is None:
            return None
        jobs = getattr(orch, "jobs", None)
        if isinstance(jobs, dict):
            return jobs.get(str(job_id))
        try:
            return orch.get_job(str(job_id))
        except Exception:
            return None

    def _waiting_on_for_job(self, runtime: Any, job: Any) -> list[dict[str, Any]]:
        wait_plane = getattr(runtime, "wait_plane", None)
        if wait_plane is not None and hasattr(wait_plane, "waiting_on_for_job"):
            try:
                return list(wait_plane.waiting_on_for_job(job) or [])
            except Exception:
                pass
        try:
            from palm.system.planes.wait.present import waiting_on_from_job

            return list(waiting_on_from_job(job) or [])
        except Exception:
            return []

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
                "resolve_continue_instance",
                "inspect",
                "list_waiting",
                "event_matches",
                "attributed_session_id",
                "make_event_filter",
            ],
            "store": "storage_engine",
            "storage_backend": backend,
            "multi_attach": True,
            "bind_law": True,
            "event_filter": True,
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
