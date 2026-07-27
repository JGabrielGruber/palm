"""Deliver wait-target completion into the owner job (continue plane).

Nested wizard parks store ``output_key`` + payload seed in interest meta.
On positive match the plane writes the final payload and the pattern advances
without re-polling after interest close.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from palm.core.wait import WAIT_KIND_JOB, WaitInterest

# Shared with wizard nested_park (string constant — no pattern import from common).
NESTED_WIZARD_SOURCE = "nested_wizard"


def is_nested_wizard_interest(interest: WaitInterest) -> bool:
    meta = interest.meta or {}
    return (
        interest.kind == WAIT_KIND_JOB
        and (
            meta.get("source") == NESTED_WIZARD_SOURCE
            or bool(meta.get("pattern_park"))
        )
    )


def deliver_nested_wizard_completion(
    owner_job: Any,
    interest: WaitInterest,
    get_job: Callable[[str], Any],
) -> bool:
    """Write child result onto owner state at meta.output_key. Returns True if written."""
    if not is_nested_wizard_interest(interest):
        return False
    meta = interest.meta or {}
    output_key = meta.get("output_key")
    if not output_key:
        return False
    child = None
    try:
        child = get_job(str(interest.target_id))
    except Exception:
        child = None
    if child is None:
        return False
    status = getattr(getattr(child, "status", None), "value", None) or str(
        getattr(child, "status", "")
    )
    if str(status).upper() != "SUCCEEDED":
        return False

    payload = dict(meta.get("child_payload") or {})
    child_meta = getattr(child, "metadata", None) or {}
    if not isinstance(child_meta, dict):
        child_meta = {}
    result = getattr(child, "result", None)
    if result is None:
        # Prefer wizard commit result if present on child state.
        state = getattr(child, "state", None)
        if state is not None and hasattr(state, "get"):
            result = state.get("__wizard__.commit_result")
    payload.update(
        {
            "job_id": getattr(child, "id", interest.target_id),
            "instance_id": child_meta.get("instance_id"),
            "status": str(status),
            "result": result,
            "waiting_for_child_wizard": False,
            "delivered_by": "wait_plane",
        }
    )
    owner_state = getattr(owner_job, "state", None)
    if owner_state is None or not hasattr(owner_state, "set"):
        return False
    owner_state.set(str(output_key), payload)
    return True


__all__ = [
    "NESTED_WIZARD_SOURCE",
    "deliver_nested_wizard_completion",
    "is_nested_wizard_interest",
]
