"""Serialize open wait interests for inspect / list-waiting / doctor / Assist."""

from __future__ import annotations

from typing import Any

from palm.core.wait import WaitInterest, list_wait_interests, list_waits_on_job


def waiting_on_row(interest: WaitInterest) -> dict[str, Any]:
    """One operator-facing wait-interest row (why a job is parked)."""
    row: dict[str, Any] = {
        "kind": interest.kind,
        "target_id": interest.target_id,
        "opened_at": interest.opened_at,
        "on_target_failed": interest.policy.on_target_failed,
    }
    meta = interest.meta or {}
    if meta:
        # Prefer compact UX fields; keep full meta under ``meta`` when non-empty.
        for key in (
            "source",
            "step_slug",
            "output_key",
            "child_instance_id",
            "child_status",
            "resource_ref",
        ):
            if meta.get(key) is not None:
                row[key] = meta[key]
        row["meta"] = dict(meta)
    return row


def waiting_on_from_state(state: Any) -> list[dict[str, Any]]:
    """Open wait interests on a job/instance state surface."""
    return [waiting_on_row(w) for w in list_wait_interests(state)]


def waiting_on_from_job(job: Any) -> list[dict[str, Any]]:
    """Open wait interests on an orchestration job (empty if none)."""
    try:
        waits = list_waits_on_job(job)
    except Exception:
        state = getattr(job, "state", None)
        if state is None:
            return []
        return waiting_on_from_state(state)
    return [waiting_on_row(w) for w in waits]


def summarize_waiting_on(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    """One-line summary for doctor / slim lists: primary target if any."""
    if not rows:
        return None
    first = rows[0]
    summary: dict[str, Any] = {
        "count": len(rows),
        "kind": first.get("kind"),
        "target_id": first.get("target_id"),
    }
    if first.get("source") is not None:
        summary["source"] = first.get("source")
    if first.get("step_slug") is not None:
        summary["step_slug"] = first.get("step_slug")
    return summary


def child_projection_from_waiting_on(
    rows: list[dict[str, Any]] | None,
) -> dict[str, Any] | None:
    """Operator child summary from the primary open wait interest, if any."""
    if not rows:
        return None
    first = rows[0]
    if not isinstance(first, dict):
        return None
    child: dict[str, Any] = {}
    target = first.get("target_id")
    if target:
        child["job_id"] = target
    instance_id = first.get("child_instance_id")
    if instance_id:
        child["instance_id"] = instance_id
    status = first.get("child_status")
    if status:
        child["status"] = status
    return child or None


__all__ = [
    "child_projection_from_waiting_on",
    "summarize_waiting_on",
    "waiting_on_from_job",
    "waiting_on_from_state",
    "waiting_on_row",
]
