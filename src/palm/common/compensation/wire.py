"""Install-board compensation bind — coordinator object, not a loop."""

from __future__ import annotations

from typing import Any

from palm.common.compensation.coordinator import CompensationCoordinator
from palm.common.compensation.registry import default_compensation_registry


def wire_install_compensation(event: Any) -> CompensationCoordinator:
    """Construct the compensation coordinator for the install board.

    Dual-attach (host.event + attach_runtimes) stays a host leftover.
    """
    return CompensationCoordinator(default_compensation_registry(), event)


__all__ = ["wire_install_compensation"]
