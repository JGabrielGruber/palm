"""Product inspect door — present operator views over system facts.

Home for :class:`InspectService` (0.61.4 / SD-007). Formerly
``palm.services.system`` / ``SystemService`` — that package remains a thin
import shim.

0.61.5: :meth:`InspectService.top` / :meth:`InspectService.vitality` present
system vitality projection only.
"""

from palm.services.inspect.present import present_top, present_vitality
from palm.services.inspect.service import InspectService

__all__ = ["InspectService", "present_top", "present_vitality"]
