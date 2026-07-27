"""Doctor report extension points — register downward (no common → providers)."""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any

# (runtime) -> {"section": dict | None, "issues": list[str]}
DoctorContributor = Callable[[Any], dict[str, Any]]

_lock = threading.RLock()
_contributors: list[DoctorContributor] = []


def register_doctor_contributor(fn: DoctorContributor) -> None:
    """Register a doctor section builder (called from provider/app ready)."""
    with _lock:
        if fn not in _contributors:
            _contributors.append(fn)


def clear_doctor_contributors() -> None:
    with _lock:
        _contributors.clear()


def collect_doctor_extensions(runtime: Any) -> tuple[dict[str, Any], list[str]]:
    """Merge contributor sections and issues for :func:`build_doctor_report`."""
    sections: dict[str, Any] = {}
    issues: list[str] = []
    with _lock:
        funcs = list(_contributors)
    for fn in funcs:
        try:
            result = fn(runtime) or {}
        except Exception as exc:
            issues.append(f"doctor contributor failed: {exc}")
            continue
        section = result.get("section")
        if isinstance(section, dict):
            sections.update(section)
        extra_issues = result.get("issues")
        if isinstance(extra_issues, list):
            issues.extend(str(i) for i in extra_issues)
    return sections, issues


__all__ = [
    "DoctorContributor",
    "clear_doctor_contributors",
    "collect_doctor_extensions",
    "register_doctor_contributor",
]
