"""
System interfaces — named contracts on the shell (execution, install).

Target home for what lived under ``palm.system.interfaces``. Prefer this package.
``palm.system.interfaces`` re-exports for one-theme compatibility.
"""

from __future__ import annotations

from palm.system.interfaces.execution import ExecutionPort
from palm.system.interfaces.install import (
    InstallInterface,
    SystemInstall,
    WirePort,
    SystemWire,
    continuous_context_from_install,
    continuous_context_from_wire,
)
from palm.system.interfaces.protocol import SystemInterface

__all__ = [
    "SystemInterface",
    "ExecutionPort",
    "InstallInterface",
    "SystemInstall",
    "WirePort",
    "SystemWire",
    "continuous_context_from_install",
    "continuous_context_from_wire",
]
