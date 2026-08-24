"""0.68.6 — runner ready() call composted. Pattern/Provider ready stays."""

from __future__ import annotations

import inspect

from palm.common.patterns.app import PatternApp
from palm.common.providers.app import ProviderApp
from palm.runners.app import RunnerApp
from palm.runners.host.app import HostRunnerApp
from palm.runners.local.app import LocalRunnerApp
from palm.runners.neonroot.app import NeonrootRunnerApp


def test_runner_register_does_not_call_ready() -> None:
    src = inspect.getsource(RunnerApp.register)
    assert "ready" not in src
    assert not hasattr(RunnerApp, "ready")
    assert not hasattr(LocalRunnerApp, "ready")
    assert not hasattr(HostRunnerApp, "ready")
    assert not hasattr(NeonrootRunnerApp, "ready")


def test_pattern_and_provider_ready_stay() -> None:
    assert callable(PatternApp.ready)
    assert callable(ProviderApp.ready)
    assert "self.ready()" in inspect.getsource(PatternApp.register)
    assert "self.ready()" in inspect.getsource(ProviderApp.register)
