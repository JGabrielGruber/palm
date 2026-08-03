"""
System plane roster — what planes a system instance runs (0.61).

**Single definition of record.** Boot attaches these; vitality discovers them.
Not composition (planes ≠ plugins). Not vitality private seeds.

If a new system plane is added, it lands here first. Schedule attach and
observation both follow this table.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final


@dataclass(frozen=True)
class SystemPlaneSpec:
    """One system plane the machine may run."""

    plane_id: str
    """Short id (``wait``, ``session``, ``work``)."""

    attr: str
    """Public property on the system instance (``wait_plane``, …)."""

    description: str = ""

    @property
    def seat_id(self) -> str:
        """Observation / vitality seat id — same as instance attr by law."""
        return self.attr


# Fixed system set today. Membership is system schedule attach, not CompositionProfile.
SYSTEM_PLANES: Final[tuple[SystemPlaneSpec, ...]] = (
    SystemPlaneSpec(
        "wait",
        "wait_plane",
        "Continue plane — interests / unpark",
    ),
    SystemPlaneSpec(
        "session",
        "session_plane",
        "Session plane — owner sessions",
    ),
    SystemPlaneSpec(
        "work",
        "work_plane",
        "Work plane — intents / drain",
    ),
)


def system_plane_ids() -> tuple[str, ...]:
    return tuple(p.plane_id for p in SYSTEM_PLANES)


def system_plane_attrs() -> tuple[str, ...]:
    return tuple(p.attr for p in SYSTEM_PLANES)


def system_plane_seat_ids() -> tuple[str, ...]:
    return tuple(p.seat_id for p in SYSTEM_PLANES)


def get_system_plane(plane_id_or_attr: str) -> SystemPlaneSpec | None:
    for p in SYSTEM_PLANES:
        if p.plane_id == plane_id_or_attr or p.attr == plane_id_or_attr:
            return p
    return None


def plane_attachment_snapshot(instance: Any) -> dict[str, bool]:
    """Which roster planes are attached on *instance* (public attrs)."""
    out: dict[str, bool] = {}
    for p in SYSTEM_PLANES:
        out[p.attr] = getattr(instance, p.attr, None) is not None
    return out


def missing_roster_planes(instance: Any) -> tuple[str, ...]:
    """Roster attrs that are None / missing on *instance*."""
    return tuple(
        p.attr
        for p in SYSTEM_PLANES
        if getattr(instance, p.attr, None) is None
    )


def roster_catalog() -> list[dict[str, str]]:
    """Inspect / doctor dump of the system plane roster."""
    return [
        {
            "plane_id": p.plane_id,
            "attr": p.attr,
            "seat_id": p.seat_id,
            "description": p.description,
        }
        for p in SYSTEM_PLANES
    ]


__all__ = [
    "SYSTEM_PLANES",
    "SystemPlaneSpec",
    "get_system_plane",
    "missing_roster_planes",
    "plane_attachment_snapshot",
    "roster_catalog",
    "system_plane_attrs",
    "system_plane_ids",
    "system_plane_seat_ids",
]
