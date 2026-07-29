"""Shim (SD-012) — canonical: :mod:`palm.system.runtime.hooks`."""

from palm.system.runtime.hooks import (
    AuthMiddleware,
    DriveObservabilityHook,
    DriveSlice,
    JobExecutionContextHook,
    authenticate_runtime,
)

__all__ = [
    "AuthMiddleware",
    "DriveObservabilityHook",
    "DriveSlice",
    "JobExecutionContextHook",
    "authenticate_runtime",
]
