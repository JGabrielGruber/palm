"""Durable WorkIntent store (StorageEngine), coalesce-aware, exclusive claim."""

from __future__ import annotations

import threading
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from palm.core.work import WorkIntent

if TYPE_CHECKING:
    from palm.core.storage import StorageEngine

WORK_PENDING_INDEX = "palm:work:pending_index"
WORK_ENTRY_PREFIX = "palm:work:entry:"
WORK_COALESCE_PREFIX = "palm:work:coalesce:"

# Default visibility timeout for a claim lease (seconds).
DEFAULT_LEASE_SECONDS = 60.0
DEFAULT_CLAIMER_ID = "default"


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.isoformat()


def _now(now: datetime | None) -> datetime:
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    return current


class WorkIntentStore:
    """Append / exclusive claim / ack work intents (run-when-able queue).

    In-process multi-claimer safety uses a store lock around mutate paths.
    Multi-process shared store still needs storage CAS (SD-019 residual).
    """

    def __init__(self, storage: StorageEngine) -> None:
        self._storage = storage
        self._lock = threading.RLock()

    def enqueue(self, intent: WorkIntent) -> str:
        with self._lock:
            data = intent.to_dict()
            data["status"] = "pending"
            data["claimed_by"] = None
            data["lease_until"] = None
            if intent.coalesce_key:
                existing_id = self._storage.get(
                    f"{WORK_COALESCE_PREFIX}{intent.coalesce_key}"
                )
                if isinstance(existing_id, str) and existing_id:
                    self._remove_pending(existing_id)
            self._storage.set(f"{WORK_ENTRY_PREFIX}{intent.id}", data)
            index = self._load_index()
            if intent.id not in index:
                index.append(intent.id)
                self._storage.set(WORK_PENDING_INDEX, index)
            if intent.coalesce_key:
                self._storage.set(
                    f"{WORK_COALESCE_PREFIX}{intent.coalesce_key}", intent.id
                )
            return intent.id

    def claim_due(
        self,
        *,
        limit: int = 10,
        claimer_id: str = DEFAULT_CLAIMER_ID,
        now: datetime | None = None,
        lease_seconds: float = DEFAULT_LEASE_SECONDS,
    ) -> list[WorkIntent]:
        """Exclusive claim: only ``pending`` and due intents; stamp lease.

        Concurrent claimers (in-process) never receive the same intent.
        """
        claimer = str(claimer_id or DEFAULT_CLAIMER_ID)
        lease = max(0.1, float(lease_seconds))
        current = _now(now)
        until = _iso(current + timedelta(seconds=lease))
        claimed: list[WorkIntent] = []
        with self._lock:
            for entry_id in list(self._load_index()):
                if len(claimed) >= limit:
                    break
                raw = self._storage.get(f"{WORK_ENTRY_PREFIX}{entry_id}")
                if not isinstance(raw, dict):
                    self._remove_pending(entry_id)
                    continue
                intent = WorkIntent.from_dict(raw)
                if intent.status != "pending":
                    continue
                if not intent.is_due(now=current):
                    continue
                # Re-read under lock: only pending may become claimed.
                fresh = self._storage.get(f"{WORK_ENTRY_PREFIX}{entry_id}")
                if not isinstance(fresh, dict):
                    self._remove_pending(entry_id)
                    continue
                if str(fresh.get("status") or "") != "pending":
                    continue
                updated = WorkIntent.from_dict(
                    {
                        **fresh,
                        "status": "claimed",
                        "claimed_by": claimer,
                        "lease_until": until,
                    }
                )
                self._storage.set(
                    f"{WORK_ENTRY_PREFIX}{entry_id}", updated.to_dict()
                )
                claimed.append(updated)
        return claimed

    def reclaim_expired(self, *, now: datetime | None = None) -> int:
        """Return expired claimed intents to ``pending``. Returns reclaim count."""
        current = _now(now)
        n = 0
        with self._lock:
            for entry_id in list(self._load_index()):
                raw = self._storage.get(f"{WORK_ENTRY_PREFIX}{entry_id}")
                if not isinstance(raw, dict):
                    self._remove_pending(entry_id)
                    continue
                intent = WorkIntent.from_dict(raw)
                if intent.status != "claimed":
                    continue
                if not intent.lease_expired(now=current):
                    continue
                restored = WorkIntent.from_dict(
                    {
                        **intent.to_dict(),
                        "status": "pending",
                        "claimed_by": None,
                        "lease_until": None,
                    }
                )
                self._storage.set(
                    f"{WORK_ENTRY_PREFIX}{entry_id}", restored.to_dict()
                )
                n += 1
        return n

    def ack(
        self, intent_id: str, *, claimer_id: str | None = None
    ) -> bool:
        """Mark done. If ``claimer_id`` set, only the owner may ack."""
        with self._lock:
            key = f"{WORK_ENTRY_PREFIX}{intent_id}"
            raw = self._storage.get(key)
            if not isinstance(raw, dict):
                self._remove_pending(intent_id)
                return False
            if claimer_id is not None:
                owner = raw.get("claimed_by")
                if owner is not None and str(owner) != str(claimer_id):
                    return False
            raw = {
                **raw,
                "status": "done",
                "claimed_by": None,
                "lease_until": None,
            }
            self._storage.set(key, raw)
            ck = raw.get("coalesce_key")
            if ck:
                cur = self._storage.get(f"{WORK_COALESCE_PREFIX}{ck}")
                if cur == intent_id:
                    self._storage.delete(f"{WORK_COALESCE_PREFIX}{ck}")
            self._remove_pending(intent_id)
            return True

    def fail(
        self,
        intent_id: str,
        error: str,
        *,
        claimer_id: str | None = None,
    ) -> bool:
        """Record failure; requeue or terminal fail. Owner check optional."""
        with self._lock:
            key = f"{WORK_ENTRY_PREFIX}{intent_id}"
            raw = self._storage.get(key)
            if not isinstance(raw, dict):
                self._remove_pending(intent_id)
                return False
            if claimer_id is not None:
                owner = raw.get("claimed_by")
                if owner is not None and str(owner) != str(claimer_id):
                    return False
            attempts = int(raw.get("attempt") or 0) + 1
            raw = {**raw, "attempt": attempts, "last_error": error}
            if attempts >= 5:
                raw["status"] = "failed"
                raw["claimed_by"] = None
                raw["lease_until"] = None
                self._storage.set(key, raw)
                self._remove_pending(intent_id)
            else:
                raw["status"] = "pending"
                raw["claimed_by"] = None
                raw["lease_until"] = None
                self._storage.set(key, raw)
            return True

    def pending_count(self) -> int:
        with self._lock:
            return len(self._load_index())

    def list_pending(self, *, limit: int = 100) -> list[WorkIntent]:
        with self._lock:
            out: list[WorkIntent] = []
            for entry_id in self._load_index()[:limit]:
                raw = self._storage.get(f"{WORK_ENTRY_PREFIX}{entry_id}")
                if isinstance(raw, dict):
                    out.append(WorkIntent.from_dict(raw))
            return out

    def _load_index(self) -> list[str]:
        raw = self._storage.get(WORK_PENDING_INDEX)
        if not isinstance(raw, list):
            return []
        return [str(i) for i in raw]

    def _remove_pending(self, intent_id: str) -> None:
        index = self._load_index()
        if intent_id in index:
            index.remove(intent_id)
            self._storage.set(WORK_PENDING_INDEX, index)


__all__ = [
    "DEFAULT_CLAIMER_ID",
    "DEFAULT_LEASE_SECONDS",
    "WORK_COALESCE_PREFIX",
    "WORK_ENTRY_PREFIX",
    "WORK_PENDING_INDEX",
    "WorkIntentStore",
]
