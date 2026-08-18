"""
ApplicationHost — role-based deployment coordinator for Palm 0.10+.
"""

from palm.app.host.composition import CompositionProfile
from palm.app.host.events import HostEventType
from palm.app.host.roles import DeploymentProfile, DeploymentProfilePreset, DeploymentRoleName

__all__ = [
    "ApplicationHost",
    "BootMode",
    "CompositionProfile",
    "DeploymentProfile",
    "DeploymentProfilePreset",
    "DeploymentRoleName",
    "HostEventType",
    "run_host",
]

_LAZY_EXPORTS: dict[str, tuple[str, str]] = {
    "ApplicationHost": ("palm.app.host.application_host", "ApplicationHost"),
    "BootMode": ("palm.app.host.boot.modes", "BootMode"),
    "run_host": ("palm.app.host.application_host", "run_host"),
}


def __getattr__(name: str) -> object:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_path, attr = _LAZY_EXPORTS[name]
    import importlib

    module = importlib.import_module(module_path)
    value = getattr(module, attr)
    globals()[name] = value
    return value
