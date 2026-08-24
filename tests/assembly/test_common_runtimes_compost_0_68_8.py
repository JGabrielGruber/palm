"""0.68.8 — empty palm.common.runtimes parking lot composted."""

from __future__ import annotations

import importlib.util


def test_common_runtimes_package_is_gone() -> None:
    assert importlib.util.find_spec("palm.common.runtimes") is None
