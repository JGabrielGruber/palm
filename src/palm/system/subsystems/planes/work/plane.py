"""WorkPlaneService — first-class **start** plane (0.60.2).

Peer of wait (continue): trigger / schedule / enqueue → WorkIntent → tick → new job.
Runtimes attach this service at system boot. Continuous drain is a supervised
service (later slice) over :meth:`tick`.

See docs/VISION-0.60.md · ADR-029 · docs/WORK-DRAIN.md.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from palm.common.triggers.registry import TriggerRegistry
from palm.core.event import Event
from palm.core.work import WorkIntent
from palm.system.subsystems.planes.work.schedule import ScheduleRegistry
from palm.system.subsystems.planes.work.store import (
    DEFAULT_CLAIMER_ID,
    DEFAULT_LEASE_SECONDS,
    WorkIntentStore,
)

if TYPE_CHECKING:
    from palm.core.event import EventEngine
    from palm.core.storage import StorageEngine


class WorkPlaneService:
    """Start plane: WorkIntent queue + schedules + trigger attach + tick.

    Lifecycle:
    * :meth:`attach` — wire storage, submit callback, optional event bus
      (callers pass collaborators; no full runtime bag)
    * :meth:`detach` — clear bus subscriptions
    * :meth:`start_background` / :meth:`stop_background` — continuous tick
      (also registered on :class:`~palm.system.subsystems.supervisor.SystemSupervisor`)
    """

    def __init__(self) -> None:
        self._store: WorkIntentStore | None = None
        self._schedules: ScheduleRegistry | None = None
        self._triggers = TriggerRegistry()
        self._submit_flow: Callable[[str, dict[str, Any]], Any] | None = None
        # 0.63.23 — fail closed until install wires admission/started able.
        self._able: Callable[[], bool] = lambda: False
        self._max_depth = 8
        self._batch_size = 10
        self._poll_interval = 1.0
        self._lease_seconds = DEFAULT_LEASE_SECONDS
        self._claimer_id = DEFAULT_CLAIMER_ID
        self._workers = 1
        self._event_engine: EventEngine | None = None
        self._subs: list[Any] = []
        self._dropped_depth = 0
        self._reclaimed = 0
        self._stop = threading.Event()
        self._threads: list[threading.Thread] = []
        self._bg_started = False

    @property
    def is_attached(self) -> bool:
        return self._store is not None

    @property
    def store(self) -> WorkIntentStore:
        if self._store is None:
            raise RuntimeError("work plane not attached")
        return self._store

    @property
    def schedules(self) -> ScheduleRegistry:
        if self._schedules is None:
            raise RuntimeError("work plane not attached")
        return self._schedules

    @property
    def triggers(self) -> TriggerRegistry:
        return self._triggers

    @property
    def max_depth(self) -> int:
        return self._max_depth

    @property
    def dropped_depth_count(self) -> int:
        return self._dropped_depth

    def attach(
        self,
        *,
        storage: StorageEngine,
        submit_flow: Callable[[str, dict[str, Any]], Any],
        able: Callable[[], bool] | None = None,
        event: EventEngine | None = None,
        max_depth: int = 8,
        batch_size: int = 10,
        poll_interval: float = 1.0,
        lease_seconds: float = DEFAULT_LEASE_SECONDS,
        claimer_id: str = DEFAULT_CLAIMER_ID,
        workers: int = 1,
        attach_events: bool = True,
    ) -> None:
        """Wire storage and effectors. Callers own extraction from the machine."""
        if self._store is not None:
            self.detach()

        if not getattr(storage, "is_initialized", True):
            raise RuntimeError("work plane requires initialized storage")

        self._store = WorkIntentStore(storage)
        self._schedules = ScheduleRegistry(storage, self._store)
        self._max_depth = max(1, int(max_depth))
        self._batch_size = max(1, int(batch_size))
        self._poll_interval = max(0.05, float(poll_interval))
        self._lease_seconds = max(0.1, float(lease_seconds))
        self._claimer_id = str(claimer_id or DEFAULT_CLAIMER_ID)
        self._workers = max(1, int(workers))
        # 0.63.23 — omit able → refuse (was fail-open True).
        self._able = able if able is not None else (lambda: False)
        self._submit_flow = submit_flow
        self._dropped_depth = 0
        self._reclaimed = 0

        if attach_events and event is not None:
            if getattr(event, "is_initialized", False):
                self.attach_event_engine(event)

    def set_submit_flow(
        self, submit_flow: Callable[[str, dict[str, Any]], Any]
    ) -> None:
        """Replace submit callback (host session enrich may rebind)."""
        self._submit_flow = submit_flow

    def set_able(self, able: Callable[[], bool] | None) -> None:
        """Replace able gate (kernel: started ∧ ready ∧ work_drain after 0.67.2).

        ``None`` clears to fail-closed (0.63.23) — not soft-open True.
        """
        self._able = able if able is not None else (lambda: False)

    def configure(
        self,
        *,
        max_depth: int | None = None,
        batch_size: int | None = None,
        poll_interval: float | None = None,
        workers: int | None = None,
        lease_seconds: float | None = None,
    ) -> None:
        """Packaging knobs. Does not rebind submit/able."""
        if max_depth is not None:
            self._max_depth = max(1, int(max_depth))
        if batch_size is not None:
            self._batch_size = max(1, int(batch_size))
        if poll_interval is not None:
            self._poll_interval = max(0.05, float(poll_interval))
        if workers is not None:
            self._workers = max(1, int(workers))
        if lease_seconds is not None:
            self._lease_seconds = max(0.1, float(lease_seconds))

    def is_able(self) -> bool:
        """Whether tick may start business work (fail closed when false)."""
        try:
            return bool(self._able())
        except Exception:
            return False

    def detach(self) -> None:
        """Stop background, unsubscribe handlers, clear store handle."""
        self.stop_background()
        for unsub in self._subs:
            try:
                if callable(unsub):
                    unsub()
            except Exception:
                pass
        self._subs.clear()
        self._event_engine = None
        self._store = None
        self._schedules = None
        self._submit_flow = None
        self._triggers = TriggerRegistry()
        self._dropped_depth = 0
        self._reclaimed = 0

    def attach_event_engine(self, event_engine: EventEngine) -> None:
        """Subscribe start-path event types (resource / flow / workload)."""
        self._event_engine = event_engine
        if self._subs:
            return
        pairs = [
            ("resource.changed", self._on_resource_event),
            ("flow.session.succeeded", self._on_flow_event),
            ("workload.started", self._on_workload_event),
            ("workload.ready", self._on_workload_event),
            ("workload.failed", self._on_workload_event),
            ("workload.stopped", self._on_workload_event),
        ]
        for et, handler in pairs:
            sub = event_engine.subscribe(et, handler)
            self._subs.append(sub)

    def reload_triggers(
        self,
        flow_rows: list[dict[str, Any]],
        *,
        get_metadata: Any = None,
    ) -> int:
        n = self._triggers.reload_from_flow_rows(
            flow_rows, get_metadata=get_metadata
        )
        if self._schedules is not None:
            self._schedules.load_from_flow_rows(flow_rows, get_metadata=get_metadata)
        return n

    def reload_from_repository(self, repository: Any) -> int:
        """0.60.7 — arm triggers/schedules from a definition repository (hostless)."""
        try:
            flows = list(repository.list_flows() or [])
        except Exception:
            return 0
        rows: list[dict[str, Any]] = []
        by_name: dict[str, Any] = {}
        for flow in flows:
            name = str(getattr(flow, "name", "") or "").strip()
            if not name:
                continue
            by_name[name] = flow
            rows.append({"name": name})

        def _meta(name: str) -> dict[str, Any] | None:
            flow = by_name.get(name)
            if flow is None:
                return None
            meta = getattr(flow, "metadata", None)
            if isinstance(meta, dict) and (
                meta.get("triggers") or meta.get("schedule")
            ):
                return meta
            opts = getattr(flow, "options", None)
            if isinstance(opts, dict):
                return opts
            return meta if isinstance(meta, dict) else None

        return self.reload_triggers(rows, get_metadata=_meta)

    def enqueue(self, intent: WorkIntent) -> str:
        if self._store is None:
            raise RuntimeError("work plane not attached")
        if intent.depth > self._max_depth:
            self._dropped_depth += 1
            return ""
        return self._store.enqueue(intent)

    def tick_schedules(self) -> int:
        """Enqueue due schedules when the plane is able (drain membership).

        Same query as :meth:`tick`. Ready without ``work_drain`` does not
        advance the schedule clock (0.67.5). Background poll already skipped
        this when not able; the explicit path now matches.
        """
        if self._schedules is None:
            return 0
        if not self.is_able():
            return 0
        return len(self._schedules.tick(limit=self._batch_size))

    def tick(
        self,
        *,
        limit: int | None = None,
        claimer_id: str | None = None,
        reclaim: bool = True,
    ) -> int:
        """Claim and execute due work. Returns number of intents processed.

        Uses exclusive claim (``claimer_id`` + lease). Optional reclaim of
        expired leases runs first when ``reclaim`` is true.
        """
        if self._store is None or self._submit_flow is None:
            return 0
        # Admission gate: able includes admission after 0.63.3 (fail closed).
        if not self.is_able():
            return 0
        cid = str(claimer_id or self._claimer_id or DEFAULT_CLAIMER_ID)
        if reclaim:
            self._reclaimed += self._store.reclaim_expired()
        batch = self._batch_size if limit is None else max(1, int(limit))
        claimed = self._store.claim_due(
            limit=batch,
            claimer_id=cid,
            lease_seconds=self._lease_seconds,
        )
        done = 0
        for intent in claimed:
            try:
                if intent.kind == "run_flow":
                    self._submit_flow(intent.target, dict(intent.payload))
                else:
                    raise ValueError(f"unsupported work kind {intent.kind!r}")
                self._store.ack(intent.id, claimer_id=cid)
                done += 1
            except Exception as exc:
                self._store.fail(intent.id, str(exc), claimer_id=cid)
        return done

    @property
    def is_running(self) -> bool:
        if not self._bg_started:
            return False
        return any(t.is_alive() for t in self._threads)

    @property
    def workers(self) -> int:
        return self._workers

    def start_background(self) -> None:
        """Continuous poll loop(s). Supervisor start walks this.

        Starts ``workers`` daemon threads (default 1). Each thread has a
        distinct claimer id under exclusive claim (0.62).
        """
        if self._bg_started:
            return
        self._stop.clear()
        n = max(1, int(self._workers))
        base = self._claimer_id or DEFAULT_CLAIMER_ID
        self._threads = []
        for i in range(n):
            claimer = base if n == 1 else f"{base}-{i}"
            # Only worker 0 ticks schedules (avoid N schedule enqueues).
            th = threading.Thread(
                target=self._poll_loop,
                name=f"palm-work-plane-{i}" if n > 1 else "palm-work-plane",
                args=(claimer, i == 0),
                daemon=True,
            )
            th.start()
            self._threads.append(th)
        self._bg_started = True

    def stop_background(self, *, timeout: float = 2.0) -> None:
        if not self._bg_started:
            return
        self._stop.set()
        per = timeout / max(1, len(self._threads)) if self._threads else timeout
        for th in self._threads:
            th.join(timeout=per)
        self._threads = []
        self._bg_started = False

    def _poll_loop(self, claimer: str, tick_schedules: bool) -> None:
        # Stable claimer id for this continuous thread (0.62 exclusive claim).
        while not self._stop.wait(self._poll_interval):
            try:
                if not self.is_able():
                    continue
                if tick_schedules:
                    self.tick_schedules()
                self.tick(limit=self._batch_size, claimer_id=claimer, reclaim=True)
            except Exception:
                continue

    def status(self) -> dict[str, Any]:
        pending = 0
        if self._store is not None:
            try:
                pending = len(self._store.list_pending())
            except Exception:
                pending = -1
        alive = sum(1 for t in self._threads if t.is_alive())
        return {
            "attached": self.is_attached,
            "pending": pending,
            "dropped_depth": self._dropped_depth,
            "max_depth": self._max_depth,
            "batch_size": self._batch_size,
            "background": self.is_running,
            "able": self.is_able(),
            "trigger_count": len(getattr(self._triggers, "_specs", []) or []),
            "claimer_id": self._claimer_id,
            "lease_seconds": self._lease_seconds,
            "reclaimed": self._reclaimed,
            "workers": self._workers,
            "workers_alive": alive,
        }

    def _payload(self, event: Event) -> dict[str, Any]:
        if hasattr(event, "enriched_payload"):
            return dict(event.enriched_payload() or {})
        return dict(event.payload or {})

    def _on_resource_event(self, event: Event) -> None:
        for intent in self._triggers.on_event(event.type, self._payload(event)):
            self.enqueue(intent)

    def _on_flow_event(self, event: Event) -> None:
        for intent in self._triggers.on_event(event.type, self._payload(event)):
            self.enqueue(intent)

    def _on_workload_event(self, event: Event) -> None:
        for intent in self._triggers.on_event(event.type, self._payload(event)):
            self.enqueue(intent)


def make_submit_flow(
    *,
    submit: Callable[..., Any],
    get_session_plane: Callable[[], Any | None],
) -> Callable[[str, dict[str, Any]], Any]:
    """Build work submit from ports (CS-008) — no runtime bag.

    *submit* is ``(flow_id, metadata=…, state=…) -> result``.
    *get_session_plane* resolves the session plane at call time (after install).
    """

    def submit_flow(flow_id: str, payload: dict[str, Any]) -> Any:
        from palm.system.subsystems.planes.work.session_attr import attribute_reactive_start

        body = dict(payload or {})
        seed = body.pop("_seed_state", None)
        body = attribute_reactive_start(
            None,
            flow_id,
            body,
            session_plane=get_session_plane(),
        )
        state = seed
        if isinstance(seed, dict):
            from palm.states import BlackboardState

            state = BlackboardState()
            try:
                for k, v in seed.items():
                    state[k] = v
            except Exception:
                state = seed
        return submit(flow_id, metadata=body, state=state)

    return submit_flow


def default_submit_flow(
    runtime: Any,
) -> Callable[[str, dict[str, Any]], Any]:
    """Compat: extract ports from *runtime* then :func:`make_submit_flow`."""

    def _submit(
        flow_id: str,
        metadata: dict[str, Any] | None = None,
        state: Any = None,
    ) -> Any:
        return runtime.submit_flow(flow_id, metadata=metadata, state=state)

    return make_submit_flow(
        submit=_submit,
        get_session_plane=lambda: getattr(runtime, "session_plane", None),
    )


__all__ = ["WorkPlaneService", "default_submit_flow", "make_submit_flow"]
