"""
Vitality capability contract — named observe/tool eyes (0.61.2).

Capabilities sample a live instance and return a **fragment**. Projection
merges enabled fragments into a snapshot. Capabilities do not start or
continue work.

Architecture of record for eyes growth (ADR-030 D5). Seat *probes* discover
attachments; *capabilities* are the registry of what observation tools run.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from palm.system.vitality.schema import (
    CAPABILITY_FRAGMENT_SCHEMA,
    COST_CHEAP,
    MATURITY_INSTALLED,
    ROLE_OBSERVE,
    STATE_ERROR,
    STATE_OK,
    STATE_SKIPPED,
)


@dataclass
class SampleContext:
    """Shared bag for one projection sample (observation only).

    Capabilities may read/write :attr:`bag` to avoid double-walking when
    later caps want the same seat reports. They must not mutate the instance
    as a side channel for work.
    """

    mode: str | None = None
    """Deployment / runtime mode hint (``safe``, ``test``, …) — cost gates."""

    walk_options: Any | None = None
    """Optional :class:`~palm.system.vitality.walk.WalkOptions` for seat_walk."""

    bag: dict[str, Any] = field(default_factory=dict)
    """Per-sample scratch (e.g. cached seat reports)."""

    enable_ids: frozenset[str] | None = None
    """If set by projection, the effective enable set for this sample."""


@dataclass
class CapabilityFragment:
    """One capability's contribution to a vitality snapshot.

    Projection does **not** re-interpret seat load contents. It records what
    the capability returned, with ``capability_id`` lineage.
    """

    capability_id: str
    present: bool
    state: str
    data: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    schema: str = CAPABILITY_FRAGMENT_SCHEMA
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.capability_id = str(self.capability_id or "").strip()
        if not self.capability_id:
            raise ValueError("capability_id required")
        self.state = str(self.state or STATE_ERROR).strip() or STATE_ERROR
        self.present = bool(self.present)
        self.data = dict(self.data or {})
        self.notes = [str(n) for n in (self.notes or []) if str(n).strip()]
        self.meta = dict(self.meta or {})
        self.schema = str(self.schema or CAPABILITY_FRAGMENT_SCHEMA)

    def to_dict(self) -> dict[str, Any]:
        row: dict[str, Any] = {
            "schema": self.schema,
            "capability_id": self.capability_id,
            "present": self.present,
            "state": self.state,
            "data": dict(self.data),
            "notes": list(self.notes),
        }
        if self.meta:
            row["meta"] = dict(self.meta)
        return row

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CapabilityFragment:
        if not isinstance(data, Mapping):
            raise ValueError("fragment must be a mapping")
        return cls(
            capability_id=str(data.get("capability_id") or ""),
            present=bool(data.get("present", True)),
            state=str(data.get("state") or STATE_ERROR),
            data=dict(data.get("data") or {})
            if isinstance(data.get("data"), Mapping)
            else {},
            notes=list(data.get("notes") or [])
            if isinstance(data.get("notes"), (list, tuple))
            else [],
            schema=str(data.get("schema") or CAPABILITY_FRAGMENT_SCHEMA),
            meta=dict(data.get("meta") or {})
            if isinstance(data.get("meta"), Mapping)
            else {},
        )

    @classmethod
    def ok(
        cls,
        capability_id: str,
        data: Mapping[str, Any] | None = None,
        *,
        notes: list[str] | None = None,
        meta: Mapping[str, Any] | None = None,
    ) -> CapabilityFragment:
        return cls(
            capability_id=capability_id,
            present=True,
            state=STATE_OK,
            data=dict(data or {}),
            notes=list(notes or []),
            meta=dict(meta or {}),
        )

    @classmethod
    def skipped(
        cls,
        capability_id: str,
        reason: str,
        *,
        meta: Mapping[str, Any] | None = None,
    ) -> CapabilityFragment:
        return cls(
            capability_id=capability_id,
            present=False,
            state=STATE_SKIPPED,
            notes=[str(reason)],
            meta=dict(meta or {}),
        )

    @classmethod
    def error(
        cls,
        capability_id: str,
        reason: str,
        *,
        meta: Mapping[str, Any] | None = None,
    ) -> CapabilityFragment:
        return cls(
            capability_id=capability_id,
            present=False,
            state=STATE_ERROR,
            notes=[str(reason)],
            meta=dict(meta or {}),
        )


# instance + SampleContext -> CapabilityFragment
CapabilitySampler = Callable[[Any, SampleContext], CapabilityFragment]


@dataclass(frozen=True)
class VitalityCapability:
    """Named eye in the vitality registry.

    Parameters
    ----------
    id:
        Stable capability id (e.g. ``seat_walk``).
    sample:
        Observation callable. Must not start/continue work.
    role:
        ``observe`` or ``tool``.
    maturity:
        ``installed`` or ``intention`` (experimental stubs).
    default_enabled:
        Whether projection enables this by default when maturity is installed.
    cost:
        Hint for mode gating (cheap by default for safe/test).
    """

    id: str
    sample: CapabilitySampler
    role: str = ROLE_OBSERVE
    maturity: str = MATURITY_INSTALLED
    default_enabled: bool = True
    cost: str = COST_CHEAP
    description: str = ""
    tags: tuple[str, ...] = ()
    order: int = 100

    def __post_init__(self) -> None:
        cid = str(self.id or "").strip()
        if not cid:
            raise ValueError("VitalityCapability.id required")
        object.__setattr__(self, "id", cid)
        if not callable(self.sample):
            raise TypeError("VitalityCapability.sample must be callable")


def intention_stub(
    capability_id: str,
    *,
    role: str = ROLE_OBSERVE,
    description: str = "",
    order: int = 500,
    tags: tuple[str, ...] = (),
) -> VitalityCapability:
    """Register an intention capability that always reports skipped."""

    def _sample(_instance: Any, _ctx: SampleContext) -> CapabilityFragment:
        return CapabilityFragment.skipped(
            capability_id,
            "intention_not_implemented",
            meta={"maturity": "intention"},
        )

    return VitalityCapability(
        id=capability_id,
        sample=_sample,
        role=role,
        maturity="intention",
        default_enabled=False,
        cost=COST_CHEAP,
        description=description or f"Intention stub: {capability_id}",
        tags=tags or ("intention",),
        order=order,
    )


__all__ = [
    "CapabilityFragment",
    "CapabilitySampler",
    "SampleContext",
    "VitalityCapability",
    "intention_stub",
]
