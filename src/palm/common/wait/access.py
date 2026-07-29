"""Shim (SD-012) — canonical: :mod:`palm.system.planes.wait.access`."""

from palm.system.planes.wait.access import (
    close_interest_for_state,
    close_interest_on_job,
    find_job_for_state,
    get_wait_plane,
    open_interest_for_state,
    open_interest_on_job,
)

__all__ = [
    "close_interest_for_state",
    "close_interest_on_job",
    "find_job_for_state",
    "get_wait_plane",
    "open_interest_for_state",
    "open_interest_on_job",
]
