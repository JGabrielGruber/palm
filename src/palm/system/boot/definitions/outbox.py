"""Phase: system.outbox.wire."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.assembly import wire_system_outbox
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    if not bool(options.get("enable_event_outbox", True)):
        raise PhaseSkip("enable_event_outbox_off")
    shell = resolve_shell(ctx)
    event = ctx.event if ctx.event is not None else shell.event
    storage = ctx.storage if ctx.storage is not None else shell.storage
    store, processor = wire_system_outbox(shell, event=event, storage=storage)
    ctx.publish(outbox_store=store, outbox_processor=processor)


DEFINITION = PhaseDefinition(
    id="system.outbox.wire",
    run=run,
    description="OutboxStore + reliable events when enabled",
)
