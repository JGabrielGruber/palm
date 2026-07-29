"""Kit registry — install-list truth for surface infrastructure packages."""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class KitInfo:
    """One registered kit (name + purpose; module is the package)."""

    name: str
    description: str
    module: str


_lock = threading.RLock()
_kits: dict[str, KitInfo] = {}


def register_kit(
    name: str,
    *,
    description: str,
    module: str | None = None,
) -> KitInfo:
    """Register a kit. Idempotent when the same name and module re-register."""
    key = str(name).strip()
    if not key:
        raise ValueError("kit name must be non-empty")
    mod = module or f"palm.kits.{key}"
    info = KitInfo(name=key, description=str(description), module=mod)
    with _lock:
        existing = _kits.get(key)
        if existing is not None and existing.module == mod:
            return existing
        _kits[key] = info
        return info


def get_kit(name: str) -> KitInfo | None:
    with _lock:
        return _kits.get(str(name))


def list_kits() -> list[KitInfo]:
    with _lock:
        return [_kits[n] for n in sorted(_kits)]


def installed_kit_names() -> list[str]:
    with _lock:
        return sorted(_kits)


def clear_kits() -> None:
    """Test helper — empty the registry."""
    with _lock:
        _kits.clear()


def doctor_section() -> dict[str, Any]:
    """Small doctor fragment: installed kits vs intention list."""
    from palm.kits._apps import INSTALLED_KITS, INTENTION_KITS

    registered = installed_kit_names()
    return {
        "installed": list(INSTALLED_KITS),
        "registered": registered,
        "intentions": list(INTENTION_KITS),
        "kits": [
            {"name": k.name, "module": k.module, "description": k.description}
            for k in list_kits()
        ],
    }


__all__ = [
    "KitInfo",
    "clear_kits",
    "doctor_section",
    "get_kit",
    "installed_kit_names",
    "list_kits",
    "register_kit",
]
