"""In-memory session store (0.58.1 seat).

Durable storage (mirror instance manager spirit) lands in 0.58.2 (SI-013).
This store is enough for lifecycle API and tests without product surfaces.
"""

from __future__ import annotations

import threading
from typing import Iterable

from palm.system.planes.session.types import SessionRecord, SessionStatus


class SessionStore:
    """Thread-safe in-memory map of session_id → SessionRecord."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._by_id: dict[str, SessionRecord] = {}

    def put(self, record: SessionRecord) -> SessionRecord:
        with self._lock:
            self._by_id[record.session_id] = record
            return record

    def get(self, session_id: str) -> SessionRecord | None:
        with self._lock:
            return self._by_id.get(session_id)

    def delete(self, session_id: str) -> bool:
        with self._lock:
            return self._by_id.pop(session_id, None) is not None

    def list(
        self,
        *,
        status: SessionStatus | None = None,
        include_closed: bool = True,
    ) -> list[SessionRecord]:
        with self._lock:
            rows: Iterable[SessionRecord] = self._by_id.values()
            out: list[SessionRecord] = []
            for rec in rows:
                if status is not None and rec.status != status:
                    continue
                if not include_closed and rec.status == SessionStatus.CLOSED:
                    continue
                out.append(rec)
            out.sort(key=lambda r: r.created_at)
            return out

    def clear(self) -> None:
        with self._lock:
            self._by_id.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._by_id)


__all__ = ["SessionStore"]
