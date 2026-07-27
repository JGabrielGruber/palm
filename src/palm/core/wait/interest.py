"""Pure wait interest — durable continue-interest vocabulary (no I/O).

0.55 Reactive Interests: owners park with an explicit interest; completers emit
self-events; Palm matches. See docs/VISION-0.55.md and ADR-025.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

# --- Locked contract keys (0.55.1) ---

WAIT_INTEREST_SCHEMA_VERSION = 1
"""Schema version embedded in serialized wait interests."""

STATE_KEY_WAIT_INTERESTS = "palm.wait.interests"
"""Job/instance state key: JSON-serializable list of wait interest dicts."""

WAIT_KIND_JOB = "job"
"""Target family: nested / peer job (child ``job_id``)."""

WAIT_KIND_WORKLOAD = "workload"
"""Target family: workload unit (stub in 0.55.7; full engine 0.56)."""

KNOWN_WAIT_KINDS: frozenset[str] = frozenset({WAIT_KIND_JOB, WAIT_KIND_WORKLOAD})
"""Kinds recognized in 0.55; unknown kinds still serialize for forward growth."""

ON_TARGET_FAILED_FAIL_OWNER = "fail_owner"
"""When the target fails, fail the owner job."""

ON_TARGET_FAILED_LEAVE = "leave"
"""When the target fails, leave the owner parked (no auto fail)."""

KNOWN_ON_TARGET_FAILED: frozenset[str] = frozenset(
    {ON_TARGET_FAILED_FAIL_OWNER, ON_TARGET_FAILED_LEAVE}
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True, slots=True)
class WaitPolicy:
    """Resume / fail policy when a matched target reaches a terminal state."""

    on_target_failed: str = ON_TARGET_FAILED_FAIL_OWNER

    def to_dict(self) -> dict[str, Any]:
        return {"on_target_failed": self.on_target_failed}

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> WaitPolicy:
        if not data:
            return cls()
        raw = data.get("on_target_failed") or ON_TARGET_FAILED_FAIL_OWNER
        return cls(on_target_failed=str(raw))


@dataclass(frozen=True, slots=True)
class WaitInterest:
    """Serializable continue-interest: owner waits for ``kind`` + ``target_id``."""

    kind: str
    target_id: str
    opened_at: str = field(default_factory=_utc_now_iso)
    policy: WaitPolicy = field(default_factory=WaitPolicy)
    meta: dict[str, Any] = field(default_factory=dict)
    v: int = WAIT_INTEREST_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.kind or not str(self.kind).strip():
            raise ValueError("WaitInterest.kind must be a non-empty string")
        if not self.target_id or not str(self.target_id).strip():
            raise ValueError("WaitInterest.target_id must be a non-empty string")

    def matches(self, *, kind: str, target_id: str) -> bool:
        return self.kind == kind and self.target_id == target_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "v": self.v,
            "kind": self.kind,
            "target_id": self.target_id,
            "opened_at": self.opened_at,
            "policy": self.policy.to_dict(),
            "meta": dict(self.meta),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WaitInterest:
        if not isinstance(data, dict):
            raise TypeError("WaitInterest.from_dict expects a dict")
        kind = str(data.get("kind") or "").strip()
        target_id = str(data.get("target_id") or "").strip()
        policy_raw = data.get("policy")
        policy = WaitPolicy.from_dict(
            policy_raw if isinstance(policy_raw, dict) else None
        )
        meta_raw = data.get("meta")
        meta = dict(meta_raw) if isinstance(meta_raw, dict) else {}
        opened = data.get("opened_at")
        v_raw = data.get("v", WAIT_INTEREST_SCHEMA_VERSION)
        try:
            v = int(v_raw)
        except (TypeError, ValueError):
            v = WAIT_INTEREST_SCHEMA_VERSION
        return cls(
            kind=kind,
            target_id=target_id,
            opened_at=str(opened) if opened else _utc_now_iso(),
            policy=policy,
            meta=meta,
            v=v,
        )


def make_job_wait(
    target_job_id: str,
    *,
    opened_at: str | None = None,
    policy: WaitPolicy | None = None,
    meta: dict[str, Any] | None = None,
) -> WaitInterest:
    """Convenience constructor for ``kind=job`` wait interest."""
    kwargs: dict[str, Any] = {
        "kind": WAIT_KIND_JOB,
        "target_id": str(target_job_id),
        "policy": policy or WaitPolicy(),
        "meta": dict(meta or {}),
    }
    if opened_at is not None:
        kwargs["opened_at"] = opened_at
    return WaitInterest(**kwargs)


def make_workload_wait(
    workload_id: str,
    *,
    opened_at: str | None = None,
    policy: WaitPolicy | None = None,
    meta: dict[str, Any] | None = None,
) -> WaitInterest:
    """Convenience constructor for ``kind=workload`` wait interest (0.55.7+)."""
    kwargs: dict[str, Any] = {
        "kind": WAIT_KIND_WORKLOAD,
        "target_id": str(workload_id),
        "policy": policy or WaitPolicy(),
        "meta": dict(meta or {}),
    }
    if opened_at is not None:
        kwargs["opened_at"] = opened_at
    return WaitInterest(**kwargs)


__all__ = [
    "KNOWN_ON_TARGET_FAILED",
    "KNOWN_WAIT_KINDS",
    "ON_TARGET_FAILED_FAIL_OWNER",
    "ON_TARGET_FAILED_LEAVE",
    "STATE_KEY_WAIT_INTERESTS",
    "WAIT_INTEREST_SCHEMA_VERSION",
    "WAIT_KIND_JOB",
    "WAIT_KIND_WORKLOAD",
    "WaitInterest",
    "WaitPolicy",
    "make_job_wait",
    "make_workload_wait",
]
