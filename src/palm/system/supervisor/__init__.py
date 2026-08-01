"""System supervisor — continuous system services for one SystemInstance (0.60).

Planes carry reactive traffic. The supervisor owns **lifecycle** for long-running
loops and worker sets (work drain, outbox poll, inbound workers, …).

See docs/VISION-0.60.md · ADR-029.
"""

from __future__ import annotations

from palm.system.supervisor.service import CallableSystemService, SystemService
from palm.system.supervisor.supervisor import SystemSupervisor

__all__ = [
    "CallableSystemService",
    "SystemService",
    "SystemSupervisor",
]
