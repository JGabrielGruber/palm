"""
Early system-log seats for the system schedule (0.59.2).

Host mode application lives under ``palm.app.host.boot`` (composition-aware).
This module only ensures the process SystemLog is alive — Linux early console.
"""

from __future__ import annotations

from palm.system.boot.context import BootContext
from palm.system.log import SystemLog, get_system_log


def ensure_system_log_ready(
    ctx: BootContext,
    *,
    log: SystemLog | None = None,
) -> SystemLog:
    """System schedule body for ``system.log.ready``.

    Does not import host modes. Mode-driven level configure happens on the
    host schedule (``host.system_log``) or when the host already configured
    the process log before spawn.
    """
    slog = log if log is not None else get_system_log()
    # Lifecycle level — visible under test/safe defaults (level 1).
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
    """Default handler for ``system.log.ready``."""
    ensure_system_log_ready(ctx)


__all__ = [
    "ensure_system_log_ready",
    "system_log_ready_handler",
]
