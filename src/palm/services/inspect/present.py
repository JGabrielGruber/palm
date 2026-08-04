"""Present system vitality for surfaces (product door).

Law (ADR-030 / VISION-0.61): truth lives in ``palm.system.vitality``.
Product **reads** ``project`` / ``project_top`` and shapes operate envelopes.
Does not invent seat counters or a second observation home.

0.61.6 / OD-001: legacy ``doctor`` is **anatomy packaging** only. Living eyes
are :func:`present_top` / :func:`present_vitality`. Doctor may nest those;
it must not invent living seat law.
"""

from __future__ import annotations

from typing import Any

from palm.system.vitality import ProjectionOptions, project, project_top

# Provenance tag for product envelopes that nest projection.
SOURCE_VITALITY = "palm.system.vitality"

# Demoted doctor envelope (OD-001).
DOCTOR_KIND = "legacy_doctor"
DOCTOR_ROLE = "anatomy_packaging"
OPERATE_EYES_PATHS = (
    "inspect/top",
    "inspect/vitality",
    "assist/top",
    "assist/vitality",
)

DOCTOR_DEMOTE_NOTE = (
    "Living physiology is system vitality (inspect top / vitality). "
    "Doctor is legacy anatomy packaging — storage, registries, job counts, "
    "contributor sections — not seat law. Prefer operate_paths for eyes."
)


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
    """Thin vitality pointer nested under legacy doctor (OD-001)."""
    return {
        "source": SOURCE_VITALITY,
        "schema": top.get("schema"),
        "sample_ts": top.get("sample_ts"),
        "summary": dict(top.get("summary") or {}),
        "note": DOCTOR_DEMOTE_NOTE,
    }


def present_doctor(
    anatomy: dict[str, Any],
    *,
    top: dict[str, Any] | None = None,
    vitality: dict[str, Any] | None = None,
    top_error: str | None = None,
) -> dict[str, Any]:
    """Demote anatomy packaging under a legacy doctor envelope.

    Flat packaging keys from ``anatomy`` stay for consumers (storage, jobs,
    registries, issues, …). Living eyes are explicit: ``top`` / ``vitality``
    plus ``kind`` / ``role`` / ``eyes_law`` / ``operate_paths``.

    Does **not** invent seat counters — those live in projection only.
    """
    report = dict(anatomy)
    report["kind"] = DOCTOR_KIND
    report["role"] = DOCTOR_ROLE
    report["eyes_law"] = SOURCE_VITALITY
    report["operate_paths"] = list(OPERATE_EYES_PATHS)
    report["note"] = DOCTOR_DEMOTE_NOTE

    if top is not None:
        report["top"] = top
    elif top_error is not None:
        report["top"] = {"error": top_error, "source": SOURCE_VITALITY}

    if vitality is not None:
        report["vitality"] = vitality
    elif top is not None:
        report["vitality"] = present_vitality_for_doctor(top)
    elif top_error is not None:
        report["vitality"] = {
            "source": SOURCE_VITALITY,
            "error": top_error,
            "note": (
                "Projection sample failed; anatomy packaging still returned. "
                + DOCTOR_DEMOTE_NOTE
            ),
        }

    # Nested residual bag (honest structure; flat keys remain for compat).
    packaging_keys = (
        "status",
        "version",
        "runtime",
        "auth_enforce",
        "storage",
        "registries",
        "resource_count",
        "resource_preflight",
        "neonroot",
        "workload_host",
        "workloads",
        "control_plane",
        "jobs",
        "reactive_interests",
        "issues",
    )
    anatomy_bag = {k: report[k] for k in packaging_keys if k in report}
    if anatomy_bag:
        report["anatomy"] = anatomy_bag

    return report


__all__ = [
    "SOURCE_VITALITY",
    "DOCTOR_KIND",
    "DOCTOR_ROLE",
    "OPERATE_EYES_PATHS",
    "DOCTOR_DEMOTE_NOTE",
    "present_top",
    "present_vitality",
    "present_vitality_for_doctor",
    "present_doctor",
]
