"""
WorkPlaneCoordinator (T2 / 0.48.3, seam 4) — owns the host's deferred-work plane.

Extracted from ``ApplicationHost``: the WorkIntent drain, inbound resource
bindings, and event-journal catch-up/redrive — their wiring, reload, tick, and
drain operations, plus the three slots (`_work_drain`/`_inbound`/`_event_journal`).
The host holds one of these and delegates; the public methods
(`reload_work_triggers`, `tick_work`, `drain_journal_*`, `redrive_journal`) keep
identical signatures.

Reads other host state (execution, definitions, runtime event engine, …) through
a back-reference, as ``HostObservability`` does; behaviour is preserved.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.app.host.workplane.work_drain_service import WorkDrainService
from palm.common.events import wire_event_journal as _wire_event_journal
from palm.common.events.consumers import consume_for_projections, consume_for_webhooks
from palm.system.subsystems.planes.work.inbound import InboundBindingService
from palm.system.subsystems.supervisor import CallableSystemService

if TYPE_CHECKING:
    from palm.app.host.application_host import ApplicationHost


class WorkPlaneCoordinator:
    """WorkIntent drain + inbound bindings + event-journal ops for the host."""

    def __init__(self, host: ApplicationHost) -> None:
        self._host = host
        self._work_drain: Any | None = None
        self._inbound: Any | None = None
        self._event_journal: Any | None = None

    @property
    def work_drain(self) -> Any | None:
        return self._work_drain

    @property
    def inbound(self) -> Any | None:
        return self._inbound

    @property
    def event_journal(self) -> Any | None:
        return self._event_journal

    @property
    def wait_plane(self) -> Any | None:
        """Continue plane on the bound runtime (0.55), if started."""
        try:
            runtime = self._host._app.runtime()
        except Exception:
            return None
        return getattr(runtime, "wait_plane", None)

    # ── wiring (called during host start) ────────────────────────────────────

    def wire_work_drain(self) -> None:
        """WorkIntent queue + trigger attach (0.37). Drain is explicit via tick().

        **0.60.5:** Prefer system ``runtime.work_plane`` when the spawned system
        already attached the start plane. Rebind submit for session enrich.
        Fall back to host :class:`WorkDrainService` when no plane is present.
        """
        host = self._host
        if not host._app.storage.is_initialized:
            return

        def _submit(flow_id: str, payload: dict[str, Any]) -> Any:
            body = dict(payload or {})
            seed = body.pop("_seed_state", None)
            submit_body: dict[str, Any] = {"flow_name": flow_id, "metadata": body}
            if seed is not None:
                submit_body["state"] = seed
            # SI-011 / 0.58.16: inherit-or-service — if the WorkIntent signal
            # carries a system session_id, keep that walk; else stable service
            # session by origin (work-drain / schedule / inbound). Never random
            # outside sess- for reactive start.
            session = getattr(host, "session", None) or getattr(host, "_session", None)
            if session is not None:
                if hasattr(session, "reactive_origin") and hasattr(
                    session, "enrich_reactive_start"
                ):
                    origin = session.reactive_origin(flow_id, body)
                    submit_body = session.enrich_reactive_start(
                        submit_body,
                        origin=origin,
                        surface="work-drain",
                    )
                elif hasattr(session, "enrich_submit_body"):
                    origin = f"work-drain:{flow_id}" if flow_id else "work-drain"
                    submit_body = session.enrich_submit_body(
                        submit_body,
                        surface="work-drain",
                        origin=origin,
                    )
            return host._execution.flows.submit_flow_body(submit_body)

        settings = host.settings
        plane = None
        try:
            runtime = host._app.runtime()
            plane = getattr(runtime, "work_plane", None)
        except Exception:
            plane = None

        if plane is not None and getattr(plane, "is_attached", False):
            # One start plane — host rebinds product submit + host-able gate.
            if hasattr(plane, "set_submit_flow"):
                plane.set_submit_flow(_submit)
            else:
                plane._submit_flow = _submit
            plane._able = lambda: bool(host._started)
            plane._max_depth = max(1, int(settings.work_drain_max_depth))
            plane._batch_size = max(1, int(settings.work_drain_batch_size))
            plane._poll_interval = max(
                0.05, float(settings.work_drain_poll_interval)
            )
            self._work_drain = plane
            self.reload_work_triggers()
            return

        self._work_drain = WorkDrainService(
            host._app.storage,
            submit_flow=_submit,
            event_engine=host._runtime_event_engine(),
            able=lambda: host._started,
            max_depth=int(settings.work_drain_max_depth),
            poll_interval=float(settings.work_drain_poll_interval),
            batch_size=int(settings.work_drain_batch_size),
        )
        job_events = host._runtime_event_engine()
        if job_events.is_initialized:
            self._work_drain.attach_events(job_events)
        # Load triggers from flow catalog (after examples/definitions already loaded)
        self.reload_work_triggers()

    def wire_inbound(self) -> None:
        """Inbound resource bindings (0.43) — metadata.inbound → WorkIntent."""
        host = self._host
        if self._work_drain is None:
            return

        def _list() -> list[dict[str, Any]]:
            try:
                return list(host._definitions.list_resources() or [])
            except Exception:
                return []

        def _get(name: str) -> dict[str, Any] | None:
            try:
                return host._definitions.get_resource(name)
            except Exception:
                return None

        def _enqueue(intent: Any) -> str:
            return self._work_drain.enqueue(intent)

        def _invoke(
            resource_ref: str,
            *,
            action: str | None = None,
            params: dict[str, Any] | None = None,
        ) -> Any:
            return host.invoke_resource(resource_ref, action=action, params=params)

        self._inbound = InboundBindingService(
            enqueue=_enqueue,
            event_engine=host._runtime_event_engine(),
            list_resources=_list,
            get_resource=_get,
            invoke_resource=_invoke,
        )
        self.reload_inbound_bindings()
        # 0.60.8 — register continuous inbound workers on the system supervisor.
        try:
            runtime = host._app.runtime()
            sup = getattr(runtime, "supervisor", None)
            if sup is not None:

                def _start() -> None:
                    self._inbound.start_workers()

                def _stop() -> None:
                    self._inbound.stop()

                sup.register(
                    CallableSystemService(
                        "inbound",
                        start=_start,
                        stop=_stop,
                        status=self._inbound.status,
                    )
                )
        except Exception:
            pass

    def wire_event_journal(self) -> None:
        host = self._host
        # 0.51.4: gated by the "journal" capability. The resolver always derives it
        # (journal has no settings flag), so this is behaviour-preserving for
        # settings-composed hosts; an explicit lean composition (e.g. embedded()) that
        # omits it correctly wires no journal.
        if not host.composition.has("journal"):
            return
        if not host._app.storage.is_initialized:
            return
        if not host._event.is_initialized:
            return
        journal, _sub = _wire_event_journal(host._event, host._app.storage)
        self._event_journal = journal

    # ── reload / tick / drain (public host API delegates here) ───────────────

    def reload_work_triggers(self) -> int:
        """Reload definition triggers into the work drain (after design/example load).

        **0.60.7:** when the drain is the system work plane and product
        definitions are unavailable, fall back to the runtime definition
        repository on the system instance.
        """
        host = self._host
        if self._work_drain is None:
            return 0
        try:
            rows = host._definitions.list_flows() or []

            def _meta(name: str) -> dict[str, Any] | None:
                try:
                    detail = host._definitions.get_flow(name, verbose=True)
                except Exception:
                    return None
                if not isinstance(detail, dict):
                    return None
                # Prefer explicit metadata; else options (examples put triggers there).
                meta = detail.get("metadata")
                if isinstance(meta, dict) and meta.get("triggers"):
                    return meta
                opts = detail.get("options")
                return opts if isinstance(opts, dict) else meta

            return int(self._work_drain.reload_triggers(rows, get_metadata=_meta) or 0)
        except Exception:
            # Hostless / product-thin: repository on the system instance.
            plane = self._work_drain
            if hasattr(plane, "reload_from_repository"):
                try:
                    runtime = host._app.runtime()
                    repo = getattr(runtime, "repository", None)
                    if repo is not None:
                        return int(plane.reload_from_repository(repo) or 0)
                except Exception:
                    return 0
            return 0

    def reload_inbound_bindings(self) -> int:
        """Rescan resources with metadata.inbound (0.43)."""
        if self._inbound is None:
            return 0
        try:
            n = int(self._inbound.reload_from_definitions() or 0)
            # Prefer supervisor start when inbound is registered (0.60.8).
            try:
                runtime = self._host._app.runtime()
                sup = getattr(runtime, "supervisor", None)
                if sup is not None and sup.get("inbound") is not None:
                    sup.start("inbound")
                    return n
            except Exception:
                pass
            self._inbound.start_workers()
            return n
        except Exception:
            return 0

    def tick_work(self, *, limit: int = 10, schedules: bool = True) -> int:
        """Process due WorkIntents (and optional schedule triggers). Returns count."""
        if self._inbound is not None:
            self._inbound.flush_debounced()
        if self._work_drain is None:
            return 0
        n = 0
        if schedules:
            n += self._work_drain.tick_schedules()
        n += self._work_drain.tick(limit=limit)
        return n

    def drain_journal_webhooks(self, *, limit: int = 50, on_entry: Any | None = None) -> int:
        """Catch-up webhooks consumer from journal (0.40.3). Returns entries processed."""
        if self._event_journal is None:
            return 0
        count = 0

        def _handler(entry: Any) -> None:
            nonlocal count
            count += 1
            if on_entry is not None:
                on_entry(entry)

        consume_for_webhooks(self._event_journal, _handler, limit=limit)
        return count

    def drain_journal_projections(self, *, limit: int = 50, on_entry: Any | None = None) -> int:
        """Catch-up projections consumer from journal (0.40.3)."""
        if self._event_journal is None:
            return 0
        count = 0

        def _handler(entry: Any) -> None:
            nonlocal count
            count += 1
            if on_entry is not None:
                on_entry(entry)

        consume_for_projections(self._event_journal, _handler, limit=limit)
        return count

    def redrive_journal(
        self,
        *,
        from_offset: int = 0,
        to_offset: int | None = None,
        event_types: list[str] | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Replay journal entries for operator tooling (does not move consumer offsets)."""
        if self._event_journal is None:
            return []
        types = frozenset(event_types) if event_types else None
        entries = self._event_journal.redrive(
            from_offset=from_offset,
            to_offset=to_offset,
            event_types=types,
            limit=limit,
        )
        return [e.to_dict() for e in entries]

    # ── background lifecycle (called from host start/shutdown) ───────────────

    def start_background(self) -> None:
        # Prefer supervisor when the system registered work_drain (0.60.5).
        try:
            runtime = self._host._app.runtime()
            sup = getattr(runtime, "supervisor", None)
            if sup is not None and sup.get("work_drain") is not None:
                sup.start("work_drain")
                return
        except Exception:
            pass
        if self._work_drain is not None:
            self._work_drain.start_background()

    def stop_background(self) -> None:
        try:
            runtime = self._host._app.runtime()
            sup = getattr(runtime, "supervisor", None)
            if sup is not None and sup.get("work_drain") is not None:
                sup.stop("work_drain")
                return
        except Exception:
            pass
        if self._work_drain is not None:
            self._work_drain.stop_background()

    def stop_inbound(self) -> None:
        try:
            runtime = self._host._app.runtime()
            sup = getattr(runtime, "supervisor", None)
            if sup is not None and sup.get("inbound") is not None:
                sup.stop("inbound")
                return
        except Exception:
            pass
        if self._inbound is not None:
            try:
                self._inbound.stop()
            except Exception:
                pass


__all__ = ["WorkPlaneCoordinator"]
