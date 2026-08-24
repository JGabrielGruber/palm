"""
System start phase: reliable event outbox (system.outbox.wire).

Subject: shell outbox seats + common events outbox.

Store wire follows DNA listing (``has_capability("outbox")``). Resolve the
same definition assemble will load. Omit → ``PhaseSkip("capability_off:outbox")``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.common.events import OutboxProcessor, OutboxStore, wire_reliable_events
from palm.core.structure import (
    CAPABILITY_OUTBOX,
    StructureDefinition,
    resolve_builtin_definition,
)
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


def _definition_from_options(options: Mapping[str, Any]) -> StructureDefinition:
    raw = options.get("structure_definition")
    if isinstance(raw, StructureDefinition):
        return raw
    if isinstance(raw, dict):
        return StructureDefinition.from_dict(raw)
    definition_id = str(options.get("structure_definition_id") or "local.embedded")
    version = str(options.get("structure_definition_version") or "1")
    return resolve_builtin_definition(definition_id, version=version)


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    if not _definition_from_options(options).has_capability(CAPABILITY_OUTBOX):
        raise PhaseSkip("capability_off:outbox")
    shell = resolve_shell(ctx)
    event = ctx.event if ctx.event is not None else shell.event
    storage = ctx.storage if ctx.storage is not None else shell.storage
    store, processor = wire_system_outbox(shell, event=event, storage=storage)
    ctx.publish(outbox_store=store, outbox_processor=processor)


DEFINITION = PhaseDefinition(
    id="system.outbox.wire",
    run=run,
    description="OutboxStore + reliable events when DNA lists outbox",
)

__all__ = ["DEFINITION", "run", "wire_system_outbox"]
