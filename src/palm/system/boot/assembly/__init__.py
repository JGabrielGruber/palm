"""
Boot assembly leaves — *how* system start pieces come up.

The schedule (``system_schedule``) owns *when* and *order*.
These modules own construct/wire policy for each phase body.

Do **not** import the schedule or re-enter phase tables from here.
"""

from __future__ import annotations

from palm.system.boot.assembly.background import start_supervised_background
from palm.system.boot.assembly.engines import init_system_engines
from palm.system.boot.assembly.hooks import install_orchestration_hooks
from palm.system.boot.assembly.outbox import wire_system_outbox
from palm.system.boot.assembly.storage import select_system_storage

__all__ = [
    "init_system_engines",
    "install_orchestration_hooks",
    "select_system_storage",
    "start_supervised_background",
    "wire_system_outbox",
]
