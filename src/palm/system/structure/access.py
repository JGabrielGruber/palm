"""Published admission access helpers — no product base class (0.63.23).

Shape discovered from assist inject (0.63.22): packaging digs once and hands a
zero-arg factory; business paths that need admission call ``require_business_admission``
on that source. Acts that need an organ call ``require_capability``.
No service hierarchy required.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def admission_source_from_runtime_resolver(
    resolve: Callable[[str | None], Any],
) -> Callable[[], Any]:
    """Build an *admission_source* factory from a runtime resolver.

    Packaging (host / ServerContext) owns the dig. Product holds only the
    returned callable and never digs the shell for readiness.
    """

    def _source() -> Any:
        return getattr(resolve(None), "admission", None)

    return _source


__all__ = [
    "admission_source_from_runtime_resolver",
]
