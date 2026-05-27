"""
RichContext - the complete snapshot returned to clients before every user interaction.

This is the primary contract between the engine and any UI layer (CLI, TUI, WebSocket).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from palm.models.common import SessionStatus, StepType


class RichContext(BaseModel):
    """
    Complete situational awareness for the current pause point in a wizard.

    Every time the engine needs the user to provide input (or confirm),
    it emits one of these. The client renders the prompt + guidelines,
    collects input according to the rules, and calls back with the value.
    """

    model_config = ConfigDict(extra="forbid")

    # Session & Wizard identity
    session_id: str
    wizard_id: str
    wizard_name: str

    # Current location
    current_step_slug: str
    current_step_type: StepType
    step_title: str

    # What to show the user
    prompt: str
    guidelines: str | None = None
    description: str | None = None

    # Input expectations
    input_type: str = Field(
        default="text",
        description="text | choice | confirm | summary | none",
    )
    choices: list[dict[str, Any]] | None = None
    validation_rules: list[dict[str, Any]] = Field(default_factory=list)
    required: bool = True

    # Navigation
    allowed_back_steps: list[str] = Field(
        default_factory=list,
        description="Slugs the user is currently allowed to backtrack to",
    )
    can_backtrack: bool = False

    # Execution path & data
    path: list[str] = Field(default_factory=list, description="Full step history so far")
    collected_data: dict[str, Any] = Field(default_factory=dict)

    # Session state
    status: SessionStatus
    is_first_step: bool = False

    # Hints for rich clients
    metadata: dict[str, Any] = Field(default_factory=dict)
    estimated_remaining_steps: int | None = None

    # Optional: pre-rendered nice display (CLI can use this)
    formatted_summary: str | None = None

    def to_display_dict(self) -> dict[str, Any]:
        """Compact representation suitable for CLI rendering."""
        return {
            "session": self.session_id[:8],
            "wizard": self.wizard_name,
            "step": f"{self.current_step_slug} ({self.current_step_type})",
            "prompt": self.prompt,
            "guidelines": self.guidelines,
            "choices": self.choices,
            "back": self.allowed_back_steps,
            "data_keys": list(self.collected_data.keys()),
        }
