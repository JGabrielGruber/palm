"""
Hermetic job smoke — multi-step resource graph (0.54.2).

Uses **only** the general ``neonroot`` provider (no domain library provider).

    preflight (health) → hermetic true (spawn)

Live spawn needs NeonRoot + ``palm-ci`` image (``just ci-image``).
Health alone works when the CLI is on PATH.

    palm flow start hermetic-job-smoke
    palm resource invoke neonroot-health
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition, ResourceDefinition

# Re-declare thin aliases so this pack is self-contained if load order varies.
# Canonical copies also live in neonroot_runners.py.

HERMETIC_PREFLIGHT = ResourceDefinition(
    id="resource-hermetic-preflight",
    name="hermetic-preflight",
    provider="neonroot",
    action="health",
    params={},
    output_key="hermetic_preflight",
    metadata={
        "example": True,
        "description": "Hermetic job preflight (neonroot CLI)",
        "tags": ["hermetic-job", "neonroot", "0.54"],
        "theme": "0.54",
        "contract": "hermetic_job",
    },
)

HERMETIC_TRUE_JOB = ResourceDefinition(
    id="resource-hermetic-true-job",
    name="hermetic-true-job",
    provider="neonroot",
    action="spawn",
    params={
        "image": "palm-ci",
        "vault": "palm-ci",
        "seed": "git-archive",
        "command": ["true"],
        "sandbox": True,
    },
    output_key="hermetic_true_job",
    metadata={
        "example": True,
        "description": "Minimal hermetic job (spawn true in palm-ci)",
        "tags": ["hermetic-job", "neonroot", "0.54"],
        "theme": "0.54",
        "contract": "hermetic_job",
    },
)

HERMETIC_JOB_SMOKE_FLOW = FlowDefinition(
    id="flow-hermetic-job-smoke",
    name="hermetic-job-smoke",
    pattern="wizard",
    options={
        "include_summary": True,
        "include_commit": False,
        "allow_backtrack": False,
        "steps": [
            {
                "slug": "preflight",
                "title": "Hermetic preflight",
                "prompt": "Probe NeonRoot CLI",
                "step_kind": "resource",
                "resource_ref": "hermetic-preflight",
                "output_key": "hermetic_preflight",
            },
            {
                "slug": "run_true",
                "title": "Run hermetic true",
                "prompt": "Spawn palm-ci with command true (needs image)",
                "step_kind": "resource",
                "resource_ref": "hermetic-true-job",
                "output_key": "hermetic_true_job",
            },
        ],
    },
)

HERMETIC_JOB_SMOKE_PROCESS = ProcessDefinition(
    id="proc-hermetic-job-smoke",
    name="hermetic-job-smoke",
    flows=[HERMETIC_JOB_SMOKE_FLOW],
    metadata={
        "example": True,
        "description": "0.54 purpose-test: multi-step hermetic jobs via neonroot only",
    },
)

# 0.54.3 — same graph as a real DAG pattern (resource nodes, implicit linear chain)
HERMETIC_JOB_DAG_FLOW = FlowDefinition(
    id="flow-hermetic-job-dag",
    name="hermetic-job-dag",
    pattern="dag",
    options={
        "nodes": [
            {
                "id": "preflight",
                "resource_ref": "hermetic-preflight",
                "output_key": "hermetic_preflight",
            },
            {
                "id": "run_true",
                "resource_ref": "hermetic-true-job",
                "output_key": "hermetic_true_job",
            },
        ],
    },
)

HERMETIC_JOB_DAG_PROCESS = ProcessDefinition(
    id="proc-hermetic-job-dag",
    name="hermetic-job-dag",
    flows=[HERMETIC_JOB_DAG_FLOW],
    metadata={
        "example": True,
        "description": "0.54.3 DAG pattern dogfood: same neonroot nodes as hermetic-job-smoke",
    },
)


def register_definitions(repository: object) -> None:
    save_resource = getattr(repository, "save_resource", None)
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_resource):
        save_resource(HERMETIC_PREFLIGHT)
        save_resource(HERMETIC_TRUE_JOB)
    if callable(save_flow):
        save_flow(HERMETIC_JOB_SMOKE_FLOW)
        save_flow(HERMETIC_JOB_DAG_FLOW)
    if callable(save_process):
        save_process(HERMETIC_JOB_SMOKE_PROCESS)
        save_process(HERMETIC_JOB_DAG_PROCESS)
