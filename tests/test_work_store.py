"""WorkIntentStore — coalesce, exclusive claim, reclaim (0.37 · 0.62)."""

from __future__ import annotations

import threading
from datetime import UTC, datetime, timedelta

from palm.core.storage import StorageEngine
from palm.core.work import WorkIntent
from palm.system.subsystems.planes.work import WorkIntentStore
from palm.system.subsystems.planes.work.store import DEFAULT_CLAIMER_ID


def _storage() -> StorageEngine:
    s = StorageEngine()
    s.initialize()
    s.select("memory")
    return s


def test_enqueue_claim_ack() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(WorkIntent(kind="run_flow", target="a"))
    assert store.pending_count() == 1
    claimed = store.claim_due(limit=5, claimer_id="w1")
    assert len(claimed) == 1
    assert claimed[0].status == "claimed"
    assert claimed[0].claimed_by == "w1"
    assert claimed[0].lease_until is not None
    store.ack(claimed[0].id, claimer_id="w1")
    assert store.pending_count() == 0


def test_coalesce_replaces_pending() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(
        WorkIntent(id="1", kind="run_flow", target="a", coalesce_key="k")
    )
    store.enqueue(
        WorkIntent(id="2", kind="run_flow", target="a", coalesce_key="k")
    )
    pending = store.list_pending()
    assert len(pending) == 1
    assert pending[0].id == "2"


def test_claim_stamps_claimer_and_lease() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(WorkIntent(kind="run_flow", target="a"))
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    claimed = store.claim_due(
        limit=1, claimer_id="alpha", now=now, lease_seconds=30.0
    )
    assert len(claimed) == 1
    assert claimed[0].claimed_by == "alpha"
    until = datetime.fromisoformat(claimed[0].lease_until or "")
    assert until == now + timedelta(seconds=30)


def test_second_claim_does_not_reclaim_same_intent() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(WorkIntent(id="x", kind="run_flow", target="a"))
    a = store.claim_due(limit=10, claimer_id="a")
    b = store.claim_due(limit=10, claimer_id="b")
    assert len(a) == 1
    assert len(b) == 0
    assert a[0].id == "x"


def test_two_claimers_never_share_same_intent() -> None:
    """Concurrent claimers: each intent claimed at most once (SD-017)."""
    store = WorkIntentStore(_storage())
    n = 40
    for i in range(n):
        store.enqueue(WorkIntent(id=f"i{i}", kind="run_flow", target="t"))

    barrier = threading.Barrier(2)
    got_a: list[str] = []
    got_b: list[str] = []
    errors: list[BaseException] = []

    def run(claimer: str, out: list[str]) -> None:
        try:
            barrier.wait(timeout=5)
            # Multiple small claims to interleave
            for _ in range(n):
                batch = store.claim_due(limit=1, claimer_id=claimer)
                out.extend(x.id for x in batch)
                if len(out) >= n:
                    break
        except BaseException as exc:  # noqa: BLE001 — collect for assert
            errors.append(exc)

    t1 = threading.Thread(target=run, args=("claimer-a", got_a))
    t2 = threading.Thread(target=run, args=("claimer-b", got_b))
    t1.start()
    t2.start()
    t1.join(timeout=10)
    t2.join(timeout=10)
    assert not errors, errors
    all_ids = got_a + got_b
    assert len(all_ids) == n
    assert len(set(all_ids)) == n
    assert not (set(got_a) & set(got_b))


def test_reclaim_expired_returns_to_pending() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(WorkIntent(id="z", kind="run_flow", target="a"))
    t0 = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    claimed = store.claim_due(
        limit=1, claimer_id="dead", now=t0, lease_seconds=10.0
    )
    assert len(claimed) == 1
    # Still claimed before lease end
    mid = t0 + timedelta(seconds=5)
    assert store.reclaim_expired(now=mid) == 0
    assert store.claim_due(limit=1, claimer_id="other", now=mid) == []
    # After lease
    later = t0 + timedelta(seconds=11)
    assert store.reclaim_expired(now=later) == 1
    again = store.claim_due(limit=1, claimer_id="other", now=later)
    assert len(again) == 1
    assert again[0].id == "z"
    assert again[0].claimed_by == "other"


def test_ack_owner_mismatch_refused() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(WorkIntent(id="o", kind="run_flow", target="a"))
    claimed = store.claim_due(limit=1, claimer_id="owner")
    assert len(claimed) == 1
    assert store.ack("o", claimer_id="thief") is False
    # still in index as claimed
    assert store.pending_count() == 1
    assert store.ack("o", claimer_id="owner") is True
    assert store.pending_count() == 0


def test_fail_clears_claim_and_requeues() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(WorkIntent(id="f", kind="run_flow", target="a"))
    store.claim_due(limit=1, claimer_id="w")
    assert store.fail("f", "boom", claimer_id="w") is True
    again = store.claim_due(limit=1, claimer_id="w2")
    assert len(again) == 1
    assert again[0].status == "claimed"
    assert again[0].attempt == 1


def test_default_claimer_id_backward_compat() -> None:
    store = WorkIntentStore(_storage())
    store.enqueue(WorkIntent(kind="run_flow", target="a"))
    claimed = store.claim_due(limit=5)
    assert claimed[0].claimed_by == DEFAULT_CLAIMER_ID


def test_work_intent_roundtrip_claim_fields() -> None:
    intent = WorkIntent(
        kind="run_flow",
        target="t",
        status="claimed",
        claimed_by="c1",
        lease_until="2026-01-01T12:00:00+00:00",
    )
    back = WorkIntent.from_dict(intent.to_dict())
    assert back.claimed_by == "c1"
    assert back.lease_until == "2026-01-01T12:00:00+00:00"
    assert back.lease_expired(
        now=datetime(2026, 1, 1, 12, 0, 1, tzinfo=UTC)
    )
    assert not back.lease_expired(
        now=datetime(2026, 1, 1, 11, 59, 0, tzinfo=UTC)
    )
