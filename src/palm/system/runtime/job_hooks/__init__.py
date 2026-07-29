"""Job lifecycle hooks registered on the orchestration engine.

Canonical home for instance persistence, outbox drain, and state snapshots.
Compatibility re-export (SD-012): ``palm.common.hooks``.
"""

from palm.system.runtime.job_hooks.instance_persistence import InstancePersistenceHook
from palm.system.runtime.job_hooks.outbox_drain import OutboxDrainHook
from palm.system.runtime.job_hooks.state_snapshot import StateSnapshotHook

__all__ = [
    "InstancePersistenceHook",
    "OutboxDrainHook",
    "StateSnapshotHook",
]
