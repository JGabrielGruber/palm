"""
System schedule handlers — start law for the system instance (0.59.3).

**Ownership:** ``palm.system.boot`` owns *when* and *in what order* the system
comes up. Handlers here are the rules. Collaborators (hooks, storage factory,
planes) are tools the schedule *uses* — they do not own boot order.

**Break / harvest:** mid-theme Palm may be red on unmigrated phenotypes.
Modes and optional phase skips are the switches. Do not restore import-order
magic to keep a path green. See VISION-0.59 §5 and ADR-028 D8.

**Dependency direction:**

- ``BaseRuntime.start`` → boot walker + these handlers
- handlers → hooks / job_hooks / wiring / planes (leaf collaborators)
- collaborators must **not** import ``BaseRuntime`` or re-enter boot tables

Control: ``walk_schedule(SYSTEM_PHASES, handlers)``.
Observation: SystemLog only (handlers do not wrap ``slog.phase`` themselves).
"""

from __future__ import annotations

from typing import Any

from palm.common.events import OutboxProcessor, OutboxStore, wire_reliable_events
from palm.common.plugins import ensure_core_plugins
from palm.common.providers._registry import get_runtime_binding
from palm.common.resource import resource_definition_resolver
from palm.common.storage import StorageFactory
from palm.core.context import BaseState
from palm.states import BlackboardState
from palm.system.boot.context import BootContext
from palm.system.boot.log_phase import system_log_ready_handler
from palm.system.boot.skip import PhaseSkip
from palm.system.boot.walker import PhaseHandler
from palm.system.log import get_system_log
from palm.system.planes.roster import SYSTEM_PLANES, missing_roster_planes
from palm.system.planes.session.plane import SessionPlaneService
from palm.system.planes.wait.plane import WaitPlaneService
from palm.system.planes.work.plane import WorkPlaneService
from palm.system.planes.workload.bootstrap import initialize_workload_engine
from palm.system.runtime.hooks import (
    AuthMiddleware,
    DriveObservabilityHook,
    JobExecutionContextHook,
    authenticate_runtime,
)
from palm.system.runtime.job_hooks import (
    InstancePersistenceHook,
    OutboxDrainHook,
    SessionOwnershipHook,
    StateSnapshotHook,
)
from palm.system.runtime.wiring import resolve_scheduler
from palm.system.supervisor import (
    CallableSystemService,
    OutboxLoopService,
    SystemSupervisor,
)


