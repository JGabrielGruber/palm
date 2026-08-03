"""Compatibility re-export — prefer :mod:`palm.system.interfaces`."""

from __future__ import annotations

from palm.system.interfaces import (
    ExecutionPort,
    InstallInterface,
    SystemInstall,
    SystemInterface,
    WirePort,
    SystemWire,
    continuous_context_from_install,
    continuous_context_from_wire,
)

__all__ = [
    "ExecutionPort",
    "InstallInterface",
    "SystemInstall",
    "SystemInterface",
    "WirePort",
    "SystemWire",
    "continuous_context_from_install",
    "continuous_context_from_wire",
]
