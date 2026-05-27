"""
Palm Wizard subsystem.

Wizards are stateful, interactive, backtrackable DAGs that pause for user input
and emit rich contextual information before every interaction point.
"""

from palm.core.wizard.context import RichContext
from palm.core.wizard.definition import WizardDefinition, StepDefinition
from palm.core.wizard.engine import WizardEngine
from palm.core.wizard.session import WizardSessionState

__all__ = [
    "RichContext",
    "WizardDefinition",
    "StepDefinition",
    "WizardEngine",
    "WizardSessionState",
]
