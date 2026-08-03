"""
Palm system boot — schedule control for how the system comes up (0.59–0.61).

**What boot owns**

- Phase **order** tables (host + system) — *when*
- Walker (order, skip/fail, SystemLog observation)
- Thin **catalog** — membership imports of subject phase definitions
- Schedule bind (``system_schedule``) — catalog → walker handlers
- BootContext — seat bag for one start walk

**What boot does not own**

- Phase **how** — co-located on the subject (interfaces, subsystems, runtime, log)
- Domain reaction, product services, surfaces
- Host schedule bodies (``palm.app.host.boot``)

**Law**

New system start step = subject ``phase_*.py`` + catalog entry + PhaseSpec row.
Do not open-code phase bodies under ``boot/``.

Observation: ``palm.system.log``. Map: docs/VISION-0.59.md · ADR-028 · SD-016.
"""

from __future__ import annotations

from palm.system.boot.catalog import (
    DEFAULT_SYSTEM_PHASE_DEFINITIONS,
    system_phase_definition,
    system_phase_definitions,
)
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.phases import (
    HOST_PHASES,
    SYSTEM_PHASES,
    PhaseSeat,
    PhaseSpec,
    ScheduleName,
    get_phase,
    host_phase_ids,
    phases_for,
    schedule_catalog,
    system_phase_ids,
)
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip
from palm.system.boot.system_schedule import bind_phase_handlers, build_system_handlers
from palm.system.boot.walker import PhaseHandler, WalkedPhase, walk_schedule

__all__ = [
    "DEFAULT_SYSTEM_PHASE_DEFINITIONS",
    "HOST_PHASES",
    "SYSTEM_PHASES",
    "BootContext",
    "PhaseDefinition",
    "PhaseHandler",
    "PhaseSeat",
    "PhaseSkip",
    "PhaseSpec",
    "ScheduleName",
    "WalkedPhase",
    "bind_phase_handlers",
    "build_system_handlers",
    "get_phase",
    "host_phase_ids",
    "phases_for",
    "resolve_shell",
    "schedule_catalog",
    "system_phase_definition",
    "system_phase_definitions",
    "system_phase_ids",
    "walk_schedule",
]
