"""Phase: system.ready."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.log import get_system_log


def run(ctx: BootContext, _options: Mapping[str, Any]) -> None:
    shell = resolve_shell(ctx)
    shell._started = True
    get_system_log().info(
        "ready",
        "system ready",
        schedule="system",
        runtime=ctx.runtime,
        mode=ctx.mode,
    )


DEFINITION = PhaseDefinition(
    id="system.ready",
    run=run,
    description="System instance ready mark",
)
