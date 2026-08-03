"""
Default discovery seeds for Palm living seats (0.61.1).

These probes observe attach points that composition + boot already wire
(0.57–0.60). They are **seeds**, not a closed forever menu: register more
via :class:`~palm.system.vitality.probe.ProbeCatalog`.
"""

from __future__ import annotations

from typing import Any

from palm.system.vitality.adapters import (
    adapt_boot_membership,
    adapt_execution,
    adapt_session_plane,
    adapt_supervisor,
    adapt_system_log,
    adapt_wait_plane,
    adapt_work_plane,
)
from palm.system.vitality.probe import (
    ProbeCatalog,
    SeatProbe,
    attr_resolver,
    private_attr_resolver,
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
    SEAT_SESSION_PLANE,
    SEAT_SUPERVISOR,
    SEAT_SYSTEM_LOG,
    SEAT_WAIT_PLANE,
    SEAT_WORK_PLANE,
)


def _resolve_execution(instance: Any) -> Any | None:
    """Execution port: property or the instance itself when it is the port."""
    port = getattr(instance, "execution", None)
    if port is not None:
        return port
    # BaseRuntime is the port structurally; still count as attached shell.
    if callable(getattr(instance, "invoke_resource", None)):
        return instance
    return None


def _resolve_system_log(instance: Any) -> Any | None:
    """Process system log — optional per-instance attr, else process default."""
    bound = getattr(instance, "system_log", None)
    if bound is not None:
        return bound
    try:
        from palm.system.log import get_system_log

        return get_system_log()
    except Exception:
        return None


def _report_system_log(instance: Any) -> SeatReport:
    log = _resolve_system_log(instance)
    if log is None:
        return SeatReport.absent(
            SEAT_SYSTEM_LOG,
            KIND_LOG,
            reason="system_log_unavailable",
        )
    return adapt_system_log(instance, log)


def build_default_probes() -> list[SeatProbe]:
    """Ordered default probes for a Palm SystemInstance graph."""
    return [
        SeatProbe(
            seat_id=SEAT_WAIT_PLANE,
            kind=KIND_PLANE,
            resolve=attr_resolver("wait_plane"),
            report=adapt_wait_plane,
            order=10,
            tags=("core", "plane"),
            description="Continue plane (wait interests on runtime.event)",
        ),
        SeatProbe(
            seat_id=SEAT_SESSION_PLANE,
            kind=KIND_PLANE,
            resolve=attr_resolver("session_plane"),
            report=adapt_session_plane,
            order=20,
            tags=("core", "plane"),
            description="Session plane (outside subject lifecycle)",
        ),
        SeatProbe(
            seat_id=SEAT_WORK_PLANE,
            kind=KIND_PLANE,
            resolve=attr_resolver("work_plane"),
            report=adapt_work_plane,
            order=30,
            tags=("core", "plane"),
            description="Start plane (WorkIntent enqueue / tick)",
        ),
        SeatProbe(
            seat_id=SEAT_SUPERVISOR,
            kind=KIND_SUPERVISOR,
            resolve=attr_resolver("supervisor"),
            report=adapt_supervisor,
            order=40,
            tags=("core", "supervisor"),
            description="Continuous system services supervisor",
        ),
        SeatProbe(
            seat_id=SEAT_EXECUTION,
            kind=KIND_PORT,
            resolve=_resolve_execution,
            report=adapt_execution,
            order=50,
            tags=("core", "port"),
            description="ExecutionPort (resource + workload effects)",
        ),
        SeatProbe(
            seat_id=SEAT_SYSTEM_LOG,
            kind=KIND_LOG,
            resolve=_resolve_system_log,
            report=lambda inst, log: adapt_system_log(inst, log),
            report_instance=_report_system_log,
            order=60,
            tags=("core", "log", "process"),
            description="Process system log ring (observation tape)",
        ),
        SeatProbe(
            seat_id=SEAT_BOOT_MEMBERSHIP,
            kind=KIND_BOOT,
            resolve=private_attr_resolver(
                "last_boot_walk",
                "_last_boot_walk",
            ),
            report=lambda inst, walk: adapt_boot_membership(inst, walk),
            when_absent="report",
            order=70,
            tags=("core", "boot"),
            description="Last system boot walk / membership facts",
        ),
    ]


_DEFAULT: ProbeCatalog | None = None


def default_probe_catalog(*, clone: bool = True) -> ProbeCatalog:
    """Return the default Palm probe catalog.

    When *clone* is True (default), callers get an isolated copy safe to
    mutate for tests or composition profiles.
    """
    global _DEFAULT
    if _DEFAULT is None:
        cat = ProbeCatalog()
        cat.extend(build_default_probes())
        _DEFAULT = cat
    return _DEFAULT.clone() if clone else _DEFAULT


def reset_default_probe_catalog_for_tests() -> None:
    """Drop cached default catalog (tests only)."""
    global _DEFAULT
    _DEFAULT = None


__all__ = [
    "build_default_probes",
    "default_probe_catalog",
    "reset_default_probe_catalog_for_tests",
]
