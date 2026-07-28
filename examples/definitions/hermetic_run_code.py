"""Deprecated name — definitions live in ``run_python.py`` (Workload plane).

Kept so older docs that mention this module path still resolve; registration is a no-op
because ``run_python.register_definitions`` already registers the ``hermetic-run-code`` alias.
"""

from __future__ import annotations


def register_definitions(repository: object) -> None:
    """No-op — see :mod:`examples.definitions.run_python`."""
    _ = repository
