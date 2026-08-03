"""
RecoveryCoordinator (T2 / 0.48.4, seam 5) — host startup recovery + background services.

Extracted from ``ApplicationHost._recover`` and the outbox/webhook build: worker
readiness, compensation, the outbox background service, webhook dispatcher, and
projection rebuild. Owns the ``compensation``/``outbox_service``/
``webhook_dispatcher``/``last_recovery`` slots; reads other host state through a
back-reference. Behaviour-preserving.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.app.host.events import HostEventType
from palm.app.host.outbox_service import OutboxBackgroundService
from palm.app.host.workers import WorkerCoordinator
from palm.common.compensation import CompensationCoordinator, default_compensation_registry
from palm.common.cqrs.rebuild import ProjectionRebuildPolicy
from palm.common.events.external import WebhookDispatcher, webhook_targets_from_urls

if TYPE_CHECKING:
    from palm.app.host.application_host import ApplicationHost
    from palm.common.events import OutboxProcessor, OutboxStore


class _SupervisorOutboxFacade:
    """Host-facing store/process handle when outbox runs under system supervisor."""

    def __init__(
        self,
        store: OutboxStore,
        processor: OutboxProcessor,
        *,
        batch_size: int = 50,
    ) -> None:
        self._store = store
        self._processor = processor
        self._batch_size = max(1, int(batch_size))

    @property
    def store(self) -> OutboxStore:
        return self._store

    @property
    def processor(self) -> OutboxProcessor:
        return self._processor

    def process_once(self) -> int:
        return self._processor.process_batch(limit=self._batch_size)

    def start(self, *, recover: bool = True) -> None:
        return None

    def stop(self, *, timeout: float = 2.0) -> None:
        return None


class RecoveryCoordinator:
    """Worker readiness, compensation, outbox/webhook, and projection rebuild."""

    def __init__(self, host: ApplicationHost) -> None:
        self._host = host
        self._compensation: CompensationCoordinator | None = None
        self._outbox_service: OutboxBackgroundService | _SupervisorOutboxFacade | None = (
            None
        )
        self._outbox_via_supervisor: bool = False
        self._webhook_dispatcher: WebhookDispatcher | None = None
        self._last_recovery: dict[str, Any] | None = None

    @property
    def compensation(self) -> CompensationCoordinator | None:
        return self._compensation

    @property
    def outbox_service(self) -> OutboxBackgroundService | None:
        return self._outbox_service

    @property
    def webhook_dispatcher(self) -> WebhookDispatcher | None:
        return self._webhook_dispatcher

    @property
    def last_recovery(self) -> dict[str, Any] | None:
        return self._last_recovery

    def recover(self) -> None:
        host = self._host
        recovery: dict[str, Any] = {}

        coordinator = host._worker_coordinator or WorkerCoordinator(host.profile, host._event)
        host._worker_coordinator = coordinator
        workers_ready = coordinator.wait_until_ready(
            host._app,
            timeout=host.settings.worker_ready_timeout,
        )
        recovery["workers_ready"] = workers_ready
        recovery["workers"] = list(coordinator.registered_workers)

        # 0.51.2: gated by the composition's capability axis. On the default path this
        # equals settings.enable_compensation (the resolver derives it from that flag);
        # an explicit composition that omits "compensation" wins (capabilities authoritative).
        if host.composition.has("compensation"):
            self._compensation = CompensationCoordinator(
                default_compensation_registry(),
                host._event,
            )
            self._compensation.attach(host._event)
            self._compensation.attach_runtimes(host._app)

        # 0.51.3: available-and-activated — the composition declares the "outbox" capability
        # is available (derived from settings.enable_event_outbox); the deployment role
        # decides whether this node runs the drainer. Don't drain an outbox you don't have.
        if (
            host.composition.has("outbox")
            and host.profile.master
            and host.profile.enable_outbox_service
        ):
            self._start_outbox_service()
            if self._outbox_service is not None:
                recovery["outbox_pending"] = self._outbox_service.store.pending_count()
            elif self._outbox_via_supervisor:
                try:
                    store = host._app.runtime().outbox_store
                    if store is not None:
                        recovery["outbox_pending"] = store.pending_count()
                        recovery["outbox_via"] = "supervisor"
                except Exception:
                    pass

        # 0.51.5: no projection layer (lean composition) → nothing to rebuild.
        if host.composition.has("projections") and host.settings.rebuild_projections_on_startup:
            report = host._projection_manager.rebuild_all(
                policy=ProjectionRebuildPolicy(
                    batch_size=host.settings.projection_rebuild_batch_size,
                    max_instances=host.settings.projection_rebuild_max_instances,
                    skip_if_fresh=host.settings.projection_rebuild_skip_if_fresh,
                )
            )
            recovery["projections"] = report.to_dict()

        if recovery:
            self._last_recovery = dict(recovery)
            host._event.emit(HostEventType.RECOVERED, **recovery)

    def _start_outbox_service(self) -> None:
        host = self._host
        if not host._app.storage.is_initialized:
            return
        dispatcher = self._build_webhook_dispatcher()
        # 0.60.6: prefer system supervisor outbox when no host webhook targets.
        if dispatcher is None:
            try:
                runtime = host._app.runtime()
                sup = getattr(runtime, "supervisor", None)
                if sup is not None and sup.get("outbox") is not None:
                    # Align poll settings if the service exposes them.
                    svc = sup.get("outbox")
                    if hasattr(svc, "_poll_interval"):
                        svc._poll_interval = max(
                            0.05, float(host.profile.outbox_poll_interval)
                        )
                    if hasattr(svc, "_recover_on_start"):
                        svc._recover_on_start = bool(
                            host.profile.outbox_recover_on_startup
                        )
                    sup.start("outbox")
                    self._outbox_via_supervisor = True
                    # Host API still exposes store / process_once for tests and ops.
                    store = getattr(runtime, "outbox_store", None)
                    proc = getattr(runtime, "outbox_processor", None)
                    if store is not None and proc is not None:
                        self._outbox_service = _SupervisorOutboxFacade(
                            store,
                            proc,
                            batch_size=int(
                                getattr(svc, "_batch_size", 50) or 50
                            ),
                        )
                    return
            except Exception:
                pass
        self._outbox_service = OutboxBackgroundService(
            host._app.storage,
            host._event,
            poll_interval=host.profile.outbox_poll_interval,
            external_dispatcher=dispatcher,
        )
        self._outbox_service.start(recover=host.profile.outbox_recover_on_startup)

    def _build_webhook_dispatcher(self) -> WebhookDispatcher | None:
        host = self._host
        # 0.51.2: the "webhook" capability gates availability (derived from
        # settings.enable_webhook_dispatcher on the default path); settings.webhook_urls
        # still configure the targets — settings refine within the capability, never bypass it.
        if not host.composition.has("webhook"):
            return None
        if not host.settings.webhook_urls:
            return None
        self._webhook_dispatcher = WebhookDispatcher(
            webhook_targets_from_urls(
                host.settings.webhook_urls,
                event_types=host.settings.webhook_event_types or None,
            )
        )
        return self._webhook_dispatcher

    def stop(self) -> None:
        if self._outbox_via_supervisor:
            try:
                sup = self._host._app.runtime().supervisor
                if sup is not None and sup.get("outbox") is not None:
                    sup.stop("outbox")
            except Exception:
                pass
            self._outbox_via_supervisor = False
            # Facade only — do not treat as host-owned background thread.
            self._outbox_service = None
        elif self._outbox_service is not None:
            self._outbox_service.stop()
            self._outbox_service = None
        if self._compensation is not None:
            self._compensation.shutdown()
            self._compensation = None


__all__ = ["RecoveryCoordinator"]
