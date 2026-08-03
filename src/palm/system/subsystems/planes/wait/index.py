"""Optional owner index: target → owner job ids (O(1) match aid)."""

from __future__ import annotations

import threading
from collections import defaultdict

from palm.core.wait import WaitInterest


def _key(kind: str, target_id: str) -> tuple[str, str]:
    return (str(kind), str(target_id))


class WaitOwnerIndex:
    """Thread-safe map from (kind, target_id) → set of owner job ids.

    Source of truth for open interest remains job/instance state; the index is
    an optimization and registration surface for the matcher.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._owners: dict[tuple[str, str], set[str]] = defaultdict(set)

    def register(self, owner_job_id: str, interest: WaitInterest) -> None:
        with self._lock:
            self._owners[_key(interest.kind, interest.target_id)].add(str(owner_job_id))

    def unregister(
        self,
        owner_job_id: str,
        *,
        kind: str,
        target_id: str,
    ) -> None:
        with self._lock:
            k = _key(kind, target_id)
            owners = self._owners.get(k)
            if not owners:
                return
            owners.discard(str(owner_job_id))
            if not owners:
                self._owners.pop(k, None)

    def unregister_all_for_owner(self, owner_job_id: str) -> int:
        """Drop every index entry for ``owner_job_id``. Returns removed count."""
        oid = str(owner_job_id)
        removed = 0
        with self._lock:
            empty_keys: list[tuple[str, str]] = []
            for k, owners in self._owners.items():
                if oid in owners:
                    owners.discard(oid)
                    removed += 1
                if not owners:
                    empty_keys.append(k)
            for k in empty_keys:
                self._owners.pop(k, None)
        return removed

    def owners_for(self, *, kind: str, target_id: str) -> frozenset[str]:
        with self._lock:
            return frozenset(self._owners.get(_key(kind, target_id), ()))

    def clear(self) -> None:
        with self._lock:
            self._owners.clear()

    def __len__(self) -> int:
        with self._lock:
            return sum(len(v) for v in self._owners.values())


__all__ = ["WaitOwnerIndex"]
