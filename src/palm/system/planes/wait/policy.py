"""Resolve wait interest + target signal → owner action (pure)."""

from __future__ import annotations

from palm.system.planes.wait.signals import (
    NEGATIVE_OUTCOMES,
    POSITIVE_OUTCOMES,
    TargetSignal,
)
from palm.core.wait import (
    ON_TARGET_FAILED_FAIL_OWNER,
    ON_TARGET_FAILED_LEAVE,
    WaitInterest,
)

ACTION_RESUME_OWNER = "resume_owner"
ACTION_FAIL_OWNER = "fail_owner"
ACTION_NOOP = "noop"


def resolve_wait_action(interest: WaitInterest, signal: TargetSignal) -> str:
    """Normative policy: positive → resume; negative → fail or leave per interest."""
    if signal.outcome in POSITIVE_OUTCOMES:
        return ACTION_RESUME_OWNER
    if signal.outcome in NEGATIVE_OUTCOMES:
        policy = interest.policy.on_target_failed
        if policy == ON_TARGET_FAILED_LEAVE:
            return ACTION_NOOP
        # Default and unknown fail policies: fail the owner.
        if policy in (ON_TARGET_FAILED_FAIL_OWNER, "", None):
            return ACTION_FAIL_OWNER
        return ACTION_FAIL_OWNER
    return ACTION_NOOP


__all__ = [
    "ACTION_FAIL_OWNER",
    "ACTION_NOOP",
    "ACTION_RESUME_OWNER",
    "resolve_wait_action",
]
