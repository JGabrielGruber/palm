"""
System schedule handlers — start law for the system instance (0.59.3 / seat DI).

**Ownership:** ``palm.system.boot`` owns *when* and *in what order* the system
comes up. Handlers here are the rules. Collaborators (hooks, storage factory,
planes) are tools the schedule *uses* — they do not own boot order.

**Seat DI:** handlers resolve the shell from ``ctx.shell`` and publish engine /
interface / subsystem seats onto :class:`BootContext` as they become live.
Prefer ``ctx.event`` / ``ctx.install`` / ``ctx.planes`` over digging the shell
when a seat is already published.

**Break / harvest:** mid-theme Palm may be red on unmigrated phenotypes.
Modes and optional phase skips are the switches. Do not restore import-order
magic to keep a path green. See VISION-0.59 §5 and ADR-028 D8.

**Dependency direction:**

- ``BaseRuntime.start`` → boot walker + these handlers (sets ``ctx.shell``)
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
from palm.system.subsystems.planes.hub import SystemPlanes
from palm.system.subsystems.planes.workload.bootstrap import initialize_workload_engine
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
from palm.system.subsystems.supervisor import SystemSupervisor


def build_system_handlers(
    runtime: Any | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, PhaseHandler]:
    """Build the full system schedule handler map for one ``start()`` call.

    *runtime* is optional when ``ctx.shell`` is already set (preferred).
    Kept as a fallback so older call sites that only pass the shell still work.
    Handlers must not close over engine fields — they read seats from *ctx*.
    """
    options = dict(options or {})

    def _shell(ctx: BootContext) -> Any:
        if ctx.shell is not None:
            return ctx.shell
        if runtime is not None:
            ctx.shell = runtime
            return runtime
        return ctx.require_shell()

    def plugins_ensure(_ctx: BootContext) -> None:
        ensure_core_plugins()

    def engines_init(ctx: BootContext) -> None:
        shell = _shell(ctx)
        shell.context.initialize()
        shell.event.initialize()
        cache_options = options.get("resource_cache")
        resource_options: dict[str, Any] = {
            "event_engine": shell.event,
            "definition_resolver": resource_definition_resolver(shell.repository),
        }
        if cache_options is not None:
            resource_options["resource_cache"] = cache_options
        shell.resource.initialize(**resource_options)

        def _publish_workload(event_type: str, payload: dict[str, Any]) -> None:
            shell.event.emit(event_type, **payload)

        initialize_workload_engine(
            shell.workload,
            host_enabled=bool(options.get("workload_host_enabled", False)),
            work_root=options.get("workload_work_root") or options.get("data_dir"),
            default_runtime=options.get("workload_default_runtime"),
            publish_event=_publish_workload,
        )

        shell.auth.initialize()
        authenticate_runtime(shell.auth, options.get("credentials"))

        ctx.publish(
            context_engine=shell.context,
            event=shell.event,
            resource=shell.resource,
            workload=shell.workload,
            auth=shell.auth,
        )

    def storage_select(ctx: BootContext) -> None:
        shell = _shell(ctx)
        if not shell.storage.is_initialized:
            StorageFactory.initialize_engine(
                shell.storage,
                storage_backend=str(options.get("storage_backend", "memory")),
                **dict(options.get("backend_options") or {}),
            )
        ctx.publish(storage=shell.storage)

    def outbox_wire(ctx: BootContext) -> None:
        if not bool(options.get("enable_event_outbox", True)):
            raise PhaseSkip("enable_event_outbox_off")
        shell = _shell(ctx)
        event = ctx.event if ctx.event is not None else shell.event
        storage = ctx.storage if ctx.storage is not None else shell.storage
        shell._outbox_store = OutboxStore(storage)
        wire_reliable_events(event, shell._outbox_store)
        shell._outbox_processor = OutboxProcessor(shell._outbox_store, event)
        ctx.publish(
            outbox_store=shell._outbox_store,
            outbox_processor=shell._outbox_processor,
        )

    def hooks_install(ctx: BootContext) -> None:
        shell = _shell(ctx)
        event = ctx.event if ctx.event is not None else shell.event
        context_engine = (
            ctx.context_engine if ctx.context_engine is not None else shell.context
        )
        auth = ctx.auth if ctx.auth is not None else shell.auth
        outbox_store = (
            ctx.outbox_store
            if ctx.outbox_store is not None
            else getattr(shell, "_outbox_store", None)
        )
        outbox_processor = (
            ctx.outbox_processor
            if ctx.outbox_processor is not None
            else getattr(shell, "_outbox_processor", None)
        )

        scheduler = resolve_scheduler(
            options,
            default_policy=shell.default_scheduler_policy,
        )
        hooks = list(options.get("hooks") or [])
        if options.get("observability"):
            hooks.append(DriveObservabilityHook())
        shell._auth_enforce = bool(options.get("auth_enforce"))
        if shell._auth_enforce:
            hooks.append(
                AuthMiddleware(
                    auth,
                    required_roles=tuple(options.get("auth_roles") or ("user",)),
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
        session_ownership = SessionOwnershipHook(
            get_plane=lambda: shell.session_plane
        )
        hooks.append(session_ownership)
        if outbox_processor is not None:
            hooks.append(OutboxDrainHook(outbox_processor))
        if options.get("enable_state_snapshot"):
            hooks.append(
                StateSnapshotHook(
                    shell.instance_manager,
                    snapshot_on_status=options.get("snapshot_on_status"),
                    max_snapshots_per_instance=int(
                        options.get("max_snapshots_per_instance", 10)
                    ),
                )
            )

        orch_options: dict[str, Any] = {
            "scheduler": scheduler,
            "event_engine": event,
            "context_engine": context_engine,
            "hooks": hooks,
        }
        max_jobs = options.get("max_concurrent_jobs")
        if isinstance(max_jobs, int) and max_jobs > 0:
            orch_options["max_concurrent_jobs"] = max_jobs
        shell.orchestration.initialize(**orch_options)

        state = options.get("state")
        bt_state: BaseState = (
            state if isinstance(state, BaseState) else BlackboardState()
        )
        shell.behavior_tree.initialize(state=bt_state)

        if not shell.instance_manager.is_initialized:
            shell.instance_manager.initialize(
                max_loaded_instances=options.get("max_loaded_instances"),
                max_concurrent_active=options.get("max_concurrent_active"),
                max_snapshots_per_instance=options.get("max_snapshots_per_instance"),
                reconcile_on_startup=options.get("reconcile_on_startup"),
            )

        ctx.publish(
            orchestration=shell.orchestration,
            instance_manager=shell.instance_manager,
        )

    def orchestration_start(ctx: BootContext) -> None:
        orch = (
            ctx.orchestration
            if ctx.orchestration is not None
            else _shell(ctx).orchestration
        )
        orch.start()

    def install_bind(ctx: BootContext) -> None:
        """Bind InstallInterface; publish on *ctx.install*."""
        shell = _shell(ctx)
        board = shell.bind_system_install()
        ctx.publish(install=board)
        bound = [k for k, v in board.status().items() if v]
        get_system_log().info(
            "install.bound",
            "system install interface ready",
            schedule="system",
            runtime=ctx.runtime,
            ports=",".join(bound) or "(none)",
        )

    def planes_attach(ctx: BootContext) -> None:
        """
        Seat planes subsystem; install members from *ctx.install*.

        Schedule owns *when*. Subsystem walks definitions; install interface
        owns collaborators.
        """
        slog = get_system_log()
        shell = _shell(ctx)
        board = ctx.install
        if board is None:
            board = shell.bind_system_install()
            ctx.publish(install=board)

        def _on_host_session_error(exc: BaseException) -> None:
            # BI-014 — still swallowed; honesty later.
            slog.system(
                "plane.session.host_session",
                f"ensure_host_session swallowed: {type(exc).__name__}",
                runtime=ctx.runtime,
                reason=str(exc),
            )

        planes = SystemPlanes.ensure_on(shell)
        planes.install(
            board,
            options,
            on_host_session_error=_on_host_session_error,
        )
        # Re-bind install so work_plane is visible to supervisor continuous install.
        board = shell.bind_system_install()
        ctx.publish(planes=planes, install=board)
        slog.info(
            "plane.hub.attached",
            "system planes subsystem ready",
            schedule="system",
            runtime=ctx.runtime,
            planes=",".join(planes.names()) or "(none)",
        )

    def supervisor_wire(ctx: BootContext) -> None:
        """Seat supervisor; walk continuous definitions from *ctx.install*."""
        shell = _shell(ctx)
        board = ctx.install if ctx.install is not None else shell.install
        ctx.publish(install=board)
        sup = SystemSupervisor.ensure_on(shell)
        sup.install(board, options)
        ctx.publish(supervisor=sup)
        get_system_log().info(
            "supervisor.wire",
            "system supervisor ready",
            schedule="system",
            runtime=ctx.runtime,
            service_count=len(sup.names()),
            services=",".join(sup.names()) or "(none)",
        )

    def bind(ctx: BootContext) -> None:
        shell = _shell(ctx)
        bind_runtime = get_runtime_binding()
        if bind_runtime is None:
            raise PhaseSkip("no_runtime_binding")
        bind_runtime(shell)

    def ready(ctx: BootContext) -> None:
        shell = _shell(ctx)
        shell._started = True
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
        shell = _shell(ctx)
        sup = ctx.supervisor if ctx.supervisor is not None else shell.supervisor
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
        "system.install.bind": install_bind,
        "system.planes.attach": planes_attach,
        "system.supervisor.wire": supervisor_wire,
        "system.bind": bind,
        "system.ready": ready,
        "system.background.start": background_start,
    }


__all__ = ["build_system_handlers"]
