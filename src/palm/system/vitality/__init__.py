"""
System vitality — living-kernel observation (0.61).

Eyes on the live ``SystemInstance`` graph: seat discovery, seat reports,
capability registry, and projection snapshot. **Observation only** — not a
plane of start/continue.

| Slice | Landed |
|-------|--------|
| **0.61.1** | Seat-report protocol + dynamic walk |
| **0.61.2** | VitalityRegistry + VitalityProjection (``seat_walk``) |

**Adapter stance:** transitional residue only — not architecture of record.
Forward design = discover + native + receive; interpret elsewhere (product).

See [VISION-0.61](docs/VISION-0.61.md) · [ADR-030](docs/adr/030-system-vitality.md).
"""

from __future__ import annotations

from palm.system.vitality.adapters import prefer_native, sample_raw
from palm.system.vitality.capability import (
    CapabilityFragment,
    SampleContext,
    VitalityCapability,
    intention_stub,
)
from palm.system.vitality.capabilities import (
    build_default_capabilities,
    build_seat_walk_capability,
    sample_seat_walk,
)
from palm.system.vitality.probe import (
    ProbeCatalog,
    SeatProbe,
    attr_resolver,
    fixed_probes,
    private_attr_resolver,
)
from palm.system.vitality.projection import (
    ProjectionOptions,
    VitalityProjection,
    VitalitySnapshot,
    project,
    project_seat_walk_only,
    project_top,
)
from palm.system.vitality.protocol import SeatReportable, has_seat_report, try_native_report
from palm.system.vitality.registry import VitalityRegistry, installed_only
from palm.system.vitality.report import (
    SeatReport,
    coerce_report,
    index_by_seat_id,
    reports_to_dicts,
)
from palm.system.vitality.schema import (
    CAPABILITY_BENCHMARK,
    CAPABILITY_BOOT_MEMBERSHIP,
    CAPABILITY_EMISSION_WINDOW,
    CAPABILITY_FRAGMENT_SCHEMA,
    CAPABILITY_LOADED_BULK,
    CAPABILITY_MONITOR_AGENT,
    CAPABILITY_PROCESS_RESOURCES,
    CAPABILITY_SEAT_WALK,
    CAPABILITY_SYSTEM_LOG_TAIL,
    COST_CHEAP,
    COST_EXPENSIVE,
    COST_MODERATE,
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
    LINEAGE_SAMPLED,
    MATURITY_INSTALLED,
    MATURITY_INTENTION,
    ROLE_OBSERVE,
    ROLE_TOOL,
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
    VITALITY_SNAPSHOT_SCHEMA,
    supervisor_service_seat_id,
)
from palm.system.vitality.seats import (
    build_default_probes,
    default_probe_catalog,
    reset_default_probe_catalog_for_tests,
)
from palm.system.vitality.seats_registry import (
    default_vitality_registry,
    reset_default_vitality_registry_for_tests,
)
from palm.system.vitality.walk import (
    SeatWalkResult,
    WalkOptions,
    discover_seats,
    seat_walk,
    walk_result,
)

__all__ = [
    "CAPABILITY_BENCHMARK",
    "CAPABILITY_BOOT_MEMBERSHIP",
    "CAPABILITY_EMISSION_WINDOW",
    "CAPABILITY_FRAGMENT_SCHEMA",
    "CAPABILITY_LOADED_BULK",
    "CAPABILITY_MONITOR_AGENT",
    "CAPABILITY_PROCESS_RESOURCES",
    "CAPABILITY_SEAT_WALK",
    "CAPABILITY_SYSTEM_LOG_TAIL",
    "COST_CHEAP",
    "COST_EXPENSIVE",
    "COST_MODERATE",
    "CapabilityFragment",
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
    "LINEAGE_SAMPLED",
    "MATURITY_INSTALLED",
    "MATURITY_INTENTION",
    "ProbeCatalog",
    "ProjectionOptions",
    "ROLE_OBSERVE",
    "ROLE_TOOL",
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
    "SampleContext",
    "SeatProbe",
    "SeatReport",
    "SeatReportable",
    "SeatWalkResult",
    "VITALITY_SNAPSHOT_SCHEMA",
    "VitalityCapability",
    "VitalityProjection",
    "VitalityRegistry",
    "VitalitySnapshot",
    "WalkOptions",
    "attr_resolver",
    "build_default_capabilities",
    "build_default_probes",
    "build_seat_walk_capability",
    "coerce_report",
    "default_probe_catalog",
    "default_vitality_registry",
    "discover_seats",
    "fixed_probes",
    "has_seat_report",
    "index_by_seat_id",
    "installed_only",
    "intention_stub",
    "prefer_native",
    "private_attr_resolver",
    "project",
    "sample_raw",
    "project_seat_walk_only",
    "project_top",
    "reports_to_dicts",
    "reset_default_probe_catalog_for_tests",
    "reset_default_vitality_registry_for_tests",
    "sample_seat_walk",
    "seat_walk",
    "supervisor_service_seat_id",
    "try_native_report",
    "walk_result",
]
