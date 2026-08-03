"""System supervisor — continuous system services for one SystemInstance (0.60).

Planes carry reactive traffic. The supervisor owns **lifecycle** for long-running
loops and worker sets (work drain, outbox poll, inbound workers, …).

Install law lives on continuous **definitions** (CS-006); the supervisor walks them.

See docs/VISION-0.60.md · ADR-029.
"""

from __future__ import annotations

from palm.system.subsystems.supervisor.definition import (
    DEFAULT_CONTINUOUS_DEFINITIONS,
    ContinuousServiceDefinition,
    ContinuousWireContext,
)
from palm.system.subsystems.supervisor.outbox_loop import OutboxLoopService
from palm.system.subsystems.supervisor.service import CallableSystemService, SystemService
from palm.system.subsystems.supervisor.supervisor import SystemSupervisor

__all__ = [
    "CallableSystemService",
    "ContinuousServiceDefinition",
    "ContinuousWireContext",
    "DEFAULT_CONTINUOUS_DEFINITIONS",
    "OutboxLoopService",
    "SystemService",
    "SystemSupervisor",
]
