"""
System vitality — living-kernel observation (0.61).

Eyes on the live ``SystemInstance`` graph: seat discovery, seat reports,
and (later) projection + registry. **Observation only** — not a plane of
start/continue.

Slice **0.61.1:** seat-report protocol + dynamic walk + lineage-marked adapters.

See [VISION-0.61](docs/VISION-0.61.md) · [ADR-030](docs/adr/030-system-vitality.md).
"""

from __future__ import annotations

from palm.system.vitality.adapters import prefer_native
from palm.system.vitality.probe import (
    ProbeCatalog,
    SeatProbe,
    attr_resolver,
    fixed_probes,
    private_attr_resolver,
)
from palm.system.vitality.protocol import SeatReportable, has_seat_report, try_native_report
from palm.system.vitality.report import (
    SeatReport,
    coerce_report,
    index_by_seat_id,
    reports_to_dicts,
)
from palm.system.vitality.schema import (
    CAPABILITY_SEAT_WALK,
    KIND_BOOT,
    KIND_ENGINE,
    KIND_LOG,
    KIND_OTHER,
    KIND_PLANE,
    KIND_PORT,
    KIND_SUPERVISOR,
    KIND_SUPERVISOR_SERVICE,
    LINEAGE_ADAPTER,
    LINEAGE_NATIVE,
    SEAT_BOOT_MEMBERSHIP,
    SEAT_EXECUTION,
    SEAT_REPORT_SCHEMA,
    SEAT_SESSION_PLANE,
    SEAT_SUPERVISOR,
    SEAT_SYSTEM_LOG,
    SEAT_WAIT_PLANE,
    SEAT_WORK_PLANE,
    STATE_ABSENT,
    STATE_DEGRADED,
    STATE_ERROR,
    STATE_OK,
    STATE_SKIPPED,
    supervisor_service_seat_id,
)
from palm.system.vitality.seats import (
    build_default_probes,
    default_probe_catalog,
    reset_default_probe_catalog_for_tests,
)
from palm.system.vitality.walk import (
    SeatWalkResult,
    WalkOptions,
    discover_seats,
    seat_walk,
    walk_result,
)

__all__ = [
    "CAPABILITY_SEAT_WALK",
    "KIND_BOOT",
    "KIND_ENGINE",
    "KIND_LOG",
    "KIND_OTHER",
    "KIND_PLANE",
    "KIND_PORT",
    "KIND_SUPERVISOR",
    "KIND_SUPERVISOR_SERVICE",
    "LINEAGE_ADAPTER",
    "LINEAGE_NATIVE",
    "ProbeCatalog",
    "SEAT_BOOT_MEMBERSHIP",
    "SEAT_EXECUTION",
    "SEAT_REPORT_SCHEMA",
    "SEAT_SESSION_PLANE",
    "SEAT_SUPERVISOR",
    "SEAT_SYSTEM_LOG",
    "SEAT_WAIT_PLANE",
    "SEAT_WORK_PLANE",
    "STATE_ABSENT",
    "STATE_DEGRADED",
    "STATE_ERROR",
    "STATE_OK",
    "STATE_SKIPPED",
    "SeatProbe",
    "SeatReport",
    "SeatReportable",
    "SeatWalkResult",
    "WalkOptions",
    "attr_resolver",
    "build_default_probes",
    "coerce_report",
    "default_probe_catalog",
    "discover_seats",
    "fixed_probes",
    "has_seat_report",
    "index_by_seat_id",
    "prefer_native",
    "private_attr_resolver",
    "reports_to_dicts",
    "reset_default_probe_catalog_for_tests",
    "seat_walk",
    "supervisor_service_seat_id",
    "try_native_report",
    "walk_result",
]
