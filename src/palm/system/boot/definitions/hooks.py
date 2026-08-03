"""Phase: system.hooks.install."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.assembly import install_orchestration_hooks
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    shell = resolve_shell(ctx)
    seats = install_orchestration_hooks(
        shell,
        event=ctx.event if ctx.event is not None else shell.event,
        context_engine=(
            ctx.context_engine if ctx.context_engine is not None else shell.context
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


DEFINITION = PhaseDefinition(
    id="system.hooks.install",
    run=run,
    description="Job hooks + orch/BT/instance_manager initialize",
)
