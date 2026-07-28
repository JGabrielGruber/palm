"""Django-style autoloading for WorkloadRuntime runner apps."""

from __future__ import annotations

import importlib

INSTALLED_RUNNERS: tuple[str, ...] = (
    "host",  # subprocess; default OFF — opt-in only
    "neonroot",  # hermetic spawn via NeonRoot CLI
)


def autoload() -> None:
    for name in INSTALLED_RUNNERS:
        importlib.import_module(f"palm.runners.{name}")


__all__ = ["INSTALLED_RUNNERS", "autoload"]
