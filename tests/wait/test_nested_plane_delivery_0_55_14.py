"""0.55.14 — plane delivers nested completion; interest always closed on match."""

from __future__ import annotations

from palm.common.wait.deliver import deliver_nested_wizard_completion
from palm.common.wait.matcher import WaitMatcher
from palm.core.orchestration import Job, JobStatus
from palm.core.wait import has_open_waits, make_job_wait, open_wait_on_job


def test_deliver_writes_output_key() -> None:
    owner = Job(id="o", executable=None)
    child = Job(id="c", executable=None)
    child.status = JobStatus.SUCCEEDED
    child.result = {"answer": 1}
    child.metadata = {"instance_id": "i1"}
    interest = make_job_wait(
        "c",
        meta={
            "source": "nested_wizard",
            "output_key": "child_job",
            "step_slug": "spawn",
            "child_payload": {"job_id": "c"},
        },
    )
    assert deliver_nested_wizard_completion(owner, interest, {child.id: child}.get)
    out = owner.state.get("child_job")
    assert isinstance(out, dict)
    assert out["status"] == "SUCCEEDED"
    assert out["nested_park"] is False
    assert out["result"] == {"answer": 1}
    assert out["delivered_by"] == "wait_plane"


def test_matcher_closes_nested_interest_after_resume() -> None:
    owner = Job(id="owner-n", executable=None)
    owner.status = JobStatus.WAITING_FOR_INPUT
    child = Job(id="child-n", executable=None)
    child.status = JobStatus.SUCCEEDED
    child.result = "done"
    open_wait_on_job(
        owner,
        make_job_wait(
            "child-n",
            meta={
                "source": "nested_wizard",
                "output_key": "child_job",
                "step_slug": "spawn",
                "child_payload": {},
            },
        ),
    )
    resumes: list[str] = []
    jobs = {owner.id: owner, child.id: child}

    def resume(oid: str, interest: object, _s: object) -> None:
        resumes.append(oid)
        deliver_nested_wizard_completion(owner, interest, jobs.get)  # type: ignore[arg-type]
        owner.status = JobStatus.RUNNING

    matcher = WaitMatcher(
        get_job=jobs.get,
        list_jobs=lambda: [owner],
        resume_owner=resume,
    )
    matcher.handle_payload(
        "job.completed",
        {"job_id": "child-n", "status": "SUCCEEDED"},
        event_id="n1",
    )
    assert resumes == ["owner-n"]
    assert not has_open_waits(owner.state)
    assert owner.state.get("child_job")["status"] == "SUCCEEDED"
