"""
RecoveryCoordinator (T2 / 0.48.4, seam 5) — host startup recovery.

Worker readiness, compensation, webhook dispatcher seat, and projection rebuild.
Outbox loop start lives on ``system.background.start`` (0.65.2).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from palm.app.host.events import HostEventType
from palm.app.host.workers import WorkerCoordinator
from palm.common.compensation import CompensationCoordinator, default_compensation_registry
from palm.common.cqrs.rebuild import ProjectionRebuildPolicy
from palm.common.events.external import WebhookDispatcher, webhook_targets_from_urls
from palm.core.structure import CAPABILITY_PROJECTIONS

if TYPE_CHECKING:
    from palm.app.host.application_host import ApplicationHost

_log = logging.getLogger(__name__)


class RecoveryCoordinator:
    """Worker readiness, compensation, webhook seat, and projection rebuild."""

    def __init__(self, host: ApplicationHost) -> None:
        self._host = host
        self._compensation: CompensationCoordinator | None = None
        self._webhook_dispatcher: WebhookDispatcher | None = None
        self._last_recovery: dict[str, Any] | None = None

    @property
    def compensation(self) -> CompensationCoordinator | None:
        return self._compensation

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

        self._build_webhook_dispatcher()
        try:
            store = host._app.runtime().outbox_store
            if store is not None:
                recovery["outbox_pending"] = store.pending_count()
        except Exception:
            # Documented ignore: pending count is status-only (CS-005).
            _log.debug("outbox pending count failed", exc_info=True)

        # 0.67.9: no projection layer (DNA omit) → nothing to rebuild.
        if (
            host.admission.has_capability(CAPABILITY_PROJECTIONS)
            and host.settings.rebuild_projections_on_startup
        ):
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
        if self._compensation is not None:
            self._compensation.shutdown()
            self._compensation = None


__all__ = ["RecoveryCoordinator"]
