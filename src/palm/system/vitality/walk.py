"""
Seat walk — dynamic discovery of living seats on a SystemInstance (0.61.1).

Observation only. Does not start, stop, or continue work.
Walks the probe catalog on the live instance graph; expands supervisor
services dynamically from the attached registry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from palm.system.vitality.adapters import adapt_supervisor_service
from palm.system.vitality.probe import ProbeCatalog, SeatProbe
from palm.system.vitality.report import SeatReport, index_by_seat_id, reports_to_dicts
from palm.system.vitality.schema import (
    CAPABILITY_SEAT_WALK,
    KIND_SUPERVISOR_SERVICE,
    SEAT_SUPERVISOR,
    STATE_ABSENT,
    STATE_ERROR,
    supervisor_service_seat_id,
)
from palm.system.vitality.seats import default_probe_catalog

ExpandPolicy = Literal["always", "never", "when_present"]


@dataclass
class WalkOptions:
    """Knobs for :func:`discover_seats` (cheap defaults for safe/test)."""

    catalog: ProbeCatalog | None = None
    """Probe seeds; default Palm catalog when omitted."""

    expand_supervisor_services: ExpandPolicy = "when_present"
    """Discover ``supervisor.<name>`` seats from the live registry."""

    include_tags: frozenset[str] | None = None
    """If set, only probes that carry at least one of these tags."""

    exclude_tags: frozenset[str] = field(default_factory=frozenset)
    """Skip probes that carry any of these tags."""

    stamp: bool = False
    """When True, set ``sample_ts`` on every report."""

    on_probe_error: Literal["error_report", "raise"] = "error_report"
    """How to handle probe/adapter exceptions."""

    skip_seat_ids: frozenset[str] = field(default_factory=frozenset)
    """Hard omit of known seat ids (tests / focus)."""


@dataclass(frozen=True)
class SeatWalkResult:
    """Structured result of one walk (reports + bookkeeping)."""

    reports: list[SeatReport]
    capability_id: str = CAPABILITY_SEAT_WALK
    probe_count: int = 0
    error_count: int = 0
    absent_count: int = 0
    present_count: int = 0

    def to_dicts(self) -> list[dict[str, Any]]:
        return reports_to_dicts(self.reports)

    def by_id(self) -> dict[str, SeatReport]:
        return index_by_seat_id(self.reports)

    def present_ids(self) -> list[str]:
        return [r.seat_id for r in self.reports if r.present]

    def absent_ids(self) -> list[str]:
        return [r.seat_id for r in self.reports if r.state == STATE_ABSENT]


def _filter_probes(catalog: ProbeCatalog, options: WalkOptions) -> list[SeatProbe]:
    probes = catalog.list()
    out: list[SeatProbe] = []
    for p in probes:
        if p.seat_id in options.skip_seat_ids:
            continue
        if options.exclude_tags and any(t in options.exclude_tags for t in p.tags):
            continue
        if options.include_tags is not None:
            if not any(t in options.include_tags for t in p.tags):
                continue
        out.append(p)
    return out


def _stamp(report: SeatReport, options: WalkOptions) -> SeatReport:
    if not options.stamp or report.sample_ts is not None:
        return report
    from datetime import UTC, datetime

    ts = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return SeatReport(
        seat_id=report.seat_id,
        kind=report.kind,
        present=report.present,
        state=report.state,
        load=dict(report.load),
        notes=list(report.notes),
        lineage=report.lineage,
        schema=report.schema,
        meta=dict(report.meta),
        sample_ts=ts,
    )


def _run_probe(
    instance: Any,
    probe: SeatProbe,
    options: WalkOptions,
) -> SeatReport:
    try:
        if probe.resolve is not None:
            seat = probe.resolve(instance)
            if seat is None:
                if probe.when_absent == "omit":
                    return SeatReport.skipped(
                        probe.seat_id,
                        probe.kind,
                        reason="omit_absent",
                        meta={"probe": probe.seat_id},
                    )
                return SeatReport.absent(
                    probe.seat_id,
                    probe.kind,
                    reason="not_attached",
                    notes=list(probe.description and [probe.description] or []),
                )
            if probe.report is not None:
                return probe.report(instance, seat)
            # Presence-only fallback when no reporter.
            from palm.system.vitality.protocol import try_native_report
            from palm.system.vitality.report import coerce_report
            from palm.system.vitality.schema import LINEAGE_NATIVE

            native = try_native_report(seat)
            if native is not None:
                return coerce_report(
                    native,
                    default_seat_id=probe.seat_id,
                    default_kind=probe.kind,
                    default_lineage=LINEAGE_NATIVE,
                )
            return SeatReport.ok(
                probe.seat_id,
                probe.kind,
                load={"present_only": True},
                notes=["no_reporter_presence_only"],
                lineage=LINEAGE_NATIVE,
            )

        # Instance-level probe (no resolve object).
        if probe.report_instance is not None:
            return probe.report_instance(instance)
        return SeatReport.error(
            probe.seat_id,
            probe.kind,
            reason="probe_misconfigured",
            present=False,
        )
    except Exception as exc:
        if options.on_probe_error == "raise":
            raise
        return SeatReport.error(
            probe.seat_id,
            probe.kind,
            reason=f"probe:{type(exc).__name__}: {exc}",
            present=False,
            meta={"probe": probe.seat_id},
        )


def _supervisor_running_set(supervisor: Any) -> set[str]:
    try:
        snap = supervisor.status() if callable(getattr(supervisor, "status", None)) else {}
        if isinstance(snap, dict):
            running = snap.get("running") or []
            return {str(x) for x in running}
    except Exception:
        pass
    # Fallback: private set if present.
    raw = getattr(supervisor, "_running", None)
    if isinstance(raw, (set, list, tuple)):
        return {str(x) for x in raw}
    return set()


def _expand_supervisor_services(
    instance: Any,
    reports: list[SeatReport],
    options: WalkOptions,
) -> list[SeatReport]:
    """Dynamically discover supervised continuous services as seats."""
    by_id = index_by_seat_id(reports)
    sup_report = by_id.get(SEAT_SUPERVISOR)
    if sup_report is None or not sup_report.present:
        return []

    supervisor = getattr(instance, "supervisor", None)
    if supervisor is None:
        return []

    names_fn = getattr(supervisor, "names", None)
    get_fn = getattr(supervisor, "get", None)
    if not callable(names_fn):
        return []

    try:
        names = list(names_fn())
    except Exception as exc:
        return [
            SeatReport.error(
                "supervisor.*",
                KIND_SUPERVISOR_SERVICE,
                reason=f"names:{type(exc).__name__}: {exc}",
                present=False,
            )
        ]

    running = _supervisor_running_set(supervisor)
    extra: list[SeatReport] = []
    for name in sorted(str(n) for n in names):
        seat_id = supervisor_service_seat_id(name)
        if seat_id in options.skip_seat_ids:
            continue
        service = get_fn(name) if callable(get_fn) else None
        if service is None:
            # Registered name without resolvable object — still honest.
            extra.append(
                SeatReport.absent(
                    seat_id,
                    KIND_SUPERVISOR_SERVICE,
                    reason="registered_but_unresolvable",
                    meta={"service_name": name},
                )
            )
            continue
        try:
            extra.append(
                adapt_supervisor_service(
                    instance,
                    service,
                    service_name=name,
                    running=name in running,
                )
            )
        except Exception as exc:
            if options.on_probe_error == "raise":
                raise
            extra.append(
                SeatReport.error(
                    seat_id,
                    KIND_SUPERVISOR_SERVICE,
                    reason=f"service:{type(exc).__name__}: {exc}",
                    meta={"service_name": name},
                )
            )
    return extra


def discover_seats(
    instance: Any,
    options: WalkOptions | None = None,
    **kwargs: Any,
) -> list[SeatReport]:
    """Discover seats on *instance* and return ordered :class:`SeatReport` list.

    Parameters
    ----------
    instance:
        Live system instance (today :class:`~palm.system.runtime.base.BaseRuntime`).
        Duck-typed: any object with known attach attributes works.
    options:
        Walk knobs; or pass keyword fields of :class:`WalkOptions`.
    """
    if options is None and kwargs:
        options = WalkOptions(**kwargs)
    elif options is None:
        options = WalkOptions()
    elif kwargs:
        # Overlay kwargs onto a shallow copy of options fields.
        data = {
            "catalog": options.catalog,
            "expand_supervisor_services": options.expand_supervisor_services,
            "include_tags": options.include_tags,
            "exclude_tags": options.exclude_tags,
            "stamp": options.stamp,
            "on_probe_error": options.on_probe_error,
            "skip_seat_ids": options.skip_seat_ids,
        }
        data.update(kwargs)
        options = WalkOptions(**data)

    catalog = options.catalog if options.catalog is not None else default_probe_catalog()
    probes = _filter_probes(catalog, options)

    reports: list[SeatReport] = []
    for probe in probes:
        report = _run_probe(instance, probe, options)
        if report.state == "skipped" and report.notes == ["omit_absent"]:
            # Omitted absents do not enter the result set.
            continue
        reports.append(_stamp(report, options))

    # Dynamic expansion: supervisor services follow composition, not a menu.
    expand = options.expand_supervisor_services
    should_expand = expand == "always" or (
        expand == "when_present"
        and any(r.seat_id == SEAT_SUPERVISOR and r.present for r in reports)
    )
    if should_expand:
        for extra in _expand_supervisor_services(instance, reports, options):
            reports.append(_stamp(extra, options))

    return reports


def seat_walk(
    instance: Any,
    options: WalkOptions | None = None,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """Public walk API returning canonical dicts (``palm.seat_report/1``)."""
    return reports_to_dicts(discover_seats(instance, options, **kwargs))


def walk_result(
    instance: Any,
    options: WalkOptions | None = None,
    **kwargs: Any,
) -> SeatWalkResult:
    """Walk and return a :class:`SeatWalkResult` with counts."""
    reports = discover_seats(instance, options, **kwargs)
    error_count = sum(1 for r in reports if r.state == STATE_ERROR)
    absent_count = sum(1 for r in reports if r.state == STATE_ABSENT)
    present_count = sum(1 for r in reports if r.present)
    catalog = (
        options.catalog
        if options is not None and options.catalog is not None
        else default_probe_catalog()
    )
    return SeatWalkResult(
        reports=reports,
        probe_count=len(catalog),
        error_count=error_count,
        absent_count=absent_count,
        present_count=present_count,
    )


__all__ = [
    "ExpandPolicy",
    "SeatWalkResult",
    "WalkOptions",
    "discover_seats",
    "seat_walk",
    "walk_result",
]
