"""
System start phase: start supervised background (system.background.start).

Subject: :class:`~palm.system.subsystems.supervisor.SystemSupervisor`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip
from palm.system.log import get_system_log


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
    *,
    definition: Any | None = None,
) -> BackgroundStartResult:
    """Start work_drain / outbox when DNA / options allow.

    ``work_drain`` starts when DNA lists it and install start ports are bound.
    Outbox still uses the start option.
    """
    from palm.system.assembly.seed import (
        dna_lists_work_drain,
        dna_refuses_background_drain,
    )

    opts = dict(options or {})
    install = opts.get("install")
    ports_bound = bool(getattr(install, "start_ports_bound", lambda: False)())
    want_drain = (
        dna_lists_work_drain(definition)
        and not dna_refuses_background_drain(definition)
        and ports_bound
    )
    want_outbox = bool(opts.get("enable_outbox_background", False))
    if not want_drain and not want_outbox:
        if definition is not None and not dna_lists_work_drain(definition):
            skip = "structure_off:work_drain"
        elif dna_lists_work_drain(definition) and not ports_bound:
            skip = "ports_off:work_drain"
        else:
            skip = "no_background_services_enabled"
        return BackgroundStartResult(started=[], skip_reason=skip)

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


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    shell = resolve_shell(ctx)
    sup = ctx.supervisor if ctx.supervisor is not None else shell.supervisor
    if sup is None:
        raise PhaseSkip("no_supervisor")
    seat = getattr(shell, "assembly", None)
    definition = getattr(seat, "definition", None) if seat is not None else None
    merged = dict(options)
    if "install" not in merged:
        merged["install"] = getattr(shell, "install", None)
    result = start_supervised_background(sup, merged, definition=definition)
    if result.should_skip:
        raise PhaseSkip(result.skip_reason or "background_skip")
    get_system_log().info(
        "supervisor.background.start",
        "supervised background started"
        if result.started
        else "supervised services already running or idle",
        schedule="system",
        runtime=ctx.runtime,
        services=",".join(result.started) or "(none)",
    )


DEFINITION = PhaseDefinition(
    id="system.background.start",
    run=run,
    description="Start supervised continuous services (work_drain, …)",
)

__all__ = [
    "BackgroundStartResult",
    "DEFINITION",
    "run",
    "start_supervised_background",
]
