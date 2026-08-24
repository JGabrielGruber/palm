"""0.68.5 — LocalRunnerApp empty ready() override composted."""

from __future__ import annotations

from palm.runners.app import RunnerApp
from palm.runners.host.app import HostRunnerApp
from palm.runners.local.app import LocalRunnerApp
from palm.runners.neonroot.app import NeonrootRunnerApp


def test_local_ready_is_the_base_hook() -> None:
    assert LocalRunnerApp.ready is RunnerApp.ready
    assert HostRunnerApp.ready is RunnerApp.ready
    assert NeonrootRunnerApp.ready is RunnerApp.ready
