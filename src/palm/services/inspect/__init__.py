"""Product inspect door — present operator views over system facts.

Home for :class:`InspectService` (0.61.4 / SD-007). Formerly
``palm.services.system`` / ``SystemService`` — that package remains a thin
import shim.
"""

from palm.services.inspect.service import InspectService

__all__ = ["InspectService"]
