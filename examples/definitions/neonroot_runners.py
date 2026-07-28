"""NeonRoot examples — resources removed (0.56).

Use workload dogfood instead::

    palm flow start run-python          # host | neonroot | auto
    palm flow start hermetic-job-smoke  # hermetic true via neonroot runtime
    palm flow start hermetic-ci-slice   # ruff + guard_core DAG

Doctor: ``palm doctor`` → neonroot WorkloadRuntime section.
"""

from __future__ import annotations


def register_definitions(repository: object) -> None:
    """No resource definitions — neonroot is a WorkloadRuntime only."""
    _ = repository
