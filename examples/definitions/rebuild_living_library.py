"""
Rebuild Living Library — Palm graph over library + neonroot resources (0.54.4).

Linear wizard of resource steps (Palm's transform ``pipeline`` pattern is for
ETL rules; resource graphs use wizard ``step_kind: resource``).

Graph::

    neonroot-health (optional preflight — soft if CLI missing at invoke)
      → docs-corpus-wiki-publish  (library provider → storage pin)
      → library-status           (read pin back into state)

Try::

    palm flow start rebuild-living-library

Or after publish::

    palm resource invoke library-status
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition, ResourceDefinition

# ── Resources ────────────────────────────────────────────────────────────────

DOCS_CORPUS_WIKI_PUBLISH = ResourceDefinition(
    id="resource-docs-corpus-wiki-publish",
    name="docs-corpus-wiki-publish",
    provider="library",
    action="publish_wiki",
    params={"pin": True},
    output_key="wiki_publish",
    metadata={
        "example": True,
        "description": "Publish docs/wiki SOURCE into Palm library storage and pin",
        "tags": ["library", "wiki", "living-library"],
        "theme": "0.54",
    },
)

LIBRARY_STATUS = ResourceDefinition(
    id="resource-library-status",
    name="library-status",
    provider="library",
    action="status",
    output_key="library_status",
    metadata={
        "example": True,
        "description": "Read current Living Library pin from storage",
        "tags": ["library", "status"],
        "theme": "0.54",
    },
)

# neonroot-health already registered by neonroot_runners.py when examples load

# ── Flow ─────────────────────────────────────────────────────────────────────

REBUILD_LIVING_LIBRARY_FLOW = FlowDefinition(
    id="flow-rebuild-living-library",
    name="rebuild-living-library",
    pattern="wizard",
    options={
        "include_summary": True,
        "include_commit": False,
        "allow_backtrack": False,
        "steps": [
            {
                "slug": "preflight_runners",
                "title": "NeonRoot preflight",
                "prompt": "Probe hermetic runner CLI (optional — continue even if soft-fail)",
                "step_kind": "resource",
                "resource_ref": "neonroot-health",
                "output_key": "neonroot_health",
            },
            {
                "slug": "publish_wiki",
                "title": "Publish wiki corpus",
                "prompt": "Publish docs/wiki into Palm storage and flip the live pin",
                "step_kind": "resource",
                "resource_ref": "docs-corpus-wiki-publish",
                "output_key": "wiki_publish",
            },
            {
                "slug": "read_pin",
                "title": "Library status",
                "prompt": "Confirm current library pin",
                "step_kind": "resource",
                "resource_ref": "library-status",
                "output_key": "library_status",
            },
        ],
    },
)

REBUILD_LIVING_LIBRARY_PROCESS = ProcessDefinition(
    id="proc-rebuild-living-library",
    name="rebuild-living-library",
    flows=[REBUILD_LIVING_LIBRARY_FLOW],
    metadata={
        "example": True,
        "description": "Process wrapper for rebuild-living-library flow",
    },
)


def register_definitions(repository: object) -> None:
    save_resource = getattr(repository, "save_resource", None)
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_resource):
        save_resource(DOCS_CORPUS_WIKI_PUBLISH)
        save_resource(LIBRARY_STATUS)
    if callable(save_flow):
        save_flow(REBUILD_LIVING_LIBRARY_FLOW)
    if callable(save_process):
        save_process(REBUILD_LIVING_LIBRARY_PROCESS)
