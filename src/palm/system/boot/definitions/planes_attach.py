"""Phase: system.planes.attach."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.log import get_system_log
from palm.system.subsystems.planes.hub import SystemPlanes


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    slog = get_system_log()
    shell = resolve_shell(ctx)
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


DEFINITION = PhaseDefinition(
    id="system.planes.attach",
    run=run,
    description="SystemPlanes subsystem: put wait, session, work from install",
)
