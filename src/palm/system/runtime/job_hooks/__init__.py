"""Job lifecycle hooks registered on the orchestration engine.

Canonical home for instance persistence, session ownership, outbox drain,
and state snapshots.

"""

from palm.system.runtime.job_hooks.instance_persistence import InstancePersistenceHook
from palm.system.runtime.job_hooks.outbox_drain import OutboxDrainHook
from palm.system.runtime.job_hooks.session_ownership import SessionOwnershipHook
from palm.system.runtime.job_hooks.state_snapshot import StateSnapshotHook

__all__ = [
    "InstancePersistenceHook",
    "OutboxDrainHook",
    "SessionOwnershipHook",
    "StateSnapshotHook",
]
