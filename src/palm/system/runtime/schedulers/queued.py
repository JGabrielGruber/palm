"""
QueuedScheduler — background job scheduling via a work queue.

Runs jobs asynchronously on one or more worker threads while preserving the
canonical drive loop: ``JobRunner.run`` → ``RunResult`` → ``apply_result``.

Default ``workers=1`` matches the historical single-thread daemon. Raise
``workers`` (or ``PALM_QUEUED_WORKERS``) for concurrent *job* drive under
exclusive per-job ownership on :class:`~palm.core.orchestration.engine.OrchestrationEngine`.
"""

from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from palm.core.orchestration.drive import drive_job
from palm.core.orchestration.execution.base_runner import JobRunner
from palm.core.orchestration.job import JobStatus
from palm.core.orchestration.mode.base_mode import OrchestrationMode

if TYPE_CHECKING:
    from palm.core.orchestration.engine import OrchestrationEngine
    from palm.core.orchestration.job import Job

_SENTINEL = object()


@dataclass(frozen=True)
class _WorkItem:
    engine: OrchestrationEngine
    job: Job
    budget: int | None


class QueuedScheduler(OrchestrationMode):
    """
    Enqueue submitted and resumed jobs for background worker(s) to drive.

    Suitable for daemon and long-lived runtimes where callers should not block
    on pattern execution. For synchronous in-process use, prefer
    :class:`~palm.system.runtime.schedulers.inline.InlineScheduler`.

    **Concurrency:** ``workers`` controls how many drive slices may run at once
    across *different* jobs. The engine still enforces one drive owner per job.
    This is I/O/wait overlap and start/drive capacity — not “all host cores for
    Python patterns.”
    """

    def __init__(
        self,
        *,
        runner: JobRunner,
        budget: int = 10_000,
        workers: int = 1,
        name: str = "QueuedScheduler",
    ) -> None:
        if runner is None:
            raise TypeError("QueuedScheduler requires runner=")
        super().__init__(name=name)
        self._runner = runner
        self._budget = budget
        self._workers = max(1, int(workers))
        self._queue: queue.Queue[_WorkItem | object] = queue.Queue()
        self._threads: list[threading.Thread] = []
        self._stop = threading.Event()
        self._running = False

    @property
    def runner(self) -> JobRunner:
        return self._runner

    @property
    def workers(self) -> int:
        """Configured drive worker count (at least 1)."""
        return self._workers

    @property
    def workers_alive(self) -> int:
        """How many worker threads are still alive."""
        return sum(1 for t in self._threads if t.is_alive())

    def start(self) -> None:
        if self._running:
            return
        self._stop.clear()
        self._threads = []
        for i in range(self._workers):
            thread = threading.Thread(
                target=self._worker,
                name=f"{self.name}-{i}",
                daemon=True,
            )
            thread.start()
            self._threads.append(thread)
        self._running = True

    def shutdown(self, *, timeout: float = 5.0) -> None:
        if not self._running:
            return
        self._stop.set()
        # One sentinel per worker so each loop can exit
        for _ in range(self._workers):
            self._queue.put(_SENTINEL)
        deadline = time.monotonic() + timeout
        for thread in self._threads:
            remaining = max(0.0, deadline - time.monotonic())
            if thread.is_alive():
                thread.join(timeout=remaining)
        self._threads = []
        self._running = False

    def is_running(self) -> bool:
        return self._running and not self._stop.is_set()

    def submit_job(self, engine: OrchestrationEngine, job: Job) -> None:
        if not self._running:
            self.start()
        self._enqueue(engine, job)

    def resume_job(self, engine: OrchestrationEngine, job: Job) -> None:
        if job.status == JobStatus.WAITING_FOR_INPUT:
            self._enqueue(engine, job)

    def wait_until_idle(self, *, timeout: float = 5.0) -> bool:
        """
        Block until all queued work has been processed.

        Intended for tests and graceful shutdown coordination; not a general
        completion API for production callers.
        """
        deadline = time.monotonic() + timeout
        while self._queue.unfinished_tasks:
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.01)
        return True

    def _enqueue(self, engine: OrchestrationEngine, job: Job) -> None:
        self._queue.put(_WorkItem(engine=engine, job=job, budget=self._budget))

    def _worker(self) -> None:
        driver_id = threading.current_thread().name
        while not self._stop.is_set():
            try:
                item = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if item is _SENTINEL:
                self._queue.task_done()
                break

            if not isinstance(item, _WorkItem):
                self._queue.task_done()
                continue

            work = item
            try:
                if not work.job.is_terminal:
                    drive_job(
                        work.engine,
                        self._runner,
                        work.job,
                        budget=work.budget,
                        driver_id=driver_id,
                    )
            finally:
                self._queue.task_done()
