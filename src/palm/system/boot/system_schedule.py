"""
System schedule — bind phase definitions for the walker (0.59.3 / 0.61 OCP).

**Ownership**

| Owns | Module |
|------|--------|
| *When* / order | :mod:`palm.system.boot.phases` (``SYSTEM_PHASES``) |
| *How* | :class:`~palm.system.boot.definition.PhaseDefinition` at the edge |
| Catalog | :mod:`palm.system.boot.catalog` |
| Walk | :func:`~palm.system.boot.walker.walk_schedule` |

This module only **binds** catalog definitions to handlers (seed shell fallback).
It does not open-code engines, hooks, planes, or skip folklore.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from palm.system.boot.catalog import (
    DEFAULT_SYSTEM_PHASE_DEFINITIONS,
    definitions_for_phases,
)
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.phases import system_phase_ids
from palm.system.boot.shell import resolve_shell
from palm.system.boot.walker import PhaseHandler


def bind_phase_handlers(
    definitions: Sequence[PhaseDefinition],
    *,
    options: Mapping[str, Any] | None = None,
    shell_fallback: Any | None = None,
) -> dict[str, PhaseHandler]:
    """
    Bind phase definitions to walker handlers.

    Each handler: resolve shell (optional fallback) → ``defn.run(ctx, options)``.
    """
    opts = dict(options or {})

    handlers: dict[str, PhaseHandler] = {}
    for defn in definitions:
        # Capture defn in default arg (avoid late-binding in loop).
        def _make(d: PhaseDefinition) -> PhaseHandler:
            def handler(ctx: BootContext) -> None:
                resolve_shell(ctx, fallback=shell_fallback)
                d.run(ctx, opts)

            return handler

        handlers[defn.id] = _make(defn)
    return handlers


def build_system_handlers(
    runtime: Any | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, PhaseHandler]:
    """
    Build system schedule handlers from the phase definition catalog.

    *runtime* is optional when ``ctx.shell`` is set before the walk
    (``BaseRuntime.start`` sets it). Used only as shell fallback.
    """
    # Prefer table order when binding (unknown table ids simply omit).
    ordered = definitions_for_phases(system_phase_ids())
    if not ordered:
        ordered = list(DEFAULT_SYSTEM_PHASE_DEFINITIONS)
    return bind_phase_handlers(
        ordered,
        options=options,
        shell_fallback=runtime,
    )


__all__ = ["bind_phase_handlers", "build_system_handlers"]
