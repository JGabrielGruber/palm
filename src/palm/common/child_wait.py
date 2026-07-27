"""Operator helpers for parents parked on nested child jobs (interest-based)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.common.interactive_runtime import resolve_interactive_job
from palm.common.patterns._registry import get_child_wait_hooks
from palm.common.providers._registry import get_bound_runtime
from palm.core.orchestration import Job
from palm.core.wait import WAIT_KIND_JOB, find_wait_interests

if TYPE_CHECKING:
    from palm.common.runtimes.base import BaseRuntime


def bound_runtime() -> Any | None:
    return get_bound_runtime()


def parent_is_waiting_for_child(job: Job) -> bool:
    """True when owner has an open job wait interest (nested or otherwise)."""
    if find_wait_interests(job.state, kind=WAIT_KIND_JOB):
        return True
    name = str(job.metadata.get("pattern") or "")
    if not name:
        return False
    hooks = get_child_wait_hooks(name)
    if hooks is None:
        return False
    return hooks.parent_is_waiting(job)


def resume_child_wait_for_instance(runtime: BaseRuntime, instance_id: str) -> Job:
    """Manually resume a parent that is still parked (re-poll path)."""
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
