"""Open/close waits while keeping the owner index in sync."""

from __future__ import annotations

from typing import Any

from palm.common.wait.index import WaitOwnerIndex
from palm.core.wait import (
    WaitInterest,
    close_wait_on_job,
    open_wait_on_job,
)


def open_tracked_wait(
    index: WaitOwnerIndex,
    job: Any,
    interest: WaitInterest,
    **kwargs: Any,
) -> WaitInterest:
    """Open wait on ``job.state`` and register owner in ``index``."""
    opened = open_wait_on_job(job, interest, **kwargs)
    owner_id = str(job.id)
    index.register(owner_id, opened)
    return opened


def close_tracked_wait(
    index: WaitOwnerIndex,
    job: Any,
    *,
    kind: str,
    target_id: str,
) -> WaitInterest | None:
    """Close wait on ``job.state`` and drop index entry."""
    closed = close_wait_on_job(job, kind=kind, target_id=target_id)
    owner_id = str(job.id)
    index.unregister(owner_id, kind=kind, target_id=target_id)
    return closed


__all__ = ["close_tracked_wait", "open_tracked_wait"]
