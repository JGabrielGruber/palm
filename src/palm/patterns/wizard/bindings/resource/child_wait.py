"""Nested wizard child-wait state — suspend parent until a child job finishes.

When a parent parks on a nested child, open a durable
:class:`~palm.core.wait.WaitInterest` (``kind=job``). Unpark is owned by
:class:`~palm.common.wait.WaitMatcher` on ``runtime.event`` — not by the child
reaching up to the parent.
"""

from __future__ import annotations

from typing import Any

from palm.core.orchestration import Job, JobStatus
from palm.core.resource.result import ProviderResult
from palm.core.wait import (
    WAIT_KIND_JOB,
    WaitInterest,
    close_wait_interest,
    find_wait_interests,
    make_job_wait,
    open_wait_interest,
)
from palm.patterns.wizard.bindings.context.keys import WizardKeys


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
    """Build durable child-wait linkage from a palm provider payload."""
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


def get_child_wait(state: Any) -> dict[str, Any] | None:
    raw = _state_get(state, WizardKeys.WAITING_FOR_CHILD)
    return dict(raw) if isinstance(raw, dict) else None


def wait_interest_from_child_wait(waiting: dict[str, Any]) -> WaitInterest | None:
    """Build a job wait interest from legacy nested-wizard wait payload."""
    child_job_id = child_job_id_from_wait(waiting)
    if not child_job_id:
        return None
    meta: dict[str, Any] = {
        "source": "nested_wizard",
        "step_slug": waiting.get("step_slug"),
        "output_key": waiting.get("output_key"),
        "resource_ref": waiting.get("resource_ref"),
        "child_instance_id": waiting.get("child_instance_id"),
        "child_status": waiting.get("child_status"),
    }
    # Drop Nones so serialized interest stays compact.
    meta = {k: v for k, v in meta.items() if v is not None}
    return make_job_wait(child_job_id, meta=meta)


def open_wait_interest_for_child(state: Any, waiting: dict[str, Any]) -> WaitInterest | None:
    """Open (or refresh) reactive wait interest for a parked nested child."""
    interest = wait_interest_from_child_wait(waiting)
    if interest is None:
        return None
    return open_wait_interest(state, interest, replace_same_target=True)


def close_wait_interest_for_child(state: Any, *, child_job_id: str | None = None) -> None:
    """Close job wait interest for the nested child (idempotent)."""
    target = child_job_id
    if not target:
        waiting = get_child_wait(state)
        target = child_job_id_from_wait(waiting)
    if not target:
        # Fall back: close any nested_wizard job interests still open.
        for w in find_wait_interests(state, kind=WAIT_KIND_JOB):
            if (w.meta or {}).get("source") == "nested_wizard":
                close_wait_interest(state, kind=w.kind, target_id=w.target_id)
        return
    close_wait_interest(state, kind=WAIT_KIND_JOB, target_id=str(target))


def set_child_wait(state: Any, payload: dict[str, Any]) -> None:
    """Park nested-child linkage and open reactive wait interest (0.55.3)."""
    body = dict(payload)
    _state_set(state, WizardKeys.WAITING_FOR_CHILD, body)
    open_wait_interest_for_child(state, body)


def clear_child_wait(state: Any) -> None:
    """Clear nested-child linkage and close reactive wait interest."""
    waiting = get_child_wait(state)
    child_id = child_job_id_from_wait(waiting)
    close_wait_interest_for_child(state, child_job_id=child_id)
    deleter = getattr(state, "delete", None)
    if callable(deleter):
        deleter(WizardKeys.WAITING_FOR_CHILD)


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


def _state_get(state: Any, key: str) -> Any:
    getter = getattr(state, "get", None)
    return getter(key) if callable(getter) else None


def _state_set(state: Any, key: str, value: Any) -> None:
    setter = getattr(state, "set", None)
    if callable(setter):
        setter(key, value)
