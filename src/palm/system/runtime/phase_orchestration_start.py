"""
System start phase: orchestration.start (system.orchestration.start).

Subject: shell orchestration engine.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell


def run(ctx: BootContext, _options: Mapping[str, Any]) -> None:
    orch = (
        ctx.orchestration
        if ctx.orchestration is not None
        else resolve_shell(ctx).orchestration
    )
    orch.start()


DEFINITION = PhaseDefinition(
    id="system.orchestration.start",
    run=run,
    description="orchestration.start — accept jobs",
)

__all__ = ["DEFINITION", "run"]
