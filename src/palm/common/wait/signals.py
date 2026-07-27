"""Map orchestration events → target lifecycle signals for wait matching."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from palm.core.wait import WAIT_KIND_JOB, WAIT_KIND_WORKLOAD

OUTCOME_SUCCEEDED = "succeeded"
OUTCOME_FAILED = "failed"
OUTCOME_CANCELLED = "cancelled"
OUTCOME_READY = "ready"

# Terminal-ish outcomes that can unpark (or fail) an owner.
POSITIVE_OUTCOMES = frozenset({OUTCOME_SUCCEEDED, OUTCOME_READY})
NEGATIVE_OUTCOMES = frozenset({OUTCOME_FAILED, OUTCOME_CANCELLED})

# Events the matcher understands in 0.55.2 (+ workload stub names for 0.55.7).
MATCHER_EVENT_TYPES: tuple[str, ...] = (
    "job.completed",
    "job.status_changed",
    "flow.session.succeeded",
    "flow.session.failed",
    "workload.ready",
    "workload.failed",
    "workload.completed",
)


@dataclass(frozen=True, slots=True)
class TargetSignal:
    """Completer announced itself: kind + target_id + outcome."""

    kind: str
    target_id: str
    outcome: str
    event_type: str
    status: str | None = None


def _status_outcome(status: str | None) -> str | None:
    if not status:
        return None
    s = str(status).upper()
    if s in ("SUCCEEDED", "SUCCESS", "DONE", "COMPLETED"):
        return OUTCOME_SUCCEEDED
    if s in ("FAILED", "ERROR"):
        return OUTCOME_FAILED
    if s in ("CANCELLED", "CANCELED"):
        return OUTCOME_CANCELLED
    return None


def extract_target_signal(
    event_type: str,
    payload: dict[str, Any] | None,
) -> TargetSignal | None:
    """Return a :class:`TargetSignal` if ``event`` is a completer lifecycle we know."""
    data = dict(payload or {})
    et = str(event_type or "")

    if et in ("flow.session.succeeded",):
        job_id = data.get("job_id")
        if not job_id:
            return None
        return TargetSignal(
            kind=WAIT_KIND_JOB,
            target_id=str(job_id),
            outcome=OUTCOME_SUCCEEDED,
            event_type=et,
            status=str(data.get("status") or "SUCCEEDED"),
        )

    if et in ("flow.session.failed",):
        job_id = data.get("job_id")
        if not job_id:
            return None
        return TargetSignal(
            kind=WAIT_KIND_JOB,
            target_id=str(job_id),
            outcome=OUTCOME_FAILED,
            event_type=et,
            status=str(data.get("status") or "FAILED"),
        )

    if et in ("job.completed", "job.status_changed"):
        job_id = data.get("job_id")
        if not job_id:
            return None
        status = data.get("status")
        outcome = _status_outcome(str(status) if status is not None else None)
        if outcome is None:
            # Non-terminal status_changed — not a completer signal.
            return None
        return TargetSignal(
            kind=WAIT_KIND_JOB,
            target_id=str(job_id),
            outcome=outcome,
            event_type=et,
            status=str(status) if status is not None else None,
        )

    if et in ("workload.ready",):
        wid = data.get("workload_id") or data.get("target_id") or data.get("id")
        if not wid:
            return None
        return TargetSignal(
            kind=WAIT_KIND_WORKLOAD,
            target_id=str(wid),
            outcome=OUTCOME_READY,
            event_type=et,
            status=str(data.get("status") or "READY"),
        )

    if et in ("workload.failed",):
        wid = data.get("workload_id") or data.get("target_id") or data.get("id")
        if not wid:
            return None
        return TargetSignal(
            kind=WAIT_KIND_WORKLOAD,
            target_id=str(wid),
            outcome=OUTCOME_FAILED,
            event_type=et,
            status=str(data.get("status") or "FAILED"),
        )

    if et in ("workload.completed",):
        wid = data.get("workload_id") or data.get("target_id") or data.get("id")
        if not wid:
            return None
        status = data.get("status")
        outcome = _status_outcome(str(status) if status is not None else None)
        if outcome is None:
            outcome = OUTCOME_SUCCEEDED
        return TargetSignal(
            kind=WAIT_KIND_WORKLOAD,
            target_id=str(wid),
            outcome=outcome,
            event_type=et,
            status=str(status) if status is not None else None,
        )

    return None


def extract_signal_from_event(event: Any) -> TargetSignal | None:
    """Accept core ``Event`` or duck-typed ``.type`` / ``.payload``."""
    et = getattr(event, "type", None)
    payload = getattr(event, "payload", None)
    if et is None and isinstance(event, dict):
        et = event.get("type")
        payload = event.get("payload")
    return extract_target_signal(str(et or ""), payload if isinstance(payload, dict) else {})


__all__ = [
    "MATCHER_EVENT_TYPES",
    "NEGATIVE_OUTCOMES",
    "OUTCOME_CANCELLED",
    "OUTCOME_FAILED",
    "OUTCOME_READY",
    "OUTCOME_SUCCEEDED",
    "POSITIVE_OUTCOMES",
    "TargetSignal",
    "extract_signal_from_event",
    "extract_target_signal",
]
