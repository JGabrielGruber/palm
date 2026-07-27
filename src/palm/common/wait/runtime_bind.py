"""Wire :class:`WaitMatcher` onto a runtime's orchestration event bus."""

from __future__ import annotations

from typing import Any

from palm.common.wait.matcher import WaitMatcher
from palm.common.wait.signals import TargetSignal
from palm.core.orchestration.job import JobStatus
from palm.core.orchestration.run_result import RunResult
from palm.core.wait import WaitInterest


def bind_wait_matcher_to_runtime(runtime: Any) -> WaitMatcher:
    """Create a matcher bound to ``runtime.event`` / orchestration jobs.

    Normative continue path (0.55.4): completer events → resume or fail owner.
    """
    orch = runtime.orchestration

    def get_job(job_id: str) -> Any:
        try:
            return orch.get_job(job_id)
        except Exception:
            return None

    def list_jobs() -> list[Any]:
        return list(orch.jobs.values())

    def resume_owner(
        owner_id: str,
        _interest: WaitInterest,
        _signal: TargetSignal,
    ) -> None:
        job = get_job(owner_id)
        if job is None or job.status != JobStatus.WAITING_FOR_INPUT:
            return
        orch.resume_job(owner_id)

    def fail_owner(
        owner_id: str,
        _interest: WaitInterest,
        signal: TargetSignal,
    ) -> None:
        job = get_job(owner_id)
        if job is None or job.is_terminal:
            return
        msg = (
            f"Wait target {signal.kind}:{signal.target_id} ended with "
            f"{signal.outcome}"
        )
        orch.apply_result(
            job,
            RunResult(status=JobStatus.FAILED, error=RuntimeError(msg)),
        )

    matcher = WaitMatcher(
        get_job=get_job,
        list_jobs=list_jobs,
        resume_owner=resume_owner,
        fail_owner=fail_owner,
    )
    event = getattr(runtime, "event", None)
    if event is not None:
        matcher.attach_events(event)
    return matcher


__all__ = ["bind_wait_matcher_to_runtime"]
