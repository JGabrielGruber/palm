"""
Palm system boot — schedule control for how the system comes up (0.59).

**What boot owns**

- Phase tables (host + system)
- Walker (order, skip/fail, SystemLog observation)
- System start handlers (``system_schedule``) — the *rules* of system start
- Later: host start handlers under app host boot

**What boot does not own**

- Domain reaction (event bus), EventJournal, product services, surfaces
- Hook *implementations* as libraries (persist, auth middleware) — boot *installs* them

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

from palm.system.boot.context import BootContext
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
from palm.system.boot.system_schedule import build_system_handlers
from palm.system.boot.walker import PhaseHandler, WalkedPhase, walk_schedule

__all__ = [
    "HOST_PHASES",
    "SYSTEM_PHASES",
    "BootContext",
    "PhaseHandler",
    "PhaseSeat",
    "PhaseSkip",
    "PhaseSpec",
    "ScheduleName",
    "WalkedPhase",
    "build_system_handlers",
    "ensure_system_log_ready",
    "get_phase",
    "host_phase_ids",
    "phases_for",
    "schedule_catalog",
    "system_log_ready_handler",
    "system_phase_ids",
    "walk_schedule",
]
