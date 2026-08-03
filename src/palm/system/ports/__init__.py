"""System interfaces (ports) — execution effects and install collaborators."""

from palm.system.ports.execution import ExecutionPort
from palm.system.ports.install import (
    InstallInterface,
    SystemInstall,
    WirePort,
    SystemWire,
    continuous_context_from_install,
    continuous_context_from_wire,
)

__all__ = [
    "ExecutionPort",
    "InstallInterface",
    "SystemInstall",
    "WirePort",
    "SystemWire",
    "continuous_context_from_install",
    "continuous_context_from_wire",
]
