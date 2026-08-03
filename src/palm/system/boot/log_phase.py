"""
Compat re-export — system log ready lives on :mod:`palm.system.log.phase_ready`.
"""

from __future__ import annotations

from palm.system.log.phase_ready import (
    ensure_system_log_ready,
    system_log_ready_handler,
)

__all__ = [
    "ensure_system_log_ready",
    "system_log_ready_handler",
]
