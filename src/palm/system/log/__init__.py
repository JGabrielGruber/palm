"""
System log — ordered narrative of Palm system life (0.59.1a).

Observation only. Not the domain event bus. Not the domain EventJournal.
See docs/SYSTEM-LOG.md.
"""

from __future__ import annotations

from palm.system.log.phase_ready import (
    ensure_system_log_ready,
    system_log_ready_handler,
)
from palm.system.log.system_log import (
    LEVEL_DETAIL,
    LEVEL_LIFECYCLE,
    LEVEL_OPERATE,
    LEVEL_QUIET,
    LEVEL_SYSTEM,
    LEVEL_TRACE,
    SystemLog,
    SystemLogRecord,
    configure_system_log,
    get_system_log,
    reset_system_log_for_tests,
)

__all__ = [
    "LEVEL_DETAIL",
    "LEVEL_LIFECYCLE",
    "LEVEL_OPERATE",
    "LEVEL_QUIET",
    "LEVEL_SYSTEM",
    "LEVEL_TRACE",
    "SystemLog",
    "SystemLogRecord",
    "configure_system_log",
    "ensure_system_log_ready",
    "get_system_log",
    "reset_system_log_for_tests",
    "system_log_ready_handler",
]
