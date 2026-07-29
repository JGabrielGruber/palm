"""
Django-style autoloading for pattern apps.

Each entry in ``INSTALLED_PATTERNS`` is a self-contained subpackage that
registers itself via ``registry.py`` on import.
"""

from __future__ import annotations

import importlib

# Real patterns only — intention stubs listed separately (ST-003 / SD-013).
INSTALLED_PATTERNS: tuple[str, ...] = (
    "dag",
    "parallel",
    "pipeline",
    "wizard",
)

# Not auto-loaded. Purpose in docs/STUBS.md (phase-ticker body must not look installed).
INTENTION_PATTERNS: tuple[str, ...] = ("etl",)


def autoload() -> None:
    """Import all installed pattern apps (triggers registry side effects)."""
    for name in INSTALLED_PATTERNS:
        importlib.import_module(f"palm.patterns.{name}")
