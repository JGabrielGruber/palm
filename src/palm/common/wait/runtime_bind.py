"""Compatibility wire entry — prefer :class:`~palm.common.wait.plane.WaitPlaneService`.

0.55.10: :func:`bind_wait_matcher_to_runtime` delegates to the continue plane and
returns the matcher for callers that still expect a :class:`WaitMatcher`.
"""

from __future__ import annotations

from typing import Any

from palm.common.wait.matcher import WaitMatcher
from palm.common.wait.plane import WaitPlaneService, bind_wait_plane_to_runtime


def bind_wait_matcher_to_runtime(runtime: Any) -> WaitMatcher:
    """Attach continue plane; return its matcher (legacy signature)."""
    existing = getattr(runtime, "wait_plane", None)
    if isinstance(existing, WaitPlaneService) and existing.matcher is not None:
        return existing.matcher
    plane = bind_wait_plane_to_runtime(runtime)
    # Stash when runtime supports the slot (BaseRuntime).
    if hasattr(runtime, "_wait_plane"):
        runtime._wait_plane = plane
    matcher = plane.matcher
    if matcher is None:
        raise RuntimeError("WaitPlaneService.attach did not produce a matcher")
    return matcher


__all__ = ["bind_wait_matcher_to_runtime"]
