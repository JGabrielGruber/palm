"""Compatibility — prefer :mod:`palm.system.interfaces.install`."""

from __future__ import annotations

from palm.system.interfaces.install import (
    InstallInterface,
    SystemInstall,
    WirePort,
    SystemWire,
    continuous_context_from_install,
    continuous_context_from_wire,
)

__all__ = [
    "InstallInterface",
    "SystemInstall",
    "WirePort",
    "SystemWire",
    "continuous_context_from_install",
    "continuous_context_from_wire",
]
