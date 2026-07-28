"""
Hermetic CI slice — non-docs dogfood via WorkloadEngine (0.56).

    ruff check → guard_core  (neonroot + palm-ci)

    just ci-image
    palm flow start hermetic-ci-slice
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition


def _neonroot_run(command: list[str], *, timeout_s: float = 600) -> dict:
    return {
        "kind": "run",
        "isolation": "hermetic",
        "lifecycle": "job",
        "image": "palm-ci",
        "command": command,
        "seed": {"type": "git_archive"},
        "placement": {"runtime": "neonroot"},
        "timeout_s": timeout_s,
    }


HERMETIC_CI_SLICE_FLOW = FlowDefinition(
    id="flow-hermetic-ci-slice",
    name="hermetic-ci-slice",
    pattern="dag",
    options={
        "chain_implicit": False,
        "nodes": [
            {
                "id": "ruff",
                "workload": _neonroot_run(
                    [
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
                    timeout_s=600,
                ),
                "output_key": "hermetic_ci_ruff",
            },
            {
                "id": "guard_core",
                "workload": _neonroot_run(
                    [
                        "uv",
                        "run",
                        "--extra",
                        "cli",
                        "--group",
                        "dev",
                        "python",
                        "scripts/guard_core.py",
                    ],
                    timeout_s=300,
                ),
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
        "description": "Hermetic ruff + guard_core via DAG workload nodes",
    },
)


def register_definitions(repository: object) -> None:
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_flow):
        save_flow(HERMETIC_CI_SLICE_FLOW)
    if callable(save_process):
        save_process(HERMETIC_CI_SLICE_PROCESS)
