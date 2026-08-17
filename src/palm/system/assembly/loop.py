"""Assembly loop — structure assemble: tick engine, apply intents, fold observations."""

from __future__ import annotations

from dataclasses import dataclass

from palm.core.assembly import (
    AssembleResult,
    AssemblyDefinition,
    AssemblyEngine,
    Observation,
)
from palm.system.assembly.effects import EffectPort

DEFAULT_MAX_TICKS = 32


@dataclass(frozen=True, slots=True)
class AssembleLoopResult:
    """Outcome of structure assemble-until-steady."""

    last: AssembleResult
    ticks: int
    steady: bool
    """True when phase is READY or BLOCKED (or EMPTY with no definition)."""


def assemble_until_steady(
    engine: AssemblyEngine,
    effects: EffectPort,
    *,
    max_ticks: int = DEFAULT_MAX_TICKS,
) -> AssembleLoopResult:
    """Run reconcile loop until ready/blocked or tick budget exhausted.

    Structure assemble / place registry only — not the product job path.
    System applies effect intents between ticks.
    """
    if max_ticks < 1:
        max_ticks = 1

    last: AssembleResult | None = None
    for i in range(1, max_ticks + 1):
        result = engine.tick()
        last = result
        for intent in result.intents:
            observations = effects.apply(intent)
            for obs in observations:
                engine.observe(obs)

        phase = result.status.phase.value
        if phase in ("ready", "blocked", "empty"):
            return AssembleLoopResult(last=result, ticks=i, steady=True)
        if not result.changed and not result.intents:
            # No progress
            return AssembleLoopResult(last=result, ticks=i, steady=False)

    assert last is not None
    return AssembleLoopResult(last=last, ticks=max_ticks, steady=False)


def load_and_assemble(
    engine: AssemblyEngine,
    effects: EffectPort,
    definition: AssemblyDefinition,
    *,
    max_ticks: int = DEFAULT_MAX_TICKS,
    pre_observations: tuple[Observation, ...] = (),
) -> AssembleLoopResult:
    """Receive the structure definition, fold optional observations, then assemble until steady."""
    engine.receive_definition(definition)
    for obs in pre_observations:
        engine.observe(obs)
    return assemble_until_steady(engine, effects, max_ticks=max_ticks)


__all__ = [
    "DEFAULT_MAX_TICKS",
    "AssembleLoopResult",
    "assemble_until_steady",
    "load_and_assemble",
]
