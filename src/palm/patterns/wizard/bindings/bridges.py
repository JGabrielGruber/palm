"""
Wizard bridge hooks — register pattern-specific runtime surfaces on ``_registry``.

Nested unpark is WaitPlaneService (interest match), not pattern hooks.
"""

from __future__ import annotations

from typing import Any

from palm.common.patterns._registry import (
    ChildWaitHooks,
    InteractiveRuntimeHooks,
    register_child_wait,
    register_interactive_runtime,
    register_read_model_builder,
)
from palm.common.providers._registry import get_bound_runtime
from palm.core.orchestration import Job
from palm.patterns.wizard.bindings.behavior_tree.backtrack import can_backtrack_to
from palm.patterns.wizard.bindings.resource.nested_park import (
    nested_park_interest,
    poll_child_job,
)
from palm.patterns.wizard.pattern import WizardPattern


def _is_wizard_executable(executable: Any) -> bool:
    return isinstance(executable, WizardPattern)


def _wizard_previous_step(executable: Any, state: Any) -> str:
    wizard = executable
    current = wizard.current_step_slug(state)
    if current is None:
        raise ValueError("Wizard has no active step; cannot backtrack")

    config = wizard.config
    if not config.allow_backtrack:
        raise ValueError("Backtracking is disabled for this wizard")

    index = config.index_of(current)
    if index <= 0:
        raise ValueError("Already at the first step; cannot backtrack further")

    steps = config.iter_tree_steps()
    target = steps[index - 1].slug
    if not can_backtrack_to(config, target):
        raise ValueError(f"Cannot backtrack to step: {target!r}")
    return target


def _wizard_parent_is_waiting(job: Job) -> bool:
    return nested_park_interest(job.state) is not None


def _wizard_poll_child_for_parent(_state: Any, child_job_id: str) -> Job | None:
    runtime = get_bound_runtime()
    if runtime is None:
        return None
    return poll_child_job(runtime, child_job_id)


def register_wizard_bridges() -> None:
    """Wire wizard runtime bridges into the global pattern extension registry."""
    register_interactive_runtime(
        "wizard",
        InteractiveRuntimeHooks(
            is_executable=_is_wizard_executable,
            previous_step=_wizard_previous_step,
        ),
    )
    register_child_wait(
        "wizard",
        ChildWaitHooks(
            parent_is_waiting=_wizard_parent_is_waiting,
            poll_child_for_parent=_wizard_poll_child_for_parent,
        ),
    )
    from palm.patterns.wizard.bindings.read_model import build_wizard_view

    register_read_model_builder("wizard", build_wizard_view)
