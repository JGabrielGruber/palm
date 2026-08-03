"""Phase: system.storage.select."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.boot.assembly import select_system_storage
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    storage = select_system_storage(resolve_shell(ctx), options)
    ctx.publish(storage=storage)


DEFINITION = PhaseDefinition(
    id="system.storage.select",
    run=run,
    description="StorageFactory when storage not yet initialized",
)
