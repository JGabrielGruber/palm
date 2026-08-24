"""Local runner app — always-on Palm process WorkloadRuntime."""

from __future__ import annotations

from palm.runners.app import RunnerApp


class LocalRunnerApp(RunnerApp):
    name = "local"
    label = "Palm local process WorkloadRuntime (always on)"
    default_enabled = True


local_runner_app = LocalRunnerApp()

__all__ = ["LocalRunnerApp", "local_runner_app"]
