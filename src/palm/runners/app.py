"""RunnerApp — Django-style manifest for WorkloadRuntime packages."""

from __future__ import annotations

from abc import ABC
from typing import ClassVar

from palm.runners._registry import register_runner_app


class RunnerApp(ABC):
    """Declarative manifest for a runner subpackage."""

    name: ClassVar[str]
    label: ClassVar[str] = ""
    default_enabled: ClassVar[bool] = False

    def register(self) -> None:
        register_runner_app(self)


__all__ = ["RunnerApp"]
