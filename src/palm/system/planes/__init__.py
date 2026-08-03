"""System planes — start (work), continue (wait), session, workload glue.

Roster (:mod:`palm.system.planes.roster`) is the definition of which planes
a system instance runs. Attach/detach (:mod:`palm.system.planes.attach`) and
vitality discovery all follow that table — not private re-lists.
"""

from palm.system.planes.attach import (
    attach_system_planes,
    detach_system_planes,
    get_attached_plane,
    log_roster_attach_result,
)
from palm.system.planes.roster import (
    SYSTEM_PLANES,
    SystemPlaneSpec,
    get_system_plane,
    missing_roster_planes,
    plane_attachment_snapshot,
    roster_catalog,
    system_plane_attrs,
    system_plane_ids,
    system_plane_seat_ids,
)

__all__ = [
    "SYSTEM_PLANES",
    "SystemPlaneSpec",
    "attach_system_planes",
    "detach_system_planes",
    "get_attached_plane",
    "get_system_plane",
    "log_roster_attach_result",
    "missing_roster_planes",
    "plane_attachment_snapshot",
    "roster_catalog",
    "system_plane_attrs",
    "system_plane_ids",
    "system_plane_seat_ids",
]
