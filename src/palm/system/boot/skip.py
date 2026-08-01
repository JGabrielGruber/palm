"""PhaseSkip — optional phase declines without failing the walk (0.59.3)."""

from __future__ import annotations


class PhaseSkip(Exception):
    """Handler signals the phase should be recorded as skip, not fail.

    Used for optional seats (outbox off, no runtime binding, …).
    """

    def __init__(self, reason: str) -> None:
        self.reason = str(reason) if reason else "skipped"
        super().__init__(self.reason)


__all__ = ["PhaseSkip"]
