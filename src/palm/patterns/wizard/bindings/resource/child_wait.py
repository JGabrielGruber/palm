"""Nested wizard child-wait — park parent until a child job finishes.

**0.55.12:** Durable authority is :class:`~palm.core.wait.WaitInterest`
(``kind=job``, ``meta.source=nested_wizard``). The old
``WizardKeys.WAITING_FOR_CHILD`` key is **not** written for new parks; it is
still **read** once for snapshots parked before this collapse.

Unpark: :class:`~palm.common.wait.WaitPlaneService` on ``runtime.event``.
"""

from __future__ import annotations

from typing import Any

from palm.common.wait.access import (
    close_interest_for_state,
    open_interest_for_state,
)
from palm.core.orchestration import Job, JobStatus
from palm.core.resource.result import ProviderResult
from palm.core.wait import (
    WAIT_KIND_JOB,
    WaitInterest,
    find_wait_interests,
    make_job_wait,
)
from palm.patterns.wizard.bindings.context.keys import WizardKeys

# meta.source value for nested wizard parks (authority discriminator)
NESTED_WIZARD_SOURCE = "nested_wizard"


def should_wait_for_child(result: ProviderResult) -> bool:
    """Return whether a compositional invoke should park the parent wizard step."""
    if result.metadata.get("waiting_for_child_wizard"):
        return True
    data = result.data
    if isinstance(data, dict) and data.get("waiting_for_child_wizard"):
        return True
    return False


def child_wait_from_result(
    result: ProviderResult | dict[str, Any],
    *,
    step_slug: str,
    output_key: str,
    resource_ref: str | None = None,
) -> dict[str, Any]:
    """Build nested-park view from a palm provider payload (feeds interest meta)."""
    data = result.data if isinstance(result, ProviderResult) else result
    if not isinstance(data, dict):
        data = {}
    child_job_id = data.get("child_job_id") or data.get("job_id")
    child_instance_id = data.get("child_instance_id") or data.get("instance_id")
    return {
        "step_slug": step_slug,
        "output_key": output_key,
        "resource_ref": resource_ref,
        "child_job_id": str(child_job_id) if child_job_id else None,
        "child_instance_id": str(child_instance_id) if child_instance_id else None,
        "child_status": str(data.get("status") or JobStatus.WAITING_FOR_INPUT.value),
        "wait_mode": data.get("wait_mode") or result.metadata.get("wait_mode")
        if isinstance(result, ProviderResult)
        else data.get("wait_mode"),
        "child_job_href": data.get("child_job_href"),
        "child_instance_href": data.get("child_instance_href"),
        "child_payload": dict(data),
    }


def child_wait_from_interest(interest: WaitInterest) -> dict[str, Any]:
    """Project operator/pattern view from durable wait interest (authority)."""
    meta = dict(interest.meta or {})
    payload = meta.get("child_payload")
    if not isinstance(payload, dict):
        payload = {}
    return {
        "step_slug": meta.get("step_slug"),
        "output_key": meta.get("output_key"),
        "resource_ref": meta.get("resource_ref"),
        "child_job_id": interest.target_id,
        "child_instance_id": meta.get("child_instance_id"),
        "child_status": meta.get("child_status"),
        "wait_mode": meta.get("wait_mode"),
        "child_job_href": meta.get("child_job_href"),
        "child_instance_href": meta.get("child_instance_href"),
        "child_payload": payload,
    }


def nested_job_interests(state: Any) -> list[WaitInterest]:
    """Open job waits owned by nested-wizard park."""
    out: list[WaitInterest] = []
    for w in find_wait_interests(state, kind=WAIT_KIND_JOB):
        src = (w.meta or {}).get("source")
        if src == NESTED_WIZARD_SOURCE or (w.meta or {}).get("pattern_park"):
            out.append(w)
    return out


def get_child_wait(state: Any) -> dict[str, Any] | None:
    """Nested park view — **interest is authority**; residual key is migration-only."""
    interests = nested_job_interests(state)
    if interests:
        return child_wait_from_interest(interests[0])
    # Pre-0.55.12 snapshots may still carry the dual key.
    raw = _state_get(state, WizardKeys.WAITING_FOR_CHILD)
    if isinstance(raw, dict) and raw.get("child_job_id"):
        return dict(raw)
    return None


