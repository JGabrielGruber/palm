"""Structure core exceptions."""

from __future__ import annotations

from palm.core.exceptions import EngineError, PalmError


class StructureError(PalmError):
    """Base for structure pure-layer errors."""


class StructureEngineError(EngineError, StructureError):
    """Structure engine misuse or invariant break."""


class NoDefinitionError(StructureEngineError):
    """Operation requires a loaded structure definition."""


__all__ = [
    "StructureEngineError",
    "StructureError",
    "NoDefinitionError",
]
