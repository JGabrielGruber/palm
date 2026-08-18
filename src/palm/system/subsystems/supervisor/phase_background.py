"""
System start phase: start supervised background (system.background.start).

Subject: :class:`~palm.system.subsystems.supervisor.SystemSupervisor`.
Walks registered services. Does not name organs.
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
from palm.system.subsystems.supervisor.service import ServiceStartContext


@dataclass(frozen=True)
class BackgroundStartResult:
    """Outcome of attempting to start supervised continuous services."""

    started: list[str]
    skip_reason: str | None = None

    @property
    def should_skip(self) -> bool:
        return self.skip_reason is not None


def _service_may_start(svc: Any, ctx: ServiceStartContext) -> bool:
    hook = getattr(svc, "may_start", None)
    if hook is None:
        return True
    return bool(hook(ctx))


def start_supervised_background(
    supervisor: Any,
    ctx: ServiceStartContext | None = None,
) -> BackgroundStartResult:
    """Start every registered service that may start."""
    start_ctx = ctx if ctx is not None else ServiceStartContext()
    names = list(supervisor.names())
    if not names:
        return BackgroundStartResult(started=[], skip_reason="none_registered")

    ready: list[str] = []
    started: list[str] = []
    for name in names:
        svc = supervisor.get(name)
        if svc is None:
            continue
        if not _service_may_start(svc, start_ctx):
            continue
        ready.append(name)
        started.extend(supervisor.start(name))
    if not ready:
        return BackgroundStartResult(started=[], skip_reason="none_ready")
    return BackgroundStartResult(started=started)


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    shell = resolve_shell(ctx)
    sup = ctx.supervisor if ctx.supervisor is not None else shell.supervisor
    if sup is None:
        raise PhaseSkip("no_supervisor")
    install = options.get("install")
    if install is None:
        install = ctx.install if ctx.install is not None else shell.install
    opts = dict(options)
    opts.pop("install", None)
    result = start_supervised_background(
        sup,
        ServiceStartContext(install=install, options=opts),
    )
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
    description="Start registered supervised continuous services",
)

__all__ = [
    "BackgroundStartResult",
    "DEFINITION",
    "run",
    "start_supervised_background",
]
