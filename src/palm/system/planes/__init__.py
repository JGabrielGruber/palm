"""System planes — start (work), continue (wait), session, workload glue.

Roster (:mod:`palm.system.planes.roster`) is the definition of which planes
a system instance runs. Boot attaches; vitality discovers from the same table.
"""

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
    "get_system_plane",
    "missing_roster_planes",
    "plane_attachment_snapshot",
    "roster_catalog",
    "system_plane_attrs",
    "system_plane_ids",
    "system_plane_seat_ids",
]
