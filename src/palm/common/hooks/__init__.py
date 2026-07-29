"""Shim (SD-012) — canonical: :mod:`palm.system.runtime.job_hooks`."""

from palm.system.runtime.job_hooks import (
    InstancePersistenceHook,
    OutboxDrainHook,
    StateSnapshotHook,
)

__all__ = [
    "InstancePersistenceHook",
    "OutboxDrainHook",
    "StateSnapshotHook",
]
