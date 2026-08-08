"""Assembly core exceptions."""

from __future__ import annotations

from palm.core.exceptions import EngineError, PalmError


class AssemblyError(PalmError):
    """Base for assembly pure-layer errors."""


class AssemblyEngineError(EngineError, AssemblyError):
    """Assembly engine misuse or invariant break."""


class NoDefinitionError(AssemblyEngineError):
    """Operation requires a loaded assembly definition."""


__all__ = [
    "AssemblyEngineError",
    "AssemblyError",
    "NoDefinitionError",
]
