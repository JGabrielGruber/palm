"""
System phase definition catalog — who participates in system start (0.61).

**Order** lives on :data:`~palm.system.boot.phases.SYSTEM_PHASES`.
**How** lives on each :class:`~palm.system.boot.definition.PhaseDefinition`.

New system start step = new definition module + entry here + PhaseSpec row.
Do not open-code phase bodies in ``system_schedule``.
"""

from __future__ import annotations

from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.definitions import (
    background,
    bind,
    engines,
    hooks,
    install_bind,
    log_ready,
    orchestration_start,
    outbox,
    planes_attach,
    plugins,
    ready,
    storage,
    supervisor_wire,
)

# Membership of the system start catalog (not walk order).
DEFAULT_SYSTEM_PHASE_DEFINITIONS: tuple[PhaseDefinition, ...] = (
    log_ready.DEFINITION,
    plugins.DEFINITION,
    engines.DEFINITION,
    storage.DEFINITION,
    outbox.DEFINITION,
    hooks.DEFINITION,
    orchestration_start.DEFINITION,
    install_bind.DEFINITION,
    planes_attach.DEFINITION,
    supervisor_wire.DEFINITION,
    bind.DEFINITION,
    ready.DEFINITION,
    background.DEFINITION,
)

_BY_ID: dict[str, PhaseDefinition] = {
    d.id: d for d in DEFAULT_SYSTEM_PHASE_DEFINITIONS
}


def system_phase_definition(phase_id: str) -> PhaseDefinition | None:
    return _BY_ID.get(phase_id)


def system_phase_definitions() -> tuple[PhaseDefinition, ...]:
    return DEFAULT_SYSTEM_PHASE_DEFINITIONS


def definitions_for_phases(
    phase_ids: tuple[str, ...] | list[str],
) -> list[PhaseDefinition]:
    """Resolve definitions in *phase_ids* order; skip unknown ids."""
    out: list[PhaseDefinition] = []
    for pid in phase_ids:
        defn = _BY_ID.get(pid)
        if defn is not None:
            out.append(defn)
    return out


__all__ = [
    "DEFAULT_SYSTEM_PHASE_DEFINITIONS",
    "definitions_for_phases",
    "system_phase_definition",
    "system_phase_definitions",
]
