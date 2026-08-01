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
from palm.system.planes.work.schedule import ScheduleRegistry
from palm.system.planes.work.store import WorkIntentStore

if TYPE_CHECKING:
    from palm.core.event import EventEngine
    from palm.core.storage import StorageEngine


class WorkPlaneService:
    """Start plane: WorkIntent queue + schedules + trigger attach + tick.

    Lifecycle:
    * :meth:`attach` — bind storage, submit callback, optional event bus
    * :meth:`detach` — clear bus subscriptions
    * :meth:`start_background` / :meth:`stop_background` — continuous tick
      (also registered on :class:`~palm.system.supervisor.SystemSupervisor`)
    """

    def __init__(self) -> None:
        self._store: WorkIntentStore | None = None
        self._schedules: ScheduleRegistry | None = None
        self._triggers = TriggerRegistry()
        self._submit_flow: Callable[[str, dict[str, Any]], Any] | None = None
        self._able: Callable[[], bool] = lambda: True
        self._max_depth = 8
        self._batch_size = 10
        self._poll_interval = 1.0
        self._event_engine: EventEngine | None = None
        self._subs: list[Any] = []
        self._dropped_depth = 0
        self._runtime: Any | None = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
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
        runtime: Any,
        *,
        submit_flow: Callable[[str, dict[str, Any]], Any] | None = None,
        able: Callable[[], bool] | None = None,
        max_depth: int = 8,
        batch_size: int = 10,
        poll_interval: float = 1.0,
        attach_events: bool = True,
    ) -> None:
        """Bind storage and effectors on a started (or starting) system instance."""
        if self._store is not None:
            self.detach()

        storage: StorageEngine = runtime.storage
        if not getattr(storage, "is_initialized", True):
            raise RuntimeError("work plane requires initialized storage")

        self._runtime = runtime
        self._store = WorkIntentStore(storage)
        self._schedules = ScheduleRegistry(storage, self._store)
        self._max_depth = max(1, int(max_depth))
        self._batch_size = max(1, int(batch_size))
        self._poll_interval = max(0.05, float(poll_interval))
        self._able = able or (lambda: bool(getattr(runtime, "is_started", True)))
        self._submit_flow = submit_flow or _default_submit(runtime)
        self._dropped_depth = 0

        if attach_events:
            event = getattr(runtime, "event", None)
            if event is not None and getattr(event, "is_initialized", False):
                self.attach_event_engine(event)

    def set_submit_flow(
        self, submit_flow: Callable[[str, dict[str, Any]], Any]
    ) -> None:
        """Replace submit callback (host session enrich may rebind)."""
        self._submit_flow = submit_flow

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
        self._runtime = None
        self._triggers = TriggerRegistry()
        self._dropped_depth = 0

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
        if self._schedules is None:
            return 0
        return len(self._schedules.tick(limit=self._batch_size))

    def tick(self, *, limit: int | None = None) -> int:
        """Claim and execute due work. Returns number of intents processed."""
        if self._store is None or self._submit_flow is None:
            return 0
        if not self._able():
            return 0
        batch = self._batch_size if limit is None else max(1, int(limit))
        claimed = self._store.claim_due(limit=batch)
        done = 0
        for intent in claimed:
            try:
                if intent.kind == "run_flow":
                    self._submit_flow(intent.target, dict(intent.payload))
                else:
                    raise ValueError(f"unsupported work kind {intent.kind!r}")
                self._store.ack(intent.id)
                done += 1
            except Exception as exc:
                self._store.fail(intent.id, str(exc))
        return done

    @property
    def is_running(self) -> bool:
        return (
            self._bg_started
            and self._thread is not None
            and self._thread.is_alive()
        )

    def start_background(self) -> None:
        """Continuous poll loop (supervisor or host may call)."""
        if self._bg_started:
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._poll_loop,
            name="palm-work-plane",
            daemon=True,
        )
        self._thread.start()
        self._bg_started = True

    def stop_background(self, *, timeout: float = 2.0) -> None:
        if not self._bg_started:
            return
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
        self._thread = None
        self._bg_started = False

    def _poll_loop(self) -> None:
        while not self._stop.wait(self._poll_interval):
            try:
                if not self._able():
                    continue
                self.tick_schedules()
                self.tick(limit=self._batch_size)
            except Exception:
                continue

    def status(self) -> dict[str, Any]:
        pending = 0
        if self._store is not None:
            try:
                pending = len(self._store.list_pending())
            except Exception:
                pending = -1
        return {
            "attached": self.is_attached,
            "pending": pending,
            "dropped_depth": self._dropped_depth,
            "max_depth": self._max_depth,
            "batch_size": self._batch_size,
            "background": self.is_running,
            "trigger_count": len(getattr(self._triggers, "_specs", []) or []),
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


def _default_submit(
    runtime: Any,
) -> Callable[[str, dict[str, Any]], Any]:
    """Submit via system executor — product façade not required.

    **0.60.4:** attribute reactive session on the system path (session plane).
    """

    def submit(flow_id: str, payload: dict[str, Any]) -> Any:
        from palm.system.planes.work.session_attr import attribute_reactive_start

        body = dict(payload or {})
        seed = body.pop("_seed_state", None)
        body = attribute_reactive_start(runtime, flow_id, body)
        state = seed
        if isinstance(seed, dict):
            from palm.states import BlackboardState

            state = BlackboardState()
            # Best-effort: many seeds are plain dict overlays.
            try:
                for k, v in seed.items():
                    state[k] = v
            except Exception:
                state = seed
        return runtime.submit_flow(flow_id, metadata=body, state=state)

    return submit


__all__ = ["WorkPlaneService"]
