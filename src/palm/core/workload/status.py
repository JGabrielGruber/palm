"""Workload lifecycle status (normative state machine).

See docs/VISION-0.56.md §5 and ADR-024.
"""

from __future__ import annotations

from enum import StrEnum


class WorkloadStatus(StrEnum):
    """Lifecycle status of a live workload allocation."""

    PENDING = "PENDING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    READY = "READY"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


TERMINAL_STATUSES: frozenset[WorkloadStatus] = frozenset(
    {WorkloadStatus.STOPPED, WorkloadStatus.FAILED}
)
"""Terminal states — no resurrection without a new workload id."""

ACTIVE_STATUSES: frozenset[WorkloadStatus] = frozenset(
    {
        WorkloadStatus.PENDING,
        WorkloadStatus.STARTING,
        WorkloadStatus.RUNNING,
        WorkloadStatus.READY,
        WorkloadStatus.STOPPING,
    }
)

# Allowed transitions (from → allowed next). stop is always allowed toward STOPPING.
_ALLOWED: dict[WorkloadStatus, frozenset[WorkloadStatus]] = {
    WorkloadStatus.PENDING: frozenset(
        {
            WorkloadStatus.STARTING,
            WorkloadStatus.FAILED,
        }
    ),
    WorkloadStatus.STARTING: frozenset(
        {
            WorkloadStatus.RUNNING,
            WorkloadStatus.READY,
            WorkloadStatus.STOPPED,
            WorkloadStatus.FAILED,
            WorkloadStatus.STOPPING,
        }
    ),
    WorkloadStatus.RUNNING: frozenset(
        {
            WorkloadStatus.READY,  # rare upgrade path
            WorkloadStatus.STOPPING,
            WorkloadStatus.STOPPED,
            WorkloadStatus.FAILED,
        }
    ),
    WorkloadStatus.READY: frozenset(
        {
            WorkloadStatus.RUNNING,  # exec in progress on workspace
            WorkloadStatus.STOPPING,
            WorkloadStatus.STOPPED,
            WorkloadStatus.FAILED,
        }
    ),
    WorkloadStatus.STOPPING: frozenset(
        {
            WorkloadStatus.STOPPED,
            WorkloadStatus.FAILED,
        }
    ),
    WorkloadStatus.STOPPED: frozenset(),
    WorkloadStatus.FAILED: frozenset(),
}


def can_transition(current: WorkloadStatus, next_status: WorkloadStatus) -> bool:
    """Return whether ``current → next_status`` is a valid lifecycle step."""
    if current == next_status:
        return True
    return next_status in _ALLOWED.get(current, frozenset())


def is_terminal(status: WorkloadStatus) -> bool:
    """Return True when the workload cannot change without a new id."""
    return status in TERMINAL_STATUSES


def is_exec_allowed(status: WorkloadStatus) -> bool:
    """exec is only valid on READY workspace/service (VISION §5)."""
    return status is WorkloadStatus.READY
