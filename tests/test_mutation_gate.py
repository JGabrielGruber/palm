"""Tests for mutation guard envelope — read vs drive signals."""

from __future__ import annotations

from palm.common.operator.mutation_gate import build_mutation_envelope


def test_waiting_choice_allows_mutations() -> None:
    inspect = {
        "status": "WAITING_FOR_INPUT",
        "step": "intent",
        "field_type": "choice",
        "choices": ["a", "b"],
    }
    env = build_mutation_envelope(inspect)
    assert env["mutations_allowed"] is True
    assert env["step_slug"] == "intent"
    assert env["requires_user_input"] is True


def test_terminal_complete_disallows_mutations() -> None:
    inspect = {"status": "SUCCEEDED", "step": "summary"}
    env = build_mutation_envelope(inspect)
    assert env["mutations_allowed"] is False
    assert env["requires_user_input"] is False


def test_summary_confirm_requires_explicit_user() -> None:
    inspect = {
        "status": "WAITING_FOR_INPUT",
        "step": "summary",
        "step_kind": "summary",
        "field_type": "confirm",
    }
    env = build_mutation_envelope(inspect)
    assert env["mutations_allowed"] is True
    assert env["confirm_step"] is True
    assert "do not send yes/no unless the user explicitly" in env.get("agent_hint", "").lower()


def test_resource_auto_step_does_not_require_free_text() -> None:
    """Portal was stuck typing into resource steps — auto-advance is resume, not value."""
    inspect = {
        "status": "WAITING_FOR_INPUT",
        "step": "run",
        "step_kind": "resource",
        "field_type": "resource",
        "auto_advance": True,
        "resource_ref": "hermetic-run-script",
    }
    env = build_mutation_envelope(inspect)
    assert env["mutations_allowed"] is True
    assert env["requires_user_input"] is False
    assert env.get("auto_advance") is True
    assert "session-resume" in env.get("agent_hint", "")