"""Shim (SD-012) — canonical: :mod:`palm.system.runtime.hooks.middleware`."""

from palm.system.runtime.hooks.middleware import (
    AuthMiddleware,
    DriveObservabilityHook,
    DriveSlice,
    authenticate_runtime,
)

__all__ = [
    "AuthMiddleware",
    "DriveObservabilityHook",
    "DriveSlice",
    "authenticate_runtime",
]
