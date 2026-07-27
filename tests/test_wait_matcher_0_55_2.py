"""0.55.2 — Wait matcher on runtime.event + resume/fail policy (fake events)."""

from __future__ import annotations

from palm.common.wait import (
    ACTION_FAIL_OWNER,
    ACTION_NOOP,
    ACTION_RESUME_OWNER,
    WaitMatcher,
    WaitOwnerIndex,
    extract_target_signal,
    open_tracked_wait,
    resolve_wait_action,
)
from palm.core.event import EventEngine
from palm.core.orchestration import Job, JobStatus
from palm.core.wait import (
    ON_TARGET_FAILED_LEAVE,
    WAIT_KIND_JOB,
    WaitInterest,
    WaitPolicy,
    has_open_waits,
    list_waits_on_job,
    make_job_wait,
    make_workload_wait,
)


def test_extract_job_completed_succeeded() -> None:
    sig = extract_target_signal(
        "job.completed",
        {"job_id": "child-1", "status": "SUCCEEDED"},
    )
    assert sig is not None
    assert sig.kind == WAIT_KIND_JOB
    assert sig.target_id == "child-1"
    assert sig.outcome == "succeeded"


def test_extract_job_status_changed_ignores_running() -> None:
    assert (
        extract_target_signal(
            "job.status_changed",
            {"job_id": "c", "status": "RUNNING"},
        )
        is None
    )


def test_extract_flow_session_and_workload() -> None:
    ok = extract_target_signal("flow.session.succeeded", {"job_id": "j1"})
    assert ok is not None and ok.outcome == "succeeded"
    fail = extract_target_signal("flow.session.failed", {"job_id": "j1"})
    assert fail is not None and fail.outcome == "failed"
    ready = extract_target_signal("workload.ready", {"workload_id": "w1"})
    assert ready is not None and ready.kind == "workload" and ready.outcome == "ready"


def test_policy_resume_and_fail_leave() -> None:
    interest = make_job_wait("c1")
    from palm.common.wait.signals import TargetSignal

    assert (
        resolve_wait_action(
            interest,
            TargetSignal(
                kind="job",
                target_id="c1",
                outcome="succeeded",
                event_type="job.completed",
            ),
        )
        == ACTION_RESUME_OWNER
    )
    assert (
        resolve_wait_action(
            interest,
            TargetSignal(
                kind="job",
                target_id="c1",
                outcome="failed",
                event_type="job.completed",
            ),
        )
        == ACTION_FAIL_OWNER
    )
    leave = WaitInterest(
        kind="job",
        target_id="c1",
        policy=WaitPolicy(on_target_failed=ON_TARGET_FAILED_LEAVE),
    )
    assert (
        resolve_wait_action(
            leave,
            TargetSignal(
                kind="job",
                target_id="c1",
                outcome="failed",
                event_type="job.completed",
            ),
        )
        == ACTION_NOOP
    )


def test_matcher_resumes_owner_on_child_success() -> None:
    index = WaitOwnerIndex()
    owner = Job(id="owner-1", executable=None)
    owner.status = JobStatus.WAITING_FOR_INPUT
    child_id = "child-9"
    open_tracked_wait(index, owner, make_job_wait(child_id, meta={"step_slug": "nest"}))

    resumes: list[str] = []
    fails: list[str] = []
    jobs = {owner.id: owner}

    matcher = WaitMatcher(
        index=index,
        get_job=jobs.get,
        resume_owner=lambda oid, _i, _s: resumes.append(oid),
        fail_owner=lambda oid, _i, _s: fails.append(oid),
    )

    disps = matcher.handle_payload(
        "job.completed",
        {"job_id": child_id, "status": "SUCCEEDED"},
    )
    assert len(disps) == 1
    assert disps[0].action == ACTION_RESUME_OWNER
    assert disps[0].owner_job_id == "owner-1"
    assert resumes == ["owner-1"]
    assert fails == []
    assert not has_open_waits(owner.state)
    assert len(index) == 0

    # Double event: idempotent (no second resume).
    disps2 = matcher.handle_payload(
        "job.completed",
        {"job_id": child_id, "status": "SUCCEEDED"},
    )
    assert disps2 == []
    assert resumes == ["owner-1"]


def test_matcher_fails_owner_on_child_failed() -> None:
    index = WaitOwnerIndex()
    owner = Job(id="owner-2", executable=None)
    open_tracked_wait(index, owner, make_job_wait("bad-child"))
    fails: list[str] = []
    jobs = {owner.id: owner}
    matcher = WaitMatcher(
        index=index,
        get_job=jobs.get,
        fail_owner=lambda oid, _i, _s: fails.append(oid),
    )
    disps = matcher.handle_payload(
        "flow.session.failed",
        {"job_id": "bad-child", "status": "FAILED"},
    )
    assert disps[0].action == ACTION_FAIL_OWNER
    assert fails == ["owner-2"]
    assert list_waits_on_job(owner) == []


def test_matcher_leave_policy_keeps_interest() -> None:
    index = WaitOwnerIndex()
    owner = Job(id="owner-3", executable=None)
    interest = WaitInterest(
        kind="job",
        target_id="fragile",
        policy=WaitPolicy(on_target_failed=ON_TARGET_FAILED_LEAVE),
    )
    open_tracked_wait(index, owner, interest)
    fails: list[str] = []
    matcher = WaitMatcher(
        index=index,
        get_job={owner.id: owner}.get,
        fail_owner=lambda oid, _i, _s: fails.append(oid),
    )
    disps = matcher.handle_payload(
        "job.completed",
        {"job_id": "fragile", "status": "FAILED"},
    )
    assert disps[0].action == ACTION_NOOP
    assert fails == []
    assert has_open_waits(owner.state)
    assert len(index.owners_for(kind="job", target_id="fragile")) == 1


def test_matcher_subscribes_to_event_engine() -> None:
    engine = EventEngine()
    engine.initialize()
    index = WaitOwnerIndex()
    owner = Job(id="owner-bus", executable=None)
    open_tracked_wait(index, owner, make_job_wait("via-bus"))
    resumes: list[str] = []
    matcher = WaitMatcher(
        index=index,
        get_job={owner.id: owner}.get,
        resume_owner=lambda oid, _i, _s: resumes.append(oid),
    )
    matcher.attach_events(engine)
    engine.emit("job.completed", job_id="via-bus", status="SUCCEEDED")
    assert resumes == ["owner-bus"]
    assert not has_open_waits(owner.state)
    matcher.detach_events()


def test_workload_ready_signal_resumes() -> None:
    index = WaitOwnerIndex()
    owner = Job(id="owner-wl", executable=None)
    open_tracked_wait(index, owner, make_workload_wait("wl-42"))
    resumes: list[str] = []
    matcher = WaitMatcher(
        index=index,
        get_job={owner.id: owner}.get,
        resume_owner=lambda oid, _i, _s: resumes.append(oid),
    )
    disps = matcher.handle_payload("workload.ready", {"workload_id": "wl-42"})
    assert disps[0].action == ACTION_RESUME_OWNER
    assert resumes == ["owner-wl"]
