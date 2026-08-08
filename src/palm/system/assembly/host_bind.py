"""Host structure bind — wire shell WorkloadEngine into assembly place hands (0.63.17).

Default household hands stay in-process for bare places. Host assemble upgrades
them to the combined ``os:`` + ``workload:`` spawn port and binds the live
engine when it is initialized.

**Opt-in:** on by default when the engine is ready; off via
``assembly_bind_workload=False``. Does not force composition membership.
Does not replace custom effect ports without a place book.
"""

from __future__ import annotations

from typing import Any

from palm.system.assembly.household import HouseholdEffectPort
from palm.system.assembly.place_book import PlaceBookEffectPort
from palm.system.assembly.place_spawn import InProcessPlaceSpawn, RegisteredPlaceSpawn
from palm.system.assembly.seat import AssemblySeat
from palm.system.assembly.workload_place import (
    WorkloadPlaceSpawn,
    combined_structure_spawn_port,
)


def resolve_workload_engine(shell: Any) -> Any | None:
    """Return shell.workload when present and initialized; else None."""
    engine = getattr(shell, "workload", None)
    if engine is None:
        return None
    if not getattr(engine, "is_initialized", False):
        return None
    return engine


def place_book_port(effects: Any) -> PlaceBookEffectPort | None:
    """Extract the place-book hands from household or bare place-book effects."""
    if isinstance(effects, PlaceBookEffectPort):
        return effects
    places = getattr(effects, "places", None)
    if isinstance(places, PlaceBookEffectPort):
        return places
    return None


def workload_spawn_hands(spawn: Any) -> WorkloadPlaceSpawn | None:
    """Find WorkloadPlaceSpawn stashed on a registered port (if any)."""
    handles = getattr(spawn, "handles", None)
    if not isinstance(handles, dict):
        return None
    hands = handles.get("__workload_spawn__")
    if isinstance(hands, WorkloadPlaceSpawn):
        return hands
    return None


def _has_structure_prefixes(spawn: Any) -> bool:
    if not isinstance(spawn, RegisteredPlaceSpawn):
        return False
    prefixes = getattr(spawn, "prefix_ensures", {}) or {}
    return any(p.startswith(("os:", "workload:")) for p in prefixes)


def bind_host_structure_to_seat(
    seat: AssemblySeat,
    shell: Any,
    *,
    bind_workload: bool = True,
) -> dict[str, Any]:
    """Upgrade default place hands and optionally bind shell WorkloadEngine.

    Returns a small report for logs and tests::

        {
          "bound": bool,           # spawn port mutated or engine attached
          "engine": bool,          # live engine bound
          "spawn": str,            # combined | existing | unchanged
          "skipped": str | None,   # why no work (no_place_book, …)
        }
    """
    report: dict[str, Any] = {
        "bound": False,
        "engine": False,
        "spawn": "unchanged",
        "skipped": None,
    }
    book = place_book_port(seat.effects)
    if book is None:
        report["skipped"] = "no_place_book"
        return report

    engine = resolve_workload_engine(shell) if bind_workload else None
    existing = workload_spawn_hands(book.spawn)

    if existing is not None:
        if engine is not None and existing.engine is not engine:
            existing.bind_engine(engine)
            report["bound"] = True
            report["engine"] = True
            report["spawn"] = "existing"
            return report
        if engine is not None and existing.engine is engine:
            report["bound"] = True
            report["engine"] = True
            report["spawn"] = "already"
            return report
        # Hands present but no engine (or bind disabled) — leave fail-closed.
        report["skipped"] = (
            "bind_disabled" if not bind_workload else "engine_not_ready"
        )
        report["spawn"] = "existing"
        return report

    # Default in-process (or bare registered without structure prefixes) → combined.
    if isinstance(book.spawn, InProcessPlaceSpawn) or not _has_structure_prefixes(
        book.spawn
    ):
        book.spawn = combined_structure_spawn_port(engine=engine)
        report["bound"] = True
        report["engine"] = engine is not None
        report["spawn"] = "combined"
        if engine is None and bind_workload:
            report["skipped"] = "engine_not_ready"
        elif not bind_workload:
            report["skipped"] = "bind_disabled"
        return report

    # Custom registered spawn without our workload hands — do not clobber.
    report["skipped"] = "custom_spawn"
    return report


def default_household_effects(*, engine: Any | None = None) -> HouseholdEffectPort:
    """Household hands with combined structure spawn (os: + workload:)."""
    return HouseholdEffectPort(
        places=PlaceBookEffectPort(spawn=combined_structure_spawn_port(engine=engine))
    )


__all__ = [
    "bind_host_structure_to_seat",
    "default_household_effects",
    "place_book_port",
    "resolve_workload_engine",
    "workload_spawn_hands",
]
