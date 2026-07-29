"""Runtime compatibility façade (SD-012).

Canonical implementations live under :mod:`palm.system.runtime`.
This package re-exports for import stability during 0.57 cutover.
Server transport helpers remain here under ``.server`` (SD-011).
"""

from palm.system.runtime.base import BaseRuntime
from palm.system.runtime.hooks import (
    AuthMiddleware,
    DriveObservabilityHook,
    DriveSlice,
    authenticate_runtime,
)
from palm.system.runtime.host import RuntimeHost
from palm.system.runtime.wiring import SchedulerPolicy, resolve_runner, resolve_scheduler

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
