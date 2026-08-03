"""
System start phase: system log ready (system.log.ready).

Subject: :mod:`palm.system.log`.
Host mode application lives under ``palm.app.host.boot`` (composition-aware).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.log.system_log import SystemLog, get_system_log


def ensure_system_log_ready(
    ctx: BootContext,
    *,
    log: SystemLog | None = None,
) -> SystemLog:
    """System schedule body for ``system.log.ready``."""
    slog = log if log is not None else get_system_log()
    slog.info(
        "system_log.ready",
        "system log ready (system schedule)",
        schedule="system",
        mode=ctx.mode,
        runtime=ctx.runtime,
        log_level=slog.level,
    )
    return slog


def system_log_ready_handler(ctx: BootContext) -> None:
    ensure_system_log_ready(ctx)


def run(ctx: BootContext, _options: Mapping[str, Any]) -> None:
    ensure_system_log_ready(ctx)


DEFINITION = PhaseDefinition(
    id="system.log.ready",
    run=run,
    description="Ensure SystemLog is process-ready (early console)",
)

__all__ = [
    "DEFINITION",
    "ensure_system_log_ready",
    "run",
    "system_log_ready_handler",
]
