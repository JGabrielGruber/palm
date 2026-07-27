"""Compat unpark for nested child success (dual-path with WaitMatcher).

**Normative path (0.55.4+):** :class:`~palm.common.wait.WaitMatcher` on
``runtime.event`` matches open wait interest and resumes or fails the owner.

This hook is **intentionally retained** after theme exit (0.55.9) as a thin
compat layer for:

* Instance parks created **before** wait interest (pre-0.55.3 snapshots)
* Safety if the matcher is disabled (``enable_wait_matcher=False``)

``resume_job`` is a no-op when the parent is no longer ``WAITING_FOR_INPUT``
(matcher already unparked). Prefer leaving the hook enabled unless tests need
matcher-only isolation (``child_completion_hook=False``).

Remove only after a future theme proves zero live parks without
``palm.wait.interests`` (not required for 0.55 exit).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.common.child_wait import resume_parent_after_child
from palm.core.orchestration.hooks import JobHookAdapter
from palm.core.orchestration.job import JobStatus

if TYPE_CHECKING:
    from palm.core.orchestration.engine import OrchestrationEngine
    from palm.core.orchestration.job import Job
    from palm.core.orchestration.run_result import RunResult


class ChildCompletionHook(JobHookAdapter):
    """Compat: resume parent when nested child succeeds (idempotent with matcher)."""

    def __init__(self, runtime: Any) -> None:
        self._runtime = runtime

    def on_job_status_changed(
        self,
        engine: OrchestrationEngine,
        job: Job,
        result: RunResult | None = None,
    ) -> None:
        if job.status != JobStatus.SUCCEEDED:
            return
        # Matcher runs during event publish (before hooks). If it already
        # resumed the parent, resume_parent_after_child is a no-op.
        resume_parent_after_child(self._runtime, job)


__all__ = ["ChildCompletionHook"]
