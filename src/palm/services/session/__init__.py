"""Product session domain — surface door over the system session plane (0.58.12)."""

from palm.services.session.service import (
    ContinueTarget,
    SessionService,
    looks_like_system_session_id,
    new_session_id,
)

__all__ = [
    "ContinueTarget",
    "SessionService",
    "looks_like_system_session_id",
    "new_session_id",
]
