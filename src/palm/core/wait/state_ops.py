"""Open / close / list wait interests on job or instance state (pure, no I/O).

Storage is a JSON-serializable list under
:data:`~palm.core.wait.interest.STATE_KEY_WAIT_INTERESTS`.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from palm.core.wait.interest import (
    STATE_KEY_WAIT_INTERESTS,
    WaitInterest,
)


@runtime_checkable
class _StateSurface(Protocol):
    def get(self, key: str, default: Any = None) -> Any: ...

    def set(self, key: str, value: Any) -> None: ...


def _require_state(state: Any) -> _StateSurface:
    if not isinstance(state, _StateSurface):
        getter = getattr(state, "get", None)
        setter = getattr(state, "set", None)
        if not (callable(getter) and callable(setter)):
            raise TypeError(
                "wait state helpers require an object with get(key)/set(key, value)"
            )
    return state  # type: ignore[return-value]


def list_wait_interests(state: Any) -> list[WaitInterest]:
    """Return all open wait interests on ``state`` (skips corrupt entries)."""
    surface = _require_state(state)
    raw = surface.get(STATE_KEY_WAIT_INTERESTS)
    if not isinstance(raw, list):
        return []
    out: list[WaitInterest] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        try:
            out.append(WaitInterest.from_dict(item))
        except (TypeError, ValueError):
            continue
    return out


def _write_interests(state: Any, interests: list[WaitInterest]) -> None:
    surface = _require_state(state)
    surface.set(STATE_KEY_WAIT_INTERESTS, [i.to_dict() for i in interests])


def open_wait_interest(
    state: Any,
    interest: WaitInterest,
    *,
    replace_same_target: bool = True,
) -> WaitInterest:
    """Record an open wait on ``state``.

    When ``replace_same_target`` is true (default), an existing interest with the
    same ``kind`` + ``target_id`` is replaced. Otherwise a duplicate is appended
    only if no match exists (still one open interest per target key).
    """
    if not isinstance(interest, WaitInterest):
        raise TypeError("interest must be a WaitInterest")
    current = list_wait_interests(state)
    match_idx = next(
        (
            i
            for i, w in enumerate(current)
            if w.matches(kind=interest.kind, target_id=interest.target_id)
        ),
        None,
    )
    if match_idx is not None:
        if replace_same_target:
            current[match_idx] = interest
        # else: leave existing open interest as-is
        _write_interests(state, current)
        return current[match_idx]
    current.append(interest)
    _write_interests(state, current)
    return interest


def close_wait_interest(
    state: Any,
    *,
    kind: str,
    target_id: str,
) -> WaitInterest | None:
    """Remove the open wait for ``kind`` + ``target_id``. Returns closed interest."""
    current = list_wait_interests(state)
    closed: WaitInterest | None = None
    remaining: list[WaitInterest] = []
    for w in current:
        if closed is None and w.matches(kind=kind, target_id=target_id):
            closed = w
            continue
        remaining.append(w)
    if closed is not None:
        _write_interests(state, remaining)
    return closed


def find_wait_interests(
    state: Any,
    *,
    kind: str | None = None,
    target_id: str | None = None,
) -> list[WaitInterest]:
    """Filter open waits by optional ``kind`` and/or ``target_id``."""
    out = list_wait_interests(state)
    if kind is not None:
        out = [w for w in out if w.kind == kind]
    if target_id is not None:
        out = [w for w in out if w.target_id == target_id]
    return out


def has_open_waits(state: Any) -> bool:
    return bool(list_wait_interests(state))


def clear_wait_interests(state: Any) -> int:
    """Remove all open waits. Returns how many were cleared."""
    current = list_wait_interests(state)
    if current:
        _write_interests(state, [])
    return len(current)


def open_wait_on_job(job: Any, interest: WaitInterest, **kwargs: Any) -> WaitInterest:
    """Open wait interest on ``job.state``."""
    state = getattr(job, "state", None)
    if state is None:
        raise TypeError("job must have a .state surface")
    return open_wait_interest(state, interest, **kwargs)


def close_wait_on_job(
    job: Any,
    *,
    kind: str,
    target_id: str,
) -> WaitInterest | None:
    """Close wait interest on ``job.state``."""
    state = getattr(job, "state", None)
    if state is None:
        raise TypeError("job must have a .state surface")
    return close_wait_interest(state, kind=kind, target_id=target_id)


def list_waits_on_job(job: Any) -> list[WaitInterest]:
    """List open wait interests on ``job.state``."""
    state = getattr(job, "state", None)
    if state is None:
        raise TypeError("job must have a .state surface")
    return list_wait_interests(state)


__all__ = [
    "clear_wait_interests",
    "close_wait_interest",
    "close_wait_on_job",
    "find_wait_interests",
    "has_open_waits",
    "list_wait_interests",
    "list_waits_on_job",
    "open_wait_interest",
    "open_wait_on_job",
]
