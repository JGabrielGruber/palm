"""Public workload lifecycle event type names (EVENT-PLANE catalog).

Payloads stay small: ids, status, exit_code, owner, labels, host_id, artifact refs.
WorkloadEngine never starts flows — only announces itself.
"""

from __future__ import annotations

WORKLOAD_EVENT_STARTED = "workload.started"
WORKLOAD_EVENT_READY = "workload.ready"
WORKLOAD_EVENT_FAILED = "workload.failed"
WORKLOAD_EVENT_STOPPED = "workload.stopped"

WORKLOAD_EVENT_TYPES: frozenset[str] = frozenset(
    {
        WORKLOAD_EVENT_STARTED,
        WORKLOAD_EVENT_READY,
        WORKLOAD_EVENT_FAILED,
        WORKLOAD_EVENT_STOPPED,
    }
)
