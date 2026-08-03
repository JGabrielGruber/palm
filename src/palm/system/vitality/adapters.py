"""
Seat sampling for vitality walk (0.61.1+).

**Law:** system vitality **samples raw** from public seat APIs. It does not
curate doctor fields into vitality ``load`` as truth. Product present
(Inspect / top) interprets ``meta.raw``.

| lineage | Meaning |
|---------|---------|
| ``sampled`` | Eyes called a public API; payload in ``meta.raw`` |
| ``native``  | Seat implemented ``seat_report()`` (optional growth) |
| ``adapter`` | Residual *interpret* bridges only — do not grow |

Prefer native when a seat truly owns a report. Otherwise sample raw.
Do not put vitality schema methods on simple seats (e.g. SystemLog).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from palm.system.vitality.protocol import try_native_report
from palm.system.vitality.report import SeatReport, coerce_report
from palm.system.vitality.schema import (
    KIND_BOOT,
    KIND_LOG,
    KIND_PLANE,
    KIND_PORT,
    KIND_SUPERVISOR,
    KIND_SUPERVISOR_SERVICE,
    LINEAGE_NATIVE,
    LINEAGE_SAMPLED,
    SEAT_BOOT_MEMBERSHIP,
    SEAT_EXECUTION,
    SEAT_SESSION_PLANE,
    SEAT_SUPERVISOR,
    SEAT_SYSTEM_LOG,
    SEAT_WAIT_PLANE,
    SEAT_WORK_PLANE,
    STATE_OK,
    supervisor_service_seat_id,
)


def _raw_meta(source: str, raw: Mapping[str, Any] | None, **extra: Any) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "sample_source": source,
        "raw": dict(raw or {}),
    }
    meta.update({k: v for k, v in extra.items() if v is not None})
    return meta


def sample_raw(
    seat_id: str,
    kind: str,
    *,
    source: str,
    raw: Mapping[str, Any] | None = None,
    notes: list[str] | tuple[str, ...] | None = None,
    present: bool = True,
    state: str = STATE_OK,
    extra_meta: Mapping[str, Any] | None = None,
) -> SeatReport:
    """Build a seat report that carries **raw** for product present.

    System vitality keeps structural fields only (id, kind, present, state).
    ``load`` stays empty unless a later native path fills vitality terms.
    """
    meta = _raw_meta(source, raw)
    if extra_meta:
        meta.update(dict(extra_meta))
    return SeatReport(
        seat_id=seat_id,
        kind=kind,
        present=present,
        state=state,
        load={},
        notes=list(notes or []),
        lineage=LINEAGE_SAMPLED,
        meta=meta,
    )


def prefer_native(
    seat: Any,
    *,
    seat_id: str,
    kind: str,
    sampler: Callable[[], SeatReport],
) -> SeatReport:
    """Use native ``seat_report`` when present; otherwise run *sampler* (raw)."""
    native = try_native_report(seat)
    if native is not None:
        report = coerce_report(
            native,
            default_seat_id=seat_id,
            default_kind=kind,
            default_lineage=LINEAGE_NATIVE,
        )
        if report.lineage != LINEAGE_NATIVE:
            report = SeatReport(
                seat_id=report.seat_id or seat_id,
                kind=report.kind or kind,
                present=report.present,
                state=report.state,
                load=dict(report.load),
                notes=list(report.notes),
                lineage=LINEAGE_NATIVE,
                schema=report.schema,
                meta={**report.meta, "lineage_forced": "native"},
                sample_ts=report.sample_ts,
            )
        if report.seat_id != seat_id:
            report = SeatReport(
                seat_id=seat_id,
                kind=report.kind or kind,
                present=report.present,
                state=report.state,
                load=dict(report.load),
                notes=list(report.notes) + [f"native_seat_id_was:{report.seat_id}"],
                lineage=LINEAGE_NATIVE,
                schema=report.schema,
                meta=dict(report.meta),
                sample_ts=report.sample_ts,
            )
        return report
    return sampler()


# ── plane samples (raw public doctor/status — no field curation) ─────────────


def adapt_wait_plane(instance: Any, plane: Any) -> SeatReport:
    def _sample() -> SeatReport:
        try:
            snap = plane.doctor_snapshot()
            if not isinstance(snap, Mapping):
                snap = {"_non_mapping": type(snap).__name__}
        except Exception as exc:
            return SeatReport.error(
                SEAT_WAIT_PLANE,
                KIND_PLANE,
                reason=f"doctor_snapshot:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta=_raw_meta("doctor_snapshot", None),
            )
        return sample_raw(
            SEAT_WAIT_PLANE,
            KIND_PLANE,
            source="doctor_snapshot",
            raw=snap,
        )

    return prefer_native(
        plane, seat_id=SEAT_WAIT_PLANE, kind=KIND_PLANE, sampler=_sample
    )


def adapt_session_plane(instance: Any, plane: Any) -> SeatReport:
    def _sample() -> SeatReport:
        try:
            snap = plane.doctor_snapshot()
            if not isinstance(snap, Mapping):
                snap = {"_non_mapping": type(snap).__name__}
        except Exception as exc:
            return SeatReport.error(
                SEAT_SESSION_PLANE,
                KIND_PLANE,
                reason=f"doctor_snapshot:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta=_raw_meta("doctor_snapshot", None),
            )
        return sample_raw(
            SEAT_SESSION_PLANE,
            KIND_PLANE,
            source="doctor_snapshot",
            raw=snap,
        )

    return prefer_native(
        plane, seat_id=SEAT_SESSION_PLANE, kind=KIND_PLANE, sampler=_sample
    )


def adapt_work_plane(instance: Any, plane: Any) -> SeatReport:
    def _sample() -> SeatReport:
        try:
            snap = plane.status() if callable(getattr(plane, "status", None)) else {}
            if not isinstance(snap, Mapping):
                snap = {"_non_mapping": type(snap).__name__}
        except Exception as exc:
            return SeatReport.error(
                SEAT_WORK_PLANE,
                KIND_PLANE,
                reason=f"status:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta=_raw_meta("status", None),
            )
        return sample_raw(
            SEAT_WORK_PLANE,
            KIND_PLANE,
            source="status",
            raw=snap,
        )

    return prefer_native(
        plane, seat_id=SEAT_WORK_PLANE, kind=KIND_PLANE, sampler=_sample
    )


# ── supervisor ───────────────────────────────────────────────────────────────


def adapt_supervisor(instance: Any, supervisor: Any) -> SeatReport:
    def _sample() -> SeatReport:
        try:
            snap = (
                supervisor.status()
                if callable(getattr(supervisor, "status", None))
                else {}
            )
            if not isinstance(snap, Mapping):
                snap = {"_non_mapping": type(snap).__name__}
        except Exception as exc:
            return SeatReport.error(
                SEAT_SUPERVISOR,
                KIND_SUPERVISOR,
                reason=f"status:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta=_raw_meta("status", None),
            )
        return sample_raw(
            SEAT_SUPERVISOR,
            KIND_SUPERVISOR,
            source="status",
            raw=snap,
        )

    return prefer_native(
        supervisor, seat_id=SEAT_SUPERVISOR, kind=KIND_SUPERVISOR, sampler=_sample
    )


def adapt_supervisor_service(
    instance: Any,
    service: Any,
    *,
    service_name: str,
    running: bool | None = None,
) -> SeatReport:
    seat_id = supervisor_service_seat_id(service_name)

    def _sample() -> SeatReport:
        try:
            snap = service.status() if callable(getattr(service, "status", None)) else {}
            if not isinstance(snap, Mapping):
                snap = {"_non_mapping": type(snap).__name__}
        except Exception as exc:
            return SeatReport.error(
                seat_id,
                KIND_SUPERVISOR_SERVICE,
                reason=f"status:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta=_raw_meta("status", None, service_name=service_name),
            )
        raw = dict(snap)
        if running is not None:
            raw.setdefault("running", running)
        return sample_raw(
            seat_id,
            KIND_SUPERVISOR_SERVICE,
            source="status",
            raw=raw,
            extra_meta={"service_name": service_name},
        )

    return prefer_native(
        service,
        seat_id=seat_id,
        kind=KIND_SUPERVISOR_SERVICE,
        sampler=_sample,
    )


# ── execution port ───────────────────────────────────────────────────────────


def adapt_execution(instance: Any, port: Any) -> SeatReport:
    def _sample() -> SeatReport:
        raw = {
            "instance_started": bool(getattr(instance, "is_started", False)),
            "has_invoke_resource": callable(getattr(port, "invoke_resource", None)),
            "has_start_workload": callable(getattr(port, "start_workload", None)),
            "port_type": type(port).__name__,
        }
        return sample_raw(
            SEAT_EXECUTION,
            KIND_PORT,
            source="execution_port_attrs",
            raw=raw,
        )

    return prefer_native(
        port, seat_id=SEAT_EXECUTION, kind=KIND_PORT, sampler=_sample
    )


# ── system log (public API only — no seat_report on the log) ─────────────────


def adapt_system_log(instance: Any, log: Any) -> SeatReport:
    def _sample() -> SeatReport:
        raw: dict[str, Any] = {"log_type": type(log).__name__}
        try:
            if hasattr(log, "record_count"):
                raw["records"] = int(log.record_count)
            elif callable(getattr(log, "recent", None)):
                raw["records"] = len(log.recent())
        except Exception as exc:
            return SeatReport.error(
                SEAT_SYSTEM_LOG,
                KIND_LOG,
                reason=f"sample:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta=_raw_meta("system_log_public", raw),
            )
        if hasattr(log, "capacity"):
            try:
                raw["capacity"] = int(log.capacity)
            except Exception:
                pass
        if hasattr(log, "level"):
            raw["level"] = log.level
        if hasattr(log, "console"):
            raw["console"] = bool(log.console)
        return sample_raw(
            SEAT_SYSTEM_LOG,
            KIND_LOG,
            source="system_log_public",
            raw=raw,
        )

    return prefer_native(
        log, seat_id=SEAT_SYSTEM_LOG, kind=KIND_LOG, sampler=_sample
    )


# ── boot membership ──────────────────────────────────────────────────────────


def adapt_boot_membership(instance: Any, walk: Any) -> SeatReport:
    def _sample() -> SeatReport:
        rows: list[Any]
        if walk is None:
            rows = []
        elif isinstance(walk, (list, tuple)):
            rows = list(walk)
        else:
            rows = [walk]
        phases: list[Any] = []
        for row in rows:
            if hasattr(row, "to_dict") and callable(row.to_dict):
                phases.append(row.to_dict())
            elif isinstance(row, Mapping):
                phases.append(dict(row))
            else:
                phases.append({"repr": repr(row)})
        return sample_raw(
            SEAT_BOOT_MEMBERSHIP,
            KIND_BOOT,
            source="last_boot_walk",
            raw={"phases": phases, "phase_count": len(phases)},
        )

    native = try_native_report(instance)
    if native is not None:
        try:
            report = coerce_report(
                native,
                default_seat_id=SEAT_BOOT_MEMBERSHIP,
                default_kind=KIND_BOOT,
                default_lineage=LINEAGE_NATIVE,
            )
            if report.seat_id == SEAT_BOOT_MEMBERSHIP:
                return report
        except Exception:
            pass
    return _sample()


# Back-compat name used by prefer_native callers in older code paths.
# prefer_native keyword is now ``sampler``; keep export of sample_raw.

__all__ = [
    "adapt_boot_membership",
    "adapt_execution",
    "adapt_session_plane",
    "adapt_supervisor",
    "adapt_supervisor_service",
    "adapt_system_log",
    "adapt_wait_plane",
    "adapt_work_plane",
    "prefer_native",
    "sample_raw",
]
