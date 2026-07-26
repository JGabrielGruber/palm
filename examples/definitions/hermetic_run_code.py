"""
Hermetic run-code wizard — Assist-friendly, definition-persisted (0.54.9).

Like todo-builder: a **saved flow definition** operators start via Assist/CLI.
User picks an image, pastes Python, Palm stages a run dir and executes via
``neonroot.run_script`` (never in-engine exec).

::

    palm flow start hermetic-run-code

Needs NeonRoot + image (e.g. ``just ci-image`` for palm-ci).

More definitions later (optional): snippet libraries, multi-file projects,
list_images resource, saved payload artifacts — not required for v0.
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition, ResourceDefinition

HERMETIC_RUN_SCRIPT = ResourceDefinition(
    id="resource-hermetic-run-script",
    name="hermetic-run-script",
    provider="neonroot",
    action="run_script",
    params={
        "image": "{{ state.image }}",
        "code": "{{ state.code }}",
        "language": "python",
        "seed_mode": "bind",
        "vault": "{{ state.image }}",
        "timeout": 120,
        "allowed_images": ["palm-ci", "palm-docs"],
    },
    output_key="run_result",
    metadata={
        "example": True,
        "description": "Stage Python code and run under allowlisted NeonRoot image",
        "tags": ["hermetic-job", "run-code", "assist", "0.54"],
        "theme": "0.54",
        "contract": "hermetic_job",
    },
)

HERMETIC_RUN_CODE_FLOW = FlowDefinition(
    id="flow-hermetic-run-code",
    name="hermetic-run-code",
    pattern="wizard",
    state_schema={
        "type": "object",
        "properties": {
            "image": {
                "type": "string",
                "enum": ["palm-ci", "palm-docs"],
            },
            "code": {"type": "string", "minLength": 1},
        },
        "required": ["image", "code"],
    },
    options={
        "include_summary": True,
        "include_commit": False,
        "allow_backtrack": True,
        "steps": [
            {
                "slug": "intro",
                "title": "Hermetic run-code",
                "prompt": (
                    "Run a short Python snippet in a NeonRoot image (tmpfs workspace). "
                    "Palm stages the file and spawns the runner — code never executes "
                    "inside the Palm engine. Images are allowlisted (palm-ci, palm-docs)."
                ),
                "step_kind": "introduction",
                "required": False,
            },
            {
                "slug": "image",
                "title": "Image",
                "prompt": "Which NeonRoot image should run your code?",
                "field_type": "choice",
                "choices": ["palm-ci", "palm-docs"],
                "validation": [{"rule": "not_empty"}],
            },
            {
                "slug": "code",
                "title": "Python code",
                "prompt": (
                    "Paste Python to run (written to payload/main.py). "
                    "Example: print('hello from hermetic job')"
                ),
                "validation": [{"rule": "min_length", "params": {"min": 1}}],
            },
            {
                "slug": "preflight",
                "title": "NeonRoot preflight",
                "prompt": "Probe NeonRoot CLI",
                "step_kind": "resource",
                "resource_ref": "hermetic-preflight",
                "output_key": "hermetic_preflight",
            },
            {
                "slug": "run",
                "title": "Run script",
                "prompt": "Stage and execute in the selected image",
                "step_kind": "resource",
                "resource_ref": "hermetic-run-script",
                "output_key": "run_result",
            },
        ],
    },
)

HERMETIC_RUN_CODE_PROCESS = ProcessDefinition(
    id="proc-hermetic-run-code",
    name="hermetic-run-code",
    flows=[HERMETIC_RUN_CODE_FLOW],
    metadata={
        "example": True,
        "description": "Assist run-code: choose image, paste Python, neonroot.run_script",
    },
)


def register_definitions(repository: object) -> None:
    save_resource = getattr(repository, "save_resource", None)
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_resource):
        save_resource(HERMETIC_RUN_SCRIPT)
    if callable(save_flow):
        save_flow(HERMETIC_RUN_CODE_FLOW)
    if callable(save_process):
        save_process(HERMETIC_RUN_CODE_PROCESS)
