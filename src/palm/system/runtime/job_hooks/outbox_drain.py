"""
Outbox drain hook — process pending outbox entries after job lifecycle changes.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from palm.core.orchestration.hooks import JobHookAdapter

if TYPE_CHECKING:
    from palm.common.events.outbox import OutboxProcessor
    from palm.core.orchestration.engine import OrchestrationEngine
    from palm.core.orchestration.job import Job
    from palm.core.orchestration.run_result import RunResult

_log = logging.getLogger(__name__)


class OutboxDrainHook(JobHookAdapter):
    """Drain the event outbox after durable job transitions."""

    def __init__(self, processor: OutboxProcessor) -> None:
        self._processor = processor

    def on_job_status_changed(
        self,
        engine: OrchestrationEngine,
        job: Job,
        result: RunResult | None = None,
    ) -> None:
        try:
            self._processor.process_batch()
        except Exception:
            # Documented ignore: outbox drain must not fail job lifecycle (CS-005).
            _log.exception(
                "outbox drain failed after job status change job_id=%s",
                getattr(job, "id", None),
            )
            return None
