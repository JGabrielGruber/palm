"""0.55.3 — nested wizard open/close reactive wait interest (unit)."""

from __future__ import annotations

from palm.core.orchestration.job_state import JobState
from palm.core.wait import WAIT_KIND_JOB, has_open_waits, list_wait_interests
from palm.patterns.wizard.bindings.resource.child_wait import (
    clear_child_wait,
    get_child_wait,
    set_child_wait,
    wait_interest_from_child_wait,
)


def test_set_child_wait_opens_job_interest() -> None:
    from palm.patterns.wizard.bindings.context.keys import WizardKeys

    state = JobState()
    payload = {
        "step_slug": "spawn",
        "output_key": "child_out",
        "resource_ref": "submit-child",
        "child_job_id": "child-abc",
        "child_instance_id": "inst-1",
        "child_status": "WAITING_FOR_INPUT",
    }
    set_child_wait(state, payload)

    waiting = get_child_wait(state)
    assert waiting is not None
    assert waiting["child_job_id"] == "child-abc"
    # Dual key not written — interest is authority (0.55.12).
    assert state.get(WizardKeys.WAITING_FOR_CHILD) is None

    interests = list_wait_interests(state)
    assert len(interests) == 1
    assert interests[0].kind == WAIT_KIND_JOB
    assert interests[0].target_id == "child-abc"
    assert interests[0].meta["source"] == "nested_wizard"
    assert interests[0].meta["step_slug"] == "spawn"
    assert interests[0].meta["output_key"] == "child_out"


def test_clear_child_wait_closes_interest() -> None:
    state = JobState()
    set_child_wait(
        state,
        {
            "step_slug": "s",
            "output_key": "o",
            "child_job_id": "c-1",
        },
    )
    assert has_open_waits(state)
    clear_child_wait(state)
    assert get_child_wait(state) is None
    assert not has_open_waits(state)


def test_set_child_wait_refresh_replaces_same_target() -> None:
    state = JobState()
    set_child_wait(
        state,
        {"step_slug": "s", "output_key": "o", "child_job_id": "c-1", "child_status": "RUNNING"},
    )
    set_child_wait(
        state,
        {
            "step_slug": "s",
            "output_key": "o",
            "child_job_id": "c-1",
            "child_status": "WAITING_FOR_INPUT",
        },
    )
    interests = list_wait_interests(state)
    assert len(interests) == 1
    assert interests[0].meta.get("child_status") == "WAITING_FOR_INPUT"


def test_wait_interest_from_child_wait_requires_child_id() -> None:
    assert wait_interest_from_child_wait({"step_slug": "x"}) is None


def test_legacy_waiting_for_child_key_still_readable() -> None:
    """Pre-0.55.12 snapshots with dual key still project via get_child_wait."""
    from palm.patterns.wizard.bindings.context.keys import WizardKeys

    state = JobState()
    state.set(
        WizardKeys.WAITING_FOR_CHILD,
        {"child_job_id": "legacy-c", "step_slug": "old", "output_key": "o"},
    )
    waiting = get_child_wait(state)
    assert waiting is not None
    assert waiting["child_job_id"] == "legacy-c"
