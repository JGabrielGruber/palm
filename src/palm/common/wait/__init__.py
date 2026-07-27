"""Wait coordination — index, matcher, policy (0.55 Reactive Interests).

Pure interest types live in :mod:`palm.core.wait`. This package owns match /
resume policy and bus-facing helpers (no pattern-specific logic).
"""

from palm.common.wait.index import WaitOwnerIndex
from palm.common.wait.matcher import MatchDisposition, WaitMatcher
from palm.common.wait.policy import (
    ACTION_FAIL_OWNER,
    ACTION_NOOP,
    ACTION_RESUME_OWNER,
    resolve_wait_action,
)
from palm.common.wait.signals import (
    MATCHER_EVENT_TYPES,
    OUTCOME_CANCELLED,
    OUTCOME_FAILED,
    OUTCOME_READY,
    OUTCOME_SUCCEEDED,
    TargetSignal,
    extract_signal_from_event,
    extract_target_signal,
)
from palm.common.wait.tracked import close_tracked_wait, open_tracked_wait

__all__ = [
    "ACTION_FAIL_OWNER",
    "ACTION_NOOP",
    "ACTION_RESUME_OWNER",
    "MATCHER_EVENT_TYPES",
    "OUTCOME_CANCELLED",
    "OUTCOME_FAILED",
    "OUTCOME_READY",
    "OUTCOME_SUCCEEDED",
    "MatchDisposition",
    "TargetSignal",
    "WaitMatcher",
    "WaitOwnerIndex",
    "close_tracked_wait",
    "extract_signal_from_event",
    "extract_target_signal",
    "open_tracked_wait",
    "resolve_wait_action",
]
