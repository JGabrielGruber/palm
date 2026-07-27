"""Wait matcher — match runtime.event completer signals → resume/fail owner.

0.55.2: contract + policy. 0.55.4: normative unpark when wired on BaseRuntime.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from palm.common.wait.index import WaitOwnerIndex
from palm.common.wait.policy import (
    ACTION_FAIL_OWNER,
    ACTION_NOOP,
    ACTION_RESUME_OWNER,
    resolve_wait_action,
)
from palm.common.wait.signals import (
    MATCHER_EVENT_TYPES,
    TargetSignal,
    extract_signal_from_event,
    extract_target_signal,
)
from palm.core.wait import WaitInterest, close_wait_on_job, list_waits_on_job

if TYPE_CHECKING:
    from palm.core.event import Event, EventEngine


GetJob = Callable[[str], Any]
ListJobs = Callable[[], Iterable[Any]]
ResumeOwner = Callable[[str, WaitInterest, TargetSignal], None]
FailOwner = Callable[[str, WaitInterest, TargetSignal], None]


@dataclass(frozen=True, slots=True)
class MatchDisposition:
    """One owner reaction produced by a single target signal."""

    owner_job_id: str
    interest: WaitInterest
    signal: TargetSignal
    action: str


@dataclass
class WaitMatcher:
    """Subscribe to completer events; unpark or fail owners with open interest.

    * ``index`` — optional O(1) target → owners map.
    * ``list_jobs`` — scan live jobs for open interests (nested flow 0.55.3+).
    * ``get_job`` — load owner job; when set, interest is verified on ``job.state``.
    * ``resume_owner`` / ``fail_owner`` — side effects (orchestration resume / fail).
    """

    index: WaitOwnerIndex = field(default_factory=WaitOwnerIndex)
    get_job: GetJob | None = None
    list_jobs: ListJobs | None = None
    resume_owner: ResumeOwner | None = None
    fail_owner: FailOwner | None = None
    _subs: list[Any] = field(default_factory=list, repr=False)
    _event_engine: Any = field(default=None, repr=False)

    def attach_events(self, event_engine: EventEngine) -> None:
        """Subscribe to normative completer event types on ``runtime.event``."""
        self._event_engine = event_engine
        if self._subs:
            return
        for et in MATCHER_EVENT_TYPES:
            sub = event_engine.subscribe(et, self._on_event)
            self._subs.append(sub)

    def detach_events(self) -> None:
        for sub in self._subs:
            unsub = getattr(sub, "unsubscribe", None)
            if callable(unsub):
                unsub()
        self._subs.clear()

    def _on_event(self, event: Event) -> None:
        self.handle_event(event)

    def handle_event(self, event: Any) -> list[MatchDisposition]:
        signal = extract_signal_from_event(event)
        if signal is None:
            return []
        return self.handle_signal(signal)

    def handle_payload(
        self,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> list[MatchDisposition]:
        signal = extract_target_signal(event_type, payload)
        if signal is None:
            return []
        return self.handle_signal(signal)

    def handle_signal(self, signal: TargetSignal) -> list[MatchDisposition]:
        owner_ids = set(self.index.owners_for(kind=signal.kind, target_id=signal.target_id))
        owner_ids.update(self._scan_owners(signal))
        results: list[MatchDisposition] = []
        for owner_id in sorted(owner_ids):
            disp = self._match_one_owner(owner_id, signal)
            if disp is not None:
                results.append(disp)
        return results

    def _scan_owners(self, signal: TargetSignal) -> set[str]:
        """Discover owners by scanning live jobs' open wait interests."""
        if self.list_jobs is None:
            return set()
        found: set[str] = set()
        try:
            jobs = self.list_jobs()
        except Exception:
            return set()
        for job in jobs:
            try:
                waits = list_waits_on_job(job)
            except Exception:
                continue
            for w in waits:
                if w.matches(kind=signal.kind, target_id=signal.target_id):
                    jid = getattr(job, "id", None)
                    if jid:
                        found.add(str(jid))
                    break
        return found

    def _match_one_owner(
        self,
        owner_job_id: str,
        signal: TargetSignal,
    ) -> MatchDisposition | None:
        interest = self._resolve_open_interest(owner_job_id, signal)
        if interest is None:
            # Stale index entry — drop it.
            self.index.unregister(
                owner_job_id,
                kind=signal.kind,
                target_id=signal.target_id,
            )
            return None

        action = resolve_wait_action(interest, signal)
        if action == ACTION_NOOP:
            return MatchDisposition(
                owner_job_id=owner_job_id,
                interest=interest,
                signal=signal,
                action=ACTION_NOOP,
            )

        # Close first for double-event idempotency (0.55.6 hardens further).
        self._close_interest(owner_job_id, interest)

        if action == ACTION_RESUME_OWNER and self.resume_owner is not None:
            self.resume_owner(owner_job_id, interest, signal)
        elif action == ACTION_FAIL_OWNER and self.fail_owner is not None:
            self.fail_owner(owner_job_id, interest, signal)

        return MatchDisposition(
            owner_job_id=owner_job_id,
            interest=interest,
            signal=signal,
            action=action,
        )

    def _resolve_open_interest(
        self,
        owner_job_id: str,
        signal: TargetSignal,
    ) -> WaitInterest | None:
        if self.get_job is not None:
            try:
                job = self.get_job(owner_job_id)
            except Exception:
                return None
            if job is None:
                return None
            for w in list_waits_on_job(job):
                if w.matches(kind=signal.kind, target_id=signal.target_id):
                    return w
            return None
        # Index-only mode (contract tests without full job store): synthetic interest.
        return WaitInterest(kind=signal.kind, target_id=signal.target_id)

    def _close_interest(self, owner_job_id: str, interest: WaitInterest) -> None:
        self.index.unregister(
            owner_job_id,
            kind=interest.kind,
            target_id=interest.target_id,
        )
        if self.get_job is None:
            return
        try:
            job = self.get_job(owner_job_id)
        except Exception:
            return
        if job is None:
            return
        close_wait_on_job(job, kind=interest.kind, target_id=interest.target_id)


__all__ = [
    "MatchDisposition",
    "WaitMatcher",
]
