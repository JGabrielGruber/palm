"""
Continuous service definitions — participation law at the edge (CS-006).

:class:`~palm.system.subsystems.supervisor.SystemSupervisor` walks these and
``register``\\s results. Boot schedule only seats the supervisor and calls
:meth:`~SystemSupervisor.install`.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from palm.system.subsystems.supervisor.service import SystemService
    from palm.system.subsystems.supervisor.supervisor import SystemSupervisor


@dataclass
class ContinuousWireContext:
    """Ports for continuous service install (no full schedule prose)."""

    options: Mapping[str, Any] = field(default_factory=dict)
    work_plane: Any = None
    outbox_processor: Any = None
    outbox_store: Any = None

    @classmethod
    def from_install(
        cls,
        install: Any,
        options: Mapping[str, Any] | None = None,
    ) -> ContinuousWireContext:
        """Build from :class:`~palm.system.interfaces.install.InstallInterface` fields only."""
        return cls(
            options=dict(options or {}),
            work_plane=install.work_plane,
            outbox_processor=install.outbox_processor,
            outbox_store=install.outbox_store,
        )

    from_wire = from_install  # temporary alias


# register(supervisor, ctx) -> service or None if skipped
ContinuousRegisterFn = Callable[
    ["SystemSupervisor", ContinuousWireContext],
    "SystemService | None",
]


@dataclass(frozen=True)
class ContinuousServiceDefinition:
    """How one continuous service becomes a supervisor member."""

    name: str
    order: int
    register: ContinuousRegisterFn


def register_work_drain(
    supervisor: SystemSupervisor,
    ctx: ContinuousWireContext,
) -> SystemService | None:
    from palm.system.subsystems.supervisor.service import CallableSystemService

    plane = ctx.work_plane
    if plane is None:
        return None
    svc = CallableSystemService(
        "work_drain",
        start=plane.start_background,
        stop=plane.stop_background,
        status=plane.status,
    )
    supervisor.register(svc)
    return svc


def register_outbox(
    supervisor: SystemSupervisor,
    ctx: ContinuousWireContext,
) -> SystemService | None:
    from palm.system.subsystems.supervisor.outbox_loop import OutboxLoopService

    proc = ctx.outbox_processor
    store = ctx.outbox_store
    if proc is None or store is None:
        return None
    opts = dict(ctx.options or {})
    svc = OutboxLoopService(
        proc,
        store,
        poll_interval=float(opts.get("outbox_poll_interval", 0.5) or 0.5),
        batch_size=int(opts.get("outbox_batch_size", 50) or 50),
        recover_on_start=bool(opts.get("outbox_recover_on_startup", True)),
    )
    supervisor.register(svc)
    return svc


WORK_DRAIN_SERVICE = ContinuousServiceDefinition(
    name="work_drain",
    order=10,
    register=register_work_drain,
)  # Named recipe. Default wire does not walk this.

OUTBOX_SERVICE = ContinuousServiceDefinition(
    name="outbox",
    order=20,
    register=register_outbox,
)

# work_drain is DNA-listed. The capability hand registers it.
# Wire must not freelance that organ.
DEFAULT_CONTINUOUS_DEFINITIONS: tuple[ContinuousServiceDefinition, ...] = (
    OUTBOX_SERVICE,
)


__all__ = [
    "ContinuousServiceDefinition",
    "ContinuousWireContext",
    "DEFAULT_CONTINUOUS_DEFINITIONS",
    "OUTBOX_SERVICE",
    "WORK_DRAIN_SERVICE",
    "register_outbox",
    "register_work_drain",
]
