"""0.62 — orchestration membership lock, exclusive drive, QueuedScheduler pool."""

from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from palm.core.context import ContextEngine
from palm.core.event import EventEngine
from palm.core.orchestration import JobStatus, OrchestrationEngine
from palm.core.orchestration.drive import drive_job
from palm.system.runtime.schedulers import QueuedScheduler
from palm.system.runtime.wiring import resolve_scheduler
from tests.core.fakes.runner import TestRunner


def _engine(scheduler=None) -> OrchestrationEngine:
    events = EventEngine()
    context = ContextEngine()
    events.initialize()
    context.initialize()
    engine = OrchestrationEngine()
    engine.initialize(
        scheduler=scheduler or QueuedScheduler(runner=TestRunner(), workers=1),
        event_engine=events,
        context_engine=context,
    )
    engine.start()
    return engine


def test_begin_drive_exclusive() -> None:
    engine = _engine()
    job = engine.submit({"steps": 1, "final_status": "WAITING_FOR_INPUT"})
    # drain first drive
    assert engine.scheduler.wait_until_idle()  # type: ignore[attr-defined]
    assert job.status == JobStatus.WAITING_FOR_INPUT

    assert engine.begin_drive(job, driver_id="a") is True
    assert engine.begin_drive(job, driver_id="b") is False
    assert engine.is_driving(job.id)
    engine.end_drive(job)
    assert engine.begin_drive(job, driver_id="b") is True
    engine.end_drive(job)
    engine.stop()


def test_drive_job_skips_when_already_driving() -> None:
    engine = OrchestrationEngine()
    events = EventEngine()
    context = ContextEngine()
    events.initialize()
    context.initialize()
    from palm.system.runtime.schedulers.inline import InlineScheduler

    engine.initialize(
        scheduler=InlineScheduler(runner=TestRunner()),
        event_engine=events,
        context_engine=context,
    )
    engine.start()
    job = engine.submit({"steps": 1, "final_status": "WAITING_FOR_INPUT"})
    assert job.status == JobStatus.WAITING_FOR_INPUT

    assert engine.begin_drive(job, driver_id="holder") is True
    # Second drive must no-op
    assert drive_job(engine, TestRunner(), job, driver_id="other") is False
    engine.end_drive(job)
    engine.stop()


def test_concurrent_submit_membership() -> None:
    engine = _engine()
    n = 40
    errors: list[BaseException] = []

    def _one(i: int) -> str:
        try:
            job = engine.submit(
                {"steps": 1, "final_status": "SUCCEEDED", "result": i},
                job_id=f"c-{i}",
            )
            return job.id
        except BaseException as exc:  # noqa: BLE001 — collect for assert
            errors.append(exc)
            raise

    with ThreadPoolExecutor(max_workers=16) as pool:
        ids = list(pool.map(_one, range(n)))

    assert not errors
    assert len(ids) == n
    assert len(set(ids)) == n
    assert engine.scheduler.wait_until_idle(timeout=10.0)  # type: ignore[attr-defined]
    assert len(engine.list_jobs(status=JobStatus.SUCCEEDED)) == n
    engine.stop()


def test_queued_pool_drives_jobs_concurrently() -> None:
    """N workers should overlap slow jobs (I/O-style sleep), not serialize all."""
    started = threading.Barrier(3, timeout=5.0)
    active = 0
    peak = 0
    lock = threading.Lock()

    def slow_ok(job):  # noqa: ANN001
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        try:
            started.wait()
            time.sleep(0.05)
            return JobStatus.SUCCEEDED
        finally:
            with lock:
                active -= 1

    scheduler = QueuedScheduler(runner=TestRunner(), workers=3)
    engine = _engine(scheduler=scheduler)

    jobs = [engine.submit(slow_ok) for _ in range(3)]
    assert scheduler.wait_until_idle(timeout=10.0)
    assert all(j.status == JobStatus.SUCCEEDED for j in jobs)
    assert peak >= 2, f"expected concurrent drive, peak={peak}"
    assert scheduler.workers == 3
    assert scheduler.workers_alive == 3
    engine.stop()
    scheduler.shutdown()


def test_resolve_scheduler_queued_workers() -> None:
    mode = resolve_scheduler({"scheduler": "queued", "queued_workers": 4})
    assert isinstance(mode, QueuedScheduler)
    assert mode.workers == 4


def test_apply_result_terminal_wins_under_lock() -> None:
    from palm.core.orchestration.run_result import RunResult
    from palm.system.runtime.schedulers.inline import InlineScheduler

    engine = OrchestrationEngine()
    events = EventEngine()
    context = ContextEngine()
    events.initialize()
    context.initialize()
    engine.initialize(
        scheduler=InlineScheduler(runner=TestRunner()),
        event_engine=events,
        context_engine=context,
    )
    engine.start()
    job = engine.submit({"steps": 1, "final_status": "WAITING_FOR_INPUT"})
    assert job.status == JobStatus.WAITING_FOR_INPUT

    engine.apply_result(job, RunResult(status=JobStatus.CANCELLED))
    assert job.status == JobStatus.CANCELLED
    # Stale success after terminal is ignored
    engine.apply_result(job, RunResult(status=JobStatus.SUCCEEDED, result="late"))
    assert job.status == JobStatus.CANCELLED
    engine.stop()
