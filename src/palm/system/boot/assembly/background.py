"""Supervised background start policy — boot assembly leaf."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BackgroundStartResult:
    """Outcome of attempting to start supervised continuous services."""

    started: list[str]
    skip_reason: str | None = None

    @property
    def should_skip(self) -> bool:
        return self.skip_reason is not None


def start_supervised_background(
    supervisor: Any,
    options: Mapping[str, Any] | None = None,
) -> BackgroundStartResult:
    """
    Start work_drain / outbox when options and membership allow.

    Returns skip_reason when the phase should PhaseSkip; otherwise started names.
    """
    opts = dict(options or {})
    if bool(opts.get("allow_background_drain", True)) is False:
        return BackgroundStartResult(started=[], skip_reason="allow_background_drain_off")

    want_drain = bool(opts.get("enable_work_drain_service", False))
    want_outbox = bool(opts.get("enable_outbox_background", False))
    if not want_drain and not want_outbox:
        return BackgroundStartResult(
            started=[],
            skip_reason="no_background_services_enabled",
        )

    has_drain = supervisor.get("work_drain") is not None
    has_outbox = supervisor.get("outbox") is not None
    if not ((want_drain and has_drain) or (want_outbox and has_outbox)):
        return BackgroundStartResult(
            started=[],
            skip_reason="no_matching_supervised_services",
        )

    started: list[str] = []
    if want_drain and has_drain:
        started.extend(supervisor.start("work_drain"))
    if want_outbox and has_outbox:
        started.extend(supervisor.start("outbox"))
    return BackgroundStartResult(started=started)


__all__ = ["BackgroundStartResult", "start_supervised_background"]
