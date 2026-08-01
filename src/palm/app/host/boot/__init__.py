"""
Host boot — modes + early host schedule seats (0.59.2).

System phase protocol lives in ``palm.system.boot``.
Host phase *handlers* and mode presets live here (may touch composition).
"""

from __future__ import annotations

from palm.app.host.boot.modes import (
    BootMode,
    BootModeName,
    apply_boot_mode_to_system_log,
    get_boot_mode,
    list_boot_modes,
    resolve_boot_mode,
)
from palm.app.host.boot.system_log_phase import make_host_system_log_handler

__all__ = [
    "BootMode",
    "BootModeName",
    "apply_boot_mode_to_system_log",
    "get_boot_mode",
    "list_boot_modes",
    "make_host_system_log_handler",
    "resolve_boot_mode",
]
