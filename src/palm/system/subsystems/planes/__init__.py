"""System planes — start (work), continue (wait), session, workload glue.

:class:`SystemPlanes` is the living seat that consumes individual planes
(parallel to :class:`~palm.system.subsystems.supervisor.SystemSupervisor`).
Install **law** lives on :class:`~palm.system.subsystems.planes.definition.PlaneDefinition`
at the edge; the hub walks definitions and seats members. Boot only says when.
"""

from palm.system.subsystems.planes.catalog import DEFAULT_PLANE_DEFINITIONS, default_plane_definitions
from palm.system.subsystems.planes.definition import PlaneDefinition
from palm.system.subsystems.planes.hub import SystemPlanes, get_system_planes
from palm.system.subsystems.planes.install_context import InstallContext

__all__ = [
    "DEFAULT_PLANE_DEFINITIONS",
    "InstallContext",
    "PlaneDefinition",
    "SystemPlanes",
    "default_plane_definitions",
    "get_system_planes",
]
