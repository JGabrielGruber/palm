"""
NeonRoot sovereign runners — example resource definitions (0.53.3).

Catalog entries for the ``neonroot`` provider. Safe defaults:

- **neonroot-health** — probe host CLI (no image required).
- **neonroot-spawn-true** — hermetic ``true`` in ``palm-ci`` (needs NeonRoot + image).

CLI (after host load with examples)::

    palm resource invoke neonroot-health
    palm resource invoke neonroot-spawn-true   # requires palm-ci image

See [VISION-0.53](../../docs/VISION-0.53.md) · [ADR-022](../../docs/adr/022-neonroot-provider.md).
"""

from __future__ import annotations

from palm.definitions import ResourceDefinition

NEONROOT_HEALTH = ResourceDefinition(
    id="resource-neonroot-health",
    name="neonroot-health",
    provider="neonroot",
    action="health",
    params={},
    metadata={
        "example": True,
        "description": "Probe NeonRoot CLI (path + version); honest when missing",
        "tags": ["neonroot", "health", "sovereign-runners"],
        "theme": "0.53",
    },
)

NEONROOT_SPAWN_TRUE = ResourceDefinition(
    id="resource-neonroot-spawn-true",
    name="neonroot-spawn-true",
    provider="neonroot",
    action="spawn",
    params={
        "image": "palm-ci",
        "vault": "palm-ci",
        "seed": "git-archive",
        "command": ["true"],
        "sandbox": True,
    },
    metadata={
        "example": True,
        "description": (
            "Hermetic spawn of `true` in palm-ci (git-archive seed). "
            "Requires NeonRoot + `just ci-image` (or equivalent) once."
        ),
        "tags": ["neonroot", "spawn", "sovereign-runners"],
        "theme": "0.53",
    },
)

# Params may be overridden at invoke time (image/command/seed) via engine merge.
NEONROOT_SPAWN_DOCS_BUILD = ResourceDefinition(
    id="resource-neonroot-spawn-docs-build",
    name="neonroot-spawn-docs-build",
    provider="neonroot",
    action="spawn",
    params={
        "image": "palm-docs",
        "vault": "palm-docs",
        "seed": "git-archive",
        "command": ["uv", "run", "python", "scripts/docs_build.py"],
        "sandbox": True,
        "timeout": 1800,
    },
    metadata={
        "example": True,
        "description": (
            "Living Library builder inside NeonRoot palm-docs (0.52 work unit + 0.53.4 image). "
            "Build once with `just docs-image`."
        ),
        "tags": ["neonroot", "spawn", "docs", "living-library"],
        "theme": "0.53",
    },
)


def register_definitions(repository: object) -> None:
    save_resource = getattr(repository, "save_resource", None)
    if not callable(save_resource):
        return
    for resource in (NEONROOT_HEALTH, NEONROOT_SPAWN_TRUE, NEONROOT_SPAWN_DOCS_BUILD):
        save_resource(resource)
