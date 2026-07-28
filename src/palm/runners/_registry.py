"""Runner app registry (bootstrap metadata; runtime classes use core registry)."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from palm.runners.app import RunnerApp

_lock = threading.RLock()
_apps: dict[str, RunnerApp] = {}


def register_runner_app(app: RunnerApp) -> None:
    with _lock:
        _apps[app.name] = app


def get_runner_apps() -> list[RunnerApp]:
    with _lock:
        return list(_apps.values())


def clear_runner_apps() -> None:
    with _lock:
        _apps.clear()


__all__ = ["clear_runner_apps", "get_runner_apps", "register_runner_app"]
