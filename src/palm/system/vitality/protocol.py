"""
SeatReportable — native self-report protocol for living seats (0.61.1).

Seats that implement :meth:`seat_report` are preferred over raw sampling.
Otherwise vitality raw-dogs public methods/attrs into ``meta.raw``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

from palm.system.vitality.report import SeatReport


@runtime_checkable
class SeatReportable(Protocol):
    """Object that can emit a vitality seat report without raw sampling."""

    def seat_report(self) -> SeatReport | Mapping[str, Any]:
        """Return a :class:`SeatReport` or a ``palm.seat_report/1`` mapping."""
        ...


def has_seat_report(obj: Any) -> bool:
    """True when *obj* looks like it implements native seat reporting."""
    if obj is None:
        return False
    if isinstance(obj, SeatReportable):
        return True
    # Structural fallback: callable seat_report without full Protocol match.
    method = getattr(obj, "seat_report", None)
    return callable(method)


def try_native_report(obj: Any) -> SeatReport | Mapping[str, Any] | None:
    """Call ``seat_report()`` when present; return ``None`` if unavailable."""
    if obj is None:
        return None
    method = getattr(obj, "seat_report", None)
    if not callable(method):
        return None
    return method()


__all__ = [
    "SeatReportable",
    "has_seat_report",
    "try_native_report",
]
