"""
Palm system boot schedule — phase tables + walker (0.59.2).

Control lives here. Observation is ``palm.system.log`` (SystemLog).
System package purity: no product / surfaces imports.
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
from palm.system.boot.walker import PhaseHandler, WalkedPhase, walk_schedule

__all__ = [
    "HOST_PHASES",
    "SYSTEM_PHASES",
    "BootContext",
    "PhaseHandler",
    "PhaseSeat",
    "PhaseSpec",
    "ScheduleName",
    "WalkedPhase",
    "ensure_system_log_ready",
    "get_phase",
    "host_phase_ids",
    "phases_for",
    "schedule_catalog",
    "system_log_ready_handler",
    "system_phase_ids",
    "walk_schedule",
]
