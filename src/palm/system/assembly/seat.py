"""Assembly seat — engine + effect port + published admission on the shell."""

from __future__ import annotations

from dataclasses import dataclass, field

from palm.core.assembly import (
    AdmissionSnapshot,
    AssemblyDefinition,
    AssemblyEngine,
    AssemblyStatus,
    local_embedded,
)
from palm.system.assembly.effects import AssemblyEffectPort, RecordingEffectPort
from palm.system.assembly.loop import (
    AssembleLoopResult,
    DEFAULT_MAX_TICKS,
    load_and_assemble,
)


@dataclass
class AssemblySeat:
    """System-owned assembly organ (not product control)."""

    engine: AssemblyEngine = field(default_factory=AssemblyEngine)
    effects: AssemblyEffectPort = field(default_factory=RecordingEffectPort)
    last_loop: AssembleLoopResult | None = None
    definition: AssemblyDefinition | None = None

    def __post_init__(self) -> None:
        if not self.engine.is_initialized:
            self.engine.initialize()

    def admission(self) -> AdmissionSnapshot:
        return self.engine.admission()

    def status(self) -> AssemblyStatus:
        return self.engine.status()

    def assemble(
        self,
        definition: AssemblyDefinition | None = None,
        *,
        max_ticks: int = DEFAULT_MAX_TICKS,
    ) -> AssembleLoopResult:
        """Household: load DNA (default embedded) and reconcile until steady."""
        dna = definition if definition is not None else local_embedded()
        self.definition = dna
        result = load_and_assemble(
            self.engine,
            self.effects,
            dna,
            max_ticks=max_ticks,
        )
        self.last_loop = result
        return result

    def reset(self) -> None:
        self.engine.shutdown()
        self.engine.initialize()
        self.last_loop = None
        self.definition = None


__all__ = ["AssemblySeat"]
