"""
Django-style autoloading for provider apps.
"""

from __future__ import annotations

import importlib

INSTALLED_PROVIDERS: tuple[str, ...] = (
    "rest",
    "graphql",
    "postgres",
    "palm",
    "kv",
    "file",
    # neonroot removed 0.56 — isolation is WorkloadRuntime under palm.runners.neonroot
)


def autoload() -> None:
    for name in INSTALLED_PROVIDERS:
        importlib.import_module(f"palm.providers.{name}")
