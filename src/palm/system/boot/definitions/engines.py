"""Phase: system.engines.init."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.assembly import init_system_engines
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    seats = init_system_engines(resolve_shell(ctx), options)
    ctx.publish(**seats)


DEFINITION = PhaseDefinition(
    id="system.engines.init",
    run=run,
    description="context, event, resource, workload, auth",
)
