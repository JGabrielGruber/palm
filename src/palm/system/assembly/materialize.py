"""Local membership materialize — walker over the hands table.

The structure definition names units. This module does not import organs. It looks up
``LOCAL_CAPABILITY_HANDS`` and applies each hand.
"""

from __future__ import annotations

from palm.core.assembly import CAPABILITY_WORK_DRAIN, AssemblyDefinition
from palm.system.assembly.hands import LOCAL_CAPABILITY_HANDS, CapabilitySeats


def definition_lists_work_drain(definition: AssemblyDefinition | None) -> bool:
    """True when the definition names work_drain as an install capability."""
    if definition is None:
        return False
    return definition.has_capability(CAPABILITY_WORK_DRAIN)


def apply_local_capabilities(
    definition: AssemblyDefinition | None,
    seats: CapabilitySeats,
) -> frozenset[str]:
    """Apply every registered hand. Listed → install; else drop.

    New organ: add a hand to ``LOCAL_CAPABILITY_HANDS``. Do not add an ``if`` here.
    """
    wanted = frozenset(definition.capabilities) if definition is not None else frozenset()
    applied: set[str] = set()
    for name, hand in LOCAL_CAPABILITY_HANDS.items():
        listed = name in wanted
        hand(seats, listed=listed)
        if listed:
            applied.add(name)
    return frozenset(applied)


__all__ = [
    "apply_local_capabilities",
    "definition_lists_work_drain",
]
