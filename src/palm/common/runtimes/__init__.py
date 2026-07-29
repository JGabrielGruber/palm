"""Runtime compatibility façade (SD-012).

Canonical implementations live under :mod:`palm.system.runtime`.
This package re-exports for import stability during 0.57 cutover.
Server transport helpers remain here under ``.server`` (SD-011).
"""

from palm.common.runtimes.base import BaseRuntime
from palm.common.runtimes.hooks import (
    AuthMiddleware,
    DriveObservabilityHook,
    DriveSlice,
    authenticate_runtime,
)
from palm.common.runtimes.host import RuntimeHost
from palm.common.runtimes.wiring import SchedulerPolicy, resolve_runner, resolve_scheduler

__all__ = [
    "AuthMiddleware",
    "BaseRuntime",
    "DriveObservabilityHook",
    "DriveSlice",
    "RuntimeHost",
    "SchedulerPolicy",
    "authenticate_runtime",
    "resolve_runner",
    "resolve_scheduler",
]
