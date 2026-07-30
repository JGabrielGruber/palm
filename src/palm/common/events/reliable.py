"""
Reliable event publishing — outbox interceptor wiring for EventEngine.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from palm.common.events.domain import CRITICAL_EVENT_TYPES
from palm.common.events.outbox import OutboxStore
from palm.core.event import Event, EventContext, EventEngine, Subscription

if TYPE_CHECKING:
    from palm.core.orchestration.job import Job


class ReliableEventPublisher:
    """
    Enqueue critical events to the outbox during live publish.

    In-process handlers still receive events synchronously; the outbox provides
    durability and a recovery path for external dispatchers.
    """

    def __init__(
        self,
        store: OutboxStore,
        *,
        critical_types: frozenset[str] | None = None,
    ) -> None:
        self._store = store
        self._critical_types = critical_types or CRITICAL_EVENT_TYPES

    def should_enqueue(self, event: Event) -> bool:
        return event.type in self._critical_types

    def enqueue(self, event: Event) -> str | None:
        if not self.should_enqueue(event):
            return None
        return self._store.enqueue(event)

    def as_interceptor(self) -> Callable[[Event], None]:
        def intercept(event: Event) -> None:
            self.enqueue(event)

        return intercept

    def attach(self, event_engine: EventEngine) -> Subscription:
        """Register the outbox interceptor on ``event_engine``."""
        return event_engine.add_interceptor(self.as_interceptor())


def event_context_from_job(job: Job) -> EventContext:
    """Build correlation context from orchestration job metadata."""
    sid_raw = job.metadata.get("session_id") or job.metadata.get("palm_session_id")
    session_id = str(sid_raw).strip() if sid_raw is not None else None
    if session_id == "":
        session_id = None
    return EventContext(
        job_id=job.id,
        instance_id=str(job.metadata["instance_id"])
        if job.metadata.get("instance_id") is not None
        else None,
        session_id=session_id,
        trace_id=str(job.metadata["trace_id"])
        if job.metadata.get("trace_id") is not None
        else None,
        principal_id=str(job.metadata["principal_id"])
        if job.metadata.get("principal_id") is not None
        else None,
    )


def wire_reliable_events(
    event_engine: EventEngine,
    store: OutboxStore,
    *,
    critical_types: frozenset[str] | None = None,
) -> ReliableEventPublisher:
    """Attach outbox interception to an initialized event engine."""
    publisher = ReliableEventPublisher(store, critical_types=critical_types)
    publisher.attach(event_engine)
    return publisher
