"""Product session domain — surface door over the system session plane (0.58.12+)."""

from palm.services.session.service import (
    HOST_SESSION_ID,
    HOST_SESSION_ORIGIN,
    WORK_DRAIN_ORIGIN,
    ContinueTarget,
    SessionService,
    looks_like_system_session_id,
    new_session_id,
    service_session_id,
)

__all__ = [
    "ContinueTarget",
    "HOST_SESSION_ID",
    "HOST_SESSION_ORIGIN",
    "SessionService",
    "WORK_DRAIN_ORIGIN",
    "looks_like_system_session_id",
    "new_session_id",
    "service_session_id",
]
