"""
Host work plane packaging — coordinator + inbound re-export.

Start law lives on system ``runtime.work_plane`` (:class:`~palm.system.subsystems.planes.work.plane.WorkPlaneService`).
The host coordinator rebinds product submit / able / catalog; it does not own a
second drain implementation.
"""

from __future__ import annotations

from palm.app.host.workplane.coordinator import WorkPlaneCoordinator
from palm.app.host.workplane.inbound_service import InboundBinding, InboundBindingService

__all__ = [
    "InboundBinding",
    "InboundBindingService",
    "WorkPlaneCoordinator",
]
