"""Install-board analytics bind — membership organ, not a loop."""

from __future__ import annotations


class AnalyticsOrgan:
    """Analytics membership on the install board. Not a supervisor loop.

    Product ``AnalyticsService`` leftover aliases this slot when DNA lists
    it. ``replace_enabled`` is the public write for ``analytics_enabled``.
    """

    __slots__ = ("_enabled",)

    def __init__(self) -> None:
        self._enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    def replace_enabled(self, enabled: bool) -> None:
        """Refine enabled on this organ. Do not mint a second seat."""
        self._enabled = bool(enabled)


def wire_install_analytics() -> AnalyticsOrgan:
    """Construct the analytics organ. Product leftover may refine enabled."""
    return AnalyticsOrgan()


__all__ = ["AnalyticsOrgan", "wire_install_analytics"]
