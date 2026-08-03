"""
System schedule handlers — *when* the system instance comes up (0.59.3 / seat DI).

**Ownership:** this module owns order and phase skips only.
Assembly leaves under :mod:`palm.system.boot.assembly` own *how*.
Subsystem install (planes / supervisor) and InstallInterface bind stay thin here.

**Seat DI:** resolve shell via :func:`~palm.system.boot.shell.resolve_shell`;
publish seats onto :class:`~palm.system.boot.context.BootContext` after each step.

Control: ``walk_schedule(SYSTEM_PHASES, handlers)``.
Observation: SystemLog only.
"""

from __future__ import annotations

from typing import Any

from palm.common.plugins import ensure_core_plugins
from palm.common.providers._registry import get_runtime_binding
from palm.system.boot.assembly import (
    init_system_engines,
    install_orchestration_hooks,
    select_system_storage,
    start_supervised_background,
    wire_system_outbox,
)
from palm.system.boot.context import BootContext
from palm.system.boot.log_phase import system_log_ready_handler
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip
from palm.system.boot.walker import PhaseHandler
from palm.system.log import get_system_log
from palm.system.subsystems.planes.hub import SystemPlanes
from palm.system.subsystems.supervisor import SystemSupervisor


def build_system_handlers(
    runtime: Any | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, PhaseHandler]:
    """Build the system schedule handler map for one ``start()`` call.

    *runtime* is optional when ``ctx.shell`` is set. Handlers publish seats;
    they do not open-code engine/hook assembly.
    """
    options = dict(options or {})

    def _shell(ctx: BootContext) -> Any:
        return resolve_shell(ctx, fallback=runtime)

    def plugins_ensure(_ctx: BootContext) -> None:
        ensure_core_plugins()

    def engines_init(ctx: BootContext) -> None:
        seats = init_system_engines(_shell(ctx), options)
        ctx.publish(**seats)

    def storage_select(ctx: BootContext) -> None:
        storage = select_system_storage(_shell(ctx), options)
        ctx.publish(storage=storage)

    def outbox_wire(ctx: BootContext) -> None:
        if not bool(options.get("enable_event_outbox", True)):
            raise PhaseSkip("enable_event_outbox_off")
        shell = _shell(ctx)
        event = ctx.event if ctx.event is not None else shell.event
        storage = ctx.storage if ctx.storage is not None else shell.storage
        store, processor = wire_system_outbox(shell, event=event, storage=storage)
        ctx.publish(outbox_store=store, outbox_processor=processor)

    def hooks_install(ctx: BootContext) -> None:
        shell = _shell(ctx)
        seats = install_orchestration_hooks(
            shell,
            event=ctx.event if ctx.event is not None else shell.event,
            context_engine=(
                ctx.context_engine
                if ctx.context_engine is not None
                else shell.context
            ),
            auth=ctx.auth if ctx.auth is not None else shell.auth,
            outbox_store=(
                ctx.outbox_store
                if ctx.outbox_store is not None
                else getattr(shell, "_outbox_store", None)
            ),
            outbox_processor=(
                ctx.outbox_processor
                if ctx.outbox_processor is not None
                else getattr(shell, "_outbox_processor", None)
            ),
            options=options,
        )
        ctx.publish(**seats)

    def orchestration_start(ctx: BootContext) -> None:
        orch = (
            ctx.orchestration
            if ctx.orchestration is not None
            else _shell(ctx).orchestration
        )
        orch.start()

    def install_bind(ctx: BootContext) -> None:
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
        shell = _shell(ctx)
        sup = ctx.supervisor if ctx.supervisor is not None else shell.supervisor
        if sup is None:
            raise PhaseSkip("no_supervisor")
        result = start_supervised_background(sup, options)
        if result.should_skip:
            raise PhaseSkip(result.skip_reason or "background_skip")
        get_system_log().info(
            "supervisor.background.start",
            "supervised background started"
            if result.started
            else "supervised services already running or idle",
            schedule="system",
            runtime=ctx.runtime,
            services=",".join(result.started) or "(none)",
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
