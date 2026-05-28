"""
ExecutionBackend — pluggable strategy for advancing a single Job's executable work.

This is the lower-level Strategy (inside the larger OrchestrationMode Strategy)
that actually knows how to make progress on `job.executable`.

Design goals:
- The Orchestrator and Job never need to know *how* work is performed.
- TestBackend (primary) enables 100% deterministic, side-effect-free unit tests.
- BehaviorTreeBackend (optional) proves clean composition with the peer
  Behavior Tree engine without creating a hard dependency.

This module is part of Palm's general-purpose Orchestration Engine and must
remain completely independent of any wizard, UI, persistence, or domain concerns
except for the optional, clearly isolated BehaviorTreeBackend.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from palm.core.behavior_tree import BehaviorTree, NodeStatus  # only for optional backend

from ..exceptions import JobExecutionError
from ..job import Job, JobStatus


class ExecutionBackend(ABC):
    """
    Abstract strategy for advancing executable work associated with a Job.

    Implementations are responsible for:
    - Interpreting `job.executable` (opaque to the rest of the engine).
    - Driving the job through valid status transitions using the internal
      `_transition_to` helper (the backend temporarily enables mutation).
    - Returning the status the job reached after this "drive" attempt.
    - Respecting max_steps guards to prevent accidental infinite loops in tests.
    """

    @abstractmethod
    def advance(self, job: Job, *, max_steps: int | None = None) -> JobStatus:
        """
        Make progress on the job (one or more logical steps).

        The backend may transition the job through RUNNING, WAITING_FOR_INPUT,
        SUCCEEDED, FAILED, etc. It must never leave the job in an inconsistent state.

        Returns the status after this advance call.
        """
        ...


class TestBackend(ExecutionBackend):
    """
    Primary backend for unit tests and the default used by TestMode.

    Accepts either:
    - A simple dict descriptor: {"steps": N, "final_status": "SUCCEEDED"|"WAITING_FOR_INPUT", "result": ..., "inject_error": exc}
    - A callable(job: Job) -> JobStatus (full control for advanced tests)

    Characteristics:
    - 100% synchronous, no threads, no I/O, no real work.
    - Deterministic and extremely fast.
    - Perfect for exercising the full Job state machine, WAITING flows,
      error isolation, shutdown-during-work, max-concurrency, etc.
    - Never imports or depends on the Behavior Tree engine.
    """

    def advance(self, job: Job, *, max_steps: int | None = None) -> JobStatus:
        if job.is_terminal:
            return job.status

        steps = max_steps or 10_000
        if steps < 1:
            raise ValueError("max_steps must be >= 1")

        # Enable controlled mutation for this drive
        job._allow_mutation = True

        try:
            executable = job.executable

            if callable(executable) and not isinstance(executable, dict):
                # Advanced usage: caller supplies full control callable
                try:
                    result_status = executable(job)
                    if isinstance(result_status, JobStatus):
                        job._transition_to(result_status)
                    return job.status
                except Exception as exc:
                    job._transition_to(JobStatus.FAILED, error=exc)
                    raise JobExecutionError(job.id, "callable executable raised", original=exc) from exc

            if isinstance(executable, dict):
                total_steps = int(executable.get("steps", 1))
                target = executable.get("final_status", "SUCCEEDED")
                result = executable.get("result")
                inject_error = executable.get("inject_error")

                # If we are resuming a job that was previously put into WAITING by this descriptor,
                # just complete it to the declared final target (ignore step count on resume).
                if job.status == JobStatus.WAITING_FOR_INPUT:
                    if target in (JobStatus.SUCCEEDED.value, "SUCCEEDED"):
                        job._transition_to(JobStatus.SUCCEEDED, result=result)
                    elif target in (JobStatus.FAILED.value, "FAILED"):
                        err = inject_error or RuntimeError("TestBackend forced failure on resume")
                        job._transition_to(JobStatus.FAILED, error=err)
                        raise JobExecutionError(job.id, "forced failure on resume", original=err) from err
                    else:
                        job._transition_to(JobStatus.SUCCEEDED, result=result)
                    return job.status

                # Simulate progress (first submission path)
                for _ in range(min(total_steps, steps)):
                    if job.status != JobStatus.RUNNING:
                        job._transition_to(JobStatus.RUNNING)

                    if target == JobStatus.WAITING_FOR_INPUT.value:
                        job._transition_to(JobStatus.WAITING_FOR_INPUT)
                        return job.status

                    if inject_error is not None:
                        job._transition_to(JobStatus.FAILED, error=inject_error)
                        raise JobExecutionError(job.id, "injected by TestBackend", original=inject_error) from inject_error

                # Normal completion path
                if target in (JobStatus.SUCCEEDED.value, "SUCCEEDED"):
                    job._transition_to(JobStatus.SUCCEEDED, result=result)
                elif target in (JobStatus.FAILED.value, "FAILED"):
                    err = inject_error or RuntimeError("TestBackend forced failure")
                    job._transition_to(JobStatus.FAILED, error=err)
                    raise JobExecutionError(job.id, "forced by test descriptor", original=err) from err
                elif target in (JobStatus.WAITING_FOR_INPUT.value, "WAITING_FOR_INPUT"):
                    job._transition_to(JobStatus.WAITING_FOR_INPUT)
                else:
                    job._transition_to(JobStatus.SUCCEEDED, result=result)

                return job.status

            # Fallback: treat anything else as instant success (useful for smoke tests)
            job._transition_to(JobStatus.SUCCEEDED, result=executable)
            return JobStatus.SUCCEEDED

        finally:
            job._allow_mutation = False


class BehaviorTreeBackend(ExecutionBackend):
    """
    Optional backend that knows how to drive a BehaviorTree as a Job executable.

    This class is the *only* place in the entire orchestration package that
    imports from `palm.core.behavior_tree` (besides the single integration test).

    It is intentionally isolated so that 99% of orchestration tests and all
    production paths that don't need BT can remain completely independent of
    the Behavior Tree engine.
    """

    def advance(self, job: Job, *, max_steps: int | None = 10_000) -> JobStatus:
        if not isinstance(job.executable, BehaviorTree):
            raise JobExecutionError(
                job.id,
                "BehaviorTreeBackend can only execute BehaviorTree instances",
            )

        tree: BehaviorTree = job.executable
        job._allow_mutation = True

        try:
            if job.status == JobStatus.PENDING:
                job._transition_to(JobStatus.RUNNING)

            if max_steps is None:
                max_steps = 10_000

            try:
                final = tree.tick_until_terminal(max_ticks=max_steps)
            except Exception as exc:  # BehaviorTreeError or others
                job._transition_to(JobStatus.FAILED, error=exc)
                raise JobExecutionError(job.id, "BehaviorTree tick failed", original=exc) from exc

            # Map NodeStatus → JobStatus
            if final == NodeStatus.SUCCESS:
                result = tree.blackboard.get("__result__")  # convention
                job._transition_to(JobStatus.SUCCEEDED, result=result)
            elif final == NodeStatus.FAILURE:
                err = tree.blackboard.get("__error__")
                job._transition_to(JobStatus.FAILED, error=err)
            elif final == NodeStatus.WAITING_FOR_INPUT:
                job._transition_to(JobStatus.WAITING_FOR_INPUT)
            else:
                # RUNNING exhausted the tick budget — treat as failure for safety
                job._transition_to(JobStatus.FAILED, error=RuntimeError("Behavior tree did not terminate"))

            return job.status

        finally:
            job._allow_mutation = False
