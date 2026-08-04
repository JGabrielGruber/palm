"""Compat re-export — prefer :class:`palm.services.inspect.InspectService`."""

from palm.services.inspect.service import InspectService, InspectService as SystemService

__all__ = ["InspectService", "SystemService"]
