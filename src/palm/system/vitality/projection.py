"""
VitalityProjection — read-only fold of enabled capabilities (0.61.2).

Law (ADR-030):
  iterate enabled capabilities → each returns a fragment → merge → snapshot

Projection **receives** seat reports and capability data. It does not:
  - start/continue work
  - re-curate doctor/status field maps
  - invent living counters
  - curate doctor fields into load

Inspect/product will **present** this snapshot (top). Adapters are not the
architecture of record; native seat reports are the growth path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping

from palm.system.vitality.capability import (
    CapabilityFragment,
    SampleContext,
)
from palm.system.vitality.capabilities import (
    BAG_SEAT_REPORTS,
    build_seat_walk_capability,
    sample_seat_walk,
)
from palm.system.vitality.registry import VitalityRegistry
from palm.system.vitality.report import SeatReport, coerce_report, reports_to_dicts
from palm.system.vitality.schema import (
    CAPABILITY_EMISSION_WINDOW,
    CAPABILITY_SEAT_WALK,
    LINEAGE_NATIVE,
    LINEAGE_SAMPLED,
    STATE_ABSENT,
    STATE_ERROR,
    STATE_OK,
    STATE_SKIPPED,
    VITALITY_SNAPSHOT_SCHEMA,
)
from palm.system.vitality.seats_registry import default_vitality_registry


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _structural_summary(seats: list[SeatReport]) -> dict[str, Any]:
    by_state: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    by_lineage: dict[str, int] = {}
    present = 0
    for r in seats:
        by_state[r.state] = by_state.get(r.state, 0) + 1
        by_kind[r.kind] = by_kind.get(r.kind, 0) + 1
        by_lineage[r.lineage] = by_lineage.get(r.lineage, 0) + 1
        if r.present:
            present += 1
    return {
        "seat_count": len(seats),
        "present_count": present,
        "absent_count": by_state.get(STATE_ABSENT, 0),
        "error_count": by_state.get(STATE_ERROR, 0),
        "ok_count": by_state.get(STATE_OK, 0),
        "by_state": by_state,
        "by_kind": by_kind,
        "by_lineage": by_lineage,
        "native_count": by_lineage.get(LINEAGE_NATIVE, 0),
        "sampled_count": by_lineage.get(LINEAGE_SAMPLED, 0),
        "present_ids": [r.seat_id for r in seats if r.present],
        "absent_ids": [r.seat_id for r in seats if r.state == STATE_ABSENT],
    }


@dataclass
class VitalitySnapshot:
    """Versioned living-physiology snapshot (``palm.vitality_snapshot/1``).

    Attributes
    ----------
    fragments:
        One entry per capability that was sampled (enabled path).
    seats:
        Convenience fold from ``seat_walk`` when that capability ran.
        Empty if seat_walk was disabled/skipped.
    summary:
        Structural counts only (present/state/kind/lineage) — not load theater.
    lineage:
        Provenance rows: which capability_id contributed which seat_id / fragment.
    """

    fragments: dict[str, CapabilityFragment] = field(default_factory=dict)
    seats: list[SeatReport] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    lineage: list[dict[str, Any]] = field(default_factory=list)
    sample_ts: str | None = None
    schema: str = VITALITY_SNAPSHOT_SCHEMA
    meta: dict[str, Any] = field(default_factory=dict)
    enabled_capabilities: list[str] = field(default_factory=list)
    skipped_capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "sample_ts": self.sample_ts,
            "enabled_capabilities": list(self.enabled_capabilities),
            "skipped_capabilities": list(self.skipped_capabilities),
            "fragments": {k: v.to_dict() for k, v in self.fragments.items()},
            "seats": reports_to_dicts(self.seats),
            "summary": dict(self.summary),
            "lineage": list(self.lineage),
            "meta": dict(self.meta),
        }

    def seat_by_id(self) -> dict[str, SeatReport]:
        return {s.seat_id: s for s in self.seats}

    def fragment(self, capability_id: str) -> CapabilityFragment | None:
        return self.fragments.get(str(capability_id or "").strip())

    def top_view(self) -> dict[str, Any]:
        """Thin present shape for inspect/top — structural only.

        Product may decorate further. System does not invent doctor health.
        """
        top: dict[str, Any] = {
            "schema": self.schema,
            "sample_ts": self.sample_ts,
            "summary": dict(self.summary),
            "seats": [
                {
                    "seat_id": s.seat_id,
                    "kind": s.kind,
                    "present": s.present,
                    "state": s.state,
                    "lineage": s.lineage,
                    "notes": list(s.notes),
                    # Structural only; product present interprets meta.raw.
                    "load": dict(s.load),
                    "raw": dict(s.meta.get("raw") or {})
                    if isinstance(s.meta.get("raw"), dict)
                    else s.meta.get("raw"),
                    "sample_source": s.meta.get("sample_source"),
                }
                for s in self.seats
            ],
            "capabilities": {
                cid: {
                    "present": frag.present,
                    "state": frag.state,
                    "notes": list(frag.notes),
                }
                for cid, frag in self.fragments.items()
            },
            "lineage": list(self.lineage),
        }
        em = self.fragments.get(CAPABILITY_EMISSION_WINDOW)
        if em is not None and em.present and isinstance(em.data, dict):
            summary = em.data.get("summary")
            top["emissions"] = {
                "state": em.state,
                "summary": dict(summary) if isinstance(summary, dict) else {},
                "heat": em.data.get("heat"),
                # Full window stays on fragment; top stays light.
                "sample_count": (
                    (summary or {}).get("emission_count")
                    if isinstance(summary, dict)
                    else None
                ),
            }
        return top


@dataclass
class ProjectionOptions:
    """Knobs for one :meth:`VitalityProjection.sample`."""

    registry: VitalityRegistry | None = None
    mode: str | None = None
    walk_options: Any | None = None
    """Optional WalkOptions for seat_walk."""

    only: frozenset[str] | None = None
    """If set, sample only these capability ids (must be registered)."""

    extra_enable: frozenset[str] = field(default_factory=frozenset)
    """Enable intention caps for this sample only."""

    extra_disable: frozenset[str] = field(default_factory=frozenset)
    """Disable caps for this sample only."""

    stamp: bool = True
    on_capability_error: str = "error_fragment"  # or "raise"


class VitalityProjection:
    """Read-only fold: enabled capabilities → snapshot."""

    def __init__(self, registry: VitalityRegistry | None = None) -> None:
        self._registry = registry

    @property
    def registry(self) -> VitalityRegistry:
        if self._registry is None:
            return default_vitality_registry()
        return self._registry

    def sample(
        self,
        instance: Any,
        options: ProjectionOptions | None = None,
        **kwargs: Any,
    ) -> VitalitySnapshot:
        """Sample *instance* through enabled capabilities."""
        if options is None and kwargs:
            options = ProjectionOptions(**kwargs)
        elif options is None:
            options = ProjectionOptions()
        elif kwargs:
            # thin overlay not fully supported; prefer explicit options
            options = ProjectionOptions(
                registry=kwargs.get("registry", options.registry),
                mode=kwargs.get("mode", options.mode),
                walk_options=kwargs.get("walk_options", options.walk_options),
                only=kwargs.get("only", options.only),
                extra_enable=kwargs.get("extra_enable", options.extra_enable),
                extra_disable=kwargs.get("extra_disable", options.extra_disable),
                stamp=kwargs.get("stamp", options.stamp),
                on_capability_error=kwargs.get(
                    "on_capability_error", options.on_capability_error
                ),
            )

        registry = options.registry if options.registry is not None else self.registry
        caps = registry.list()
        if options.only is not None:
            wanted = set(options.only)
            caps = [c for c in caps if c.id in wanted]
            # unknown only-ids become skipped lineage later
            known = {c.id for c in caps}
            unknown = wanted - known
        else:
            unknown = set()
            caps = [
                c
                for c in caps
                if (
                    (
                        registry.is_enabled(c.id)
                        or c.id in options.extra_enable
                    )
                    and c.id not in options.extra_disable
                )
            ]

        ctx = SampleContext(
            mode=options.mode,
            walk_options=options.walk_options,
            enable_ids=frozenset(c.id for c in caps),
        )

        fragments: dict[str, CapabilityFragment] = {}
        lineage: list[dict[str, Any]] = []
        enabled_ids: list[str] = []
        skipped_ids: list[str] = []

        for cap in caps:
            enabled_ids.append(cap.id)
            try:
                frag = cap.sample(instance, ctx)
                if not isinstance(frag, CapabilityFragment):
                    if isinstance(frag, Mapping):
                        frag = CapabilityFragment.from_dict(frag)
                    else:
                        frag = CapabilityFragment.error(
                            cap.id,
                            f"bad_fragment_type:{type(frag).__name__}",
                        )
            except Exception as exc:
                if options.on_capability_error == "raise":
                    raise
                frag = CapabilityFragment.error(
                    cap.id,
                    f"sample:{type(exc).__name__}: {exc}",
                )
            # Ensure capability_id matches registration.
            if frag.capability_id != cap.id:
                frag = CapabilityFragment(
                    capability_id=cap.id,
                    present=frag.present,
                    state=frag.state,
                    data=dict(frag.data),
                    notes=list(frag.notes)
                    + [f"fragment_id_was:{frag.capability_id}"],
                    schema=frag.schema,
                    meta=dict(frag.meta),
                )
            fragments[cap.id] = frag
            lineage.append(
                {
                    "capability_id": cap.id,
                    "state": frag.state,
                    "present": frag.present,
                    "maturity": cap.maturity,
                    "role": cap.role,
                }
            )
            if frag.state == STATE_SKIPPED:
                skipped_ids.append(cap.id)

        for uid in sorted(unknown):
            skipped_ids.append(uid)
            fragments[uid] = CapabilityFragment.skipped(
                uid, "unknown_capability"
            )
            lineage.append(
                {
                    "capability_id": uid,
                    "state": STATE_SKIPPED,
                    "present": False,
                    "maturity": "unknown",
                    "role": "unknown",
                }
            )

        seats = self._extract_seats(fragments, ctx)
        for s in seats:
            lineage.append(
                {
                    "capability_id": CAPABILITY_SEAT_WALK,
                    "seat_id": s.seat_id,
                    "lineage": s.lineage,
                    "state": s.state,
                    "present": s.present,
                }
            )

        summary = _structural_summary(seats)
        summary["capability_count"] = len(fragments)
        summary["enabled_count"] = len(enabled_ids)
        summary["skipped_count"] = len(skipped_ids)

        return VitalitySnapshot(
            fragments=fragments,
            seats=seats,
            summary=summary,
            lineage=lineage,
            sample_ts=_now_iso() if options.stamp else None,
            meta={
                "mode": options.mode,
                "registry_size": len(registry),
            },
            enabled_capabilities=enabled_ids,
            skipped_capabilities=skipped_ids,
        )

    def _extract_seats(
        self,
        fragments: dict[str, CapabilityFragment],
        ctx: SampleContext,
    ) -> list[SeatReport]:
        """Pull seats from seat_walk fragment or bag — receive only."""
        bag_reports = ctx.bag.get(BAG_SEAT_REPORTS)
        if isinstance(bag_reports, list) and bag_reports:
            if isinstance(bag_reports[0], SeatReport):
                return list(bag_reports)

        frag = fragments.get(CAPABILITY_SEAT_WALK)
        if frag is None or not frag.present:
            return []
        raw = frag.data.get("seats")
        if not isinstance(raw, list):
            return []
        out: list[SeatReport] = []
        for row in raw:
            try:
                if isinstance(row, SeatReport):
                    out.append(row)
                elif isinstance(row, Mapping):
                    out.append(coerce_report(row))
            except Exception:
                continue
        return out


def project(
    instance: Any,
    options: ProjectionOptions | None = None,
    **kwargs: Any,
) -> VitalitySnapshot:
    """Module-level sample using the default registry."""
    return VitalityProjection().sample(instance, options, **kwargs)


def project_top(
    instance: Any,
    options: ProjectionOptions | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience: snapshot.top_view() for inspect/top present path."""
    return project(instance, options, **kwargs).top_view()


def project_seat_walk_only(
    instance: Any,
    *,
    walk_options: Any | None = None,
) -> VitalitySnapshot:
    """Sample with only the seat_walk capability (tests / lean)."""
    # Ensure seat_walk runs even if default enable set is empty somehow.
    reg = default_vitality_registry().clone()
    if CAPABILITY_SEAT_WALK not in reg:
        reg.register(build_seat_walk_capability(), enabled=True)
    else:
        reg.enable(CAPABILITY_SEAT_WALK)
    return VitalityProjection(reg).sample(
        instance,
        ProjectionOptions(
            only=frozenset({CAPABILITY_SEAT_WALK}),
            walk_options=walk_options,
        ),
    )


# Re-export sample_seat_walk for tests that want the raw fragment path.
__all__ = [
    "ProjectionOptions",
    "VitalityProjection",
    "VitalitySnapshot",
    "project",
    "project_seat_walk_only",
    "project_top",
    "sample_seat_walk",
]
