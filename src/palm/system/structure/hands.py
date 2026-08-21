"""Local capability hands — explicit table, not a private menu.

The manager walks this map. A new organ is a name + a hand here.
Hands import their organs. Hands take seats, not a shell bag.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from palm.common.compensation.wire import wire_install_compensation
from palm.common.cqrs.projections.wire import wire_install_projections
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


def _drop_projections(install: Any) -> None:
    if install is None:
        return
    bag = getattr(install, "projections", None)
    manager = getattr(bag, "manager", None) if bag is not None else None
    if manager is not None:
        shutdown = getattr(manager, "shutdown", None)
        if callable(shutdown):
            shutdown()
    bind = getattr(install, "bind", None)
    if callable(bind):
        bind(projections=None)


def apply_projections(seats: CapabilitySeats, *, listed: bool) -> None:
    """Attach core projections when listed; drop them otherwise. Attach, not a loop."""
    install = seats.install
    if not listed:
        _drop_projections(install)
        return
    if install is None or getattr(install, "projections", None) is not None:
        return
    storage = seats.storage
    event = seats.event
    instance_manager = getattr(install, "instance_manager", None)
    if storage is None or instance_manager is None or event is None:
        return
    install.bind(projections=wire_install_projections(storage, instance_manager, event))


def _drop_compensation(install: Any) -> None:
    if install is None:
        return
    bag = getattr(install, "compensation", None)
    if bag is not None:
        shutdown = getattr(bag, "shutdown", None)
        if callable(shutdown):
            shutdown()
    bind = getattr(install, "bind", None)
    if callable(bind):
        bind(compensation=None)


def apply_compensation(seats: CapabilitySeats, *, listed: bool) -> None:
    """Attach compensation when listed; drop it otherwise. Attach, not a loop."""
    install = seats.install
    if not listed:
        _drop_compensation(install)
        return
    if install is None or getattr(install, "compensation", None) is not None:
        return
    event = seats.event
    if event is None:
        return
    install.bind(compensation=wire_install_compensation(event))


LOCAL_CAPABILITY_HANDS: dict[str, CapabilityHand] = {
    "work_drain": apply_work_drain,
    "outbox": apply_outbox,
    "journal": apply_journal,
    "projections": apply_projections,
    "compensation": apply_compensation,
}

__all__ = [
    "CapabilitySeats",
    "LOCAL_CAPABILITY_HANDS",
    "apply_compensation",
    "apply_journal",
    "apply_outbox",
    "apply_projections",
    "apply_work_drain",
]
