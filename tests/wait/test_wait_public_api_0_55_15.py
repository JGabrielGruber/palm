"""0.55.15 — continue plane public package surface is the slim door."""

from __future__ import annotations

import palm.common.wait as wait_pkg

# Locked by VISION-0.55.15 — expand only with deliberate API design.
EXPECTED_PUBLIC = frozenset(
    {
        "WaitPlaneService",
        "bind_wait_plane_to_runtime",
        "close_interest_for_state",
        "close_interest_on_job",
        "find_job_for_state",
        "get_wait_plane",
        "open_interest_for_state",
        "open_interest_on_job",
        "summarize_waiting_on",
        "waiting_on_from_job",
        "waiting_on_from_state",
        "waiting_on_row",
    }
)

# Kit symbols removed from the package root (import submodules if needed).
FORBIDDEN_ROOT = frozenset(
    {
        "open_tracked_wait",
        "close_tracked_wait",
        "bind_wait_matcher_to_runtime",
        "WaitMatcher",
        "WaitOwnerIndex",
        "open_workload_wait",
        "emit_workload_ready",
        "deliver_nested_wizard_completion",
    }
)


def test_package_all_is_slim_door() -> None:
    assert frozenset(wait_pkg.__all__) == EXPECTED_PUBLIC


def test_kit_symbols_not_on_package_root() -> None:
    for name in FORBIDDEN_ROOT:
        assert not hasattr(wait_pkg, name), f"{name} must not re-export from package root"


def test_plane_is_primary_export() -> None:
    assert wait_pkg.WaitPlaneService is not None
    assert callable(wait_pkg.bind_wait_plane_to_runtime)
    assert callable(wait_pkg.open_interest_on_job)
