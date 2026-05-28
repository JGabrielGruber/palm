"""
Execution backends — pluggable strategies for advancing Job executables.

TestBackend is the primary concrete implementation and the one used by
the vast majority of tests. BehaviorTreeBackend is optional and isolated.
"""

from __future__ import annotations

from .backend import (
    BehaviorTreeBackend,
    ExecutionBackend,
    TestBackend,
)

__all__ = ["ExecutionBackend", "TestBackend", "BehaviorTreeBackend"]
