"""0.55.16 — pluggable wait completion deliverers."""

from __future__ import annotations

from palm.common.wait.deliver import (
    clear_wait_deliverers,
    deliver_nested_wizard_completion,
    deliver_wait_completion,
    list_wait_deliverers,
    register_wait_deliverer,
    unregister_wait_deliverer,
)
from palm.common.wait.plane import WaitPlaneService
from palm.core.orchestration import Job, JobStatus
from palm.core.wait import make_job_wait, make_workload_wait, open_wait_on_job


def test_default_nested_deliverer_registered() -> None:
    assert "nested_wizard" in list_wait_deliverers()


def test_deliver_wait_completion_nested() -> None:
    owner = Job(id="o", executable=None)
    child = Job(id="c", executable=None)
    child.status = JobStatus.SUCCEEDED
    child.result = {"answer": 2}
    interest = make_job_wait(
        "c",
        meta={
            "source": "nested_wizard",
            "output_key": "child_job",
            "child_payload": {},
        },
    )
    assert deliver_wait_completion(owner, interest, {child.id: child}.get)
    assert owner.state.get("child_job")["result"] == {"answer": 2}
    assert owner.state.get("child_job")["delivered_by"] == "wait_plane"


def test_custom_deliverer_for_workload_kind() -> None:
    delivered: list[str] = []

    def _workload_deliver(owner: object, interest: object, _get: object) -> bool:
        delivered.append(getattr(interest, "target_id", ""))
        state = getattr(owner, "state", None)
        if state is not None and hasattr(state, "set"):
            state.set("workload_done", True)
        return True

    register_wait_deliverer("test_workload", _workload_deliver, kind="workload")
    try:
        assert "test_workload" in list_wait_deliverers()
        owner = Job(id="ow", executable=None)
        interest = make_workload_wait("wl-9", meta={"source": "test"})
        assert deliver_wait_completion(owner, interest, lambda _i: None)
        assert delivered == ["wl-9"]
        assert owner.state.get("workload_done") is True
    finally:
        unregister_wait_deliverer("test_workload")


def test_unregister_and_clear_restore_defaults() -> None:
    register_wait_deliverer(
        "ephemeral",
        lambda *_a: False,
        kind="job",
        source="ephemeral",
    )
    assert "ephemeral" in list_wait_deliverers()
    assert unregister_wait_deliverer("ephemeral")
    assert "ephemeral" not in list_wait_deliverers()

    clear_wait_deliverers(restore_defaults=False)
    assert list_wait_deliverers() == []
    clear_wait_deliverers(restore_defaults=True)
    assert "nested_wizard" in list_wait_deliverers()


def test_plane_resume_uses_registry_not_nested_only() -> None:
    """Plane delivery path runs registry (custom deliverer for non-nested)."""
    hits: list[str] = []

    def _mark(owner: object, interest: object, _get: object) -> bool:
        hits.append(str(getattr(interest, "target_id", "")))
        state = getattr(owner, "state", None)
        if state is not None:
            state.set("via_registry", True)
        return True

    register_wait_deliverer("plane_probe", _mark, source="plane_probe", kind="job")
    try:
        rt_jobs: dict[str, Job] = {}
        owner = Job(id="owner-p", executable=None)
        owner.status = JobStatus.WAITING_FOR_INPUT
        child = Job(id="child-p", executable=None)
        child.status = JobStatus.SUCCEEDED
        rt_jobs[owner.id] = owner
        rt_jobs[child.id] = child
        open_wait_on_job(
            owner,
            make_job_wait("child-p", meta={"source": "plane_probe"}),
        )

        class _Orch:
            jobs = rt_jobs

            def get_job(self, job_id: str) -> Job | None:
                return rt_jobs.get(job_id)

            def resume_job(self, job_id: str) -> None:
                j = rt_jobs[job_id]
                j.status = JobStatus.RUNNING

            def apply_result(self, *_a: object, **_k: object) -> None:
                return None

        class _Runtime:
            orchestration = _Orch()
            event = None

        plane = WaitPlaneService()
        plane.attach(_Runtime())
        plane.handle_payload(
            "job.completed",
            {"job_id": "child-p", "status": "SUCCEEDED"},
        )
        assert hits == ["child-p"]
        assert owner.state.get("via_registry") is True
        plane.detach()
    finally:
        unregister_wait_deliverer("plane_probe")


def test_nested_direct_helper_still_works() -> None:
    """Compat: explicit nested helper remains for unit tests."""
    owner = Job(id="o2", executable=None)
    child = Job(id="c2", executable=None)
    child.status = JobStatus.SUCCEEDED
    interest = make_job_wait(
        "c2",
        meta={"source": "nested_wizard", "output_key": "out", "child_payload": {}},
    )
    assert deliver_nested_wizard_completion(owner, interest, {child.id: child}.get)
    assert owner.state.get("out")["status"] == "SUCCEEDED"
