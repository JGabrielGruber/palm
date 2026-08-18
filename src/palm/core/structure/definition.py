"""Structure definition — pure desired structure.

Floor: identity, role intent, refuse, capabilities, places required.
Capabilities are the local install set. First unit: work_drain.
Richer fields (projection, authority pointers) grow without breaking these names.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Self

# Builtin structure-definition ids (VISION-0.63 catalog)
LOCAL_EMBEDDED_ID = "local.embedded"
LOCAL_CLI_ID = "local.cli"
LOCAL_SERVER_ID = "local.server"
LOCAL_ALL_IN_ONE_ID = "local.all_in_one"
LOCAL_WORKER_ID = "local.worker"
LOCAL_MCP_ID = "local.mcp"

# Local install names. Phenotypes that list drain also list outbox (0.65).
CAPABILITY_WORK_DRAIN = "work_drain"
CAPABILITY_OUTBOX = "outbox"
_DRAIN_AND_OUTBOX = frozenset({CAPABILITY_WORK_DRAIN, CAPABILITY_OUTBOX})


@dataclass(frozen=True, slots=True)
class StructureDefinition:
    """Declarative desired structure for one process.

    After load, this is structure law. Profiles/env only *seed* it.
    """

    id: str
    version: str = "1"
    role_intent: str = "embedded"
    #: Capabilities / memberships this shape refuses (e.g. server_surfaces).
    refuse: frozenset[str] = field(default_factory=frozenset)
    #: Capabilities this phenotype installs (local names). First unit: work_drain.
    capabilities: frozenset[str] = field(default_factory=frozenset)
    #: Place keys that must be ready before definition-ready (empty = in-process only).
    places_required: tuple[str, ...] = ()
    #: Free-form seed notes (not business rules).
    meta: dict[str, Any] = field(default_factory=dict)

    def has_capability(self, name: str) -> bool:
        """Whether this definition lists ``name`` as an install capability."""
        return name in self.capabilities

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "role_intent": self.role_intent,
            "refuse": sorted(self.refuse),
            "capabilities": sorted(self.capabilities),
            "places_required": list(self.places_required),
            "meta": dict(self.meta),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        refuse_raw = data.get("refuse") or ()
        caps_raw = data.get("capabilities") or ()
        places_raw = data.get("places_required") or ()
        return cls(
            id=str(data.get("id") or ""),
            version=str(data.get("version") or "1"),
            role_intent=str(data.get("role_intent") or "embedded"),
            refuse=frozenset(str(x) for x in refuse_raw),
            capabilities=frozenset(str(x) for x in caps_raw),
            places_required=tuple(str(x) for x in places_raw),
            meta=dict(data.get("meta") or {}),
        )


def local_embedded(*, version: str = "1") -> StructureDefinition:
    """Floor builtin structure definition: thin body — core ground, no surfaces, no drain membership."""
    return StructureDefinition(
        id=LOCAL_EMBEDDED_ID,
        version=version,
        role_intent="embedded",
        refuse=frozenset({"server_surfaces"}),
        capabilities=frozenset(),
        places_required=(),
        meta={"builtin": True, "source": "floor"},
    )


def local_cli(*, version: str = "1") -> StructureDefinition:
    """Operator CLI body — full services, no HTTP surfaces, drain membership."""
    return StructureDefinition(
        id=LOCAL_CLI_ID,
        version=version,
        role_intent="cli",
        refuse=frozenset({"server_surfaces"}),
        capabilities=_DRAIN_AND_OUTBOX,
        places_required=(),
        meta={"builtin": True, "source": "seed"},
    )


def local_server(*, version: str = "1") -> StructureDefinition:
    """HTTP server body — surfaces + continuous drain membership."""
    return StructureDefinition(
        id=LOCAL_SERVER_ID,
        version=version,
        role_intent="server",
        refuse=frozenset(),
        capabilities=_DRAIN_AND_OUTBOX,
        places_required=(),
        meta={"builtin": True, "source": "seed"},
    )


def local_all_in_one(*, version: str = "1") -> StructureDefinition:
    """Collapsed full host phenotype — includes continuous drain."""
    return StructureDefinition(
        id=LOCAL_ALL_IN_ONE_ID,
        version=version,
        role_intent="all_in_one",
        refuse=frozenset(),
        capabilities=_DRAIN_AND_OUTBOX,
        places_required=(),
        meta={"builtin": True, "source": "seed"},
    )


def local_worker(*, version: str = "1") -> StructureDefinition:
    """Headless worker — execution + drain, no surfaces."""
    return StructureDefinition(
        id=LOCAL_WORKER_ID,
        version=version,
        role_intent="worker",
        refuse=frozenset({"server_surfaces", "product_catalog_home"}),
        capabilities=_DRAIN_AND_OUTBOX,
        places_required=(),
        meta={"builtin": True, "source": "seed"},
    )


def local_mcp(*, version: str = "1") -> StructureDefinition:
    """MCP operator surface — full services, MCP surface only (no drain)."""
    return StructureDefinition(
        id=LOCAL_MCP_ID,
        version=version,
        role_intent="mcp",
        refuse=frozenset({"http_server_surfaces"}),
        capabilities=frozenset(),
        places_required=(),
        meta={"builtin": True, "source": "seed"},
    )


_BUILTIN_FACTORIES: dict[str, Callable[..., StructureDefinition]] = {
    LOCAL_EMBEDDED_ID: local_embedded,
    "embedded": local_embedded,
    LOCAL_CLI_ID: local_cli,
    "cli": local_cli,
    LOCAL_SERVER_ID: local_server,
    "server": local_server,
    LOCAL_ALL_IN_ONE_ID: local_all_in_one,
    "all_in_one": local_all_in_one,
    LOCAL_WORKER_ID: local_worker,
    "worker": local_worker,
    LOCAL_MCP_ID: local_mcp,
    "mcp": local_mcp,
}


def resolve_builtin_definition(definition_id: str, *, version: str = "1") -> StructureDefinition:
    """Resolve a known builtin structure-definition id (or alias). Unknown ids stay thin shells."""
    key = str(definition_id or "").strip()
    factory = _BUILTIN_FACTORIES.get(key)
    if factory is not None:
        return factory(version=version)
    return StructureDefinition(
        id=key or "local.unknown",
        version=version,
        role_intent="unknown",
        meta={"builtin": False, "source": "explicit"},
    )


__all__ = [
    "CAPABILITY_OUTBOX",
    "CAPABILITY_WORK_DRAIN",
    "LOCAL_ALL_IN_ONE_ID",
    "LOCAL_CLI_ID",
    "LOCAL_EMBEDDED_ID",
    "LOCAL_MCP_ID",
    "LOCAL_SERVER_ID",
    "LOCAL_WORKER_ID",
    "StructureDefinition",
    "local_all_in_one",
    "local_cli",
    "local_embedded",
    "local_mcp",
    "local_server",
    "local_worker",
    "resolve_builtin_definition",
]
