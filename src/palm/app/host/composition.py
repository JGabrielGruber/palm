"""
CompositionProfile — *what* an app is made of (services, surfaces, capabilities).

The composition axis, twin of ``DeploymentProfile`` (the deployment axis, in
``roles.py``). A running app is assembled from one ``CompositionProfile`` and one
``DeploymentProfile``; the two are orthogonal and never merge.

**0.59.5 / 0.64 membership:** this profile seeds product services, surfaces, and
capabilities other than ``work_drain``. ``work_drain`` is not a composition
name — after structure definition load, install is definition ``capabilities``.
Deployment may feed the settings resolver but does not OR at phase time.
See ADR-028 D4, VISION-0.64, and ``composition_profile_from_settings``.

History: skeleton 0.50 · living capabilities 0.51 · boot schedule 0.59.2-.4 ·
membership truth 0.59.5. Design mirrors ``DeploymentProfile``: typed name-tuples +
presets, palm's ``INSTALLED_*`` idiom - not a manifest DSL.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self

ServiceName = Literal[
    "inspect",
    "session",
    "definitions",
    "execution",
    "assist",
    "design",
    "analytics",
]
SurfaceName = Literal["rest", "websocket", "mcp", "explorer", "studio"]
Capability = Literal[
    "outbox",
    "compensation",
    "webhook",
    "journal",
    "analytics",
    "projections",
    "neonroot",  # 0.53.8 — hermetic runners available (provider optional at CLI)
    "workloads",  # 0.56 — WorkloadEngine plane (host OFF by default)
]

#: The full service set the host builds today (pinned to CORE_SERVICE_PROVIDERS by tests).
ALL_SERVICES: tuple[ServiceName, ...] = (
    "inspect",
    "session",
    "definitions",
    "execution",
    "assist",
    "design",
    "analytics",
)
#: Minimal services for an embedded/library shape — no assist/design/analytics chrome.
#: Includes product ``session`` (0.58.12) so core submit paths have the surface door.
CORE_SERVICES: tuple[ServiceName, ...] = (
    "inspect",
    "session",
    "definitions",
    "execution",
)
#: The surfaces the server runtime ships (see runtimes/server/surfaces default_surfaces).
SERVER_SURFACES: tuple[SurfaceName, ...] = ("rest", "websocket", "mcp", "explorer", "studio")
#: Background/optional capabilities on for a full host by default.
DEFAULT_CAPABILITIES: frozenset[Capability] = frozenset(
    {
        "outbox",
        "compensation",
        "journal",
        "analytics",
        "projections",
        "neonroot",
        "workloads",
    }
)


@dataclass(frozen=True)
class CompositionProfile:
    """The declared composition of an app: which services, surfaces, and capabilities."""

    services: tuple[str, ...] = ALL_SERVICES
    surfaces: tuple[str, ...] = ()
    capabilities: frozenset[str] = DEFAULT_CAPABILITIES

    def has(self, capability: str) -> bool:
        """Whether ``capability`` is part of this composition."""
        return capability in self.capabilities

    def exposes(self, surface: str) -> bool:
        """Whether ``surface`` is exposed by this composition."""
        return surface in self.surfaces

    # ── Presets — palm's already-shipped shapes, declared ────────────────────

    @classmethod
    def all_in_one(cls) -> Self:
        """The full host — every service + every surface available, background work on.

        Surfaces are *available*; the server deployment mounts them, other deployments
        (CLI) simply don't run a server. So all_in_one declares the full surface set to
        stay behavior-preserving when server-deployed (the common case)."""
        return cls(
            services=ALL_SERVICES,
            surfaces=SERVER_SURFACES,
            capabilities=DEFAULT_CAPABILITIES,
        )

    @classmethod
    def server(cls) -> Self:
        """The HTTP server shape — every service + all surfaces + webhook dispatch."""
        return cls(
            services=ALL_SERVICES,
            surfaces=SERVER_SURFACES,
            capabilities=DEFAULT_CAPABILITIES | {"webhook"},
        )

    @classmethod
    def embedded(cls) -> Self:
        """Library / embedded (the palmengine-django case) — core services, no surfaces,
        no background services. Just submit / ask."""
        return cls(services=CORE_SERVICES, surfaces=(), capabilities=frozenset())

    @classmethod
    def worker(cls) -> Self:
        """Headless worker/daemon — execution + outbox, no surfaces."""
        return cls(
            services=("execution",),
            surfaces=(),
            capabilities=frozenset({"outbox"}),
        )

    @classmethod
    def cli(cls) -> Self:
        """The CLI/REPL shape — full services, no server surfaces."""
        return cls(
            services=ALL_SERVICES,
            surfaces=(),
            capabilities=DEFAULT_CAPABILITIES,
        )

    @classmethod
    def mcp(cls) -> Self:
        """The MCP operator shape — full services, MCP surface only."""
        return cls(services=ALL_SERVICES, surfaces=("mcp",), capabilities=DEFAULT_CAPABILITIES)


__all__ = [
    "ALL_SERVICES",
    "CORE_SERVICES",
    "DEFAULT_CAPABILITIES",
    "SERVER_SURFACES",
    "Capability",
    "CompositionProfile",
    "ServiceName",
    "SurfaceName",
]
