"""
StepDefinition - the atomic unit of a wizard.

Steps are declarative. The WizardEngine interprets them at runtime.
"""

from __future__ import annotations

from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field

from palm.models.common import StepType, ValidationRule


class StepDefinition(BaseModel):
    """
    Declarative definition of a single step in a wizard.

    Hierarchical support is prepared via optional `children` (future Behavior Tree style).
    For v0.1 most wizards will use a flat list with explicit `next_step` or dynamic resolution.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        arbitrary_types_allowed=True,   # needed for Callable / ContextBuilder
    )

    # Identity & navigation
    slug: str = Field(min_length=1, max_length=64, description="Unique identifier within the wizard")
    type: StepType

    # Human presentation
    title: str = Field(min_length=1, max_length=120)
    prompt: str | None = Field(
        default=None,
        description="Primary question or instruction shown to the user",
    )
    guidelines: str | None = Field(
        default=None,
        description="Help text, constraints, or examples shown alongside the prompt",
    )
    description: str | None = Field(default=None, description="Longer explanation (admin/debug)")

    # Input / choice configuration
    choices: list[dict[str, Any]] | None = Field(
        default=None,
        description="For CHOICE steps: [{'value': 'yes', 'label': 'Yes, continue'}]",
    )
    input_schema: dict[str, Any] | None = Field(
        default=None,
        description="Optional JSON Schema or simple type hint for the expected input",
    )

    # Validation
    validation_rules: list[ValidationRule] = Field(default_factory=list)
    required: bool = Field(default=True)

    # Flow control
    next_step: str | None = Field(
        default=None,
        description="Static slug of the next step. If None, engine uses definition order or dynamic logic.",
    )
    is_backtrackable: bool = Field(
        default=True,
        description="Whether users may return to this step via the back command",
    )

    # Extensibility
    metadata: dict[str, Any] = Field(default_factory=dict)
    children: list[StepDefinition] | None = Field(
        default=None,
        description="Optional nested sub-steps (hierarchical / sub-wizard). When present, this step acts as a composite.",
    )

    # 0.2.0: Dynamic Context Builders (can override guidelines, choices, validation, help text, etc. at runtime)
    # Stored as Any to avoid Pydantic serialization issues with callables.
    # Expected signature: (collected_data: dict, step: StepDefinition) -> dict
    context_builder: Any = Field(
        default=None,
        description="Callable that receives collected_data + step and returns overrides for RichContext fields",
        exclude=True,
    )

    # 0.2.0: For CONDITION steps - a predicate that decides branching
    # Expected: (collected_data: dict) -> bool
    condition: Any = Field(
        default=None,
        description="For CONDITION steps: returns True/False to select branch (children[0]=true, children[1]=false)",
        exclude=True,
    )

    def is_terminal(self) -> bool:
        return self.type in (StepType.COMMIT,)

    def requires_user_input(self) -> bool:
        """Returns True if this step itself pauses for user input (leaves usually do)."""
        if self.children:
            # Composite steps generally don't ask for input themselves unless explicitly a user-facing type
            return self.type in (
                StepType.USER_INPUT,
                StepType.CHOICE,
                StepType.CONFIRM,
                StepType.INTRODUCTION,
                StepType.SUMMARY,
            )
        return self.type in (
            StepType.USER_INPUT,
            StepType.CHOICE,
            StepType.CONFIRM,
            StepType.INTRODUCTION,
            StepType.SUMMARY,
        )

    def is_composite(self) -> bool:
        """True if this step contains child steps (hierarchical container)."""
        return bool(self.children)

    def get_child_by_slug(self, slug: str) -> StepDefinition | None:
        if not self.children:
            return None
        for child in self.children:
            if child.slug == slug:
                return child
        return None
