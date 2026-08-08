"""Assembly seat — engine + effect port + published admission on the shell."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from palm.core.assembly import (
    AdmissionSnapshot,
    AssemblyDefinition,
    AssemblyEngine,
    AssemblyStatus,
    Observation,
    ObservationKind,
    local_embedded,
    refuse_violations,
)
from palm.system.assembly.effects import AssemblyEffectPort
from palm.system.assembly.household import HouseholdEffectPort
from palm.system.assembly.loop import (
    AssembleLoopResult,
    DEFAULT_MAX_TICKS,
    assemble_until_steady,
)


@dataclass
class AssemblySeat:
    """System-owned assembly organ (not product control)."""

    engine: AssemblyEngine = field(default_factory=AssemblyEngine)
    effects: AssemblyEffectPort = field(default_factory=HouseholdEffectPort)
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
        surfaces: Iterable[str] = (),
        capabilities: Iterable[str] = (),
        force: bool = False,
    ) -> AssembleLoopResult:
        """Household: load DNA (default embedded) and reconcile until steady.

        When *surfaces* / *capabilities* are provided, DNA refuse is checked
        (0.63.6). Violations block admission — fail closed, no soft dual.

        *force* voids same-id READY and re-converges (0.63.18 reassemble edge).
        Membership is always re-evaluated: prior refuse reasons clear first.
        """
        dna = definition if definition is not None else local_embedded()
        self.definition = dna
        bind = getattr(self.effects, "bind_structure", None)
        if callable(bind):
            bind(dna, surfaces=surfaces, capabilities=capabilities)
        # Honest membership re-check before / after definition load.
        self.engine.observe(
            Observation(kind=ObservationKind.STRUCTURE_POLICY_CLEARED)
        )
        self.engine.receive_definition(dna, force=force)
        for reason in refuse_violations(
            dna, surfaces=surfaces, capabilities=capabilities
        ):
            self.engine.observe(
                Observation(
                    kind=ObservationKind.STRUCTURE_POLICY_VIOLATION,
                    target=reason,
                )
            )
        result = assemble_until_steady(
            self.engine,
            self.effects,
            max_ticks=max_ticks,
        )
        self.last_loop = result
        return result

    def reassemble(
        self,
        definition: AssemblyDefinition | None = None,
        *,
        max_ticks: int = DEFAULT_MAX_TICKS,
        surfaces: Iterable[str] = (),
        capabilities: Iterable[str] = (),
        force: bool = False,
    ) -> AssembleLoopResult:
        """Re-converge after DNA or membership change (0.63.18).

        Uses the current seat definition when *definition* is omitted.
        Fails closed while invalidated/blocked; citizens must not soft-skip.
        """
        dna = (
            definition
            if definition is not None
            else (self.definition if self.definition is not None else local_embedded())
        )
        return self.assemble(
            dna,
            max_ticks=max_ticks,
            surfaces=surfaces,
            capabilities=capabilities,
            force=force,
        )

    def reset(self) -> None:
        self.engine.shutdown()
        self.engine.initialize()
        self.last_loop = None
        self.definition = None


__all__ = ["AssemblySeat"]
