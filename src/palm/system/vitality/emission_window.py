"""
Emission window — recent yield / heat sample + actor partition (0.61.3).

**Law (ADR-030 D8 / VISION-0.61):**
  - Observation only — no start/continue, no second metrics write path.
  - Envelope: actor_kind · session subject · channel · kind · outcome · time.
  - Prefer **declared** actor_kind; otherwise explicit ``unknown``.
  - System-log channel may declare ``system`` as its natural emitter class
    (the log is system narrative). Do not invent human/agent from timing.

Primary source today: process :func:`~palm.system.log.get_system_log` ring.
Optional heat: live ``work_plane.status()`` when attached (pending / drops).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.system.log import get_system_log
from palm.system.vitality.capability import CapabilityFragment, SampleContext
from palm.system.vitality.schema import (
    ACTOR_KIND_SYSTEM,
    ACTOR_KIND_UNKNOWN,
    CAPABILITY_EMISSION_WINDOW,
    CHANNEL_SYSTEM_LOG,
    CHANNEL_WORK_PLANE,
    DEFAULT_EMISSION_WINDOW_LIMIT,
    KNOWN_ACTOR_KINDS,
)


def coerce_actor_kind(value: Any) -> str:
    """Map a declared label to a core actor_kind, else ``unknown``."""
    raw = str(value or "").strip().lower()
    if raw in KNOWN_ACTOR_KINDS:
        return raw
    return ACTOR_KIND_UNKNOWN


def _outcome_from_event(event: str, fields: Mapping[str, Any]) -> str:
    """Coarse outcome label from declared field or event name — not health law."""
    declared = fields.get("outcome")
    if declared is not None and str(declared).strip():
        return str(declared).strip().lower()
    ev = str(event or "").strip().lower()
    if not ev:
        return "unknown"
    if "fail" in ev or "error" in ev or ev.endswith(".error"):
        return "fail"
    if "skip" in ev:
        return "skip"
    if ev.endswith(".end") or ev in {"ready", "install.bound"}:
        return "ok"
    if ev.endswith(".start") or ev == "boot.start":
        return "start"
    return "info"


def _kind_from_event(event: str, fields: Mapping[str, Any]) -> str:
    declared = fields.get("kind")
    if declared is not None and str(declared).strip():
        return str(declared).strip()
    ev = str(event or "").strip()
    if not ev:
        return "unknown"
    if ev.startswith("phase.") or ev.startswith("boot.") or ev in {
        "ready",
        "system_log.ready",
        "install.bound",
        "plane.hub.attached",
        "supervisor.wire",
    }:
        return "lifecycle"
    head = ev.split(".", 1)[0]
    return head or "unknown"


def envelope_from_log_record(record: Any) -> dict[str, Any]:
    """Build one emission envelope from a :class:`SystemLogRecord`-like object."""
    event = str(getattr(record, "event", "") or "")
    message = str(getattr(record, "message", "") or "")
    ts = getattr(record, "ts", None)
    level = getattr(record, "level", None)
    fields = getattr(record, "fields", None)
    if not isinstance(fields, Mapping):
        fields = {}
    fields = dict(fields)

    declared = fields.get("actor_kind")
    if declared is None:
        declared = fields.get("actor")
    if declared is not None and str(declared).strip():
        actor_kind = coerce_actor_kind(declared)
        actor_source = "declared"
    else:
        # Channel is system narrative — emitter class is system, not guessed.
        actor_kind = ACTOR_KIND_SYSTEM
        actor_source = "channel_default"

    session_subject = (
        fields.get("session_subject")
        or fields.get("session_id")
        or fields.get("subject")
    )
    if session_subject is not None:
        session_subject = str(session_subject)

    return {
        "actor_kind": actor_kind,
        "actor_source": actor_source,
        "session_subject": session_subject,
        "channel": CHANNEL_SYSTEM_LOG,
        "kind": _kind_from_event(event, fields),
        "outcome": _outcome_from_event(event, fields),
        "time": None if ts is None else str(ts),
        "event": event,
        "message": message[:200] if message else "",
        "level": level,
    }


def _count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        label = str(row.get(key) or ACTOR_KIND_UNKNOWN)
        out[label] = out.get(label, 0) + 1
    return out


def _sample_work_heat(instance: Any) -> dict[str, Any] | None:
    """Optional raw heat from work plane public status — no dual counters."""
    work = getattr(instance, "work_plane", None)
    if work is None:
        return None
    status_fn = getattr(work, "status", None)
    if not callable(status_fn):
        return None
    try:
        snap = status_fn()
    except Exception:
        return None
    if not isinstance(snap, Mapping):
        return None
    return {
        "channel": CHANNEL_WORK_PLANE,
        "attached": bool(snap.get("attached")),
        "pending": snap.get("pending"),
        "dropped_depth": snap.get("dropped_depth"),
        "max_depth": snap.get("max_depth"),
        "background": snap.get("background"),
        "trigger_count": snap.get("trigger_count"),
        "raw": dict(snap),
    }


def _window_limit(ctx: SampleContext) -> int:
    raw = ctx.bag.get("emission_window_limit")
    if raw is None:
        return DEFAULT_EMISSION_WINDOW_LIMIT
    try:
        return max(1, min(500, int(raw)))
    except (TypeError, ValueError):
        return DEFAULT_EMISSION_WINDOW_LIMIT


def sample_emission_window(instance: Any, ctx: SampleContext) -> CapabilityFragment:
    """Core capability: recent emissions + actor_kind partition."""
    limit = _window_limit(ctx)
    slog = get_system_log()
    try:
        records = list(slog.recent(limit=limit))
    except Exception as exc:
        return CapabilityFragment.error(
            CAPABILITY_EMISSION_WINDOW,
            f"system_log:{type(exc).__name__}: {exc}",
            meta={"capability": CAPABILITY_EMISSION_WINDOW},
        )

    emissions = [envelope_from_log_record(r) for r in records]
    by_actor = _count_by(emissions, "actor_kind")
    by_outcome = _count_by(emissions, "outcome")
    by_channel = _count_by(emissions, "channel")
    by_kind = _count_by(emissions, "kind")
    unknown_actor = by_actor.get(ACTOR_KIND_UNKNOWN, 0)

    heat = _sample_work_heat(instance)
    sources = [CHANNEL_SYSTEM_LOG]
    if heat is not None:
        sources.append(CHANNEL_WORK_PLANE)

    summary = {
        "emission_count": len(emissions),
        "window_limit": limit,
        "by_actor_kind": by_actor,
        "by_outcome": by_outcome,
        "by_channel": by_channel,
        "by_kind": by_kind,
        "unknown_actor_count": unknown_actor,
        "sources": sources,
    }

    data: dict[str, Any] = {
        "emissions": emissions,
        "summary": summary,
    }
    if heat is not None:
        data["heat"] = heat

    notes: list[str] = []
    if not emissions:
        notes.append("empty_window")
    if unknown_actor:
        notes.append(f"unknown_actor:{unknown_actor}")

    return CapabilityFragment.ok(
        CAPABILITY_EMISSION_WINDOW,
        data,
        notes=notes,
        meta={
            "capability": CAPABILITY_EMISSION_WINDOW,
            "sample_source": "system_log+optional_work_heat",
        },
    )


__all__ = [
    "coerce_actor_kind",
    "envelope_from_log_record",
    "sample_emission_window",
]
