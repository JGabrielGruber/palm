"""Autoload WorkloadRuntime packages listed in INSTALLED_RUNNERS."""

from __future__ import annotations

import importlib

INSTALLED_RUNNERS: tuple[str, ...] = (
    "local",  # Palm-managed process runner — always on (trusted default)
    "host",  # full-machine subprocess; default OFF — opt-in only
    "neonroot",  # hermetic spawn via NeonRoot CLI
)


def autoload() -> None:
    for name in INSTALLED_RUNNERS:
        importlib.import_module(f"palm.runners.{name}")


__all__ = ["INSTALLED_RUNNERS", "autoload"]
