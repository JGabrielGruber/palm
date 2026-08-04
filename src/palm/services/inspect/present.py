"""Present system vitality for surfaces (product door).

Law (ADR-030 / VISION-0.61): truth lives in ``palm.system.vitality``.
Product **reads** ``project`` / ``project_top`` and shapes operate envelopes.
Does not invent seat counters or a second observation home.
"""

from __future__ import annotations

from typing import Any

from palm.system.vitality import ProjectionOptions, project, project_top

# Provenance tag for product envelopes that nest projection.
SOURCE_VITALITY = "palm.system.vitality"


def present_top(
    instance: Any,
    options: ProjectionOptions | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Living ``top`` view — structural fold from vitality projection only."""
    top = project_top(instance, options, **kwargs)
    # Product envelope: mark source without rewriting system fields.
    if isinstance(top, dict) and "source" not in top:
        top = {**top, "source": SOURCE_VITALITY}
    return top


def present_vitality(
    instance: Any,
    options: ProjectionOptions | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Full vitality snapshot dict from projection only."""
    snap = project(instance, options, **kwargs)
    body = snap.to_dict()
    body["source"] = SOURCE_VITALITY
    return body


def present_vitality_for_doctor(top: dict[str, Any]) -> dict[str, Any]:
    """Thin vitality pointer nested under legacy doctor (OD-001 demotion path)."""
    return {
        "source": SOURCE_VITALITY,
        "schema": top.get("schema"),
        "sample_ts": top.get("sample_ts"),
        "summary": dict(top.get("summary") or {}),
        "note": (
            "Living physiology is system vitality; doctor packaging is legacy. "
            "Use InspectService.top / vitality for the operate eyes path."
        ),
    }


__all__ = [
    "SOURCE_VITALITY",
    "present_top",
    "present_vitality",
    "present_vitality_for_doctor",
]
