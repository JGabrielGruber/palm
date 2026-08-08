"""Assembly definition (DNA) — pure desired structure.

Floor DNA is thin: identity, role intent, refuse, places required.
Richer fields (projection, authority pointers) grow under 0.63 without
breaking these names.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self


# Builtin id used by floor (VISION-0.63 §6.1)
LOCAL_EMBEDDED_ID = "local.embedded"


@dataclass(frozen=True, slots=True)
class AssemblyDefinition:
    """Declarative desired structure for one process (DNA).

    After load, this is structure law. Profiles/env only *seed* it.
    """

    id: str
    version: str = "1"
    role_intent: str = "embedded"
    #: Capabilities / memberships this shape refuses (e.g. server_surfaces).
    refuse: frozenset[str] = field(default_factory=frozenset)
    #: Place keys that must be ready before definition-ready (empty = in-process only).
    places_required: tuple[str, ...] = ()
    #: Free-form seed notes (not business rules).
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "role_intent": self.role_intent,
            "refuse": sorted(self.refuse),
            "places_required": list(self.places_required),
            "meta": dict(self.meta),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        refuse_raw = data.get("refuse") or ()
        places_raw = data.get("places_required") or ()
        return cls(
            id=str(data.get("id") or ""),
            version=str(data.get("version") or "1"),
            role_intent=str(data.get("role_intent") or "embedded"),
            refuse=frozenset(str(x) for x in refuse_raw),
            places_required=tuple(str(x) for x in places_raw),
            meta=dict(data.get("meta") or {}),
        )


def local_embedded(*, version: str = "1") -> AssemblyDefinition:
    """Floor builtin DNA: thin body — core ground, no surfaces, no drain membership."""
    return AssemblyDefinition(
        id=LOCAL_EMBEDDED_ID,
        version=version,
        role_intent="embedded",
        refuse=frozenset({"server_surfaces", "background_drain"}),
        places_required=(),
        meta={"builtin": True, "source": "floor"},
    )


__all__ = [
    "LOCAL_EMBEDDED_ID",
    "AssemblyDefinition",
    "local_embedded",
]
