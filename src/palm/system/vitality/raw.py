"""
Raw sampling — system vitality observes public seat APIs (0.61).

No adapters. No doctor field maps. Eyes:

1. Prefer native ``seat_report()`` only if the seat implements it.
2. Else call a **named public method** or read **public attrs**.
3. Stash the payload in ``meta.raw`` with ``lineage: sampled``.

Product present interprets raw. System does not curate.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from palm.system.vitality.protocol import try_native_report
from palm.system.vitality.report import SeatReport, coerce_report
from palm.system.vitality.schema import (
    LINEAGE_NATIVE,
    LINEAGE_SAMPLED,
    STATE_OK,
)


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
    """Structural seat report + uninterpreted ``meta.raw`` for product."""
    meta: dict[str, Any] = {
        "sample_source": source,
        "raw": dict(raw or {}),
    }
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
    """Native ``seat_report`` if present; else *sampler* (raw public API)."""
    native = try_native_report(seat)
    if native is None:
        return sampler()
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


def _as_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "to_dict") and callable(value.to_dict):
        try:
            d = value.to_dict()
            if isinstance(d, Mapping):
                return dict(d)
        except Exception:
            pass
    return {"value": value, "type": type(value).__name__}


def call_public(obj: Any, method: str, *args: Any, **kwargs: Any) -> Any:
    """Call a public method on *obj*; raise if missing or non-callable."""
    fn = getattr(obj, method, None)
    if not callable(fn):
        raise AttributeError(f"{type(obj).__name__}.{method} not callable")
    return fn(*args, **kwargs)


def sample_method(
    seat: Any,
    *,
    seat_id: str,
    kind: str,
    method: str,
    args: Sequence[Any] = (),
    kwargs: Mapping[str, Any] | None = None,
    extra_raw: Mapping[str, Any] | None = None,
    extra_meta: Mapping[str, Any] | None = None,
) -> SeatReport:
    """Raw-dog: call ``seat.method(...)`` and store the return as raw."""

    def _sample() -> SeatReport:
        try:
            result = call_public(seat, method, *args, **dict(kwargs or {}))
            raw = _as_mapping(result)
            if extra_raw:
                raw = {**raw, **dict(extra_raw)}
        except Exception as exc:
            return SeatReport.error(
                seat_id,
                kind,
                reason=f"{method}:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta={
                    "sample_source": method,
                    "raw": dict(extra_raw or {}),
                    **dict(extra_meta or {}),
                },
            )
        return sample_raw(
            seat_id,
            kind,
            source=method,
            raw=raw,
            extra_meta=extra_meta,
        )

    return prefer_native(seat, seat_id=seat_id, kind=kind, sampler=_sample)


def sample_attrs(
    seat: Any,
    *,
    seat_id: str,
    kind: str,
    attrs: Sequence[str],
    source: str = "attrs",
    extra_raw: Mapping[str, Any] | None = None,
    extra_meta: Mapping[str, Any] | None = None,
    instance: Any | None = None,
    instance_attrs: Sequence[str] = (),
) -> SeatReport:
    """Raw-dog: read public attributes into ``meta.raw``."""

    def _sample() -> SeatReport:
        raw: dict[str, Any] = {"type": type(seat).__name__}
        try:
            for name in attrs:
                if hasattr(seat, name):
                    raw[name] = getattr(seat, name)
            if instance is not None:
                for name in instance_attrs:
                    if hasattr(instance, name):
                        raw[name] = getattr(instance, name)
            if extra_raw:
                raw.update(dict(extra_raw))
        except Exception as exc:
            return SeatReport.error(
                seat_id,
                kind,
                reason=f"attrs:{type(exc).__name__}: {exc}",
                lineage=LINEAGE_SAMPLED,
                meta={"sample_source": source, "raw": raw, **dict(extra_meta or {})},
            )
        return sample_raw(
            seat_id,
            kind,
            source=source,
            raw=raw,
            extra_meta=extra_meta,
        )

    return prefer_native(seat, seat_id=seat_id, kind=kind, sampler=_sample)


def sample_sequence(
    rows: Any,
    *,
    seat_id: str,
    kind: str,
    source: str,
    extra_meta: Mapping[str, Any] | None = None,
) -> SeatReport:
    """Raw-dog: sequence of objects with optional ``to_dict`` (e.g. boot walk)."""
    if rows is None:
        seq: list[Any] = []
    elif isinstance(rows, (list, tuple)):
        seq = list(rows)
    else:
        seq = [rows]
    items: list[Any] = []
    for row in seq:
        if hasattr(row, "to_dict") and callable(row.to_dict):
            try:
                items.append(row.to_dict())
                continue
            except Exception:
                pass
        if isinstance(row, Mapping):
            items.append(dict(row))
        else:
            items.append({"repr": repr(row), "type": type(row).__name__})
    return sample_raw(
        seat_id,
        kind,
        source=source,
        raw={"items": items, "count": len(items)},
        extra_meta=extra_meta,
    )


# Public sample convention (order). First callable wins. Not a field map.
PUBLIC_SAMPLE_METHODS: tuple[str, ...] = ("status", "doctor_snapshot")


def sample_by_convention(
    seat: Any,
    *,
    seat_id: str,
    kind: str,
    methods: Sequence[str] = PUBLIC_SAMPLE_METHODS,
    extra_meta: Mapping[str, Any] | None = None,
) -> SeatReport:
    """
    Raw-dog by **convention**: try public methods in order, else type-only.

    No per-seat field maps. Product interprets whatever raw appears.
    """

    def _sample() -> SeatReport:
        tried: list[str] = []
        for method in methods:
            fn = getattr(seat, method, None)
            if not callable(fn):
                continue
            tried.append(method)
            try:
                result = fn()
                raw = _as_mapping(result)
                return sample_raw(
                    seat_id,
                    kind,
                    source=method,
                    raw=raw,
                    notes=[f"convention:{method}"],
                    extra_meta=extra_meta,
                )
            except Exception as exc:
                return SeatReport.error(
                    seat_id,
                    kind,
                    reason=f"{method}:{type(exc).__name__}: {exc}",
                    lineage=LINEAGE_SAMPLED,
                    meta={
                        "sample_source": method,
                        "raw": {},
                        "convention_tried": tried,
                        **dict(extra_meta or {}),
                    },
                )
        return sample_raw(
            seat_id,
            kind,
            source="present_only",
            raw={"type": type(seat).__name__},
            notes=["no_public_sample_method", f"tried:{','.join(methods)}"],
            extra_meta=extra_meta,
        )

    return prefer_native(seat, seat_id=seat_id, kind=kind, sampler=_sample)


def bound_method_reporter(
    seat_id: str,
    kind: str,
    method: str,
) -> Callable[[Any, Any], SeatReport]:
    """Probe report: raw-call ``seat.method()``."""

    def _report(instance: Any, seat: Any) -> SeatReport:
        return sample_method(seat, seat_id=seat_id, kind=kind, method=method)

    return _report


def bound_convention_reporter(
    seat_id: str,
    kind: str,
    methods: Sequence[str] = PUBLIC_SAMPLE_METHODS,
) -> Callable[[Any, Any], SeatReport]:
    """Probe report: sample by public method convention."""

    def _report(instance: Any, seat: Any) -> SeatReport:
        return sample_by_convention(
            seat, seat_id=seat_id, kind=kind, methods=methods
        )

    return _report


def bound_attrs_reporter(
    seat_id: str,
    kind: str,
    attrs: Sequence[str],
    *,
    source: str = "attrs",
    instance_attrs: Sequence[str] = (),
) -> Callable[[Any, Any], SeatReport]:
    """Probe report: raw-read attributes."""

    def _report(instance: Any, seat: Any) -> SeatReport:
        return sample_attrs(
            seat,
            seat_id=seat_id,
            kind=kind,
            attrs=attrs,
            source=source,
            instance=instance,
            instance_attrs=instance_attrs,
        )

    return _report


def bound_sequence_reporter(
    seat_id: str,
    kind: str,
    *,
    source: str,
) -> Callable[[Any, Any], SeatReport]:
    """Probe report: raw-sample a sequence (boot walk)."""

    def _report(instance: Any, walk: Any) -> SeatReport:
        return sample_sequence(walk, seat_id=seat_id, kind=kind, source=source)

    return _report


__all__ = [
    "PUBLIC_SAMPLE_METHODS",
    "bound_attrs_reporter",
    "bound_convention_reporter",
    "bound_method_reporter",
    "bound_sequence_reporter",
    "call_public",
    "prefer_native",
    "sample_attrs",
    "sample_by_convention",
    "sample_method",
    "sample_raw",
    "sample_sequence",
]
