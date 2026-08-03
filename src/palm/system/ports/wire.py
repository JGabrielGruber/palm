"""
Compatibility re-export — prefer :mod:`palm.system.ports.install`.

``WirePort`` / ``SystemWire`` are aliases of
:class:`~palm.system.ports.install.InstallInterface` /
:class:`~palm.system.ports.install.SystemInstall`.
"""

from __future__ import annotations

from palm.system.ports.install import (
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
