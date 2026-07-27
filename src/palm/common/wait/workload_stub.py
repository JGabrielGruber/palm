"""Workload wait-kind stub (0.55.7) — socket for 0.56 WorkloadEngine.

Proves the reactive grammar for ``kind=workload`` without a full engine:

* open wait interest on an owner job
* emit self-describing ``workload.*`` lifecycle events on ``runtime.event``
* WaitMatcher resumes or fails the owner

Full placement / runners / WorkloadLeaf land in 0.56 ([VISION-0.56], ADR-024).
"""

from __future__ import annotations

from typing import Any

from palm.common.wait.access import open_interest_on_job
from palm.core.wait import (
    WAIT_KIND_WORKLOAD,
    WaitInterest,
    make_workload_wait,
)

# Normative stub event names (matcher already understands these).
WORKLOAD_EVENT_READY = "workload.ready"
WORKLOAD_EVENT_FAILED = "workload.failed"
WORKLOAD_EVENT_COMPLETED = "workload.completed"

WORKLOAD_STUB_EVENT_TYPES: frozenset[str] = frozenset(
    {
        WORKLOAD_EVENT_READY,
        WORKLOAD_EVENT_FAILED,
        WORKLOAD_EVENT_COMPLETED,
    }
)


def open_workload_wait(
    job: Any,
    workload_id: str,
    *,
    meta: dict[str, Any] | None = None,
) -> WaitInterest:
    """Park owner interest on a workload target (``kind=workload``)."""
    body = {"source": "workload_stub", **dict(meta or {})}
    interest = make_workload_wait(str(workload_id), meta=body)
    return open_interest_on_job(job, interest)


def emit_workload_ready(
    event_engine: Any,
    workload_id: str,
    *,
    status: str = "READY",
    **extra: Any,
) -> Any:
    """Announce workload ready — matcher positive outcome for wait interest."""
    return event_engine.emit(
        WORKLOAD_EVENT_READY,
        workload_id=str(workload_id),
        kind=WAIT_KIND_WORKLOAD,
        status=status,
        **extra,
    )


def emit_workload_failed(
    event_engine: Any,
    workload_id: str,
    *,
    status: str = "FAILED",
    error: str | None = None,
    **extra: Any,
) -> Any:
    """Announce workload failed — matcher applies on_target_failed policy."""
    payload: dict[str, Any] = {
        "workload_id": str(workload_id),
        "kind": WAIT_KIND_WORKLOAD,
        "status": status,
    }
    if error is not None:
        payload["error"] = error
    payload.update(extra)
    return event_engine.emit(WORKLOAD_EVENT_FAILED, **payload)


def emit_workload_completed(
    event_engine: Any,
    workload_id: str,
    *,
    status: str = "SUCCEEDED",
    **extra: Any,
) -> Any:
    """Announce workload completed (terminal success/fail via status)."""
    return event_engine.emit(
        WORKLOAD_EVENT_COMPLETED,
        workload_id=str(workload_id),
        kind=WAIT_KIND_WORKLOAD,
        status=status,
        **extra,
    )


__all__ = [
    "WORKLOAD_EVENT_COMPLETED",
    "WORKLOAD_EVENT_FAILED",
    "WORKLOAD_EVENT_READY",
    "WORKLOAD_STUB_EVENT_TYPES",
    "emit_workload_completed",
    "emit_workload_failed",
    "emit_workload_ready",
    "open_workload_wait",
]
