"""Reliable event outbox wire — boot assembly leaf."""

from __future__ import annotations

from typing import Any

from palm.common.events import OutboxProcessor, OutboxStore, wire_reliable_events


def wire_system_outbox(
    shell: Any,
    *,
    event: Any,
    storage: Any,
) -> tuple[Any, Any]:
    """
    Attach outbox store + processor on *shell*.

    Returns ``(outbox_store, outbox_processor)`` for BootContext publish.
    Caller owns the enable/skip policy (schedule phase).
    """
    store = OutboxStore(storage)
    wire_reliable_events(event, store)
    processor = OutboxProcessor(store, event)
    shell._outbox_store = store
    shell._outbox_processor = processor
    return store, processor


__all__ = ["wire_system_outbox"]
