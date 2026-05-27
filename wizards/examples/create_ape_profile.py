"""
Palm Example Wizard: Create APE Profile (Basic / Reliable)

This is the recommended "getting started" example. It is intentionally
mostly flat for maximum simplicity and reliability.

It demonstrates:
- Standard Introduction → input steps → summary → commit flow
- Validation rules
- A simple commit handler
- Backtracking by slug

For a full demonstration of 0.2.1 hierarchical features (SEQUENCE composites,
dynamic ContextBuilder, and CONDITION branching), see:
    wizards/examples/onboard_new_ape.py
"""

from __future__ import annotations

from typing import Any

from palm.core.wizard.definition import WizardDefinition
from palm.models.common import StepType
from palm.models.step import StepDefinition


def create_ape_profile_wizard() -> WizardDefinition:
    """Returns a clean, flat, production-style wizard definition."""

    steps = [
        StepDefinition(
            slug="introduction",
            type=StepType.INTRODUCTION,
            title="Welcome to APE Profile Creator",
            prompt="This wizard will help you create a new APE (Ape Profile Entity) profile.",
            guidelines="Type 'confirm', 'yes', or 'y' to begin.",
            is_backtrackable=False,
        ),
        StepDefinition(
            slug="ask_name",
            type=StepType.USER_INPUT,
            title="Full Name",
            prompt="What is your full name?",
            guidelines="Use the name you want associated with this profile.",
            validation_rules=[
                {"type": "required"},
                {"type": "min_length", "params": {"value": 2}},
                {"type": "max_length", "params": {"value": 80}},
            ],
        ),
        StepDefinition(
            slug="ask_age",
            type=StepType.USER_INPUT,
            title="Age",
            prompt="How old are you?",
            guidelines="You must be at least 13 years old.",
            validation_rules=[
                {"type": "required"},
                {"type": "min_value", "params": {"value": 13}},
                {"type": "max_value", "params": {"value": 120}},
            ],
            input_schema={"type": "integer"},
        ),
        StepDefinition(
            slug="summary",
            type=StepType.SUMMARY,
            title="Review Your Profile",
            prompt="Please review the information below.",
            guidelines="Use the 'back' command if you need to change anything.",
        ),
        StepDefinition(
            slug="commit",
            type=StepType.COMMIT,
            title="Create Profile",
            prompt="Ready to create your APE profile?",
            guidelines="This is the final step. The profile will be recorded.",
            is_backtrackable=False,
        ),
    ]

    return WizardDefinition(
        id="create_ape_profile",
        name="Create APE Profile",
        description="Simple flat wizard for creating an APE profile (recommended starting example).",
        version="1.2.0",
        steps=steps,
        on_commit_hook="create_ape_profile_commit",
        metadata={"category": "examples", "tags": ["basic", "flat", "recommended"]},
    )


def ape_profile_commit_handler(session: Any) -> dict[str, Any]:
    """Example transactional commit handler."""
    data = session.collected_data
    name = data.get("ask_name", "Unknown")
    age = data.get("ask_age", 0)

    profile_id = f"ape_{name.lower().replace(' ', '_')[:20]}_{age}"

    return {
        "profile_id": profile_id,
        "name": name,
        "age": age,
        "status": "created",
        "message": f"APE Profile '{profile_id}' created successfully. Welcome, {name}!",
    }


COMMIT_HANDLERS = {
    "create_ape_profile_commit": ape_profile_commit_handler,
}
