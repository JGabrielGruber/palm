"""
Hermetic CI slice — non-docs dogfood (0.54.6).

Proves the hermetic-job + DAG grammar outside Living Library tooling:

    preflight → ruff check → guard_core

Uses only ``neonroot`` + ``palm-ci`` (git-archive seed). Live run needs::

    just ci-image
    palm flow start hermetic-ci-slice

See [docs/HERMETIC-JOBS.md](../../docs/HERMETIC-JOBS.md).
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition, ResourceDefinition

# Shared preflight name from hermetic_job_smoke (also registered there).
# Local resources for the CI steps — self-contained pack.

HERMETIC_CI_RUFF = ResourceDefinition(
    id="resource-hermetic-ci-ruff",
    name="hermetic-ci-ruff",
    provider="neonroot",
    action="spawn",
    params={
        "image": "palm-ci",
        "vault": "palm-ci",
        "seed": "git-archive",
        "seed_mode": "copy",
        "command": [
            "uv",
            "run",
            "--extra",
            "cli",
            "--group",
            "dev",
            "ruff",
            "check",
            "src/palm/",
            "tests/",
            "examples/",
        ],
        "sandbox": True,
        "timeout": 600,
    },
    output_key="hermetic_ci_ruff",
    metadata={
        "example": True,
        "description": "Hermetic ruff check (slice of just ci)",
        "tags": ["hermetic-job", "ci", "neonroot", "0.54"],
        "theme": "0.54",
        "contract": "hermetic_job",
    },
)

HERMETIC_CI_GUARD_CORE = ResourceDefinition(
    id="resource-hermetic-ci-guard-core",
    name="hermetic-ci-guard-core",
    provider="neonroot",
    action="spawn",
    params={
        "image": "palm-ci",
        "vault": "palm-ci",
        "seed": "git-archive",
        "seed_mode": "copy",
        "command": [
            "uv",
            "run",
            "--extra",
            "cli",
            "--group",
            "dev",
            "python",
            "scripts/guard_core.py",
        ],
        "sandbox": True,
        "timeout": 300,
    },
    output_key="hermetic_ci_guard_core",
    metadata={
        "example": True,
        "description": "Hermetic guard_core (core purity)",
        "tags": ["hermetic-job", "ci", "neonroot", "0.54"],
        "theme": "0.54",
        "contract": "hermetic_job",
    },
)

HERMETIC_CI_SLICE_FLOW = FlowDefinition(
    id="flow-hermetic-ci-slice",
    name="hermetic-ci-slice",
    pattern="dag",
    options={
        "chain_implicit": False,
        "nodes": [
            {
                "id": "preflight",
                "resource_ref": "hermetic-preflight",
                "output_key": "hermetic_preflight",
            },
            {
                "id": "ruff",
                "resource_ref": "hermetic-ci-ruff",
                "depends_on": ["preflight"],
                "output_key": "hermetic_ci_ruff",
            },
            {
                "id": "guard_core",
                "resource_ref": "hermetic-ci-guard-core",
                "depends_on": ["ruff"],
                "output_key": "hermetic_ci_guard_core",
            },
        ],
    },
)

HERMETIC_CI_SLICE_PROCESS = ProcessDefinition(
    id="proc-hermetic-ci-slice",
    name="hermetic-ci-slice",
    flows=[HERMETIC_CI_SLICE_FLOW],
    metadata={
        "example": True,
        "description": "0.54.6 non-docs dogfood: hermetic ruff + guard_core via DAG",
    },
)


def register_definitions(repository: object) -> None:
    save_resource = getattr(repository, "save_resource", None)
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_resource):
        save_resource(HERMETIC_CI_RUFF)
        save_resource(HERMETIC_CI_GUARD_CORE)
    if callable(save_flow):
        save_flow(HERMETIC_CI_SLICE_FLOW)
    if callable(save_process):
        save_process(HERMETIC_CI_SLICE_PROCESS)
