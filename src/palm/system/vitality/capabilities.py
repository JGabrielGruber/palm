"""
Default vitality capabilities (0.61.2).

``seat_walk`` is the installed core observe path. Other catalog ids may exist
as intention stubs (disabled) so the registry shape is honest about growth
without fake-green bodies.

**Law:** capabilities *receive* seat reports; they do not re-curate doctor
fields. Adapter lineage on seats is pass-through truth, not a foundation to
deepen here.
"""

from __future__ import annotations

from typing import Any

from palm.system.vitality.capability import (
    CapabilityFragment,
    SampleContext,
    VitalityCapability,
    intention_stub,
)
from palm.system.vitality.report import SeatReport, reports_to_dicts
from palm.system.vitality.schema import (
    CAPABILITY_BENCHMARK,
    CAPABILITY_BOOT_MEMBERSHIP,
    CAPABILITY_EMISSION_WINDOW,
    CAPABILITY_LOADED_BULK,
    CAPABILITY_MONITOR_AGENT,
    CAPABILITY_PROCESS_RESOURCES,
    CAPABILITY_SEAT_WALK,
    CAPABILITY_SYSTEM_LOG_TAIL,
    COST_CHEAP,
    LINEAGE_ADAPTER,
    LINEAGE_NATIVE,
    MATURITY_INSTALLED,
    ROLE_OBSERVE,
    ROLE_TOOL,
    STATE_ABSENT,
    STATE_ERROR,
    STATE_OK,
)
from palm.system.vitality.walk import WalkOptions, discover_seats, walk_result


BAG_SEAT_REPORTS = "seat_reports"
BAG_SEAT_WALK_RESULT = "seat_walk_result"


def _summarize_seats(reports: list[SeatReport]) -> dict[str, Any]:
    """Aggregate only structural fields — no load interpretation."""
    by_state: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    by_lineage: dict[str, int] = {}
    present = 0
    for r in reports:
        by_state[r.state] = by_state.get(r.state, 0) + 1
        by_kind[r.kind] = by_kind.get(r.kind, 0) + 1
        by_lineage[r.lineage] = by_lineage.get(r.lineage, 0) + 1
        if r.present:
            present += 1
    return {
        "seat_count": len(reports),
        "present_count": present,
        "absent_count": by_state.get(STATE_ABSENT, 0),
        "error_count": by_state.get(STATE_ERROR, 0),
        "ok_count": by_state.get(STATE_OK, 0),
        "by_state": by_state,
        "by_kind": by_kind,
        "by_lineage": by_lineage,
        "native_count": by_lineage.get(LINEAGE_NATIVE, 0),
        "adapter_count": by_lineage.get(LINEAGE_ADAPTER, 0),
        "present_ids": [r.seat_id for r in reports if r.present],
        "absent_ids": [r.seat_id for r in reports if r.state == STATE_ABSENT],
    }


def sample_seat_walk(instance: Any, ctx: SampleContext) -> CapabilityFragment:
    """Core capability: discover seats on the live instance."""
    # Reuse reports if projection or a prior cap already walked.
    cached = ctx.bag.get(BAG_SEAT_REPORTS)
    if isinstance(cached, list) and cached and isinstance(cached[0], SeatReport):
        reports = list(cached)
        summary = _summarize_seats(reports)
    else:
        options = ctx.walk_options
        if options is not None and not isinstance(options, WalkOptions):
            options = None
        result = walk_result(instance, options)
        reports = list(result.reports)
        ctx.bag[BAG_SEAT_REPORTS] = reports
        ctx.bag[BAG_SEAT_WALK_RESULT] = result
        summary = _summarize_seats(reports)
        summary["probe_count"] = result.probe_count

    return CapabilityFragment.ok(
        CAPABILITY_SEAT_WALK,
        {
            "seats": reports_to_dicts(reports),
            "summary": summary,
        },
        notes=[],
        meta={"capability": CAPABILITY_SEAT_WALK},
    )


def build_seat_walk_capability() -> VitalityCapability:
    return VitalityCapability(
        id=CAPABILITY_SEAT_WALK,
        sample=sample_seat_walk,
        role=ROLE_OBSERVE,
        maturity=MATURITY_INSTALLED,
        default_enabled=True,
        cost=COST_CHEAP,
        description="Discover living seats; fold seat reports (no second write path)",
        tags=("core", "observe"),
        order=10,
    )


def build_default_capabilities() -> list[VitalityCapability]:
    """Installed core + intention stubs for catalog honesty."""
    return [
        build_seat_walk_capability(),
        intention_stub(
            CAPABILITY_EMISSION_WINDOW,
            role=ROLE_OBSERVE,
            description="Emission window + actor_kind partition (0.61.3+)",
            order=20,
            tags=("observe", "intention"),
        ),
        intention_stub(
            CAPABILITY_BOOT_MEMBERSHIP,
            role=ROLE_OBSERVE,
            description="Boot membership as capability (seat_walk already samples seat)",
            order=30,
            tags=("observe", "intention"),
        ),
        intention_stub(
            CAPABILITY_SYSTEM_LOG_TAIL,
            role=ROLE_OBSERVE,
            description="System log tail sample (BI-015 neighbor)",
            order=40,
            tags=("observe", "intention"),
        ),
        intention_stub(
            CAPABILITY_PROCESS_RESOURCES,
            role=ROLE_OBSERVE,
            description="RSS/CPU/threads (stdlib; mode-gated later)",
            order=50,
            tags=("observe", "intention"),
        ),
        intention_stub(
            CAPABILITY_LOADED_BULK,
            role=ROLE_OBSERVE,
            description="Light bulk of attached seats — visibility not shame",
            order=60,
            tags=("observe", "intention"),
        ),
        intention_stub(
            CAPABILITY_BENCHMARK,
            role=ROLE_TOOL,
            description="Benchmark tool (grow when ready)",
            order=100,
            tags=("tool", "intention"),
        ),
        intention_stub(
            CAPABILITY_MONITOR_AGENT,
            role=ROLE_TOOL,
            description="Monitor agent tool (grow when ready)",
            order=110,
            tags=("tool", "intention"),
        ),
    ]


__all__ = [
    "BAG_SEAT_REPORTS",
    "BAG_SEAT_WALK_RESULT",
    "build_default_capabilities",
    "build_seat_walk_capability",
    "sample_seat_walk",
]
