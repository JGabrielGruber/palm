"""Place-book + structure-intent effect port (0.63.15).

Closed intent set from pure assembly: ensure/release place, invalidate/refresh
projection, apply structure policy, request structure seed. System hands only.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from palm.core.assembly import (
    AssemblyDefinition,
    EffectIntent,
    EffectIntentKind,
    Observation,
    ObservationKind,
    refuse_violations,
)
from palm.system.assembly.place_book import PlaceBookEffectPort


@dataclass
class HouseholdEffectPort:
    """Default assembly hands: places + projection/policy/seed structure intents."""

    places: PlaceBookEffectPort = field(default_factory=PlaceBookEffectPort)
    definition: AssemblyDefinition | None = None
    surfaces: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    projections_loaded: set[str] = field(default_factory=set)
    applied: list[EffectIntent] = field(default_factory=list)

    def bind_structure(
        self,
        definition: AssemblyDefinition | None,
        *,
        surfaces: Iterable[str] = (),
        capabilities: Iterable[str] = (),
    ) -> None:
        """Bind structure definition + membership so APPLY_STRUCTURE_POLICY can re-check refuse."""
        self.definition = definition
        self.surfaces = tuple(str(s) for s in surfaces if s)
        self.capabilities = tuple(str(c) for c in capabilities if c)

    @property
    def book(self):
        """Ledger passthrough for tests that dig ``effects.book``."""
        return self.places.book

    @property
    def spawn(self):
        return self.places.spawn

    def apply(self, intent: EffectIntent) -> tuple[Observation, ...]:
        self.applied.append(intent)
        kind = intent.kind

        if kind in (EffectIntentKind.ENSURE_PLACE, EffectIntentKind.RELEASE_PLACE):
            return self.places.apply(intent)

        target = str(intent.target or "").strip()

        if kind is EffectIntentKind.INVALIDATE_PROJECTION:
            name = target or "default"
            self.projections_loaded.discard(name)
            return (
                Observation(
                    kind=ObservationKind.PROJECTION_FAILED,
                    target=name,
                    payload={"reason": "invalidated"},
                ),
            )

        if kind is EffectIntentKind.REFRESH_PROJECTION:
            name = target or "default"
            # Floor: local projection “load” succeeds (no remote authority yet).
            self.projections_loaded.add(name)
            return (
                Observation(
                    kind=ObservationKind.PROJECTION_LOADED,
                    target=name,
                    payload={"reason": "refreshed"},
                ),
            )

        if kind is EffectIntentKind.APPLY_STRUCTURE_POLICY:
            if self.definition is None:
                return (
                    Observation(
                        kind=ObservationKind.STRUCTURE_SEED_FAILED,
                        target=target or "policy",
                        payload={"reason": "no_definition"},
                    ),
                )
            violations = refuse_violations(
                self.definition,
                surfaces=self.surfaces,
                capabilities=self.capabilities,
            )
            if violations:
                return tuple(
                    Observation(
                        kind=ObservationKind.STRUCTURE_POLICY_VIOLATION,
                        target=reason,
                    )
                    for reason in violations
                )
            # Clear common refuse codes when membership is clean.
            clear_targets = (
                "refuse:server_surfaces",
                "refuse:http_server_surfaces",
                "refuse:product_catalog_home",
            )
            return tuple(
                Observation(
                    kind=ObservationKind.STRUCTURE_POLICY_CLEARED,
                    target=code,
                )
                for code in clear_targets
            )

        if kind is EffectIntentKind.REQUEST_STRUCTURE_SEED:
            if self.definition is None:
                return (
                    Observation(
                        kind=ObservationKind.STRUCTURE_SEED_FAILED,
                        target=target or "seed",
                        payload={"reason": "no_definition"},
                    ),
                )
            return (
                Observation(
                    kind=ObservationKind.STRUCTURE_SEED_FINISHED,
                    target=self.definition.id,
                    payload={"version": self.definition.version},
                ),
            )

        return ()


__all__ = ["HouseholdEffectPort"]
