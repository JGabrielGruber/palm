"""System planes — start (work), continue (wait), session, workload glue.

:class:`SystemPlanes` is the living seat that consumes individual planes
(parallel to :class:`~palm.system.supervisor.SystemSupervisor`).
Install **law** lives on :class:`~palm.system.planes.definition.PlaneDefinition`
at the edge; the hub walks definitions and seats members. Boot only says when.
"""

from palm.system.planes.catalog import DEFAULT_PLANE_DEFINITIONS, default_plane_definitions
from palm.system.planes.definition import (
    InstallContext,
    PlaneDefinition,
    PlaneWireSource,
)
from palm.system.planes.hub import SystemPlanes, get_system_planes

__all__ = [
    "DEFAULT_PLANE_DEFINITIONS",
    "InstallContext",
    "PlaneDefinition",
    "PlaneWireSource",
    "SystemPlanes",
    "default_plane_definitions",
    "get_system_planes",
]
