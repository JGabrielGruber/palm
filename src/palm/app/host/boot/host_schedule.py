"""
Host schedule handlers — start law for ApplicationHost (0.59.4).

**Ownership:** host boot owns *when* and *in what order* the composition root
comes up. Handlers here are the rules. Collaborators (kernel, spawner, CQRS
wire, recovery, workplane) are tools — they do not own boot order.

**Break / harvest:** mid-theme breakage is expected. BootMode and PhaseSkip
are the switches. Do not restore import-order magic.

**Dependency direction:**

- ``ApplicationHost.start`` → walker + these handlers
- handlers → host collaborators (methods / coordinators) as a bag of tools
- collaborators must not re-enter host boot tables

Observation: SystemLog only (handlers do not wrap ``slog.phase`` themselves).
"""

from __future__ import annotations

from typing import Any

from palm.app.bootstrap import runtime_start_options
from palm.app.host.boot.system_log_phase import make_host_system_log_handler
from palm.app.host.events import HostEventType
from palm.app.host.workers import WorkerCoordinator
from palm.system.boot.context import BootContext
from palm.system.boot.skip import PhaseSkip
from palm.system.boot.walker import PhaseHandler
from palm.system.log import get_system_log


def build_host_handlers(
    host: Any,
    options: dict[str, Any],
) -> dict[str, PhaseHandler]:
    """Build the full host schedule handler map for one ``start()`` call.

    ``host`` is the ApplicationHost shell — assembly target, not schedule owner.
    """

    def kernel_bootstrap(_ctx: BootContext) -> None:
        host._app.bootstrap()

    def host_event(_ctx: BootContext) -> None:
        host._event.initialize()
        host._event_recorder.attach(host._event)

    def workers_note(_ctx: BootContext) -> None:
        host._worker_coordinator = WorkerCoordinator(host.profile, host._event)

    def system_spawn(_ctx: BootContext) -> None:
        merged = runtime_start_options(host.settings, **options)
        host._spawner.spawn_runtimes(merged)

    def definitions_load(_ctx: BootContext) -> None:
        host._app.load_definitions()

    def product_wire(_ctx: BootContext) -> None:
        host._wire_cqrs()

    def surfaces_mount(_ctx: BootContext) -> None:
        # Always call collaborator (inventory); skip narrative when deployment off.
        host._start_server_surface()
        if not host.profile.server:
            raise PhaseSkip("deployment.server_off")

    def projections_attach(_ctx: BootContext) -> None:
        host._attach_projections()
        if not host.composition.has("projections"):
            raise PhaseSkip("composition_off:projections")

    def recover(_ctx: BootContext) -> None:
        if host.boot_mode is not None and not host.boot_mode.recover_on_start:
            raise PhaseSkip("mode_recover_off")
        host._recovery.recover()

    def ready(ctx: BootContext) -> None:
        roles = sorted(host.profile.roles)
        host._event.emit(
            HostEventType.STARTED,
            roles=roles,
            primary=host._app.primary_name,
        )
        host._started = True
        get_system_log().info(
            "ready",
            "host ready",
            schedule="host",
            mode=ctx.mode,
            primary=host._app.primary_name,
            roles=",".join(roles) or "(none)",
        )

    def background_work_drain(_ctx: BootContext) -> None:
        if not host._work_drain_background_enabled():
            raise PhaseSkip("work_drain_off")
        host._workplane.start_background()

    return {
        "host.system_log": make_host_system_log_handler(host.boot_mode),
        "host.kernel.bootstrap": kernel_bootstrap,
        "host.event": host_event,
        "host.workers.note": workers_note,
        "host.system.spawn": system_spawn,
        "host.definitions.load": definitions_load,
        "host.product.wire": product_wire,
        "host.surfaces.mount": surfaces_mount,
        "host.projections.attach": projections_attach,
        "host.recover": recover,
        "host.ready": ready,
        "host.background.work_drain": background_work_drain,
    }


__all__ = ["build_host_handlers"]
