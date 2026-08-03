"""
PhaseDefinition — participation law for one boot phase (0.61 / seat DI).

**Registry extension:** each phase owns *how* it runs (skip policy, assembly,
seat publish). The schedule table owns *when* (order). The walker only runs
handlers bound from the catalog — it does not open-code start soup.

Rhymes with :class:`~palm.system.subsystems.planes.definition.PlaneDefinition`.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from palm.system.boot.context import BootContext

# run(ctx, options) — may raise PhaseSkip for optional declines
PhaseRunFn = Callable[[BootContext, Mapping[str, Any]], None]


@dataclass(frozen=True)
class PhaseDefinition:
    """
    How one boot phase participates in a schedule walk.

    * ``id`` — must match :class:`~palm.system.boot.phases.PhaseSpec`.id
    * ``run`` — body: resolve seats, assemble, publish, or PhaseSkip
    * ``description`` — short human note (optional; table may also describe)
    """

    id: str
    run: PhaseRunFn
    description: str = ""


__all__ = ["PhaseDefinition", "PhaseRunFn"]
