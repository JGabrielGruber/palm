"""
HostObservability — residual packaging status for ApplicationHost (CS-002).

0.48.1 (PD-018): extracted the three status reports from the composition root.
0.61.7 (CS-002): demoted — these bags are **host packaging residual**, not
living-load law. Living eyes live in ``palm.system.vitality`` and are
presented via ``InspectService.top`` / ``.vitality``.

Public host methods ``event_plane_status`` / ``ops_status`` /
``control_plane_status`` remain thin residual aliases for consumers.
Prefer :meth:`packaging_status` when a single packaging bag is needed.

Do **not** grow a fourth host status method as living truth.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.app.cli_settings import is_durable_storage
from palm.app.host.boot.modes import list_boot_modes
from palm.common.events.consumers import DEFAULT_JOURNAL_CONSUMERS, journal_consumer_status
from palm.common.resource.document_storage import resolve_kv_backend
from palm.system.boot import schedule_catalog
from palm.system.log import get_system_log

if TYPE_CHECKING:
    from palm.app.host.application_host import ApplicationHost

# CS-002 demotion markers — packaging residual, not seat / vitality law.
PACKAGING_ROLE = "host_packaging"
EYES_LAW = "palm.system.vitality"
OPERATE_EYES_PATHS = (
    "inspect/top",
    "inspect/vitality",
    "assist/top",
    "assist/vitality",
)
PACKAGING_NOTE = (
    "Host packaging residual (CS-002). Living load eyes: InspectService.top / "
    "vitality → palm.system.vitality. Do not treat this bag as seat law."
)


def _with_packaging_markers(
    bag: dict[str, Any],
    *,
    extra_note: str | None = None,
) -> dict[str, Any]:
    """Stamp demotion markers; preserve domain notes when present."""
    out = dict(bag)
    out["role"] = PACKAGING_ROLE
    out["eyes_law"] = EYES_LAW
    out["operate_paths"] = list(OPERATE_EYES_PATHS)
    domain = extra_note if extra_note is not None else bag.get("note")
    if isinstance(domain, str) and domain.strip() and domain.strip() != PACKAGING_NOTE:
        out["note"] = f"{PACKAGING_NOTE} | {domain}"
    else:
        out["note"] = PACKAGING_NOTE
    return out


class HostObservability:
    """Owns residual host packaging reports (not living vitality)."""

    def __init__(self, host: ApplicationHost) -> None:
        self._host = host

    def packaging_status(self) -> dict[str, Any]:
        """Single residual packaging bag (control-plane body + demotion).

        Prefer this over the triple method names for new packaging consumers.
        Living eyes remain ``inspect.top`` / ``inspect.vitality``.
        """
        return self.control_plane_status()

    def event_plane_status(self) -> dict[str, Any]:
        """Residual bus/packaging map (0.45.5). Not living seat law."""
        host = self._host
        orchestration_bus = "host_fallback"
        try:
            runtime = host._app.runtime()
            engine = runtime.event
            if engine is not None and engine.is_initialized:
                orchestration_bus = "runtime"
        except Exception:
            pass
        internal_bindings = 0
        if host.inbound is not None:
            try:
                internal_bindings = sum(
                    1 for row in host.inbound.list_bindings() if row.get("mode") == "internal"
                )
            except Exception:
                internal_bindings = 0
        slog = get_system_log()
        domain_note = (
            "Orchestration events emit on runtime.event when the runtime is "
            "started; host.event is coordination only (host.started, journal, "
            "outbox). Internal inbound and work-drain subscribe to the "
            "orchestration bus. system_log_* is process narrative (0.59.1a), "
            "not the domain event bus."
        )
        return _with_packaging_markers(
            {
                "orchestration_bus": orchestration_bus,
                "host_coordination_bus": "host",
                "inbound_internal_bus": orchestration_bus,
                "work_drain_bus": orchestration_bus,
                "journal_bus": "host",
                "internal_inbound_bindings": internal_bindings,
                "orchestration_event_types": [
                    "job.completed",
                    "flow.session.succeeded",
                    "flow.session.failed",
                ],
                "system_log_level": slog.level,
                "system_log_recent": [r.to_dict() for r in slog.recent(limit=15)],
            },
            extra_note=domain_note,
        )

    def ops_status(self) -> dict[str, Any]:
        """Residual operator ergonomics packaging (0.45.8). Not living seat law."""
        host = self._host
        storage = host._app.storage
        backend_name = storage.backend_name if storage is not None else None
        durable = is_durable_storage(backend_name)
        event_log_durable: bool | None = None
        event_log_note: str | None = None
        try:
            described = host._definitions.get_resource("palm-system-event-log")
        except Exception:
            described = None
        if isinstance(described, dict):
            params = described.get("params") if isinstance(described.get("params"), dict) else {}
            kv_param = str((params or {}).get("backend") or "auto")
            try:
                resolved = resolve_kv_backend(
                    kv_param,
                    storage=storage,
                    storage_backend_name=backend_name,
                )
                event_log_durable = resolved != "memory"
            except ValueError:
                event_log_durable = False
            if event_log_durable is False:
                event_log_note = (
                    "palm-system-event-log resolves to memory kv; use "
                    "PALM_STORAGE_BACKEND=filesystem or params.backend=storage "
                    "for durable ops tail"
                )
        server_hint: str | None = None
        if host.profile.server and not durable:
            server_hint = (
                "server profile: set PALM_STORAGE_BACKEND=filesystem (or postgres) "
                "so instances, kv tails, and work queue survive restart"
            )
        return _with_packaging_markers(
            {
                "invoke_route": "POST /v1/api/providers/{provider}/{resource_ref}/invoke",
                "invoke_route_short": "POST /v1/api/resources/{resource_ref}/invoke",
                "storage_backend": backend_name,
                "storage_durable": durable,
                "event_log_durable": event_log_durable,
                "event_log_note": event_log_note,
                "server_profile_hint": server_hint,
            }
        )

    def control_plane_status(self) -> dict[str, Any]:
        """Residual work/journal/boot packaging (0.38 / 0.40.3). Not living seat law."""
        host = self._host
        work_pending = 0
        if host.work_drain is not None:
            work_pending = host.work_drain.store.pending_count()
        journal_status: dict[str, Any] = {}
        if host.event_journal is not None:
            journal_status = journal_consumer_status(
                host.event_journal,
                consumers=list(DEFAULT_JOURNAL_CONSUMERS),
            )
        outbox_pending = 0
        if host.outbox_service is not None:
            outbox_pending = host.outbox_service.store.pending_count()
        bg = False
        dropped = 0
        if host.work_drain is not None:
            bg = bool(host.work_drain.is_running)
            dropped = int(host.work_drain.dropped_depth_count)
        schedules: list[dict[str, Any]] = []
        if host.work_drain is not None:
            try:
                schedules = list(host.work_drain.schedules.list_entries())
            except Exception:
                schedules = []
        inbound_bindings: list[dict[str, Any]] = []
        if host.inbound is not None:
            try:
                inbound_bindings = list(host.inbound.list_bindings())
            except Exception:
                inbound_bindings = []
        boot_mode = getattr(host, "boot_mode", None)
        domain_note = (
            "0.59.7 mode dogfood: ApplicationHost.for_mode('test'|'safe'|shapes); "
            "server/prod CI use server_port=0. CompositionProfile is the sole "
            "membership switch (0.59.5); deployment feeds resolver only; "
            "modes + PhaseSkip strictness."
        )
        return _with_packaging_markers(
            {
                "work_pending": work_pending,
                "work_drain_running": bg,
                # Residual alias (compat); same as work_drain_running.
                "work_drain_background": bg,
                "work_dropped_depth": dropped,
                "schedules": schedules,
                "schedule_count": len(schedules),
                "outbox_pending": outbox_pending,
                "journal": journal_status,
                "journal_consumers": list(DEFAULT_JOURNAL_CONSUMERS),
                "inbound_bindings": inbound_bindings,
                "inbound_count": len(inbound_bindings),
                "boot": {
                    "mode": None if boot_mode is None else boot_mode.name,
                    "mode_detail": None if boot_mode is None else boot_mode.to_dict(),
                    "modes_available": list(list_boot_modes()),
                    "phase_tables": schedule_catalog(),
                    "membership": host.membership_snapshot(),
                    "last_walk": getattr(host, "boot_walk", None),
                    "note": domain_note,
                },
                "event_plane": self.event_plane_status(),
                "ops": self.ops_status(),
            },
            extra_note=domain_note,
        )


__all__ = [
    "HostObservability",
    "PACKAGING_ROLE",
    "EYES_LAW",
    "OPERATE_EYES_PATHS",
    "PACKAGING_NOTE",
]
