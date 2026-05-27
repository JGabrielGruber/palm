"""
Palm exception hierarchy.

All engine errors inherit from PalmError to allow broad catching
while still permitting fine-grained handling.
"""

from __future__ import annotations


class PalmError(Exception):
    """Base exception for all Palm engine errors."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.__class__.__name__


class WizardNotFoundError(PalmError):
    """Requested wizard definition was not found in the registry."""


class SessionNotFoundError(PalmError):
    """Session ID does not exist or has been purged."""


class SessionExpiredError(PalmError):
    """Session TTL has elapsed and the session is no longer usable."""


class InvalidStepError(PalmError):
    """Step slug is invalid for the current wizard or state."""


class ValidationError(PalmError):
    """User input failed validation rules for the current step."""

    def __init__(
        self,
        message: str,
        *,
        field: str | None = None,
        errors: list[str] | None = None,
    ) -> None:
        super().__init__(message, code="VALIDATION_ERROR")
        self.field = field
        self.errors = errors or [message]


class BacktrackNotAllowedError(PalmError):
    """Attempted to backtrack to a step that is not permitted (e.g. introduction)."""


class CommitError(PalmError):
    """Transactional commit step failed."""


class ProcessManagerError(PalmError):
    """Error in the ProcessManager (spawning, communication, termination)."""
