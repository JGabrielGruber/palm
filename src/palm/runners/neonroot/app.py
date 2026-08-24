"""Neonroot runner app — WorkloadRuntime (hermetic spawn)."""

from __future__ import annotations

from palm.runners.app import RunnerApp


class NeonrootRunnerApp(RunnerApp):
    name = "neonroot"
    label = "NeonRoot WorkloadRuntime (hermetic spawn)"
    default_enabled = True


neonroot_runner_app = NeonrootRunnerApp()

__all__ = ["NeonrootRunnerApp", "neonroot_runner_app"]
