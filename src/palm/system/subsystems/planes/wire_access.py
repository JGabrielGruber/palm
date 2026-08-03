"""Compatibility re-export — prefer :mod:`palm.system.subsystems.planes.install_access`."""

from __future__ import annotations

from palm.system.subsystems.planes.install_access import (
    require_system_install,
    require_system_wire,
)

__all__ = ["require_system_install", "require_system_wire"]
