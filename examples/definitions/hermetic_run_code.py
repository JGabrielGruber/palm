"""
Hermetic run-code — basic Palm flow dogfooding NeonRoot (0.54.9+).

Textbook resource-action loop (no in-engine exec)::

    1. Select image          → state.image
    2. Write run file        → state.code  (staged as payload/main.py)
    3. Run via resource      → neonroot.run_script
    4. Store result in memory→ state.run_result / state.stdout / state.exit_code
    5. Display to the user   → result step + summary

::

    palm flow start hermetic-run-code
    # or palm_assist(params={flow_id: "hermetic-run-code"})

Needs NeonRoot + image (``just ci-image`` for palm-ci).
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition, ResourceDefinition

# ── Resource: stage file + neonroot spawn (the action under test) ────────────

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
        "description": "Stage payload/main.py and run under allowlisted NeonRoot image",
        "tags": ["hermetic-job", "run-code", "assist", "neonroot", "0.54"],
        "theme": "0.54",
        "contract": "hermetic_job",
    },
)

# ── Flow: image → code → run → remember → show ───────────────────────────────

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
            # Memory after the resource call
            "run_result": {"type": "object"},
            "stdout": {"type": "string"},
            "exit_code": {},
        },
        "required": ["image", "code"],
    },
    options={
        "include_summary": True,
        "include_commit": False,
        "allow_backtrack": True,
        "steps": [
            # 1 — select image
            {
                "slug": "image",
                "title": "Image",
                "prompt": (
                    "Pick a NeonRoot image. The runner stages your code into a "
                    "disposable workspace and spawns this image (never executes "
                    "inside Palm)."
                ),
                "field_type": "choice",
                "choices": ["palm-ci", "palm-docs"],
                "validation": [{"rule": "not_empty"}],
            },
            # 2 — update run file content
            {
                "slug": "code",
                "title": "Run file",
                "prompt": (
                    "Python for payload/main.py. Use print(...) so stdout is captured. "
                    "Example:\nprint('hello from hermetic job')\nprint(2 + 2)"
                ),
                "validation": [{"rule": "min_length", "params": {"min": 1}}],
            },
            # 3 — resource action call (stage + neonroot spawn)
            {
                "slug": "run",
                "title": "Run",
                "prompt": "Stage payload and invoke neonroot.run_script",
                "step_kind": "resource",
                "resource_ref": "hermetic-run-script",
                "output_key": "run_result",
            },
            # 4 — store result as flat memory (for display + later steps)
            {
                "slug": "remember_stdout",
                "step_kind": "transform",
                "title": "Remember stdout",
                "source_key": "run_result",
                "target_key": "stdout",
                "rule": "jsonpath_extract",
                "options": {
                    "path": "stdout",
                    "default": "",
                },
            },
            {
                "slug": "remember_exit",
                "step_kind": "transform",
                "title": "Remember exit code",
                "source_key": "run_result",
                "target_key": "exit_code",
                "rule": "jsonpath_extract",
                "options": {
                    "path": "exit_code",
                    "default": -1,
                },
            },
            # 5 — display to the user (prompt binds state → Assist/WS turn)
            {
                "slug": "result",
                "title": "Result",
                "step_kind": "introduction",
                "required": False,
                "prompt": (
                    "NeonRoot run finished · exit {{ state.exit_code }}\n\n"
                    "--- stdout ---\n"
                    "{{ state.stdout }}"
                ),
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
        "description": (
            "Basic NeonRoot loop: select image → write run file → "
            "resource run_script → store result → display"
        ),
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