def wait_interest_from_child_wait(waiting: dict[str, Any]) -> WaitInterest | None:
    """Build a job wait interest from nested-wizard park view."""
    child_job_id = child_job_id_from_wait(waiting)
    if not child_job_id:
        return None
    meta: dict[str, Any] = {
        "source": NESTED_WIZARD_SOURCE,
        "pattern_park": True,
        "step_slug": waiting.get("step_slug"),
        "output_key": waiting.get("output_key"),
        "resource_ref": waiting.get("resource_ref"),
        "child_instance_id": waiting.get("child_instance_id"),
        "child_status": waiting.get("child_status"),
        "wait_mode": waiting.get("wait_mode"),
        "child_job_href": waiting.get("child_job_href"),
        "child_instance_href": waiting.get("child_instance_href"),
    }
    payload = waiting.get("child_payload")
    if isinstance(payload, dict):
        meta["child_payload"] = dict(payload)
    meta = {k: v for k, v in meta.items() if v is not None}
    return make_job_wait(child_job_id, meta=meta)


def open_wait_interest_for_child(state: Any, waiting: dict[str, Any]) -> WaitInterest | None:
    """Open (or refresh) nested wait interest via continue plane when bound."""
    interest = wait_interest_from_child_wait(waiting)
    if interest is None:
        return None
    return open_interest_for_state(state, interest, replace_same_target=True)


def close_wait_interest_for_child(state: Any, *, child_job_id: str | None = None) -> None:
    """Close nested job wait interest (idempotent)."""
    target = child_job_id
    if not target:
        waiting = get_child_wait(state)
        target = child_job_id_from_wait(waiting)
    if not target:
        for w in nested_job_interests(state):
            close_interest_for_state(state, kind=w.kind, target_id=w.target_id)
        return
    close_interest_for_state(state, kind=WAIT_KIND_JOB, target_id=str(target))


def set_child_wait(state: Any, payload: dict[str, Any]) -> None:
    """Park nested child: write **only** wait interest (0.55.12 authority)."""
    body = dict(payload)
    open_wait_interest_for_child(state, body)
    # Drop dual-key so interest is the sole durable record.
    _clear_legacy_child_wait_key(state)


def clear_child_wait(state: Any) -> None:
    """Clear nested park (interest + residual legacy key)."""
    waiting = get_child_wait(state)
    child_id = child_job_id_from_wait(waiting)
    close_wait_interest_for_child(state, child_job_id=child_id)
    _clear_legacy_child_wait_key(state)


def child_job_id_from_wait(waiting: dict[str, Any] | None) -> str | None:
    if not waiting:
        return None
    raw = waiting.get("child_job_id")
    return str(raw) if raw else None


def poll_child_job(runtime: Any, child_job_id: str) -> Job | None:
    getter = getattr(runtime, "get_job", None)
    if not callable(getter):
        return None
    try:
        return getter(child_job_id)
    except Exception:
        return None


def child_is_terminal(job: Job) -> bool:
    return job.is_terminal


def child_is_live(job: Job) -> bool:
    return job.status in (JobStatus.RUNNING, JobStatus.WAITING_FOR_INPUT)


def default_child_wait_prompt(waiting: dict[str, Any]) -> str:
    child_job_id = waiting.get("child_job_id") or "child"
    status = waiting.get("child_status") or JobStatus.WAITING_FOR_INPUT.value
    return (
        f"Waiting for nested wizard (job {child_job_id}, status={status}). "
        "Complete the child wizard to continue this step."
    )


def _clear_legacy_child_wait_key(state: Any) -> None:
    deleter = getattr(state, "delete", None)
    if callable(deleter):
        deleter(WizardKeys.WAITING_FOR_CHILD)


def _state_get(state: Any, key: str) -> Any:
    getter = getattr(state, "get", None)
    return getter(key) if callable(getter) else None
