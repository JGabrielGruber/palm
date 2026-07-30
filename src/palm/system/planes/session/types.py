"""Session plane types — system outside subject (0.58).

Session ≠ instance ≠ job. One session may attach many instances later
(attach API grows in 0.58.2; the record already holds the list).
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


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class SessionRecord:
    """Durable-shaped session subject held by the session plane.

    ``instance_ids`` is ordered attach list (0..N). Empty at open until
    multi-attach slices bind work under this session.
    """

    session_id: str
    status: SessionStatus = SessionStatus.OPEN
    instance_ids: list[str] = field(default_factory=list)
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
        return cls(
            session_id=str(data["session_id"]),
            status=status,
            instance_ids=[str(i) for i in ids],
            metadata=dict(data.get("metadata") or {}),
            created_at=str(data.get("created_at") or _now_iso()),
            updated_at=str(data.get("updated_at") or _now_iso()),
        )


__all__ = [
    "SessionRecord",
    "SessionStatus",
    "new_session_id",
]
