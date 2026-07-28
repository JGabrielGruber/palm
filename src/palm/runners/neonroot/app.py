"""Neonroot runner app — WorkloadRuntime registration (distinct from provider)."""

from __future__ import annotations

from palm.runners.app import RunnerApp


class NeonrootRunnerApp(RunnerApp):
    name = "neonroot"
    label = "NeonRoot WorkloadRuntime (hermetic spawn)"
    default_enabled = True

    def ready(self) -> None:
        # Provider already registers neonroot doctor; workload doctor is aggregate.
        return None


neonroot_runner_app = NeonrootRunnerApp()

__all__ = ["NeonrootRunnerApp", "neonroot_runner_app"]
