"""
Hermetic job smoke — multi-step **workload** graph (0.56; was neonroot provider).

    preflight note → hermetic true (WorkloadEngine + neonroot runtime)

Live spawn needs NeonRoot + ``palm-ci`` image (``just ci-image``).

    palm flow start hermetic-job-smoke
    palm flow start hermetic-job-dag
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition

_TRUE_WORKLOAD = {
    "kind": "run",
    "isolation": "hermetic",
    "lifecycle": "job",
    "image": "palm-ci",
    "command": ["true"],
    "seed": {"type": "git_archive"},
    "placement": {"runtime": "neonroot"},
    "timeout_s": 120,
}

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
                "slug": "intro",
                "title": "Hermetic smoke",
                "step_kind": "introduction",
                "required": False,
                "prompt": (
                    "Runs a hermetic ``true`` via WorkloadEngine + neonroot runtime "
                    "(not ResourceEngine). Needs NeonRoot CLI + palm-ci image."
                ),
            },
            {
                "slug": "run_true",
                "title": "Run hermetic true",
                "prompt": "Spawn palm-ci with command true",
                "step_kind": "workload",
                "output_key": "hermetic_true_job",
                "params": dict(_TRUE_WORKLOAD),
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
        "description": "Hermetic true via workload plane (neonroot runtime)",
    },
)

HERMETIC_JOB_DAG_FLOW = FlowDefinition(
    id="flow-hermetic-job-dag",
    name="hermetic-job-dag",
    pattern="dag",
    options={
        "nodes": [
            {
                "id": "run_true",
                "workload": dict(_TRUE_WORKLOAD),
                "output_key": "hermetic_true_job",
            },
        ],
    },
)

HERMETIC_JOB_DAG_PROCESS = ProcessDefinition(
    id="proc-hermetic-job-dag",
    name="hermetic-job-dag",
    flows=[HERMETIC_JOB_DAG_FLOW],
    metadata={"example": True, "description": "DAG with workload node (neonroot)"},
)

# Fan-out keeps same true job twice after a linear preflight true
HERMETIC_JOB_FANOUT_FLOW = FlowDefinition(
    id="flow-hermetic-job-fanout",
    name="hermetic-job-fanout",
    pattern="dag",
    options={
        "chain_implicit": False,
        "nodes": [
            {
                "id": "preflight",
                "workload": dict(_TRUE_WORKLOAD),
                "output_key": "preflight",
            },
            {
                "id": "branch_a",
                "workload": dict(_TRUE_WORKLOAD),
                "output_key": "branch_a",
                "depends_on": ["preflight"],
            },
            {
                "id": "branch_b",
                "workload": dict(_TRUE_WORKLOAD),
                "output_key": "branch_b",
                "depends_on": ["preflight"],
            },
            {
                "id": "join",
                "workload": dict(_TRUE_WORKLOAD),
                "output_key": "join",
                "depends_on": ["branch_a", "branch_b"],
            },
        ],
    },
)

HERMETIC_JOB_FANOUT_PROCESS = ProcessDefinition(
    id="proc-hermetic-job-fanout",
    name="hermetic-job-fanout",
    flows=[HERMETIC_JOB_FANOUT_FLOW],
    metadata={"example": True, "description": "DAG fan-out with workload nodes"},
)


def register_definitions(repository: object) -> None:
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_flow):
        for flow in (
            HERMETIC_JOB_SMOKE_FLOW,
            HERMETIC_JOB_DAG_FLOW,
            HERMETIC_JOB_FANOUT_FLOW,
        ):
            save_flow(flow)
    if callable(save_process):
        for proc in (
            HERMETIC_JOB_SMOKE_PROCESS,
            HERMETIC_JOB_DAG_PROCESS,
            HERMETIC_JOB_FANOUT_PROCESS,
        ):
            save_process(proc)
