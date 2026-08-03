"""
System start phase: wire supervisor subsystem (system.supervisor.wire).

Subject: :class:`~palm.system.subsystems.supervisor.SystemSupervisor`.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.log import get_system_log
from palm.system.subsystems.supervisor.supervisor import SystemSupervisor


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    shell = resolve_shell(ctx)
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


DEFINITION = PhaseDefinition(
    id="system.supervisor.wire",
    run=run,
    description="SystemSupervisor seat — continuous services registry",
)

__all__ = ["DEFINITION", "run"]
