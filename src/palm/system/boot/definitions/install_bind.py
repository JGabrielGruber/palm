"""Phase: system.install.bind."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.log import get_system_log


def run(ctx: BootContext, _options: Mapping[str, Any]) -> None:
    shell = resolve_shell(ctx)
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


DEFINITION = PhaseDefinition(
    id="system.install.bind",
    run=run,
    description="Bind InstallInterface collaborator ports (peer of execution)",
)
