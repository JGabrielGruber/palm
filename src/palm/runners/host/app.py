"""Host runner app manifest."""

from __future__ import annotations

from palm.runners.app import RunnerApp


class HostRunnerApp(RunnerApp):
    name = "host"
    label = "Host subprocess WorkloadRuntime (default OFF)"
    default_enabled = False


host_runner_app = HostRunnerApp()

__all__ = ["HostRunnerApp", "host_runner_app"]
