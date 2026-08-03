"""Phase: system.plugins.ensure."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.common.plugins import ensure_core_plugins
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition


def run(_ctx: BootContext, _options: Mapping[str, Any]) -> None:
    ensure_core_plugins()


DEFINITION = PhaseDefinition(
    id="system.plugins.ensure",
    run=run,
    description="ensure_core_plugins (idempotent)",
)
