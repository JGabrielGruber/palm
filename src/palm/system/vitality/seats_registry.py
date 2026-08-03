"""
Default VitalityRegistry factory (0.61.2).

Separate from seat *probe* catalog (:func:`default_probe_catalog`).
"""

from __future__ import annotations

from palm.system.vitality.capabilities import build_default_capabilities
from palm.system.vitality.registry import VitalityRegistry

_DEFAULT: VitalityRegistry | None = None


def default_vitality_registry(*, clone: bool = True) -> VitalityRegistry:
    """Return the default Palm vitality capability registry.

    When *clone* is True (default), callers get an isolated copy safe to
    mutate for tests or composition profiles.
    """
    global _DEFAULT
    if _DEFAULT is None:
        reg = VitalityRegistry()
        reg.extend(build_default_capabilities())
        _DEFAULT = reg
    return _DEFAULT.clone() if clone else _DEFAULT


def reset_default_vitality_registry_for_tests() -> None:
    """Drop cached default registry (tests only)."""
    global _DEFAULT
    _DEFAULT = None


__all__ = [
    "default_vitality_registry",
    "reset_default_vitality_registry_for_tests",
]
