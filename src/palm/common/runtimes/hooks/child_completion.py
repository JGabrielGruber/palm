"""Compat unpark for nested child success (pre-matcher / dual-path).

**Normative path (0.55.4+):** :class:`~palm.common.wait.WaitMatcher` on
``runtime.event`` matches open wait interest and resumes or fails the owner.

This hook remains as a thin compatibility layer: when a child job succeeds and
still carries ``__palm:parent_job_id``, attempt the inverted parent resume.
``resume_job`` is a no-op if the parent is no longer ``WAITING_FOR_INPUT``
(matcher already unparked). Remove or gate further in 0.55.9 if unused.
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
        # Dual-path with WaitMatcher: matcher runs during event publish (before
        # hooks). If it already resumed the parent, this is a no-op.
        resume_parent_after_child(self._runtime, job)


__all__ = ["ChildCompletionHook"]
