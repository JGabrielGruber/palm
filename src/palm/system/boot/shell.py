"""Resolve the system instance shell from a boot context."""

from __future__ import annotations

from typing import Any

from palm.system.boot.context import BootContext


def resolve_shell(ctx: BootContext, fallback: Any | None = None) -> Any:
    """
    Return the system instance for this walk.

    Prefer ``ctx.shell``. Optionally seed from *fallback* (legacy
    ``build_system_handlers(runtime, …)`` closure).
    """
    if ctx.shell is not None:
        return ctx.shell
    if fallback is not None:
        ctx.shell = fallback
        return fallback
    return ctx.require_shell()


__all__ = ["resolve_shell"]
