"""Deliver wait-target completion into the owner job (continue plane).

**0.55.16** — pluggable deliverers (kind / source / predicate). Nested wizard
is the default registration; the plane calls :func:`deliver_wait_completion`
and never hardcodes a single product shape.

Nested parks store ``output_key`` + payload seed in interest meta. On positive
match the deliverer writes the final payload so the pattern advances without
re-polling after interest close.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any

from palm.core.wait import WAIT_KIND_JOB, WaitInterest

# Shared with wizard nested_park (string constant — no pattern import from common).
NESTED_WIZARD_SOURCE = "nested_wizard"

WaitDeliverFn = Callable[[Any, WaitInterest, Callable[[str], Any]], bool]
WaitDeliverMatchFn = Callable[[WaitInterest], bool]

_lock = threading.RLock()
# Ordered list: (name, matches, fn)
_entries: list[tuple[str, WaitDeliverMatchFn, WaitDeliverFn]] = []


def is_nested_wizard_interest(interest: WaitInterest) -> bool:
    meta = interest.meta or {}
    return interest.kind == WAIT_KIND_JOB and (
        meta.get("source") == NESTED_WIZARD_SOURCE or bool(meta.get("pattern_park"))
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


def _match_kind(kind: str) -> WaitDeliverMatchFn:
    def _matches(interest: WaitInterest) -> bool:
        return interest.kind == kind

    return _matches


def _match_source(source: str, *, kind: str | None = None) -> WaitDeliverMatchFn:
    def _matches(interest: WaitInterest) -> bool:
        if kind is not None and interest.kind != kind:
            return False
        return (interest.meta or {}).get("source") == source

    return _matches


def register_wait_deliverer(
    name: str,
    fn: WaitDeliverFn,
    *,
    matches: WaitDeliverMatchFn | None = None,
    kind: str | None = None,
    source: str | None = None,
) -> None:
    """Register a completion deliverer (replaces same ``name`` if present).

    Match with ``matches`` predicate, or ``kind`` / ``source`` shortcuts.
    At least one of ``matches``, ``kind``, ``source`` is required.
    """
    if matches is None:
        if source is not None:
            matches = _match_source(source, kind=kind)
        elif kind is not None:
            matches = _match_kind(kind)
        else:
            raise ValueError(
                "register_wait_deliverer requires matches=, kind=, and/or source="
            )
    key = str(name).strip()
    if not key:
        raise ValueError("deliverer name must be non-empty")
    with _lock:
        _entries[:] = [(n, m, f) for n, m, f in _entries if n != key]
        _entries.append((key, matches, fn))


def unregister_wait_deliverer(name: str) -> bool:
    """Remove a deliverer by name. Returns True if it was present."""
    key = str(name).strip()
    with _lock:
        before = len(_entries)
        _entries[:] = [(n, m, f) for n, m, f in _entries if n != key]
        return len(_entries) < before


def list_wait_deliverers() -> list[str]:
    """Registered deliverer names in try order."""
    with _lock:
        return [n for n, _, _ in _entries]


def clear_wait_deliverers(*, restore_defaults: bool = True) -> None:
    """Clear registry. Restores nested default unless ``restore_defaults=False``."""
    with _lock:
        _entries.clear()
    if restore_defaults:
        _register_defaults()


def deliver_wait_completion(
    owner_job: Any,
    interest: WaitInterest,
    get_job: Callable[[str], Any],
) -> bool:
    """Run the first matching deliverer that returns True. Plane entry point."""
    with _lock:
        snapshot = list(_entries)
    for _name, matches, fn in snapshot:
        try:
            if not matches(interest):
                continue
        except Exception:
            continue
        try:
            if fn(owner_job, interest, get_job):
                return True
        except Exception:
            continue
    return False


def _register_defaults() -> None:
    register_wait_deliverer(
        "nested_wizard",
        deliver_nested_wizard_completion,
        matches=is_nested_wizard_interest,
    )


_register_defaults()


__all__ = [
    "NESTED_WIZARD_SOURCE",
    "WaitDeliverFn",
    "WaitDeliverMatchFn",
    "clear_wait_deliverers",
    "deliver_nested_wizard_completion",
    "deliver_wait_completion",
    "is_nested_wizard_interest",
    "list_wait_deliverers",
    "register_wait_deliverer",
    "unregister_wait_deliverer",
]
