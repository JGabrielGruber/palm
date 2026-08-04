"""
Shared job-driving primitive for synchronous schedulers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from palm.core.orchestration.exceptions import JobAuthorizationError
from palm.core.orchestration.job import JobStatus
from palm.core.orchestration.run_result import RunResult

if TYPE_CHECKING:
    from palm.core.orchestration.engine import OrchestrationEngine
    from palm.core.orchestration.execution.base_runner import JobRunner
    from palm.core.orchestration.job import Job


def drive_job(
    engine: OrchestrationEngine,
    runner: JobRunner,
    job: Job,
    *,
    budget: int | None = None,
    driver_id: str | None = None,
) -> bool:
    """
    Run a job through a runner and apply the outcome on the engine.

    Acquires exclusive drive ownership first. Returns ``False`` when another
    driver already owns the job (or the job is terminal/unknown) so multi-worker
    queues can drop duplicate work items safely.
    """
    if not engine.begin_drive(job, driver_id=driver_id):
        return False
    try:
        try:
            engine.notify_before_drive(job)
        except JobAuthorizationError as exc:
            engine.apply_result(
                job,
                RunResult(status=JobStatus.FAILED, error=exc),
            )
            return True

        exec_ctx = engine.execution_context(job)
        bus = engine.event_engine
        event_context = engine.event_context_for_job(job)
        if bus is not None and bus.is_initialized and event_context is not None:
            with bus.bind_context(event_context):
                result = runner.run(exec_ctx, budget=budget)
        else:
            result = runner.run(exec_ctx, budget=budget)
        engine.apply_result(job, result)
        engine.notify_after_drive(job, result)
        return True
    finally:
        engine.end_drive(job)
