"""0.68.5 — LocalRunnerApp empty ready() override composted."""

from __future__ import annotations

from palm.runners.host.app import HostRunnerApp
from palm.runners.local.app import LocalRunnerApp
from palm.runners.neonroot.app import NeonrootRunnerApp


def test_local_has_no_ready_override() -> None:
    assert not hasattr(LocalRunnerApp, "ready")
    assert not hasattr(HostRunnerApp, "ready")
    assert not hasattr(NeonrootRunnerApp, "ready")
