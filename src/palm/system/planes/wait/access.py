"""Register-downward open/close when code has job/state but not a plane ref.

Prefer :meth:`~palm.system.planes.wait.plane.WaitPlaneService.open_on_job` when the
caller already holds the continue plane. These helpers resolve
``runtime.wait_plane`` from the bound runtime and fall back to pure
:mod:`palm.core.wait` open/close when unbound (tests / engines).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from palm.common.providers._registry import get_bound_runtime
from palm.core.wait import (
    WaitInterest,
    close_wait_interest,
    close_wait_on_job,
    open_wait_interest,
    open_wait_on_job,
)

if TYPE_CHECKING:
    from palm.system.planes.wait.plane import WaitPlaneService


def get_wait_plane() -> WaitPlaneService | None:
    """Return the bound runtime's :class:`WaitPlaneService`, if any."""
    runtime = get_bound_runtime()
    if runtime is None:
        return None
    plane = getattr(runtime, "wait_plane", None)
    if plane is None:
        return None
    return plane  # type: ignore[return-value]


def find_job_for_state(state: Any) -> Any | None:
    """Locate a live job whose ``.state`` is ``state`` (identity)."""
    runtime = get_bound_runtime()
    if runtime is None:
        return None
    orch = getattr(runtime, "orchestration", None)
    if orch is None:
        return None
    for job in list(orch.jobs.values()):
        if getattr(job, "state", None) is state:
            return job
    return None


def open_interest_on_job(job: Any, interest: WaitInterest, **kwargs: Any) -> WaitInterest:
    """Open via continue plane when available; else pure state open."""
    plane = get_wait_plane()
    if plane is not None:
        return plane.open_on_job(job, interest, **kwargs)
    return open_wait_on_job(job, interest, **kwargs)


def close_interest_on_job(
    job: Any,
    *,
    kind: str,
    target_id: str,
) -> WaitInterest | None:
    """Close via continue plane when available; else pure state close."""
    plane = get_wait_plane()
    if plane is not None:
        return plane.close_on_job(job, kind=kind, target_id=target_id)
    return close_wait_on_job(job, kind=kind, target_id=target_id)


def open_interest_for_state(
    state: Any,
    interest: WaitInterest,
    **kwargs: Any,
) -> WaitInterest:
    """Open interest preferring plane+job when the owner job is live."""
    job = find_job_for_state(state)
    if job is not None:
        return open_interest_on_job(job, interest, **kwargs)
    return open_wait_interest(state, interest, **kwargs)


def close_interest_for_state(
    state: Any,
    *,
    kind: str,
    target_id: str,
) -> WaitInterest | None:
    """Close interest preferring plane+job when the owner job is live."""
    job = find_job_for_state(state)
    if job is not None:
        return close_interest_on_job(job, kind=kind, target_id=target_id)
    return close_wait_interest(state, kind=kind, target_id=target_id)


__all__ = [
    "close_interest_for_state",
    "close_interest_on_job",
    "find_job_for_state",
    "get_wait_plane",
    "open_interest_for_state",
    "open_interest_on_job",
]
