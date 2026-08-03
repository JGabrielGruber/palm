"""
System start phase: optional palm provider bind (system.bind).

Subject: provider runtime binding (common registry).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.common.providers._registry import get_runtime_binding
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip


def run(ctx: BootContext, _options: Mapping[str, Any]) -> None:
    bind_runtime = get_runtime_binding()
    if bind_runtime is None:
        raise PhaseSkip("no_runtime_binding")
    bind_runtime(resolve_shell(ctx))


DEFINITION = PhaseDefinition(
    id="system.bind",
    run=run,
    description="Optional palm provider bind",
)

__all__ = ["DEFINITION", "run"]
