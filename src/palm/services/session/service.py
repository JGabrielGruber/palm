"""Product SessionService — surface door for system session + related context.

Surfaces and other product services use this instead of reinventing
``runtime.session_plane`` access. The **plane remains law** (bind, attach,
ownership, active focus, watches). This service shapes that law for product
use and adds helpers surfaces need to drive **other** services correctly
(continue target, submit metadata, journey view, event filter).

**0.58.14:** :class:`BoundSurface` is the session-owned surface context handle
(session_id + instance focus + kind/origin + session metadata). Prefer
session-context metadata for walk/surface facts; job metadata stays run facts.

Does **not** resume jobs. Continue remains the wait plane via execution/assist.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from palm.common.services.base import BaseService
from palm.services.session.bound_surface import (
    SESSION_CONTEXT_KEYS,
    BoundSurface,
    derive_session_kind,
    derive_session_origin,
)
from palm.system.planes.session import (
    HOST_SESSION_ID,
    HOST_SESSION_ORIGIN,
    WORK_DRAIN_ORIGIN,
    SessionAttributionError,
    looks_like_system_session_id,
    new_session_id,
    service_session_id,
)

if TYPE_CHECKING:
    from palm.system.runtime.base import BaseRuntime
    from palm.services.system.service import SystemService
    from palm.system.planes.session import SessionPlaneService, SessionRecord, SessionBind


@dataclass(frozen=True)
class ContinueTarget:
    """Resolved pair for continue under a system session.

    * ``session_id`` — system subject (``sess-…``) when known
    * ``instance_id`` — product continue handle (job-path instance)
    """

    session_id: str | None
    instance_id: str | None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.session_id:
            out["session_id"] = self.session_id
        if self.instance_id:
            out["instance_id"] = self.instance_id
        return out


class SessionService(BaseService):
    """Product API for the session plane and surface-oriented session helpers.

    Construction is host-wired (``HostServiceRegistry``). Surfaces call
    ``host.session`` / ``ctx.session`` rather than the plane directly.
    """

    def __init__(
        self,
        *,
        commands: Any,
        queries: Any,
        schemas: Any,
        system: SystemService,
        runtime: BaseRuntime | None = None,
        runtime_resolver: Callable[[str | None], BaseRuntime] | None = None,
        strict_attribution: bool = True,
    ) -> None:
        super().__init__(commands=commands, queries=queries, schemas=schemas)
        self._system = system
        self._runtime = runtime
        self._runtime_resolver = runtime_resolver
        # 0.58.15: when plane ready, continue/start must be attributed.
        # Set False only for a short compat window (tests / migration).
        self.strict_attribution = bool(strict_attribution)

    # ── runtime / plane ────────────────────────────────────────────────────

    def resolve_runtime(self, runtime_name: str | None = None) -> BaseRuntime:
        if self._runtime_resolver is not None:
            return self._runtime_resolver(runtime_name)
        if self._runtime is not None:
            return self._runtime
        raise RuntimeError("SessionService requires a runtime or runtime_resolver")

    @property
    def system(self) -> SystemService:
        return self._system

    def plane(self) -> SessionPlaneService:
        """System session plane on the resolved runtime.

        Raises ``RuntimeError`` when the plane is not attached (runtime not ready).
        """
        runtime = self.resolve_runtime()
        plane = getattr(runtime, "session_plane", None)
        if plane is None:
            raise RuntimeError(
                "SessionService has no session plane; primary runtime not ready"
            )
        return plane

    def plane_or_none(self) -> SessionPlaneService | None:
        try:
            return self.plane()
        except Exception:
            return None

    # ── bind / lifecycle (plane verbs, product door) ───────────────────────

    def bind(
        self,
        session_id: str | None = None,
        *,
        create: bool = True,
        metadata: dict[str, Any] | None = None,
        surface: str | None = None,
    ) -> SessionBind:
        """Bind law: resolve or create a system session for a surface entry."""
        return self.plane().bind(
            session_id,
            create=create,
            metadata=metadata,
            surface=surface,
        )

    # ── BoundSurface + session context metadata (0.58.14) ──────────────────

    def bind_surface(
        self,
        session_id: str | None = None,
        *,
        create: bool = True,
        metadata: dict[str, Any] | None = None,
        surface: str | None = None,
        instance_id: str | None = None,
        origin: str | None = None,
        resolve_instance: bool = True,
    ) -> BoundSurface:
        """Bind and return a :class:`BoundSurface` (session owns surface context).

        Surfaces should hold this handle rather than inventing dual session
        slots. Session-context facts go in *metadata* (merged onto the plane
        record). *instance_id* is continue focus under the bound session.
        """
        meta = dict(metadata or {})
        if origin:
            meta.setdefault("origin", str(origin).strip())
        sid_hint = (session_id or "").strip() or None
        # Outside subjects get kind=outside unless already service-shaped.
        if not (sid_hint and str(sid_hint).startswith("sess-svc-")):
            meta.setdefault("kind", "outside")
        bind = self.bind(
            sid_hint,
            create=create,
            metadata=meta or None,
            surface=surface,
        )
        return self.surface_from_session(
            bind.session_id,
            instance_id=instance_id,
            resolve_instance=resolve_instance,
        )

    def surface_from_session(
        self,
        session_id: str,
        *,
        instance_id: str | None = None,
        resolve_instance: bool = True,
    ) -> BoundSurface:
        """Build :class:`BoundSurface` from a known system session id."""
        rec = self.require_open(session_id)
        iid = (instance_id or "").strip() or None
        if iid is None and resolve_instance:
            try:
                resolved = self.resolve_continue_instance(rec.session_id)
                iid = str(resolved) if resolved else None
            except Exception:
                iid = rec.active_instance_id
        return BoundSurface.from_record(rec, instance_id=iid)

    def surface_from_bind(
        self,
        bind: SessionBind,
        *,
        instance_id: str | None = None,
        resolve_instance: bool = True,
    ) -> BoundSurface:
        """Build :class:`BoundSurface` from a :class:`SessionBind` proof."""
        return self.surface_from_session(
            bind.session_id,
            instance_id=instance_id
            if instance_id is not None
            else bind.active_instance_id,
            resolve_instance=resolve_instance and instance_id is None,
        )

    def surface_from_params(
        self,
        params: Mapping[str, Any] | None,
        *,
        create: bool = False,
        surface: str | None = None,
        resolve_instance: bool = True,
    ) -> BoundSurface | None:
        """Extract or bind a BoundSurface from product params.

        * System-shaped ``session_id`` present → :meth:`surface_from_session`.
        * Missing + ``create=True`` → :meth:`bind_surface`.
        * Otherwise ``None`` (caller may use legacy bare-instance residual).
        """
        params = dict(params or {})
        raw_sid = params.get("session_id")
        raw_iid = params.get("instance_id")
        iid = str(raw_iid).strip() if raw_iid is not None and str(raw_iid).strip() else None
        if looks_like_system_session_id(raw_sid):
            return self.surface_from_session(
                str(raw_sid).strip(),
                instance_id=iid,
                resolve_instance=resolve_instance and iid is None,
            )
        # Misplaced system id in instance_id slot (legacy rewrite residual).
        if looks_like_system_session_id(raw_iid) and not looks_like_system_session_id(
            raw_sid
        ):
            return self.surface_from_session(
                str(raw_iid).strip(),
                resolve_instance=resolve_instance,
            )
        if create:
            origin = params.get("origin") or params.get("session_origin")
            return self.bind_surface(
                surface=surface or params.get("surface"),
                origin=str(origin).strip() if origin else None,
                instance_id=iid,
                resolve_instance=resolve_instance and iid is None,
            )
        return None

    def surface_from_dict(self, data: Mapping[str, Any]) -> BoundSurface:
        """Rebuild BoundSurface from :meth:`BoundSurface.to_dict` payload."""
        # Prefer live plane record so metadata is current.
        sid = data.get("session_id")
        if looks_like_system_session_id(sid):
            try:
                return self.surface_from_session(
                    str(sid),
                    instance_id=data.get("instance_id"),
                    resolve_instance=data.get("instance_id") is None,
                )
            except Exception:
                pass
        return BoundSurface.from_dict(data)

    def get_metadata(self, session_id: str) -> dict[str, Any]:
        """Session-context metadata (walk / surface / attribution)."""
        return self.plane().get_metadata(session_id)

    def merge_metadata(
        self,
        session_id: str,
        metadata: dict[str, Any] | None,
    ) -> BoundSurface:
        """Merge session-context facts onto the plane record; return BoundSurface.

        Prefer this over stuffing walk facts into job metadata (ADR-027 D14).
        """
        self.plane().merge_metadata(session_id, metadata)
        return self.surface_from_session(session_id)

    def replace_metadata(
        self,
        session_id: str,
        metadata: dict[str, Any] | None,
    ) -> BoundSurface:
        """Replace session-context metadata entirely; return BoundSurface."""
        self.plane().replace_metadata(session_id, metadata)
        return self.surface_from_session(session_id)

    def require_open(self, session_id: str) -> SessionRecord:
        return self.plane().require_open(session_id)

    def get(self, session_id: str) -> SessionRecord | None:
        plane = self.plane_or_none()
        if plane is None:
            return None
        return plane.get(session_id)

    def close(self, session_id: str) -> SessionRecord:
        return self.plane().close(session_id)

    def list_sessions(
        self,
        *,
        status: Any = None,
        include_closed: bool = True,
    ) -> list[SessionRecord]:
        return self.plane().list_sessions(
            status=status, include_closed=include_closed
        )

    # ── attach / focus ─────────────────────────────────────────────────────

    def attach_instance(self, session_id: str, instance_id: str) -> SessionRecord:
        return self.plane().attach_instance(session_id, instance_id)

    def detach_instance(self, session_id: str, instance_id: str) -> SessionRecord:
        return self.plane().detach_instance(session_id, instance_id)

    def set_active_instance(self, session_id: str, instance_id: str) -> SessionRecord:
        return self.plane().set_active_instance(session_id, instance_id)

    def clear_active_instance(self, session_id: str) -> SessionRecord:
        return self.plane().clear_active_instance(session_id)

    def list_instances(self, session_id: str) -> list[str]:
        return self.plane().list_instances(session_id)

    def active_instance(self, session_id: str) -> str | None:
        """Plane continue focus id, or None."""
        return self.plane().active_instance(session_id)

    def session_for_instance(self, instance_id: str) -> SessionRecord | None:
        plane = self.plane_or_none()
        if plane is None:
            return None
        return plane.session_for_instance(instance_id)

    def owner_session_id(self, instance_id: str) -> str | None:
        """System session id that owns *instance_id*, if any."""
        rec = self.session_for_instance(instance_id)
        return rec.session_id if rec is not None else None

    # ── ownership / continue resolve ───────────────────────────────────────

    def owns_instance(self, session_id: str, instance_id: str) -> bool:
        plane = self.plane_or_none()
        if plane is None:
            return False
        return bool(plane.owns_instance(session_id, instance_id))

    def require_owned_instance(
        self, session_id: str, instance_id: str
    ) -> SessionRecord:
        """Owner gate (SI-015): bound session must own continue instance."""
        return self.plane().require_owned_instance(session_id, instance_id)

    def resolve_continue_instance(self, session_id: str) -> str | None:
        """Pick continue instance: active → waiting → last. Does not resume."""
        return self.plane().resolve_continue_instance(session_id)

    def resolve_instance_id(self, session_or_instance: str) -> str:
        """Map system session id → continue instance; pass instance ids through.

        Product edges use this so they do not reimplement plane resolve.
        """
        text = str(session_or_instance or "").strip()
        if not text:
            return text
        if not looks_like_system_session_id(text):
            return text
        plane = self.plane_or_none()
        if plane is None:
            return text
        try:
            inst = plane.resolve_continue_instance(text)
            return str(inst) if inst else text
        except Exception:
            return text

    def continue_target(
        self,
        *,
        session_id: str | None = None,
        instance_id: str | None = None,
        gate: bool = True,
    ) -> ContinueTarget:
        """Resolve the (system session, instance) pair for continue.

        * System-shaped ``session_id`` + missing instance → resolve focus.
        * System-shaped value only in ``instance_id`` → treat as session and resolve.
        * When ``gate`` and both known → ownership / attribution (0.58.11–15).
        * Bare instance without session: under strict attribution, resolve owner
          from plane or raise :class:`SessionAttributionError`.
        """
        sid = (session_id or "").strip() or None
        iid = (instance_id or "").strip() or None

        if looks_like_system_session_id(iid) and not looks_like_system_session_id(sid):
            sid = iid
            iid = None

        if looks_like_system_session_id(sid):
            if not iid or looks_like_system_session_id(iid):
                resolved = self.resolve_continue_instance(sid)
                iid = str(resolved) if resolved else None
            if gate and iid:
                self.require_owned_instance(sid, iid)
            return ContinueTarget(session_id=sid, instance_id=iid)

        # No system session in args — attribute via plane or refuse (0.58.15).
        if iid and looks_like_system_session_id(iid):
            # Misplaced sess- only in instance slot without session_id handled above.
            resolved = self.resolve_continue_instance(str(iid))
            return ContinueTarget(
                session_id=str(iid),
                instance_id=str(resolved) if resolved else None,
            )
        if gate and iid and self.plane_or_none() is not None:
            params: dict[str, Any] = {"instance_id": iid}
            bound = self.gate_bound_session_owns(
                iid, params, allow_unknown=False
            )
            return ContinueTarget(
                session_id=bound or params.get("session_id"),
                instance_id=iid,
            )
        return ContinueTarget(session_id=sid, instance_id=iid)

    def gate_bound_session_owns(
        self,
        instance_id: str,
        params: dict[str, Any] | None,
        *,
        strict: bool | None = None,
        allow_unknown: bool = True,
    ) -> str | None:
        """Continue attribution gate (SI-015 + 0.58.15 strict policy).

        When the session plane is ready and *strict* (default
        :attr:`strict_attribution`):

        * system ``session_id`` in *params* → must own *instance_id*
        * missing system session → resolve owner from plane reverse index;
          inject ``session_id`` into *params* when found
        * no owner + instance **known** → :class:`SessionAttributionError`
        * no owner + instance **unknown** + *allow_unknown* → no-op
          (product inspect/input may 404)
        * no owner + not *allow_unknown* → :class:`SessionAttributionError`
          (operator rewrite / explicit continue_target)

        When *strict* is False: legacy SI-015 only (gate only if system
        ``session_id`` is present). Plane missing → no-op.

        Returns the bound system session id, or ``None`` when not enforced.
        """
        params_mut = params if params is not None else {}
        plane = self.plane_or_none()
        if plane is None:
            return None
        use_strict = self.strict_attribution if strict is None else bool(strict)
        raw = params_mut.get("session_id")
        sid = str(raw).strip() if looks_like_system_session_id(raw) else None
        if not use_strict and sid is None:
            return None
        iid = str(instance_id).strip()
        try:
            bound = plane.require_continue_attribution(iid, sid, strict=use_strict)
        except SessionAttributionError:
            # Unknown product instance → optionally defer to not-found (404).
            # Known job without owner session → always refuse.
            if (
                use_strict
                and sid is None
                and allow_unknown
                and not self._instance_known(iid)
            ):
                return None
            raise
        if bound and not looks_like_system_session_id(params_mut.get("session_id")):
            params_mut["session_id"] = bound
        return bound

    def _instance_known(self, instance_id: str) -> bool:
        """True when system inspect can see the product instance."""
        iid = str(instance_id or "").strip()
        if not iid:
            return False
        try:
            view = self._system.inspect_instance(iid)
            return view is not None
        except Exception:
            return False

    # ── submit / metadata helpers (for execution and other services) ───────

    def ensure_system_session_id(
        self,
        *,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        surface: str = "product",
        create: bool = True,
        origin: str | None = None,
    ) -> str | None:
        """Return a system session id for job metadata / start paths.

        Prefers an existing system-shaped id on *session_id* or *metadata*.
        When *origin* is set, uses a stable **service** session (0.58.13)
        instead of minting a new outside subject. Otherwise binds a new
        outside session when *create* is true.
        """
        meta = dict(metadata or {})
        for raw in (session_id, meta.get("session_id")):
            if looks_like_system_session_id(raw):
                return str(raw).strip()
        if not create:
            return None
        if origin:
            return self.ensure_service_session(origin)
        plane = self.plane_or_none()
        if plane is None:
            return None
        try:
            bind = plane.bind(
                surface=surface,
                metadata={"via": "session_service.ensure"},
            )
            return str(bind.session_id)
        except Exception:
            return None

    def ensure_service_session(
        self,
        origin: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> str | None:
        """Stable system session for automated / internal *origin* (0.58.13).

        Surfaces still :meth:`bind` for outside subjects. Work drain, schedules,
        and host housekeeping use service sessions so every job-path start has
        an owner without one random session per intent.
        """
        plane = self.plane_or_none()
        if plane is None:
            return None
        try:
            rec = plane.ensure_service_session(origin, metadata=metadata)
            return str(rec.session_id)
        except Exception:
            return None

    def ensure_host_session(self) -> str | None:
        """Well-known host service session (``sess-svc-host``)."""
        plane = self.plane_or_none()
        if plane is None:
            return None
        try:
            rec = plane.ensure_host_session()
            return str(rec.session_id)
        except Exception:
            return None

    def enrich_submit_body(
        self,
        body: dict[str, Any] | None,
        *,
        surface: str = "execution",
        origin: str | None = None,
    ) -> dict[str, Any]:
        """Ensure submit body metadata carries system ``session_id``.

        Edge law: ``session_id`` on body/meta is system subject only when
        system-shaped. Instance-shaped values are not promoted.

        * *origin* set → stable service session when no session present
          (work drain / schedules / internal).
        * No origin → outside bind (new ``sess-…``) for interactive surfaces.
        """
        out = dict(body or {})
        meta = dict(out.get("metadata") or {})
        # Intent payload may carry origin for automated start.
        origin_hint = (origin or meta.get("session_origin") or "").strip() or None
        if not origin_hint and surface in ("work-drain", "schedule", "inbound", "trigger"):
            origin_hint = surface
        candidates = (
            out.get("session_id")
            if looks_like_system_session_id(out.get("session_id"))
            else None,
            meta.get("session_id")
            if looks_like_system_session_id(meta.get("session_id"))
            else None,
        )
        sid = None
        for raw in candidates:
            if raw is not None and str(raw).strip():
                sid = str(raw).strip()
                break
        if sid is None:
            sid = self.ensure_system_session_id(
                surface=surface,
                create=True,
                origin=origin_hint,
            )
        if sid:
            meta["session_id"] = sid
            if origin_hint:
                meta.setdefault("session_origin", origin_hint)
            out["metadata"] = meta
        elif (
            self.strict_attribution
            and self.plane_or_none() is not None
        ):
            raise SessionAttributionError(
                "start requires system session when session plane is ready "
                "(0.58.15 strict attribution)"
            )
        return out

    def system_session_from_instance(self, instance_id: str) -> str | None:
        """Best-effort system session for an instance (meta reverse, then plane)."""
        iid = str(instance_id or "").strip()
        if not iid:
            return None
        owner = self.owner_session_id(iid)
        if owner:
            return owner
        # Instance repository meta may lag plane reverse index.
        try:
            view = self._system.inspect_instance(iid)
            if isinstance(view, dict):
                meta = view.get("metadata") if isinstance(view.get("metadata"), dict) else view
                raw = None
                if isinstance(meta, dict):
                    raw = meta.get("session_id")
                if looks_like_system_session_id(raw):
                    return str(raw).strip()
        except Exception:
            pass
        return None

    # ── journey / watches ──────────────────────────────────────────────────

    def inspect(self, session_id: str) -> dict[str, Any]:
        """Session journey view (instances + open waits). Inspect only."""
        return self.plane().inspect(session_id)

    def list_waiting(self, session_id: str) -> list[dict[str, Any]]:
        plane = self.plane()
        if hasattr(plane, "list_waiting"):
            return list(plane.list_waiting(session_id))
        data = plane.inspect(session_id)
        return list(data.get("waiting_on") or [])

    def surface_view(self, session_id: str) -> dict[str, Any]:
        """Enriched view for surfaces: journey + BoundSurface + continue refs.

        Surfaces use this to know which instance to drive and which other
        services (execution inspect, assist) to call — without each edge
        assembling plane + system inspect itself.

        ``kind`` stays ``session_surface_view`` (envelope). Subject kind lives
        under ``bound_surface.session_kind`` / ``session_kind``.
        """
        journey = self.inspect(session_id)
        bound = self.surface_from_session(session_id)
        continue_id = bound.instance_id or self.resolve_continue_instance(session_id)
        active = journey.get("active_instance_id")
        return {
            **journey,
            "kind": "session_surface_view",
            "continue_instance_id": continue_id,
            "active_instance_id": active,
            "session_kind": bound.kind,
            "origin": bound.origin,
            "bound_surface": bound.to_dict(),
            "refs": {
                "session_id": session_id,
                "instance_id": continue_id,
                "active_instance_id": active,
            },
        }

    def event_matches(
        self,
        session_id: str,
        *,
        event: Any = None,
        payload: dict[str, Any] | None = None,
        context: Any = None,
    ) -> bool:
        return bool(
            self.plane().event_matches(
                session_id, event=event, payload=payload, context=context
            )
        )

    def make_event_filter(self, session_id: str) -> Any:
        """Predicate ``(event) -> bool`` for WS / subscribe wrappers."""
        return self.plane().make_event_filter(session_id)

    def attributed_session_id(
        self,
        *,
        event: Any = None,
        payload: dict[str, Any] | None = None,
        context: Any = None,
    ) -> str | None:
        return self.plane().attributed_session_id(
            event=event, payload=payload, context=context
        )


__all__ = [
    "SESSION_CONTEXT_KEYS",
    "BoundSurface",
    "ContinueTarget",
    "HOST_SESSION_ID",
    "HOST_SESSION_ORIGIN",
    "SessionAttributionError",
    "SessionService",
    "WORK_DRAIN_ORIGIN",
    "derive_session_kind",
    "derive_session_origin",
    "looks_like_system_session_id",
    "new_session_id",
    "service_session_id",
]