def build_system_handlers(
    runtime: Any,
    options: dict[str, Any],
) -> dict[str, PhaseHandler]:
    """Build the full system schedule handler map for one ``start()`` call.

    ``runtime`` is the system instance shell (today ``BaseRuntime``). Boot
    treats it as a bag of engines/planes to assemble — not as the schedule owner.
    """

    def plugins_ensure(_ctx: BootContext) -> None:
        ensure_core_plugins()

    def engines_init(_ctx: BootContext) -> None:
        runtime.context.initialize()
        runtime.event.initialize()
        cache_options = options.get("resource_cache")
        resource_options: dict[str, Any] = {
            "event_engine": runtime.event,
            "definition_resolver": resource_definition_resolver(runtime.repository),
        }
        if cache_options is not None:
            resource_options["resource_cache"] = cache_options
        runtime.resource.initialize(**resource_options)

        def _publish_workload(event_type: str, payload: dict[str, Any]) -> None:
            runtime.event.emit(event_type, **payload)

        initialize_workload_engine(
            runtime.workload,
            host_enabled=bool(options.get("workload_host_enabled", False)),
            work_root=options.get("workload_work_root") or options.get("data_dir"),
            default_runtime=options.get("workload_default_runtime"),
            publish_event=_publish_workload,
        )

        runtime.auth.initialize()
        authenticate_runtime(runtime.auth, options.get("credentials"))

    def storage_select(_ctx: BootContext) -> None:
        if runtime.storage.is_initialized:
            return
        StorageFactory.initialize_engine(
            runtime.storage,
            storage_backend=str(options.get("storage_backend", "memory")),
            **dict(options.get("backend_options") or {}),
        )

    def outbox_wire(_ctx: BootContext) -> None:
        if not bool(options.get("enable_event_outbox", True)):
            raise PhaseSkip("enable_event_outbox_off")
        runtime._outbox_store = OutboxStore(runtime.storage)
        wire_reliable_events(runtime.event, runtime._outbox_store)
        runtime._outbox_processor = OutboxProcessor(
            runtime._outbox_store, runtime.event
        )

    def hooks_install(_ctx: BootContext) -> None:
        scheduler = resolve_scheduler(
            options,
            default_policy=runtime.default_scheduler_policy,
        )
        hooks = list(options.get("hooks") or [])
        if options.get("observability"):
            hooks.append(DriveObservabilityHook())
        runtime._auth_enforce = bool(options.get("auth_enforce"))
        if runtime._auth_enforce:
            hooks.append(
                AuthMiddleware(
                    runtime.auth,
                    required_roles=tuple(options.get("auth_roles") or ("user",)),
                )
            )
        hooks.append(JobExecutionContextHook())
        hooks.append(
            InstancePersistenceHook(
                runtime.instance_manager,
                outbox_store=runtime._outbox_store,
            )
        )
        session_ownership = SessionOwnershipHook(
            get_plane=lambda: runtime._session_plane
        )
        hooks.append(session_ownership)
        if runtime._outbox_processor is not None:
            hooks.append(OutboxDrainHook(runtime._outbox_processor))
        if options.get("enable_state_snapshot"):
            hooks.append(
                StateSnapshotHook(
                    runtime.instance_manager,
                    snapshot_on_status=options.get("snapshot_on_status"),
                    max_snapshots_per_instance=int(
                        options.get("max_snapshots_per_instance", 10)
                    ),
                )
            )

        orch_options: dict[str, Any] = {
            "scheduler": scheduler,
            "event_engine": runtime.event,
            "context_engine": runtime.context,
            "hooks": hooks,
        }
        max_jobs = options.get("max_concurrent_jobs")
        if isinstance(max_jobs, int) and max_jobs > 0:
            orch_options["max_concurrent_jobs"] = max_jobs
        runtime.orchestration.initialize(**orch_options)

        state = options.get("state")
        bt_state: BaseState = (
            state if isinstance(state, BaseState) else BlackboardState()
        )
        runtime.behavior_tree.initialize(state=bt_state)

        if not runtime.instance_manager.is_initialized:
            runtime.instance_manager.initialize(
                max_loaded_instances=options.get("max_loaded_instances"),
                max_concurrent_active=options.get("max_concurrent_active"),
                max_snapshots_per_instance=options.get("max_snapshots_per_instance"),
                reconcile_on_startup=options.get("reconcile_on_startup"),
            )

    def orchestration_start(_ctx: BootContext) -> None:
        runtime.orchestration.start()

    def planes_attach(ctx: BootContext) -> None:
        """
        Attach system planes listed in :data:`~palm.system.planes.roster.SYSTEM_PLANES`.

        Roster is the definition of **what** runs. This handler is the **how**
        (constructors differ). Vitality discovers from the same roster.
        """
        slog = get_system_log()
        # Roster order: wait → session → work (SYSTEM_PLANES).
        assert [p.plane_id for p in SYSTEM_PLANES] == [
            "wait",
            "session",
            "work",
        ], "planes_attach out of sync with SYSTEM_PLANES roster"

        runtime._wait_plane = WaitPlaneService()
        runtime._wait_plane.attach(runtime)

        runtime._session_plane = SessionPlaneService(storage=runtime.storage)
        runtime._session_plane.attach(runtime)
        try:
            runtime._session_plane.ensure_host_session()
        except Exception as exc:
            # BI-014 — still swallowed; honesty later.
            slog.system(
                "plane.session.host_session",
                f"ensure_host_session swallowed: {type(exc).__name__}",
                runtime=ctx.runtime,
                reason=str(exc),
            )

        # 0.60.2 — start plane (enqueue / tick). Continuous drain → supervisor later.
        max_depth = int(options.get("work_drain_max_depth", 8) or 8)
        batch_size = int(options.get("work_drain_batch_size", 10) or 10)
        poll_interval = float(options.get("work_drain_poll_interval", 1.0) or 1.0)
        runtime._work_plane = WorkPlaneService()
        runtime._work_plane.attach(
            runtime,
            max_depth=max_depth,
            batch_size=batch_size,
            poll_interval=poll_interval,
            # able after ready; is_started gates tick.
            able=lambda: bool(getattr(runtime, "is_started", False)),
        )
        missing = missing_roster_planes(runtime)
        if missing:
            slog.system(
                "plane.roster.incomplete",
                f"roster planes missing after attach: {','.join(missing)}",
                schedule="system",
                runtime=ctx.runtime,
                missing=list(missing),
            )
        else:
            slog.info(
                "plane.roster.attached",
                "system planes attached per roster",
                schedule="system",
                runtime=ctx.runtime,
                planes=[p.plane_id for p in SYSTEM_PLANES],
            )

    def supervisor_wire(ctx: BootContext) -> None:
        """Register continuous services (work_drain, outbox) — start later."""
        sup = SystemSupervisor()
        runtime._supervisor = sup
        plane = getattr(runtime, "_work_plane", None) or getattr(
            runtime, "work_plane", None
        )
        if plane is not None:
            sup.register(
                CallableSystemService(
                    "work_drain",
                    start=plane.start_background,
                    stop=plane.stop_background,
                    status=plane.status,
                )
            )
        # 0.60.6 — outbox continuous when processor was wired.
        proc = getattr(runtime, "_outbox_processor", None) or getattr(
            runtime, "outbox_processor", None
        )
        store = getattr(runtime, "_outbox_store", None) or getattr(
            runtime, "outbox_store", None
        )
        if proc is not None and store is not None:
            sup.register(
                OutboxLoopService(
                    proc,
                    store,
                    poll_interval=float(
                        options.get("outbox_poll_interval", 0.5) or 0.5
                    ),
                    batch_size=int(options.get("outbox_batch_size", 50) or 50),
                    recover_on_start=bool(
                        options.get("outbox_recover_on_startup", True)
                    ),
                )
            )
        get_system_log().info(
            "supervisor.wire",
            "system supervisor ready",
            schedule="system",
            runtime=ctx.runtime,
            service_count=len(sup.names()),
            services=",".join(sup.names()) or "(none)",
        )

    def bind(_ctx: BootContext) -> None:
        bind_runtime = get_runtime_binding()
        if bind_runtime is None:
            raise PhaseSkip("no_runtime_binding")
        bind_runtime(runtime)

    def ready(ctx: BootContext) -> None:
        runtime._started = True
        get_system_log().info(
            "ready",
            "system ready",
            schedule="system",
            runtime=ctx.runtime,
            mode=ctx.mode,
        )

    def background_start(ctx: BootContext) -> None:
        """Start supervised continuous services when options allow (0.60.5-6)."""
        if bool(options.get("allow_background_drain", True)) is False:
            raise PhaseSkip("allow_background_drain_off")
        sup = runtime._supervisor
        if sup is None:
            raise PhaseSkip("no_supervisor")

        want_drain = bool(options.get("enable_work_drain_service", False))
        want_outbox = bool(options.get("enable_outbox_background", False))
        if not want_drain and not want_outbox:
            raise PhaseSkip("no_background_services_enabled")

        started: list[str] = []
        if want_drain and sup.get("work_drain") is not None:
            started.extend(sup.start("work_drain"))
        if want_outbox and sup.get("outbox") is not None:
            started.extend(sup.start("outbox"))
        if not started and not (
            (want_drain and sup.get("work_drain") is not None)
            or (want_outbox and sup.get("outbox") is not None)
        ):
            raise PhaseSkip("no_matching_supervised_services")

        get_system_log().info(
            "supervisor.background.start",
            "supervised background started"
            if started
            else "supervised services already running or idle",
            schedule="system",
            runtime=ctx.runtime,
            services=",".join(started) or "(none)",
        )

    return {
        "system.log.ready": system_log_ready_handler,
        "system.plugins.ensure": plugins_ensure,
        "system.engines.init": engines_init,
        "system.storage.select": storage_select,
        "system.outbox.wire": outbox_wire,
        "system.hooks.install": hooks_install,
        "system.orchestration.start": orchestration_start,
        "system.planes.attach": planes_attach,
        "system.supervisor.wire": supervisor_wire,
        "system.bind": bind,
        "system.ready": ready,
        "system.background.start": background_start,
    }


__all__ = ["build_system_handlers"]
