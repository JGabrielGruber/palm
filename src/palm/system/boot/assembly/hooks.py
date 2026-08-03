"""
Orchestration hooks + engine init — boot assembly leaf.

Builds the drive hook chain, initializes orchestration, behavior tree, and
instance manager. Schedule only calls this and publishes returned seats.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.core.context import BaseState
from palm.states import BlackboardState
from palm.system.runtime.hooks import (
    AuthMiddleware,
    DriveObservabilityHook,
    JobExecutionContextHook,
)
from palm.system.runtime.job_hooks import (
    InstancePersistenceHook,
    OutboxDrainHook,
    SessionOwnershipHook,
    StateSnapshotHook,
)
from palm.system.runtime.wiring import resolve_scheduler


def install_orchestration_hooks(
    shell: Any,
    *,
    event: Any,
    context_engine: Any,
    auth: Any,
    outbox_store: Any = None,
    outbox_processor: Any = None,
    options: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Assemble hooks, initialize orchestration / BT / instance manager.

    Returns seats ``orchestration`` and ``instance_manager`` for BootContext.
    """
    opts = dict(options or {})

    scheduler = resolve_scheduler(
        opts,
        default_policy=shell.default_scheduler_policy,
    )
    hooks = list(opts.get("hooks") or [])
    if opts.get("observability"):
        hooks.append(DriveObservabilityHook())

    shell._auth_enforce = bool(opts.get("auth_enforce"))
    if shell._auth_enforce:
        hooks.append(
            AuthMiddleware(
                auth,
                required_roles=tuple(opts.get("auth_roles") or ("user",)),
            )
        )
    hooks.append(JobExecutionContextHook())
    hooks.append(
        InstancePersistenceHook(
            shell.instance_manager,
            outbox_store=outbox_store,
        )
    )
    # session_plane is not seated until planes.attach; hook resolves late.
    hooks.append(SessionOwnershipHook(get_plane=lambda: shell.session_plane))
    if outbox_processor is not None:
        hooks.append(OutboxDrainHook(outbox_processor))
    if opts.get("enable_state_snapshot"):
        hooks.append(
            StateSnapshotHook(
                shell.instance_manager,
                snapshot_on_status=opts.get("snapshot_on_status"),
                max_snapshots_per_instance=int(
                    opts.get("max_snapshots_per_instance", 10)
                ),
            )
        )

    orch_options: dict[str, Any] = {
        "scheduler": scheduler,
        "event_engine": event,
        "context_engine": context_engine,
        "hooks": hooks,
    }
    max_jobs = opts.get("max_concurrent_jobs")
    if isinstance(max_jobs, int) and max_jobs > 0:
        orch_options["max_concurrent_jobs"] = max_jobs
    shell.orchestration.initialize(**orch_options)

    state = opts.get("state")
    bt_state: BaseState = state if isinstance(state, BaseState) else BlackboardState()
    shell.behavior_tree.initialize(state=bt_state)

    if not shell.instance_manager.is_initialized:
        shell.instance_manager.initialize(
            max_loaded_instances=opts.get("max_loaded_instances"),
            max_concurrent_active=opts.get("max_concurrent_active"),
            max_snapshots_per_instance=opts.get("max_snapshots_per_instance"),
            reconcile_on_startup=opts.get("reconcile_on_startup"),
        )

    return {
        "orchestration": shell.orchestration,
        "instance_manager": shell.instance_manager,
    }


__all__ = ["install_orchestration_hooks"]
