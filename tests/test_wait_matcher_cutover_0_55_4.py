"""0.55.4 — WaitMatcher normative unpark; ChildCompletionHook dual-path compat."""

from __future__ import annotations

import pytest

import palm.providers  # noqa: F401
from palm.core.orchestration import JobStatus
from palm.core.wait import has_open_waits, list_wait_interests
from palm.definitions import FlowDefinition, ResourceDefinition
from palm.patterns.wizard import WizardKeys
from palm.providers.palm.bindings.runtimes.wiring import clear_palm_runtime
from palm.runtimes.embedded import EmbeddedRuntime


def _child_wizard_flow() -> FlowDefinition:
    return FlowDefinition(
        id="flow-child-wizard-554",
        name="child-wizard-554",
        pattern="wizard",
        options={
            "steps": [
                {"slug": "question", "title": "Question", "prompt": "Child?"},
            ],
        },
    )


def _parent_wizard_flow() -> FlowDefinition:
    return FlowDefinition(
        id="flow-parent-wizard-554",
        name="parent-wizard-554",
        pattern="wizard",
        options={
            "steps": [
                {
                    "slug": "spawn_child",
                    "title": "Spawn",
                    "step_kind": "resource",
                    "resource_ref": "submit-child-554",
                    "output_key": "child_job",
                },
            ],
        },
    )


def _submit_child_resource() -> ResourceDefinition:
    return ResourceDefinition(
        id="resource-submit-child-554",
        name="submit-child-554",
        provider="palm",
        action="submit_flow",
        resource_id="flow:child-wizard-554",
        params={
            "wait": True,
            "wait_mode": "until_input",
            "timeout_seconds": 5,
        },
    )


def _seed(runtime: EmbeddedRuntime) -> None:
    runtime.repository.save_flow(_child_wizard_flow())
    runtime.repository.save_flow(_parent_wizard_flow())
    runtime.repository.save_resource(_submit_child_resource())


@pytest.fixture
def runtime_matcher_only() -> EmbeddedRuntime:
    """Matcher normative path — ChildCompletionHook disabled."""
    rt = EmbeddedRuntime()
    rt.start(child_completion_hook=False, enable_wait_matcher=True)
    _seed(rt)
    yield rt
    rt.stop()
    clear_palm_runtime()


@pytest.fixture
def runtime_dual() -> EmbeddedRuntime:
    rt = EmbeddedRuntime()
    rt.start()  # matcher + hook
    _seed(rt)
    yield rt
    rt.stop()
    clear_palm_runtime()


def test_runtime_wires_wait_matcher(runtime_dual: EmbeddedRuntime) -> None:
    assert runtime_dual.wait_matcher is not None


def test_nested_unpark_matcher_without_hook(
    runtime_matcher_only: EmbeddedRuntime,
) -> None:
    """Normative path: wait interest + matcher alone completes nested flow."""
    runtime = runtime_matcher_only
    parent_job = runtime.submit_flow("parent-wizard-554")
    runtime.wait_until_idle(timeout=5)

    assert parent_job.status == JobStatus.WAITING_FOR_INPUT
    waiting = parent_job.state.get(WizardKeys.WAITING_FOR_CHILD)
    assert isinstance(waiting, dict)
    child_job_id = waiting["child_job_id"]
    assert has_open_waits(parent_job.state)
    interests = list_wait_interests(parent_job.state)
    assert interests[0].target_id == str(child_job_id)

    runtime.provide_input(child_job_id, "answer")
    runtime.wait_until_idle(timeout=5)

    child_job = runtime.get_job(str(child_job_id))
    assert child_job.status == JobStatus.SUCCEEDED

    parent_job = runtime.get_job(parent_job.id)
    assert parent_job.status == JobStatus.SUCCEEDED
    answers = parent_job.state.get(WizardKeys.ANSWERS) or {}
    assert isinstance(answers.get("child_job"), dict)
    assert not has_open_waits(parent_job.state)
    assert parent_job.state.get(WizardKeys.WAITING_FOR_CHILD) is None


def test_nested_unpark_dual_path_still_green(runtime_dual: EmbeddedRuntime) -> None:
    """Matcher + compat hook both present — nested dogfood remains green."""
    runtime = runtime_dual
    parent_job = runtime.submit_flow("parent-wizard-554")
    runtime.wait_until_idle(timeout=5)
    waiting = parent_job.state.get(WizardKeys.WAITING_FOR_CHILD)
    assert isinstance(waiting, dict)
    child_job_id = waiting["child_job_id"]

    runtime.provide_input(child_job_id, "answer")
    runtime.wait_until_idle(timeout=5)

    parent_job = runtime.get_job(parent_job.id)
    assert parent_job.status == JobStatus.SUCCEEDED


def test_matcher_scan_discovers_owner_without_index() -> None:
    """list_jobs scan finds parents that only opened state interest (0.55.3)."""
    from palm.common.wait import WaitMatcher, WaitOwnerIndex
    from palm.core.orchestration import Job
    from palm.core.wait import make_job_wait, open_wait_on_job

    owner = Job(id="owner-scan", executable=None)
    owner.status = JobStatus.WAITING_FOR_INPUT
    open_wait_on_job(owner, make_job_wait("child-scan"))

    resumes: list[str] = []
    matcher = WaitMatcher(
        index=WaitOwnerIndex(),  # empty — force scan
        get_job={owner.id: owner}.get,
        list_jobs=lambda: [owner],
        resume_owner=lambda oid, _i, _s: resumes.append(oid),
    )
    disps = matcher.handle_payload(
        "job.completed",
        {"job_id": "child-scan", "status": "SUCCEEDED"},
    )
    assert len(disps) == 1
    assert resumes == ["owner-scan"]
    assert not has_open_waits(owner.state)
