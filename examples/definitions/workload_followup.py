"""
workload-followup — reactive dogfood (0.56.9).

When a workload with label ``dogfood=run-python`` stops, work-drain enqueues
this flow (start verb). Completer only emits; Palm matches.

::

    # Enable work drain + host (or use neonroot run-python)
    PALM_WORKLOAD_HOST_ENABLED=1 palm flow start run-python
    # after run completes → tick_work starts workload-followup
"""

from __future__ import annotations

from palm.definitions import FlowDefinition, ProcessDefinition

_ON_WORKLOAD_TRIGGERS = [
    {
        "kind": "on_workload",
        "when": "stopped",
        "labels": {"dogfood": "run-python"},
        "debounce": 0.5,
        "work": {
            "flow_id": "workload-followup",
            "coalesce_key": "on_workload:stopped:workload-followup",
        },
    },
]

WORKLOAD_FOLLOWUP_FLOW = FlowDefinition(
    id="flow-workload-followup",
    name="workload-followup",
    pattern="wizard",
    options={
        "include_summary": False,
        "include_commit": False,
        "allow_backtrack": False,
        "triggers": _ON_WORKLOAD_TRIGGERS,
        "steps": [
            {
                "slug": "intro",
                "title": "Pipeline stage",
                "step_kind": "introduction",
                "required": False,
                "prompt": (
                    "Reactive path: a workload (dogfood=run-python) reached "
                    "**stopped**. Completer emitted ``workload.stopped``; "
                    "trigger interest enqueued this flow via work-drain.\n\n"
                    "Allocate · emit · match · start — no inverted hooks."
                ),
            },
        ],
    },
)

WORKLOAD_FOLLOWUP_PROCESS = ProcessDefinition(
    id="proc-workload-followup",
    name="workload-followup",
    flows=[WORKLOAD_FOLLOWUP_FLOW],
    metadata={
        "example": True,
        "description": "on_workload stopped → follow-up wizard (0.56 reactive dogfood)",
        "triggers": _ON_WORKLOAD_TRIGGERS,
    },
)


def register_definitions(repository: object) -> None:
    save_flow = getattr(repository, "save_flow", None)
    save_process = getattr(repository, "save_process", None)
    if callable(save_flow):
        save_flow(WORKLOAD_FOLLOWUP_FLOW)
    if callable(save_process):
        save_process(WORKLOAD_FOLLOWUP_PROCESS)


__all__ = [
    "WORKLOAD_FOLLOWUP_FLOW",
    "WORKLOAD_FOLLOWUP_PROCESS",
    "register_definitions",
]
