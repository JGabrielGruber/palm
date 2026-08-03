"""
PlaneDefinition — participation law at the edge (0.61 / SD-015).

**Registry extension:** each plane package owns construct + attach recipe.
:class:`~palm.system.planes.hub.SystemPlanes` walks definitions and ``put``s.

Install ports come from :class:`~palm.system.planes.install_context.InstallContext`
(built from :class:`~palm.system.ports.install.InstallInterface`). This module
does **not** import wait/session/work services or dig a runtime bag.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from palm.system.planes.install_context import InstallContext

if TYPE_CHECKING:
    from palm.system.planes.hub import SystemPlanes


# install(hub, ctx) -> plane instance (already put on hub)
PlaneInstallFn = Callable[["SystemPlanes", InstallContext], object]


@dataclass(frozen=True)
class PlaneDefinition:
    """
    How one plane becomes a hub member.

    * ``name`` — canonical membership key (``wait``, ``session``, ``work``)
    * ``aliases`` — attr / seat ids (``wait_plane``, …)
    * ``order`` — lower installs first
    * ``install`` — construct, wire from *ctx*, ``hub.put``; return plane
    """

    name: str
    aliases: tuple[str, ...]
    order: int
    install: PlaneInstallFn
    after: tuple[str, ...] = ()

    def seat_id(self) -> str:
        for a in self.aliases:
            if a.endswith("_plane"):
                return a
        return f"{self.name}_plane"


__all__ = [
    "InstallContext",
    "PlaneDefinition",
    "PlaneInstallFn",
]
