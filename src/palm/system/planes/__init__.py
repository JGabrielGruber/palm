"""System planes — start (work), continue (wait), session, workload glue.

:class:`SystemPlanes` is the living seat that consumes individual planes
(parallel to :class:`~palm.system.supervisor.SystemSupervisor`).
Install policy (construct · wire · put) lives on the hub; boot only says when.
"""

from palm.system.planes.hub import SystemPlanes, get_system_planes

__all__ = [
    "SystemPlanes",
    "get_system_planes",
]
