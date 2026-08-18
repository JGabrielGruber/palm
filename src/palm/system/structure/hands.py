"""Local capability hands — explicit table, not a private menu.

The manager walks this map. A new organ is a name + a hand here.
Hands import their organs. Hands take seats, not a shell bag.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from palm.system.subsystems.supervisor.definition import (
    ContinuousWireContext,
    register_work_drain,
)


@dataclass(frozen=True, slots=True)
class CapabilitySeats:
    """Seats a local capability hand may use. Built once at the walker edge."""

    supervisor: Any = None
    work_plane: Any = None
    outbox_store: Any = None
    outbox_processor: Any = None


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


LOCAL_CAPABILITY_HANDS: dict[str, CapabilityHand] = {
    "work_drain": apply_work_drain,
}

__all__ = [
    "CapabilitySeats",
    "LOCAL_CAPABILITY_HANDS",
    "apply_work_drain",
]
