"""Local capability hands — explicit table, not a private menu.

The manager walks this map. A new organ is a name + a hand here.
Hands import their organs. Hands take seats, not a shell bag.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from palm.common.events import wire_event_journal
from palm.system.subsystems.supervisor.definition import (
    ContinuousWireContext,
    register_outbox,
    register_work_drain,
)


@dataclass(frozen=True, slots=True)
class CapabilitySeats:
    """Seats a local capability hand may use. Built once at the walker edge."""

    supervisor: Any = None
    work_plane: Any = None
    outbox_store: Any = None
    outbox_processor: Any = None
    event: Any = None
    storage: Any = None
    install: Any = None


CapabilityHand = Callable[..., None]


def apply_work_drain(seats: CapabilitySeats, *, listed: bool) -> None:
    """Register supervisor work_drain when listed; drop it otherwise."""
    supervisor = seats.supervisor
    if not listed:
        if supervisor is not None:
            supervisor.unregister("work_drain")
        return
    if supervisor is None or supervisor.get("work_drain") is not None:
        return
    plane = seats.work_plane
    if plane is None:
        return
    register_work_drain(supervisor, ContinuousWireContext(work_plane=plane))


def apply_outbox(seats: CapabilitySeats, *, listed: bool) -> None:
    """Register supervisor outbox when listed; drop it otherwise."""
    supervisor = seats.supervisor
    if not listed:
        if supervisor is not None:
            supervisor.unregister("outbox")
        return
    if supervisor is None or supervisor.get("outbox") is not None:
        return
    store = seats.outbox_store
    processor = seats.outbox_processor
    if store is None or processor is None:
        return
    register_outbox(
        supervisor,
        ContinuousWireContext(outbox_store=store, outbox_processor=processor),
    )


def _drop_journal(install: Any) -> None:
    if install is None:
        return
    sub = getattr(install, "event_journal_sub", None)
    if sub is not None:
        sub.unsubscribe()
    bind = getattr(install, "bind", None)
    if callable(bind):
        bind(event_journal=None, event_journal_sub=None)


def apply_journal(seats: CapabilitySeats, *, listed: bool) -> None:
    """Attach event journal when listed; drop it otherwise. Attach, not a loop."""
    install = seats.install
    if not listed:
        _drop_journal(install)
        return
    if install is None or getattr(install, "event_journal", None) is not None:
        return
    event = seats.event
    storage = seats.storage
    if event is None or storage is None:
        return
    journal, sub = wire_event_journal(event, storage)
    install.bind(event_journal=journal, event_journal_sub=sub)


LOCAL_CAPABILITY_HANDS: dict[str, CapabilityHand] = {
    "work_drain": apply_work_drain,
    "outbox": apply_outbox,
    "journal": apply_journal,
}

__all__ = [
    "CapabilitySeats",
    "LOCAL_CAPABILITY_HANDS",
    "apply_journal",
    "apply_outbox",
    "apply_work_drain",
]
