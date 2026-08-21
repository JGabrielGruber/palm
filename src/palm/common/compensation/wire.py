"""Install-board compensation bind — coordinator object, not a loop."""

from __future__ import annotations

from typing import Any

from palm.common.compensation.coordinator import CompensationCoordinator
from palm.common.compensation.registry import default_compensation_registry


def wire_install_compensation(event: Any) -> CompensationCoordinator:
    """Construct the compensation coordinator and attach it to the runtime bus."""
    coordinator = CompensationCoordinator(default_compensation_registry(), event)
    coordinator.attach(event)
    return coordinator


__all__ = ["wire_install_compensation"]
