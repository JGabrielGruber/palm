"""Local membership materialize — manager applies definition capabilities.

First unit: ``work_drain``. Register on the supervisor only when DNA lists it.
Host / boot mode / composition do not freelance that membership.
"""

from __future__ import annotations

from typing import Any

from palm.core.assembly import CAPABILITY_WORK_DRAIN, AssemblyDefinition
from palm.system.subsystems.supervisor.definition import (
    ContinuousWireContext,
    register_work_drain,
)


def definition_lists_work_drain(definition: AssemblyDefinition | None) -> bool:
    """True when DNA names work_drain as an install capability."""
    if definition is None:
        return False
    return definition.has_capability(CAPABILITY_WORK_DRAIN)


def apply_local_capabilities(
    definition: AssemblyDefinition | None,
    shell: Any,
) -> frozenset[str]:
    """Install local capabilities listed on *definition*. Returns what was applied.

    ``work_drain``: register on the supervisor when listed; unregister otherwise.
    Other capability names are ignored until they have a materialize hand.
    """
    applied: set[str] = set()
    supervisor = getattr(shell, "supervisor", None)
    if definition_lists_work_drain(definition):
        _ensure_work_drain_registered(shell, supervisor)
        applied.add(CAPABILITY_WORK_DRAIN)
    else:
        _drop_work_drain(supervisor)
    return frozenset(applied)


def _ensure_work_drain_registered(shell: Any, supervisor: Any) -> None:
    if supervisor is None:
        return
    if supervisor.get("work_drain") is not None:
        return
    plane = getattr(shell, "work_plane", None)
    if plane is None:
        return
    register_work_drain(supervisor, ContinuousWireContext(work_plane=plane))


def _drop_work_drain(supervisor: Any) -> None:
    if supervisor is None:
        return
    unregister = getattr(supervisor, "unregister", None)
    if callable(unregister):
        unregister("work_drain")


__all__ = [
    "apply_local_capabilities",
    "definition_lists_work_drain",
]
