"""Phase: system.log.ready."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.log_phase import ensure_system_log_ready


def run(ctx: BootContext, _options: Mapping[str, Any]) -> None:
    ensure_system_log_ready(ctx)


DEFINITION = PhaseDefinition(
    id="system.log.ready",
    run=run,
    description="Ensure SystemLog is process-ready (early console)",
)
