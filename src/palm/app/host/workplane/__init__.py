"""
Host work plane packaging — coordinator + inbound re-export.

Start law lives on system ``runtime.work_plane`` (:class:`~palm.system.subsystems.planes.work.plane.WorkPlaneService`).
The host coordinator rebinds product submit / drain able / ready admission_able
/ catalog; it does not own a second drain implementation.
"""

from __future__ import annotations

from palm.app.host.workplane.coordinator import WorkPlaneCoordinator
from palm.app.host.workplane.inbound_service import InboundBinding, InboundBindingService
from palm.app.host.workplane.start_ports import product_start_ports

__all__ = [
    "InboundBinding",
    "InboundBindingService",
    "WorkPlaneCoordinator",
    "product_start_ports",
]
