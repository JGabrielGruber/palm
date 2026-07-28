"""
run-python — simple Workload plane dogfood (0.56).

One Spec, two places:

* **host** — local subprocess (requires ``PALM_WORKLOAD_HOST_ENABLED=1``)
* **neonroot** — hermetic spawn (needs NeonRoot + image e.g. ``palm-ci``)
* **auto** — neonroot when CLI present, else host

::

    palm flow start run-python
    # or palm_assist(params={flow_id: "run-python"})

Replaces the heavier hermetic-run-code / run_script loop for basic proof.
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition

RUN_PYTHON_FLOW = FlowDefinition(
    id="flow-run-python",
    name="run-python",
    pattern="wizard",
    state_schema={
        "type": "object",
        "properties": {
            "runtime": {
                "type": "string",
                "enum": ["auto", "local", "host", "neonroot"],
            },
            "code": {"type": "string", "minLength": 1},
            "run_result": {"type": "object"},
            "stdout": {"type": "string"},
            "exit_code": {},
        },
        "required": ["runtime", "code"],
    },
    options={
        "include_summary": True,
        "include_commit": False,
        "allow_backtrack": True,
        "steps": [
            {
                "slug": "runtime",
                "title": "Runtime",
                "prompt": (
                    "Where should this Python run?\n"
                    "• auto — neonroot if CLI present, else Palm **local** (always on)\n"
                    "• local — Palm process runner under data_dir (trusted default)\n"
                    "• host — full-machine subprocess (PALM_WORKLOAD_HOST_ENABLED=1)\n"
                    "• neonroot — hermetic image spawn (CLI + palm-ci)"
                ),
                "field_type": "choice",
                "choices": ["auto", "local", "host", "neonroot"],
                "validation": [{"rule": "not_empty"}],
            },
            {
                "slug": "code",
                "title": "Python",
                "prompt": (
                    "Python source passed as ``python -c …``.\n"
                    "Example:\nprint('hello from workload')\nprint(2 + 2)"
                ),
                "validation": [{"rule": "min_length", "params": {"min": 1}}],
            },
            {
                "slug": "run",
                "title": "Run",
                "prompt": "Allocate workload and run python -c",
                "step_kind": "workload",
                "output_key": "run_result",
                "params": {
                    "code": "{{ state.code }}",
                    "runtime": "{{ state.runtime }}",
                    "image": "palm-ci",
                    "timeout_s": 120,
                },
            },
            {
                "slug": "result",
                "title": "Result",
                "step_kind": "introduction",
                "required": False,
                "prompt": (
                    "Workload finished · exit {{ state.exit_code }}\n"
                    "runtime={{ state.runtime }}\n\n"
                    "--- stdout ---\n"
                    "{{ state.stdout }}"
                ),
            },
        ],
    },
)

# Discoverability: old hermetic name points at the same simple contract.
HERMETIC_RUN_CODE_ALIAS = FlowDefinition(
    id="flow-hermetic-run-code",
    name="hermetic-run-code",
    pattern="wizard",
    state_schema=RUN_PYTHON_FLOW.state_schema,
    options=RUN_PYTHON_FLOW.options,
)

RUN_PYTHON_PROCESS = ProcessDefinition(
    id="proc-run-python",
    name="run-python",
    flows=[RUN_PYTHON_FLOW],
    metadata={
        "example": True,
        "description": "runtime choice → code → workload run → display",
    },
)


def register_definitions(repository: object) -> None:
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_flow):
        save_flow(RUN_PYTHON_FLOW)
        save_flow(HERMETIC_RUN_CODE_ALIAS)
    if callable(save_process):
        save_process(RUN_PYTHON_PROCESS)
