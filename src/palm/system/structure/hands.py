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
from palm.system.subsystems.supervisor.service import CallableSystemService


@dataclass(frozen=True, slots=True)
class CapabilitySeats:
    """Seats a local capability hand may use. Built once at the walker edge."""

    supervisor: Any = None
    work_plane: Any = None
    outbox_store: Any = None
    outbox_processor: Any = None
    event: Any = None
    storage: Any = None


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


def apply_journal(seats: CapabilitySeats, *, listed: bool) -> None:
    """Attach event journal when listed; drop it otherwise. Attach, not a loop."""
    supervisor = seats.supervisor
    if not listed:
        if supervisor is not None:
            existing = supervisor.get("journal")
            if existing is not None:
                existing.stop()
            supervisor.unregister("journal")
        return
    if supervisor is None or supervisor.get("journal") is not None:
        return
    event = seats.event
    storage = seats.storage
    if event is None or storage is None:
        return

    holder: dict[str, Any] = {}

    def start() -> None:
        if holder.get("sub") is not None:
            return
        _journal, sub = wire_event_journal(event, storage)
        holder["journal"] = _journal
        holder["sub"] = sub

    def stop() -> None:
        sub = holder.pop("sub", None)
        if sub is not None:
            sub.unsubscribe()
        holder.pop("journal", None)

    def status() -> dict[str, Any]:
        return {"name": "journal", "attached": holder.get("sub") is not None}

    svc = CallableSystemService(
        "journal",
        start=start,
        stop=stop,
        status=status,
        may_start=lambda _ctx: True,
    )
    supervisor.register(svc)
    svc.start()


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
