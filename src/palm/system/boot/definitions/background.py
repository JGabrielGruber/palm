"""Phase: system.background.start."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.assembly import start_supervised_background
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip
from palm.system.log import get_system_log


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    shell = resolve_shell(ctx)
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


DEFINITION = PhaseDefinition(
    id="system.background.start",
    run=run,
    description="Start supervised continuous services (work_drain, …)",
)
