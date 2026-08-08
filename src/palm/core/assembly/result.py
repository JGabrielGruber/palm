"""AssembleResult — outcome of one engine tick."""

from __future__ import annotations

from dataclasses import dataclass, field

from palm.core.assembly.intent import EffectIntent
from palm.core.assembly.status import AdmissionSnapshot, AssemblyStatus


@dataclass(frozen=True, slots=True)
class AssembleResult:
    """Status after tick plus effect intents the system should apply."""

    status: AssemblyStatus
    admission: AdmissionSnapshot
    intents: tuple[EffectIntent, ...] = ()
    #: True when phase or readiness changed this tick.
    changed: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)


__all__ = ["AssembleResult"]
