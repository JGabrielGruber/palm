"""
Enhanced Example Wizard for Palm 0.2.0

Demonstrates:
- Hierarchical / nested steps (personal_info as a container with children)
- Dynamic ContextBuilder (changes guidelines + suggested actions based on data)
- Basic CONDITION step (over_18 branch)
- Proper use of SEQUENCE (implicit) and backtracking across levels

All previous flat behavior is preserved for backward compatibility.
"""

from __future__ import annotations

from typing import Any

from palm.core.wizard.definition import WizardDefinition
from palm.models.common import StepType
from palm.models.step import StepDefinition


def create_ape_profile_wizard() -> WizardDefinition:
    """Factory returning a 0.2.0 hierarchical wizard."""

    # ------------------------------------------------------------------
    # Child steps inside "personal_info" composite
    # ------------------------------------------------------------------
    personal_children = [
        StepDefinition(
            slug="ask_name",
            type=StepType.USER_INPUT,
            title="Full Name",
            prompt="What is your full name?",
            guidelines="Use your legal name or the name you want on your APE profile.",
            validation_rules=[
                {"type": "required"},
                {"type": "min_length", "params": {"value": 2}},
            ],
        ),
        StepDefinition(
            slug="ask_age",
            type=StepType.USER_INPUT,
            title="Age",
            prompt="How old are you?",
            guidelines="Must be at least 13 years old.",
            validation_rules=[
                {"type": "required"},
                {"type": "min_value", "params": {"value": 0}},
                {"type": "max_value", "params": {"value": 150}},
            ],
            input_schema={"type": "integer"},
        ),
    ]

    # Dynamic builder example: changes message depending on age
    def age_based_guidelines(data: dict[str, Any], step: StepDefinition) -> dict[str, Any]:
        age = data.get("ask_age")
        if isinstance(age, int) and age >= 65:
            return {
                "guidelines": "Thank you for your wisdom! We have special senior APE benefits.",
                "suggested_input": "confirm",
                "available_actions": ["Type 'confirm' to continue with senior benefits"],
            }
        if isinstance(age, int) and age < 18:
            return {
                "guidelines": "Note: Some features require parental consent.",
                "suggested_input": "ok",
            }
        return {"guidelines": "Standard adult profile flow."}

    ask_age_step = personal_children[1]
    ask_age_step.context_builder = age_based_guidelines

    # ------------------------------------------------------------------
    # Conditional branch example (over_18)
    # ------------------------------------------------------------------
    over_18_true = StepDefinition(
        slug="ask_id_number",
        type=StepType.USER_INPUT,
        title="Government ID",
        prompt="Please enter your ID number:",
        guidelines="Required for adults.",
        validation_rules=[{"type": "required"}, {"type": "min_length", "params": {"value": 5}}],
    )

    over_18_false = StepDefinition(
        slug="ask_guardian",
        type=StepType.USER_INPUT,
        title="Guardian Name",
        prompt="Please provide a parent's or guardian's name:",
        guidelines="Required for profiles under 18.",
        validation_rules=[{"type": "required"}],
    )

    over_18_condition = StepDefinition(
        slug="over_18_check",
        type=StepType.CONDITION,
        title="Age Verification",
        prompt="Checking age...",
        condition=lambda data: (data.get("ask_age") or 0) >= 18,
        children=[over_18_true, over_18_false],
    )

    # ------------------------------------------------------------------
    # Main top-level steps
    # ------------------------------------------------------------------
    steps = [
        # Introduction (unchanged behavior)
        StepDefinition(
            slug="introduction",
            type=StepType.INTRODUCTION,
            title="Welcome to APE Profile Creator",
            prompt="This wizard will help you create a new APE profile.",
            guidelines="You will provide personal details. Type 'confirm' to begin.",
            is_backtrackable=False,
        ),
        # Hierarchical container (0.2.0 feature)
        StepDefinition(
            slug="personal_info",
            type=StepType.SEQUENCE,
            title="Personal Information",
            prompt="Let's collect your basic details.",
            guidelines="This section contains nested steps.",
            children=personal_children,
        ),
        # The conditional branch (auto-evaluated)
        over_18_condition,
        # Summary + Commit (classic)
        StepDefinition(
            slug="summary",
            type=StepType.SUMMARY,
            title="Review Your Profile",
            prompt="Please review everything before we create your APE profile.",
            guidelines="Use 'back personal_info.ask_name' or 'back ask_age' to edit previous answers.",
        ),
        StepDefinition(
            slug="commit",
            type=StepType.COMMIT,
            title="Create Profile",
            prompt="Ready to create your APE profile?",
            guidelines="This is the final transactional step.",
            is_backtrackable=False,
        ),
    ]

    return WizardDefinition(
        id="create_ape_profile",
        name="Create APE Profile",
        description="0.2.0 Hierarchical wizard with dynamic builders and conditional branching.",
        version="2.0.0",
        steps=steps,
        on_commit_hook="create_ape_profile_commit",
        metadata={"category": "examples", "tags": ["hierarchical", "dynamic", "0.2.0"]},
    )


# ----------------------------------------------------------------------
# Commit handler (unchanged)
# ----------------------------------------------------------------------

def ape_profile_commit_handler(session: Any) -> dict[str, Any]:
    data = session.collected_data
    name = data.get("ask_name", "Unknown")
    age = data.get("ask_age", "?")
    id_or_guardian = data.get("ask_id_number") or data.get("ask_guardian", "N/A")

    profile_id = f"ape_{name.lower().replace(' ', '_')[:20]}_{age}"

    return {
        "profile_id": profile_id,
        "name": name,
        "age": age,
        "id_or_guardian": id_or_guardian,
        "status": "created",
        "message": f"Welcome to the APE family, {name}!",
    }


COMMIT_HANDLERS = {
    "create_ape_profile_commit": ape_profile_commit_handler,
}
