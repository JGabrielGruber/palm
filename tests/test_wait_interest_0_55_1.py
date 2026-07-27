"""0.55.1 — Wait interest contract + open/close helpers (pure, no I/O)."""

from __future__ import annotations

import pytest

from palm.core.orchestration import Job
from palm.core.orchestration.job_state import JobState
from palm.core.wait import (
    ON_TARGET_FAILED_FAIL_OWNER,
    ON_TARGET_FAILED_LEAVE,
    STATE_KEY_WAIT_INTERESTS,
    WAIT_INTEREST_SCHEMA_VERSION,
    WAIT_KIND_JOB,
    WAIT_KIND_WORKLOAD,
    WaitInterest,
    WaitPolicy,
    clear_wait_interests,
    close_wait_interest,
    close_wait_on_job,
    find_wait_interests,
    has_open_waits,
    list_wait_interests,
    list_waits_on_job,
    make_job_wait,
    make_workload_wait,
    open_wait_interest,
    open_wait_on_job,
)


def test_wait_interest_roundtrip() -> None:
    w = WaitInterest(
        kind=WAIT_KIND_JOB,
        target_id="child-1",
        policy=WaitPolicy(on_target_failed=ON_TARGET_FAILED_LEAVE),
        meta={"step_slug": "invoke_child", "output_key": "child_result"},
    )
    w2 = WaitInterest.from_dict(w.to_dict())
    assert w2.kind == WAIT_KIND_JOB
    assert w2.target_id == "child-1"
    assert w2.policy.on_target_failed == ON_TARGET_FAILED_LEAVE
    assert w2.meta["step_slug"] == "invoke_child"
    assert w2.v == WAIT_INTEREST_SCHEMA_VERSION
    assert w2.matches(kind=WAIT_KIND_JOB, target_id="child-1")
    assert not w2.matches(kind=WAIT_KIND_JOB, target_id="other")


def test_wait_interest_rejects_empty_fields() -> None:
    with pytest.raises(ValueError, match="kind"):
        WaitInterest(kind="", target_id="x")
    with pytest.raises(ValueError, match="target_id"):
        WaitInterest(kind="job", target_id="")
    with pytest.raises(ValueError, match="target_id"):
        WaitInterest.from_dict({"kind": "job", "target_id": "  "})


def test_make_job_and_workload_helpers() -> None:
    j = make_job_wait("j-9", meta={"output_key": "out"})
    assert j.kind == WAIT_KIND_JOB
    assert j.target_id == "j-9"
    assert j.policy.on_target_failed == ON_TARGET_FAILED_FAIL_OWNER

    w = make_workload_wait("wl-1")
    assert w.kind == WAIT_KIND_WORKLOAD
    assert w.target_id == "wl-1"


def test_open_close_list_on_state() -> None:
    state = JobState()
    assert not has_open_waits(state)

    first = make_job_wait("child-a", meta={"step_slug": "a"})
    open_wait_interest(state, first)
    assert has_open_waits(state)
    listed = list_wait_interests(state)
    assert len(listed) == 1
    assert listed[0].target_id == "child-a"

    raw = state.get(STATE_KEY_WAIT_INTERESTS)
    assert isinstance(raw, list)
    assert raw[0]["kind"] == WAIT_KIND_JOB
    assert raw[0]["v"] == WAIT_INTEREST_SCHEMA_VERSION

    second = make_workload_wait("wl-z")
    open_wait_interest(state, second)
    assert len(list_wait_interests(state)) == 2
    assert find_wait_interests(state, kind=WAIT_KIND_WORKLOAD)[0].target_id == "wl-z"

    closed = close_wait_interest(state, kind=WAIT_KIND_JOB, target_id="child-a")
    assert closed is not None
    assert closed.target_id == "child-a"
    assert len(list_wait_interests(state)) == 1
    assert close_wait_interest(state, kind=WAIT_KIND_JOB, target_id="child-a") is None

    n = clear_wait_interests(state)
    assert n == 1
    assert not has_open_waits(state)


def test_open_replaces_same_target() -> None:
    state = JobState()
    open_wait_interest(
        state,
        make_job_wait("same", meta={"output_key": "old"}),
    )
    open_wait_interest(
        state,
        make_job_wait("same", meta={"output_key": "new"}),
        replace_same_target=True,
    )
    listed = list_wait_interests(state)
    assert len(listed) == 1
    assert listed[0].meta["output_key"] == "new"


def test_open_without_replace_keeps_first() -> None:
    state = JobState()
    open_wait_interest(
        state,
        make_job_wait("same", meta={"output_key": "first"}),
    )
    open_wait_interest(
        state,
        make_job_wait("same", meta={"output_key": "second"}),
        replace_same_target=False,
    )
    listed = list_wait_interests(state)
    assert len(listed) == 1
    assert listed[0].meta["output_key"] == "first"


def test_skips_corrupt_entries() -> None:
    state = JobState()
    state.set(
        STATE_KEY_WAIT_INTERESTS,
        [
            "not-a-dict",
            {"kind": "", "target_id": "x"},
            {"kind": "job", "target_id": "ok"},
        ],
    )
    listed = list_wait_interests(state)
    assert len(listed) == 1
    assert listed[0].target_id == "ok"


def test_job_helpers() -> None:
    job = Job(id="owner-1", executable=None)
    open_wait_on_job(job, make_job_wait("child-2", meta={"step_slug": "nest"}))
    waits = list_waits_on_job(job)
    assert len(waits) == 1
    assert waits[0].target_id == "child-2"

    closed = close_wait_on_job(job, kind=WAIT_KIND_JOB, target_id="child-2")
    assert closed is not None
    assert list_waits_on_job(job) == []


def test_policy_default_roundtrip() -> None:
    w = WaitInterest.from_dict({"kind": "job", "target_id": "c1"})
    assert w.policy.on_target_failed == ON_TARGET_FAILED_FAIL_OWNER
    d = w.to_dict()
    assert d["policy"]["on_target_failed"] == ON_TARGET_FAILED_FAIL_OWNER
