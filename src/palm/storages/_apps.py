"""
Django-style autoloading for storage apps.
"""

from __future__ import annotations

import importlib

CORE_STORAGES: tuple[str, ...] = ("memory", "filesystem")
# Intention backends (ST-002) — load only via StorageFactory / explicit opt-in.
OPTIONAL_STORAGES: tuple[str, ...] = ("postgres", "mongodb")
# Truthful default install = core only (not optional placeholders).
INSTALLED_STORAGES: tuple[str, ...] = CORE_STORAGES


def autoload(*, include_optional: bool = False) -> None:
    """Import core storage apps; optional backends load lazily via StorageFactory."""
    for name in CORE_STORAGES:
        importlib.import_module(f"palm.storages.{name}")
    if include_optional:
        for name in OPTIONAL_STORAGES:
            importlib.import_module(f"palm.storages.{name}")
