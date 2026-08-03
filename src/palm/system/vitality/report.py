"""
SeatReport — versioned unit of vitality truth (0.61.1).

Each discovered seat contributes one report. Projection (later) folds many
reports into a snapshot. This type is the protocol surface for native seats
and for raw-sampled public API payloads (``meta.raw``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping

from palm.system.vitality.schema import (
    KNOWN_KINDS,
    KNOWN_LINEAGES,
    KNOWN_STATES,
    LEGACY_LINEAGES,
    LINEAGE_ADAPTER,
    LINEAGE_NATIVE,
    LINEAGE_SAMPLED,
    SEAT_REPORT_SCHEMA,
    STATE_ABSENT,
    STATE_DEGRADED,
    STATE_ERROR,
    STATE_OK,
    STATE_SKIPPED,
)


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _clean_notes(notes: list[str] | tuple[str, ...] | None) -> list[str]:
    if not notes:
        return []
    out: list[str] = []
    for n in notes:
        s = str(n).strip()
        if s and s not in out:
            out.append(s)
    return out


def _clean_load(load: Mapping[str, Any] | None) -> dict[str, Any]:
    if not load:
        return {}
    return {str(k): v for k, v in load.items() if v is not None}


@dataclass
class SeatReport:
    """One seat's self-report (or honest absent / error / skipped).

    Fields match VISION-0.61 §6.3 / ADR-030 D4. Extra structured detail may
    live under :attr:`load` (vitality counters) or :attr:`meta` (lineage
    provenance, raw fragment refs — not dual truth).
    """

    seat_id: str
    kind: str
    present: bool
    state: str
    load: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    lineage: str = LINEAGE_NATIVE
    schema: str = SEAT_REPORT_SCHEMA
    meta: dict[str, Any] = field(default_factory=dict)
    sample_ts: str | None = None

    def __post_init__(self) -> None:
        self.seat_id = str(self.seat_id or "").strip()
        if not self.seat_id:
            raise ValueError("seat_id required")
        self.kind = str(self.kind or "").strip() or "other"
        self.state = str(self.state or "").strip() or STATE_ERROR
        self.lineage = str(self.lineage or "").strip() or LINEAGE_NATIVE
        # CS-007: coerce legacy adapter lineage to sampled (do not emit adapter).
        if self.lineage == LINEAGE_ADAPTER or self.lineage in LEGACY_LINEAGES:
            self.meta = dict(self.meta or {})
            self.meta.setdefault("legacy_lineage", LINEAGE_ADAPTER)
            self.lineage = LINEAGE_SAMPLED
        self.schema = str(self.schema or "").strip() or SEAT_REPORT_SCHEMA
        self.present = bool(self.present)
        self.load = _clean_load(self.load)
        self.notes = _clean_notes(self.notes)
        self.meta = dict(self.meta or {})
        # Consistency: absent seats are never "present".
        if self.state == STATE_ABSENT:
            self.present = False
        if self.present is False and self.state == STATE_OK:
            # Presence false with ok is incoherent — coerce to absent.
            self.state = STATE_ABSENT

    # ── factories ────────────────────────────────────────────────────────────

    @classmethod
    def ok(
        cls,
        seat_id: str,
        kind: str,
        *,
        load: Mapping[str, Any] | None = None,
        notes: list[str] | tuple[str, ...] | None = None,
        lineage: str = LINEAGE_NATIVE,
        meta: Mapping[str, Any] | None = None,
        sample_ts: str | None = None,
        stamp: bool = False,
    ) -> SeatReport:
        return cls(
            seat_id=seat_id,
            kind=kind,
            present=True,
            state=STATE_OK,
            load=dict(load or {}),
            notes=list(notes or []),
            lineage=lineage,
            meta=dict(meta or {}),
            sample_ts=sample_ts or (_now_iso() if stamp else None),
        )

    @classmethod
    def degraded(
        cls,
        seat_id: str,
        kind: str,
        *,
        load: Mapping[str, Any] | None = None,
        notes: list[str] | tuple[str, ...] | None = None,
        lineage: str = LINEAGE_NATIVE,
        meta: Mapping[str, Any] | None = None,
        sample_ts: str | None = None,
        stamp: bool = False,
    ) -> SeatReport:
        return cls(
            seat_id=seat_id,
            kind=kind,
            present=True,
            state=STATE_DEGRADED,
            load=dict(load or {}),
            notes=list(notes or []),
            lineage=lineage,
            meta=dict(meta or {}),
            sample_ts=sample_ts or (_now_iso() if stamp else None),
        )

    @classmethod
    def absent(
        cls,
        seat_id: str,
        kind: str,
        *,
        notes: list[str] | tuple[str, ...] | None = None,
        reason: str | None = None,
        meta: Mapping[str, Any] | None = None,
        sample_ts: str | None = None,
        stamp: bool = False,
    ) -> SeatReport:
        note_list = list(notes or [])
        if reason:
            note_list.append(str(reason))
        return cls(
            seat_id=seat_id,
            kind=kind,
            present=False,
            state=STATE_ABSENT,
            notes=note_list,
            lineage=LINEAGE_NATIVE,
            meta=dict(meta or {}),
            sample_ts=sample_ts or (_now_iso() if stamp else None),
        )

    @classmethod
    def error(
        cls,
        seat_id: str,
        kind: str,
        *,
        reason: str,
        present: bool = True,
        load: Mapping[str, Any] | None = None,
        lineage: str = LINEAGE_NATIVE,
        meta: Mapping[str, Any] | None = None,
        sample_ts: str | None = None,
        stamp: bool = False,
    ) -> SeatReport:
        return cls(
            seat_id=seat_id,
            kind=kind,
            present=present,
            state=STATE_ERROR,
            load=dict(load or {}),
            notes=[str(reason)],
            lineage=lineage,
            meta=dict(meta or {}),
            sample_ts=sample_ts or (_now_iso() if stamp else None),
        )

    @classmethod
    def skipped(
        cls,
        seat_id: str,
        kind: str,
        *,
        reason: str,
        present: bool = False,
        meta: Mapping[str, Any] | None = None,
        sample_ts: str | None = None,
        stamp: bool = False,
    ) -> SeatReport:
        return cls(
            seat_id=seat_id,
            kind=kind,
            present=present,
            state=STATE_SKIPPED,
            notes=[str(reason)],
            lineage=LINEAGE_NATIVE,
            meta=dict(meta or {}),
            sample_ts=sample_ts or (_now_iso() if stamp else None),
        )

    # ── serialization ────────────────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """Canonical dict form (schema ``palm.seat_report/1``)."""
        row: dict[str, Any] = {
            "schema": self.schema,
            "seat_id": self.seat_id,
            "kind": self.kind,
            "present": self.present,
            "state": self.state,
            "load": dict(self.load),
            "notes": list(self.notes),
            "lineage": self.lineage,
        }
        if self.meta:
            row["meta"] = dict(self.meta)
        if self.sample_ts is not None:
            row["sample_ts"] = self.sample_ts
        return row

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SeatReport:
        """Parse a seat-report dict. Raises ``ValueError`` on hard failures."""
        if not isinstance(data, Mapping):
            raise ValueError("seat report must be a mapping")
        seat_id = str(data.get("seat_id") or "").strip()
        if not seat_id:
            raise ValueError("seat_id required")
        kind = str(data.get("kind") or "other").strip() or "other"
        state = str(data.get("state") or STATE_ERROR).strip() or STATE_ERROR
        present = bool(data.get("present", state not in (STATE_ABSENT, STATE_SKIPPED)))
        load = data.get("load") if isinstance(data.get("load"), Mapping) else {}
        notes_raw = data.get("notes")
        if isinstance(notes_raw, str):
            notes: list[str] = [notes_raw]
        elif isinstance(notes_raw, (list, tuple)):
            notes = [str(n) for n in notes_raw]
        else:
            notes = []
        lineage = str(data.get("lineage") or LINEAGE_NATIVE).strip() or LINEAGE_NATIVE
        schema = str(data.get("schema") or SEAT_REPORT_SCHEMA).strip() or SEAT_REPORT_SCHEMA
        meta = data.get("meta") if isinstance(data.get("meta"), Mapping) else {}
        sample_ts = data.get("sample_ts")
        return cls(
            seat_id=seat_id,
            kind=kind,
            present=present,
            state=state,
            load=dict(load),
            notes=notes,
            lineage=lineage,
            schema=schema,
            meta=dict(meta),
            sample_ts=None if sample_ts is None else str(sample_ts),
        )

    def with_note(self, note: str) -> SeatReport:
        """Return a copy with an extra note (immutable-style)."""
        notes = list(self.notes)
        s = str(note).strip()
        if s and s not in notes:
            notes.append(s)
        return SeatReport(
            seat_id=self.seat_id,
            kind=self.kind,
            present=self.present,
            state=self.state,
            load=dict(self.load),
            notes=notes,
            lineage=self.lineage,
            schema=self.schema,
            meta=dict(self.meta),
            sample_ts=self.sample_ts,
        )

    def validate(self, *, strict_kind: bool = False) -> list[str]:
        """Return soft validation warnings (empty = clean). Does not raise."""
        warnings: list[str] = []
        if self.schema != SEAT_REPORT_SCHEMA:
            warnings.append(f"schema_mismatch:{self.schema}")
        if strict_kind and self.kind not in KNOWN_KINDS:
            warnings.append(f"unknown_kind:{self.kind}")
        if self.state not in KNOWN_STATES:
            warnings.append(f"unknown_state:{self.state}")
        if self.lineage not in KNOWN_LINEAGES:
            warnings.append(f"unknown_lineage:{self.lineage}")
        if self.state == STATE_ABSENT and self.present:
            warnings.append("absent_but_present")
        if self.lineage == LINEAGE_SAMPLED and "raw" not in self.meta:
            warnings.append("sampled_without_raw")
        return warnings


def coerce_report(
    value: SeatReport | Mapping[str, Any],
    *,
    default_seat_id: str | None = None,
    default_kind: str = "other",
    default_lineage: str = LINEAGE_NATIVE,
) -> SeatReport:
    """Normalize a SeatReport or mapping into a SeatReport."""
    if isinstance(value, SeatReport):
        return value
    if not isinstance(value, Mapping):
        raise TypeError(f"cannot coerce seat report from {type(value)!r}")
    data = dict(value)
    if "seat_id" not in data and default_seat_id:
        data["seat_id"] = default_seat_id
    if "kind" not in data:
        data["kind"] = default_kind
    if "lineage" not in data:
        data["lineage"] = default_lineage
    if "present" not in data and "state" in data:
        data["present"] = str(data["state"]) not in (STATE_ABSENT, STATE_SKIPPED)
    elif "present" not in data:
        data["present"] = True
        data.setdefault("state", STATE_OK)
    return SeatReport.from_dict(data)


def reports_to_dicts(reports: list[SeatReport]) -> list[dict[str, Any]]:
    return [r.to_dict() for r in reports]


def index_by_seat_id(reports: list[SeatReport]) -> dict[str, SeatReport]:
    return {r.seat_id: r for r in reports}


__all__ = [
    "SeatReport",
    "coerce_report",
    "index_by_seat_id",
    "reports_to_dicts",
]
