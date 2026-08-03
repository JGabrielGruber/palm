"""
Palm system boot — schedule control for how the system comes up (0.59).

**What boot owns**

- Phase tables (host + system)
- Walker (order, skip/fail, SystemLog observation)
- Phase table (``phases``) — *when* / order
- Phase definitions + catalog — *how* each system phase runs (OCP)
- Assembly leaves (``boot.assembly``) — shared construct helpers
- Schedule bind (``system_schedule``) — catalog → walker handlers
- Later: host phase definitions under app host boot

**What boot does not own**

- Domain reaction (event bus), EventJournal, product services, surfaces
- Hook *implementations* as libraries (persist, auth middleware) — assembly *installs* them

**Break / harvest**

Theme 0.59 rewrites start. Mid-theme breakage on unmigrated paths is expected.
Modes (``BootMode``) and optional ``PhaseSkip`` are the switches. Prefer smaller
honest modes over dual-path soup. Spine regressions fix in-theme.

**Dependency direction**

- Instance shell (``BaseRuntime``) calls boot to start
- Boot handlers may import leaf collaborators (hooks, planes, storage factory)
- Collaborators and ``runtime`` package init must not re-enter ``BaseRuntime`` /
  boot tables (see ``runtime/__init__.py`` lazy façade)

Observation: ``palm.system.log``. Map: docs/VISION-0.59.md · ADR-028.
"""

from __future__ import annotations

from palm.system.boot.catalog import (
    DEFAULT_SYSTEM_PHASE_DEFINITIONS,
    system_phase_definition,
    system_phase_definitions,
)
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.log_phase import ensure_system_log_ready, system_log_ready_handler
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
from palm.system.boot.skip import PhaseSkip
from palm.system.boot.shell import resolve_shell
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
    "ensure_system_log_ready",
    "get_phase",
    "host_phase_ids",
    "phases_for",
    "resolve_shell",
    "schedule_catalog",
    "system_log_ready_handler",
    "system_phase_definition",
    "system_phase_definitions",
    "system_phase_ids",
    "walk_schedule",
]
