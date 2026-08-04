"""Compat shim — product inspect lived here as ``SystemService`` (SD-007).

Prefer :mod:`palm.services.inspect` / :class:`~palm.services.inspect.InspectService`.
"""

from palm.services.inspect import InspectService
from palm.services.inspect.service import InspectService as SystemService

__all__ = ["InspectService", "SystemService"]
