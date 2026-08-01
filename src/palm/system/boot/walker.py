"""
Schedule walker — control path for boot phases (0.59.2+).

Observation goes through SystemLog only (no second narrative).
Missing handlers are honest: skip with reason from seat type.
Handlers may raise :class:`PhaseSkip` for optional declines (0.59.3).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from palm.system.boot.context import BootContext
from palm.system.boot.phases import PhaseSpec
from palm.system.boot.skip import PhaseSkip
from palm.system.log import SystemLog, get_system_log

PhaseHandler = Callable[[BootContext], None]
WalkOutcome = Literal["ok", "skip", "fail"]


@dataclass(frozen=True)
class WalkedPhase:
    """Result of one phase on a walk."""

    phase: str
    schedule: str
    outcome: WalkOutcome
    reason: str | None = None
    duration_ms: float | None = None
    seat: str | None = None

    def to_dict(self) -> dict[str, Any]:
        row: dict[str, Any] = {
            "phase": self.phase,
            "schedule": self.schedule,
            "outcome": self.outcome,
        }
        if self.reason is not None:
            row["reason"] = self.reason
        if self.duration_ms is not None:
            row["duration_ms"] = self.duration_ms
        if self.seat is not None:
            row["seat"] = self.seat
        return row


def _skip_reason_for_seat(seat: str) -> str:
    if seat == "imperative":
        return "imperative_until_migrated"
    if seat == "stub":
        return "not_migrated"
    return "no_handler"


def walk_schedule(
    phases: Sequence[PhaseSpec],
    handlers: Mapping[str, PhaseHandler] | None = None,
    *,
    ctx: BootContext | None = None,
    log: SystemLog | None = None,
    require_handlers: bool = False,
    schedule: str | None = None,
) -> list[WalkedPhase]:
    """Walk a phase table in order.

    Parameters
    ----------
    phases:
        Ordered phase specs (usually ``HOST_PHASES`` / ``SYSTEM_PHASES``).
    handlers:
        Map phase id → callable. Implemented seats should register handlers.
    ctx:
        Shared context; created if omitted.
    log:
        SystemLog used for phase.start/end/skip/fail. Defaults to process log.
    require_handlers:
        When True, missing handler fails the walk for ``implemented`` seats.
        When False (default), missing handler → honest skip by seat type.
    schedule:
        Override schedule name on context when phases may be mixed (rare).
    """
    handlers = handlers or {}
    slog = log if log is not None else get_system_log()
    if not phases:
        return []
    sched = schedule or phases[0].schedule
    boot_ctx = ctx or BootContext(schedule=sched)
    if boot_ctx.schedule != sched and schedule is None:
        boot_ctx.schedule = sched

    walked: list[WalkedPhase] = []
    for spec in phases:
        handler = handlers.get(spec.id)
        if handler is None:
            reason = _skip_reason_for_seat(spec.seat)
            if require_handlers and spec.seat == "implemented":
                slog.phase_fail(spec.schedule, spec.id, reason="missing_handler")
                walked.append(
                    WalkedPhase(
                        phase=spec.id,
                        schedule=spec.schedule,
                        outcome="fail",
                        reason="missing_handler",
                        seat=spec.seat,
                    )
                )
                raise RuntimeError(
                    f"boot phase {spec.id!r} is implemented but has no handler"
                )
            slog.phase_skip(spec.schedule, spec.id, reason=reason)
            walked.append(
                WalkedPhase(
                    phase=spec.id,
                    schedule=spec.schedule,
                    outcome="skip",
                    reason=reason,
                    seat=spec.seat,
                )
            )
            continue

        slog.phase_start(
            spec.schedule,
            spec.id,
            mode=boot_ctx.mode,
            runtime=boot_ctx.runtime,
            seat=spec.seat,
        )
        t0 = time.perf_counter()
        try:
            handler(boot_ctx)
        except PhaseSkip as skip:
            duration_ms = round((time.perf_counter() - t0) * 1000.0, 1)
            slog.phase_skip(
                spec.schedule,
                spec.id,
                reason=skip.reason,
                duration_ms=duration_ms,
                mode=boot_ctx.mode,
                runtime=boot_ctx.runtime,
            )
            walked.append(
                WalkedPhase(
                    phase=spec.id,
                    schedule=spec.schedule,
                    outcome="skip",
                    reason=skip.reason,
                    duration_ms=duration_ms,
                    seat=spec.seat,
                )
            )
            continue
        except Exception as exc:
            duration_ms = round((time.perf_counter() - t0) * 1000.0, 1)
            slog.phase_fail(
                spec.schedule,
                spec.id,
                reason=f"{type(exc).__name__}: {exc}",
                duration_ms=duration_ms,
                mode=boot_ctx.mode,
                runtime=boot_ctx.runtime,
            )
            walked.append(
                WalkedPhase(
                    phase=spec.id,
                    schedule=spec.schedule,
                    outcome="fail",
                    reason=f"{type(exc).__name__}: {exc}",
                    duration_ms=duration_ms,
                    seat=spec.seat,
                )
            )
            raise
        duration_ms = round((time.perf_counter() - t0) * 1000.0, 1)
        slog.phase_end(
            spec.schedule,
            spec.id,
            duration_ms=duration_ms,
            mode=boot_ctx.mode,
            runtime=boot_ctx.runtime,
        )
        walked.append(
            WalkedPhase(
                phase=spec.id,
                schedule=spec.schedule,
                outcome="ok",
                duration_ms=duration_ms,
                seat=spec.seat,
            )
        )
    return walked


__all__ = [
    "PhaseHandler",
    "PhaseSkip",
    "WalkOutcome",
    "WalkedPhase",
    "walk_schedule",
]
