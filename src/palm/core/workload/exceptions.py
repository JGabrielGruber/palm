"""Workload engine exceptions (pure core)."""

from __future__ import annotations

from palm.core.exceptions import EngineError


class WorkloadError(EngineError):
    """Base error for workload plane failures."""


class WorkloadPolicyError(WorkloadError):
    """Raised when isolation, runtime, or placement policy denies an operation."""


class WorkloadPlacementError(WorkloadError):
    """Raised when no host/runtime can satisfy the Spec."""


class WorkloadNotFoundError(WorkloadError):
    """Raised when a workload id is unknown to the engine."""


class WorkloadStateError(WorkloadError):
    """Raised when an operation is invalid for the current lifecycle status."""


class WorkloadSpecError(WorkloadError):
    """Raised when a WorkloadSpec is invalid or rejected."""
