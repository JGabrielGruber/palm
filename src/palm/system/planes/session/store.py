"""Session store over :class:`~palm.core.storage.StorageEngine` (0.58.1).

Same pattern as :class:`~palm.system.planes.work.store.WorkIntentStore`:
keys on the system instance storage backend (memory, filesystem, …).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from palm.system.planes.session.types import SessionRecord, SessionStatus

if TYPE_CHECKING:
    from palm.core.storage import StorageEngine

SESSION_INDEX = "palm:session:index"
SESSION_ENTRY_PREFIX = "palm:session:entry:"


class SessionStore:
    """Session records on StorageEngine (index + entry keys)."""

    def __init__(self, storage: StorageEngine) -> None:
        self._storage = storage

    @property
    def storage(self) -> StorageEngine:
        return self._storage

    def put(self, record: SessionRecord) -> SessionRecord:
        self._storage.set(f"{SESSION_ENTRY_PREFIX}{record.session_id}", record.to_dict())
        index = self._load_index()
        if record.session_id not in index:
            index.append(record.session_id)
            self._storage.set(SESSION_INDEX, index)
        return record

    def get(self, session_id: str) -> SessionRecord | None:
        raw = self._storage.get(f"{SESSION_ENTRY_PREFIX}{session_id}")
        if not isinstance(raw, dict):
            return None
        return SessionRecord.from_dict(raw)

    def delete(self, session_id: str) -> bool:
        key = f"{SESSION_ENTRY_PREFIX}{session_id}"
        raw = self._storage.get(key)
        if raw is None:
            self._remove_from_index(session_id)
            return False
        self._storage.delete(key)
        self._remove_from_index(session_id)
        return True

    def list(
        self,
        *,
        status: SessionStatus | None = None,
        include_closed: bool = True,
    ) -> list[SessionRecord]:
        out: list[SessionRecord] = []
        for sid in self._load_index():
            rec = self.get(sid)
            if rec is None:
                self._remove_from_index(sid)
                continue
            if status is not None and rec.status != status:
                continue
            if not include_closed and rec.status == SessionStatus.CLOSED:
                continue
            out.append(rec)
        out.sort(key=lambda r: r.created_at)
        return out

    def clear(self) -> None:
        for sid in list(self._load_index()):
            self._storage.delete(f"{SESSION_ENTRY_PREFIX}{sid}")
        self._storage.set(SESSION_INDEX, [])

    def __len__(self) -> int:
        return len(self._load_index())

    def _load_index(self) -> list[str]:
        raw = self._storage.get(SESSION_INDEX)
        if not isinstance(raw, list):
            return []
        return [str(i) for i in raw]

    def _remove_from_index(self, session_id: str) -> None:
        index = self._load_index()
        if session_id in index:
            index.remove(session_id)
            self._storage.set(SESSION_INDEX, index)


__all__ = [
    "SESSION_ENTRY_PREFIX",
    "SESSION_INDEX",
    "SessionStore",
]
