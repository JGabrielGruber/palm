"""
Workload plane — pure lifecycle engine for isolated work.

**Invariant:** no neonroot/docker/k8s/SSH clients. Concrete adapters register
via :data:`workload_runtime_registry` from outside core (``palm.runners``).

See docs/VISION-0.56.md and ADR-024.
"""

from palm.core.workload.driver import WorkloadDriver
from palm.core.workload.engine import WorkloadEngine
from palm.core.workload.events import (
    WORKLOAD_EVENT_FAILED,
    WORKLOAD_EVENT_READY,
    WORKLOAD_EVENT_STARTED,
    WORKLOAD_EVENT_STOPPED,
    WORKLOAD_EVENT_TYPES,
)
from palm.core.workload.exceptions import (
    WorkloadError,
    WorkloadNotFoundError,
    WorkloadPlacementError,
    WorkloadPolicyError,
    WorkloadSpecError,
    WorkloadStateError,
)
from palm.core.workload.handle import WorkloadHandle
from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.protocol import (
    RuntimeCapabilities,
    RuntimeHealth,
    RuntimePollOutcome,
    RuntimeStartOutcome,
    RuntimeStopOutcome,
    WorkloadRuntime,
)
from palm.core.workload.record import Workload
from palm.core.workload.registry import workload_runtime_registry
from palm.core.workload.result import WorkloadResult
from palm.core.workload.spec import (
    SPEC_VERSION,
    IsolationPolicy,
    LifecyclePolicy,
    WorkloadKind,
    WorkloadPlacement,
    WorkloadSpec,
)
from palm.core.workload.status import (
    ACTIVE_STATUSES,
    TERMINAL_STATUSES,
    WorkloadStatus,
    can_transition,
    is_exec_allowed,
    is_terminal,
)

__all__ = [
    "ACTIVE_STATUSES",
    "SPEC_VERSION",
    "TERMINAL_STATUSES",
    "WORKLOAD_EVENT_FAILED",
    "WORKLOAD_EVENT_READY",
    "WORKLOAD_EVENT_STARTED",
    "WORKLOAD_EVENT_STOPPED",
    "WORKLOAD_EVENT_TYPES",
    "IsolationPolicy",
    "LifecyclePolicy",
    "RuntimeCapabilities",
    "RuntimeHealth",
    "RuntimePollOutcome",
    "RuntimeStartOutcome",
    "RuntimeStopOutcome",
    "Workload",
    "WorkloadDriver",
    "WorkloadEngine",
    "WorkloadError",
    "WorkloadHandle",
    "WorkloadKind",
    "WorkloadNotFoundError",
    "WorkloadOwner",
    "WorkloadPlacement",
    "WorkloadPlacementError",
    "WorkloadPolicyError",
    "WorkloadResult",
    "WorkloadRuntime",
    "WorkloadSpec",
    "WorkloadSpecError",
    "WorkloadStateError",
    "WorkloadStatus",
    "can_transition",
    "is_exec_allowed",
    "is_terminal",
    "workload_runtime_registry",
]
