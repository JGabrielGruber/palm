"""Nested child-wait helpers — poll and manual resume of parked parents.

Unpark on child completion is owned by :class:`~palm.common.wait.WaitMatcher`
(wait interest on the owner). These helpers support operator re-poll and
pattern-side ``parent_is_waiting`` checks only — no inverted parent resume.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.common.patterns._registry import ChildWaitHooks, get_child_wait_hooks
from palm.common.providers._registry import get_bound_runtime
from palm.core.orchestration import Job
from palm.core.wait import WAIT_KIND_JOB, find_wait_interests

if TYPE_CHECKING:
    from palm.common.runtimes.base import BaseRuntime


def _child_wait_hooks(job: Job) -> ChildWaitHooks:
    name = str(job.metadata.get("pattern") or "")
    if not name:
        raise RuntimeError("Job has no pattern metadata for child-wait dispatch")
    hooks = get_child_wait_hooks(name)
    if hooks is None:
        raise RuntimeError(f"Pattern {name!r} has no child-wait hooks registered")
    return hooks


def bound_runtime() -> Any | None:
    """Return the in-process runtime used for compositional palm invokes."""

    return get_bound_runtime()


def parent_is_waiting_for_child(job: Job) -> bool:
    """True when the job is parked on a nested child (interest and/or pattern wait)."""
    if find_wait_interests(job.state, kind=WAIT_KIND_JOB):
        return True
    return _child_wait_hooks(job).parent_is_waiting(job)


def resume_child_wait_for_instance(runtime: BaseRuntime, instance_id: str) -> Job:
    """Manually re-poll the nested child and advance the parent flow if ready."""
    from palm.common.interactive_runtime import resolve_interactive_job

    job = resolve_interactive_job(runtime, instance_id)
    if not parent_is_waiting_for_child(job):
        raise RuntimeError(f"Instance {instance_id!r} is not waiting for a nested child")
    runtime.orchestration.resume_job(job.id)
    return runtime.get_job(job.id)


def poll_child_for_parent(state: Any, child_job_id: str, *, pattern: str) -> Job | None:
    hooks = get_child_wait_hooks(pattern)
    if hooks is None:
        return None
    return hooks.poll_child_for_parent(state, child_job_id)


__all__ = [
    "bound_runtime",
    "parent_is_waiting_for_child",
    "poll_child_for_parent",
    "resume_child_wait_for_instance",
]
