"""Session plane types — system outside subject (0.58).

Session ≠ instance ≠ job. One session may attach many instances
(:meth:`~palm.system.planes.session.plane.SessionPlaneService.attach_instance`).

Surfaces **bind** a session before they drive work
(:meth:`~palm.system.planes.session.plane.SessionPlaneService.bind`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class SessionStatus(str, Enum):
    """Lifecycle of a system session."""

    OPEN = "open"
    ACTIVE = "active"
    CLOSED = "closed"


def new_session_id() -> str:
    """Return a new stable session id (not an instance id)."""
    return f"sess-{uuid4().hex}"


def looks_like_system_session_id(value: Any) -> bool:
    """True when *value* is system-session shaped (``sess-…``), not a bare instance id."""
    if value is None:
        return False
    text = str(value).strip()
    return text.startswith("sess-")


# Well-known **service** origins (0.58.13). Not outside subjects.
# Automated start (work drain, schedules) uses stable service sessions so
# every instance has an owner without minting a random session per job.
HOST_SESSION_ORIGIN = "host"
HOST_SESSION_ID = "sess-svc-host"
WORK_DRAIN_ORIGIN = "work-drain"


def service_session_id(origin: str) -> str:
    """Deterministic system session id for a service *origin*.

    Outside surfaces still use :func:`new_session_id` / bind without id.
    Service origins (work-drain, host, schedules, …) get stable
    ``sess-svc-…`` ids so cancel/watch can group automated work.
    """
    raw = str(origin or "").strip().lower()
    if not raw:
        raise ValueError("service session origin must be non-empty")
    # Keep alnum and a few separators; collapse the rest to hyphen.
    parts: list[str] = []
    prev_hyphen = False
    for ch in raw:
        if ch.isalnum():
            parts.append(ch)
            prev_hyphen = False
        elif ch in ("-", "_", ".", ":", "/"):
            if not prev_hyphen:
                parts.append("-")
                prev_hyphen = True
        else:
            if not prev_hyphen:
                parts.append("-")
                prev_hyphen = True
    slug = "".join(parts).strip("-")
    if not slug:
        raise ValueError(f"service session origin has no usable slug: {origin!r}")
    # Cap length so storage keys stay reasonable.
    if len(slug) > 80:
        slug = slug[:80].rstrip("-")
    if slug == HOST_SESSION_ORIGIN:
        return HOST_SESSION_ID
    return f"sess-svc-{slug}"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class SessionRecord:
    """Durable-shaped session subject held by the session plane.

    ``instance_ids`` is the ordered attach list (0..N). Empty at open
    until :meth:`~SessionPlaneService.attach_instance` binds work under
    this session.

    ``active_instance_id`` (0.58.10) is the plane-owned **continue focus**
    among attached instances. Not equal to ``session_id``. None when no
    instance is attached (or after detach of the last).

    Focus is not ownership: only ids on ``instance_ids`` may be active.
    Another session cannot point active at this session's instances.
    See VISION-0.58 §4.1 and ADR-027 D9–D10.
    """

    session_id: str
    status: SessionStatus = SessionStatus.OPEN
    instance_ids: list[str] = field(default_factory=list)
    active_instance_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)

    def touch(self) -> None:
        self.updated_at = _now_iso()

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "session",
            "session_id": self.session_id,
            "status": self.status.value,
            "instance_ids": list(self.instance_ids),
            "active_instance_id": self.active_instance_id,
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionRecord:
        raw_status = data.get("status", SessionStatus.OPEN.value)
        try:
            status = SessionStatus(str(raw_status))
        except ValueError:
            status = SessionStatus.OPEN
        ids = data.get("instance_ids") or []
        instance_ids = [str(i) for i in ids]
        active: str | None = None
        if "active_instance_id" not in data:
            # Legacy store rows (pre-0.58.10): seed focus to last attached.
            if instance_ids:
                active = instance_ids[-1]
        else:
            active_raw = data.get("active_instance_id")
            if active_raw is not None and str(active_raw).strip():
                active = str(active_raw).strip()
                # Drop stale focus not on the attach list (corrupt store).
                if active not in instance_ids:
                    active = None
            # Explicit null means cleared focus — do not re-seed.
        return cls(
            session_id=str(data["session_id"]),
            status=status,
            instance_ids=instance_ids,
            active_instance_id=active,
            metadata=dict(data.get("metadata") or {}),
            created_at=str(data.get("created_at") or _now_iso()),
            updated_at=str(data.get("updated_at") or _now_iso()),
        )


@dataclass(frozen=True)
class SessionBind:
    """Result of a surface bind — proof the outside subject is resolved.

    ``session_id`` is always a system session id (not an instance id).
    ``created`` is True when bind opened a new record.
    ``active_instance_id`` is the plane continue focus when one is set (0.58.10).
    """

    session_id: str
    status: SessionStatus
    created: bool = False
    surface: str | None = None
    instance_ids: tuple[str, ...] = ()
    active_instance_id: str | None = None

    @classmethod
    def from_record(
        cls,
        record: SessionRecord,
        *,
        created: bool = False,
        surface: str | None = None,
    ) -> SessionBind:
        surf = surface
        if surf is None:
            meta_surf = record.metadata.get("surface") or record.metadata.get(
                "last_surface"
            )
            surf = str(meta_surf) if meta_surf else None
        return cls(
            session_id=record.session_id,
            status=record.status,
            created=created,
            surface=surf,
            instance_ids=tuple(record.instance_ids),
            active_instance_id=record.active_instance_id,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "session_bind",
            "session_id": self.session_id,
            "status": self.status.value,
            "created": self.created,
            "surface": self.surface,
            "instance_ids": list(self.instance_ids),
            "active_instance_id": self.active_instance_id,
        }


__all__ = [
    "SessionBind",
    "SessionRecord",
    "SessionStatus",
    "HOST_SESSION_ID",
    "HOST_SESSION_ORIGIN",
    "WORK_DRAIN_ORIGIN",
    "looks_like_system_session_id",
    "new_session_id",
    "service_session_id",
]
