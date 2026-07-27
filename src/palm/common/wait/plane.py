"""WaitPlaneService — first-class **continue** plane (0.55.10).

Peer of work-drain (**start**): completer events on ``runtime.event`` match
open wait interests and resume or fail owner jobs. Runtimes attach this service
at start; completers never import it (register-downward).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.common.wait.index import WaitOwnerIndex
from palm.common.wait.matcher import MatchDisposition, WaitMatcher
from palm.common.wait.present import summarize_waiting_on, waiting_on_from_job
from palm.common.wait.rehydrate import rehydrate_wait_interests
from palm.common.wait.signals import TargetSignal
from palm.core.orchestration.job import JobStatus
from palm.core.orchestration.run_result import RunResult
from palm.core.wait import (
    WaitInterest,
    close_wait_on_job,
    open_wait_on_job,
)

if TYPE_CHECKING:
    from palm.core.event import EventEngine


class WaitPlaneService:
    """Continue plane: interest open/close + event match → resume/fail.

    Lifecycle:
    * :meth:`attach` — bind to a runtime's orchestration + ``runtime.event``
    * :meth:`detach` — unsubscribe
    """

    def __init__(self) -> None:
        self._index = WaitOwnerIndex()
        self._matcher: WaitMatcher | None = None
        self._runtime: Any | None = None

    @property
    def matcher(self) -> WaitMatcher | None:
        return self._matcher

    @property
    def index(self) -> WaitOwnerIndex:
        return self._index

    @property
    def is_attached(self) -> bool:
        return self._matcher is not None and bool(getattr(self._matcher, "_subs", None))

    def attach(self, runtime: Any) -> WaitMatcher:
        """Wire matcher to ``runtime.event`` and orchestration job store."""
        if self._matcher is not None:
            self.detach()
        self._runtime = runtime
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
            index=self._index,
            get_job=get_job,
            list_jobs=list_jobs,
            resume_owner=resume_owner,
            fail_owner=fail_owner,
        )
        event: EventEngine | None = getattr(runtime, "event", None)
        if event is not None:
            matcher.attach_events(event)
        self._matcher = matcher
        return matcher

    def detach(self) -> None:
        if self._matcher is not None:
            self._matcher.detach_events()
            self._matcher = None
        self._runtime = None

    def open_on_job(
        self,
        job: Any,
        interest: WaitInterest,
        **kwargs: Any,
    ) -> WaitInterest:
        """Open interest on job state and register owner index."""
        opened = open_wait_on_job(job, interest, **kwargs)
        self._index.register(str(job.id), opened)
        return opened

    def close_on_job(
        self,
        job: Any,
        *,
        kind: str,
        target_id: str,
    ) -> WaitInterest | None:
        """Close interest on job state and drop index entry."""
        closed = close_wait_on_job(job, kind=kind, target_id=target_id)
        self._index.unregister(str(job.id), kind=kind, target_id=target_id)
        return closed

    def rehydrate_state(self, state: Any) -> list[WaitInterest]:
        """Normalize wait interests after snapshot restore."""
        return rehydrate_wait_interests(state)

    def handle_payload(
        self,
        event_type: str,
        payload: dict[str, Any] | None = None,
        *,
        event_id: str | None = None,
    ) -> list[MatchDisposition]:
        if self._matcher is None:
            return []
        return self._matcher.handle_payload(event_type, payload, event_id=event_id)

    def doctor_snapshot(self, jobs: list[Any] | None = None) -> dict[str, Any]:
        """Compact continue-plane health for doctor / control plane."""
        job_list = jobs
        if job_list is None and self._runtime is not None:
            orch = getattr(self._runtime, "orchestration", None)
            if orch is not None:
                job_list = list(orch.jobs.values())
        job_list = job_list or []
        open_owners = 0
        open_interests = 0
        wait_kinds: dict[str, int] = {}
        for job in job_list:
            rows = waiting_on_from_job(job)
            if not rows:
                continue
            open_owners += 1
            open_interests += len(rows)
            for row in rows:
                kind = str(row.get("kind") or "unknown")
                wait_kinds[kind] = wait_kinds.get(kind, 0) + 1
        return {
            "wait_plane_attached": self._matcher is not None,
            "wait_matcher_wired": self._matcher is not None,
            "open_wait_owners": open_owners,
            "open_wait_interests": open_interests,
            "wait_kinds": wait_kinds,
            "verbs": ["start", "continue"],
            "note": (
                "start = trigger → WorkIntent; continue = WaitPlaneService "
                "(VISION-0.55 / 0.55.10)"
            ),
        }

    def waiting_on_for_job(self, job: Any) -> list[dict[str, Any]]:
        return waiting_on_from_job(job)

    def waiting_on_summary_for_job(self, job: Any) -> dict[str, Any] | None:
        rows = waiting_on_from_job(job)
        return summarize_waiting_on(rows)


def bind_wait_plane_to_runtime(runtime: Any) -> WaitPlaneService:
    """Create and attach a :class:`WaitPlaneService` on ``runtime``."""
    plane = WaitPlaneService()
    plane.attach(runtime)
    return plane


__all__ = [
    "WaitPlaneService",
    "bind_wait_plane_to_runtime",
]
