"""
Default discovery seeds for Palm living seats (0.61).

**Planes** come from :data:`palm.system.planes.roster.SYSTEM_PLANES` — the
system definition of record. Vitality does **not** own a private plane list.

Other seeds (supervisor, execution, log, boot) declare where to look and which
public API to raw-sample. Product interprets ``meta.raw``.
"""

from __future__ import annotations

from typing import Any

from palm.system.planes.roster import SYSTEM_PLANES
from palm.system.vitality.probe import (
    ProbeCatalog,
    SeatProbe,
    attr_resolver,
    private_attr_resolver,
)
from palm.system.vitality.raw import (
    bound_convention_reporter,
    bound_method_reporter,
    bound_sequence_reporter,
    sample_attrs,
)
from palm.system.vitality.report import SeatReport
from palm.system.vitality.schema import (
    KIND_BOOT,
    KIND_LOG,
    KIND_PLANE,
    KIND_PORT,
    KIND_SUPERVISOR,
    SEAT_BOOT_MEMBERSHIP,
    SEAT_EXECUTION,
    SEAT_SUPERVISOR,
    SEAT_SYSTEM_LOG,
)


def _resolve_execution(instance: Any) -> Any | None:
    port = getattr(instance, "execution", None)
    if port is not None:
        return port
    if callable(getattr(instance, "invoke_resource", None)):
        return instance
    return None


def _resolve_system_log(instance: Any) -> Any | None:
    bound = getattr(instance, "system_log", None)
    if bound is not None:
        return bound
    try:
        from palm.system.log import get_system_log

        return get_system_log()
    except Exception:
        return None


def _report_execution(instance: Any, port: Any) -> SeatReport:
    return sample_attrs(
        port,
        seat_id=SEAT_EXECUTION,
        kind=KIND_PORT,
        attrs=("invoke_resource", "start_workload"),
        source="execution_port",
        instance=instance,
        instance_attrs=("is_started",),
        extra_raw={
            "has_invoke_resource": callable(getattr(port, "invoke_resource", None)),
            "has_start_workload": callable(getattr(port, "start_workload", None)),
            "port_type": type(port).__name__,
        },
    )


def _report_system_log(instance: Any, log: Any) -> SeatReport:
    return sample_attrs(
        log,
        seat_id=SEAT_SYSTEM_LOG,
        kind=KIND_LOG,
        attrs=("record_count", "capacity", "level", "console"),
        source="system_log_public",
    )


def _report_system_log_instance(instance: Any) -> SeatReport:
    log = _resolve_system_log(instance)
    if log is None:
        return SeatReport.absent(
            SEAT_SYSTEM_LOG,
            KIND_LOG,
            reason="system_log_unavailable",
        )
    return _report_system_log(instance, log)


def _plane_probes_from_roster() -> list[SeatProbe]:
    """Plane discovery seeds — driven only by SYSTEM_PLANES."""
    probes: list[SeatProbe] = []
    for i, spec in enumerate(SYSTEM_PLANES):
        probes.append(
            SeatProbe(
                seat_id=spec.seat_id,
                kind=KIND_PLANE,
                resolve=attr_resolver(spec.attr),
                report=bound_convention_reporter(spec.seat_id, KIND_PLANE),
                order=10 + i,
                tags=("core", "plane", spec.plane_id),
                description=spec.description or f"System plane {spec.plane_id}",
            )
        )
    return probes


def build_default_probes() -> list[SeatProbe]:
    """Ordered default probes — planes from roster; rest raw public APIs."""
    return [
        *_plane_probes_from_roster(),
        SeatProbe(
            seat_id=SEAT_SUPERVISOR,
            kind=KIND_SUPERVISOR,
            resolve=attr_resolver("supervisor"),
            report=bound_method_reporter(SEAT_SUPERVISOR, KIND_SUPERVISOR, "status"),
            order=40,
            tags=("core", "supervisor"),
            description="Supervisor — raw status()",
        ),
        SeatProbe(
            seat_id=SEAT_EXECUTION,
            kind=KIND_PORT,
            resolve=_resolve_execution,
            report=_report_execution,
            order=50,
            tags=("core", "port"),
            description="ExecutionPort — raw port attrs",
        ),
        SeatProbe(
            seat_id=SEAT_SYSTEM_LOG,
            kind=KIND_LOG,
            resolve=_resolve_system_log,
            report=_report_system_log,
            report_instance=_report_system_log_instance,
            order=60,
            tags=("core", "log", "process"),
            description="System log — raw public attrs",
        ),
        SeatProbe(
            seat_id=SEAT_BOOT_MEMBERSHIP,
            kind=KIND_BOOT,
            resolve=private_attr_resolver("last_boot_walk", "_last_boot_walk"),
            report=bound_sequence_reporter(
                SEAT_BOOT_MEMBERSHIP, KIND_BOOT, source="last_boot_walk"
            ),
            when_absent="report",
            order=70,
            tags=("core", "boot"),
            description="Boot walk — raw phase rows",
        ),
    ]


_DEFAULT: ProbeCatalog | None = None


def default_probe_catalog(*, clone: bool = True) -> ProbeCatalog:
    global _DEFAULT
    if _DEFAULT is None:
        cat = ProbeCatalog()
        cat.extend(build_default_probes())
        _DEFAULT = cat
    return _DEFAULT.clone() if clone else _DEFAULT


def reset_default_probe_catalog_for_tests() -> None:
    global _DEFAULT
    _DEFAULT = None


__all__ = [
    "build_default_probes",
    "default_probe_catalog",
    "reset_default_probe_catalog_for_tests",
]
