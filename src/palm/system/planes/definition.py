"""
PlaneDefinition — participation law at the edge (0.61 / SD-015).

**Registry extension:** each plane package owns how it is constructed and
wired. :class:`~palm.system.planes.hub.SystemPlanes` only holds definitions,
orders install, and consumes the resulting instance (``put``).

Do not teach the hub open-coded wait/session/work install prose.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from palm.system.planes.hub import SystemPlanes


@dataclass
class InstallContext:
    """Shared knobs for one hub :meth:`~SystemPlanes.install` pass."""

    options: Mapping[str, Any] = field(default_factory=dict)
    on_host_session_error: Callable[[BaseException], None] | None = None
    reuse_existing: bool = True


# install(hub, runtime, ctx) -> plane instance (already put on hub)
PlaneInstallFn = Callable[["SystemPlanes", Any, InstallContext], Any]


@dataclass(frozen=True)
class PlaneDefinition:
    """
    How one plane becomes a hub member.

    * ``name`` — canonical membership key (``wait``, ``session``, ``work``)
    * ``aliases`` — attr / seat ids (``wait_plane``, …)
    * ``order`` — lower installs first (deps: wait before session before work)
    * ``install`` — construct, wire collaborators, ``hub.put``; return plane
    """

    name: str
    aliases: tuple[str, ...]
    order: int
    install: PlaneInstallFn
    after: tuple[str, ...] = ()
    """Soft dep names for docs / future graph; install order uses ``order``."""

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
