"""
System start phase: reliable event outbox (system.outbox.wire).

Subject: shell outbox seats + common events outbox.

**0.63.28:** On the host path, ``enable_event_outbox`` is aligned from
``composition.has("outbox")`` at spawn (settings only seed composition at
resolve). Bare ``BaseRuntime.start(enable_event_outbox=…)`` remains packaging
for tests and non-host shells.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.common.events import OutboxProcessor, OutboxStore, wire_reliable_events
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip


def wire_system_outbox(
    shell: Any,
    *,
    event: Any,
    storage: Any,
) -> tuple[Any, Any]:
    """Attach outbox store + processor on *shell*."""
    store = OutboxStore(storage)
    wire_reliable_events(event, store)
    processor = OutboxProcessor(store, event)
    shell._outbox_store = store
    shell._outbox_processor = processor
    return store, processor


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

__all__ = ["DEFINITION", "run", "wire_system_outbox"]
