"""
Default system plane definitions (composition membership).

**Law:** this catalog only **names which** definitions join a default system.
Each plane's **install law** lives on its definition module (edge), not here
and not open-coded on :class:`~palm.system.planes.hub.SystemPlanes`.

To add a plane: write ``planes/<name>/definition.py`` with a
:class:`~palm.system.planes.definition.PlaneDefinition`, then register it
here (or pass custom definitions into the hub).
"""

from __future__ import annotations

from palm.system.planes.definition import PlaneDefinition
from palm.system.planes.session.definition import SESSION_PLANE
from palm.system.planes.wait.definition import WAIT_PLANE
from palm.system.planes.work.definition import WORK_PLANE

# Install order is PlaneDefinition.order (wait → session → work).
DEFAULT_PLANE_DEFINITIONS: tuple[PlaneDefinition, ...] = (
    WAIT_PLANE,
    SESSION_PLANE,
    WORK_PLANE,
)


def default_plane_definitions() -> tuple[PlaneDefinition, ...]:
    """Default reactive planes for a system instance."""
    return DEFAULT_PLANE_DEFINITIONS


def definition_by_name(
    name: str,
    definitions: tuple[PlaneDefinition, ...] | list[PlaneDefinition] | None = None,
) -> PlaneDefinition | None:
    """Lookup by canonical name or alias."""
    defs = definitions if definitions is not None else DEFAULT_PLANE_DEFINITIONS
    key = str(name or "").strip()
    if not key:
        return None
    for d in defs:
        if d.name == key or key in d.aliases:
            return d
    return None


__all__ = [
    "DEFAULT_PLANE_DEFINITIONS",
    "default_plane_definitions",
    "definition_by_name",
]
