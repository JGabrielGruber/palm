"""Session store over :class:`~palm.core.storage.StorageEngine` (0.58).

Same pattern as :class:`~palm.system.subsystems.planes.work.store.WorkIntentStore`:
keys on the system instance storage backend (memory, filesystem, …).

**Keys (0.58.2):**

* ``palm:session:entry:{session_id}`` — session record dict
* ``palm:session:index`` — list of session ids
* ``palm:session:by_instance:{instance_id}`` — reverse index → session_id
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from palm.system.subsystems.planes.session.types import SessionRecord, SessionStatus

if TYPE_CHECKING:
    from palm.core.storage import StorageEngine

SESSION_INDEX = "palm:session:index"
SESSION_ENTRY_PREFIX = "palm:session:entry:"
SESSION_BY_INSTANCE_PREFIX = "palm:session:by_instance:"


class SessionStore:
    """Session records on StorageEngine (index + entry + instance reverse)."""

    def __init__(self, storage: StorageEngine) -> None:
        self._storage = storage

    @property
    def storage(self) -> StorageEngine:
        return self._storage

    def put(self, record: SessionRecord) -> SessionRecord:
        """Write record and keep instance→session reverse index in sync."""
        old = self.get(record.session_id)
        old_ids = set(old.instance_ids) if old is not None else set()
        new_ids = set(record.instance_ids)

        self._storage.set(f"{SESSION_ENTRY_PREFIX}{record.session_id}", record.to_dict())
        index = self._load_index()
        if record.session_id not in index:
            index.append(record.session_id)
            self._storage.set(SESSION_INDEX, index)

        for iid in old_ids - new_ids:
            self._clear_instance_owner(iid, expected_session=record.session_id)
        for iid in new_ids:
            self._set_instance_owner(iid, record.session_id)
        return record

    def get(self, session_id: str) -> SessionRecord | None:
        raw = self._storage.get(f"{SESSION_ENTRY_PREFIX}{session_id}")
        if not isinstance(raw, dict):
            return None
        return SessionRecord.from_dict(raw)

    def session_id_for_instance(self, instance_id: str) -> str | None:
        """Reverse index: which session owns this instance (if any)."""
        iid = (instance_id or "").strip()
        if not iid:
            return None
        raw = self._storage.get(f"{SESSION_BY_INSTANCE_PREFIX}{iid}")
        if raw is None:
            return None
        return str(raw)

    def get_by_instance(self, instance_id: str) -> SessionRecord | None:
        sid = self.session_id_for_instance(instance_id)
        if sid is None:
            return None
        return self.get(sid)

    def delete(self, session_id: str) -> bool:
        key = f"{SESSION_ENTRY_PREFIX}{session_id}"
        rec = self.get(session_id)
        if rec is None:
            self._remove_from_index(session_id)
            return False
        for iid in rec.instance_ids:
            self._clear_instance_owner(iid, expected_session=session_id)
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
            self.delete(sid)
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

    def _set_instance_owner(self, instance_id: str, session_id: str) -> None:
        iid = (instance_id or "").strip()
        if not iid:
            return
        self._storage.set(f"{SESSION_BY_INSTANCE_PREFIX}{iid}", session_id)

    def _clear_instance_owner(
        self, instance_id: str, *, expected_session: str
    ) -> None:
        iid = (instance_id or "").strip()
        if not iid:
            return
        key = f"{SESSION_BY_INSTANCE_PREFIX}{iid}"
        cur = self._storage.get(key)
        if cur is None or str(cur) == expected_session:
            self._storage.delete(key)


__all__ = [
    "SESSION_BY_INSTANCE_PREFIX",
    "SESSION_ENTRY_PREFIX",
    "SESSION_INDEX",
    "SessionStore",
]
