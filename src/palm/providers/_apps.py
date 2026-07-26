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
    "neonroot",  # 0.53 — optional host CLI; health is honest when missing
)


def autoload() -> None:
    for name in INSTALLED_PROVIDERS:
        importlib.import_module(f"palm.providers.{name}")
