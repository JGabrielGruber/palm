"""
Continuous service definitions — participation law at the edge (CS-006).

:class:`~palm.system.supervisor.SystemSupervisor` walks these and
``register``\\s results. Boot schedule only seats the supervisor and calls
:meth:`~SystemSupervisor.install`.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from palm.system.supervisor.service import SystemService
    from palm.system.supervisor.supervisor import SystemSupervisor


@dataclass
class ContinuousWireContext:
    """Ports for continuous service install (no full schedule prose)."""

    options: Mapping[str, Any] = field(default_factory=dict)
    work_plane: Any = None
    outbox_processor: Any = None
    outbox_store: Any = None

    @classmethod
    def from_source(
        cls,
        source: Any,
        options: Mapping[str, Any] | None = None,
    ) -> ContinuousWireContext:
        """Extract ports from a *source* with named collaborators (ISP)."""
        proc = getattr(source, "outbox_processor", None) or getattr(
            source, "_outbox_processor", None
        )
        store = getattr(source, "outbox_store", None) or getattr(
            source, "_outbox_store", None
        )
        return cls(
            options=dict(options or {}),
            work_plane=getattr(source, "work_plane", None),
            outbox_processor=proc,
            outbox_store=store,
        )

    @classmethod
    def from_runtime(
        cls,
        runtime: Any,
        options: Mapping[str, Any] | None = None,
    ) -> ContinuousWireContext:
        """Compat: prefer ``runtime.continuous_wire(options)``."""
        continuous_wire = getattr(runtime, "continuous_wire", None)
        if callable(continuous_wire):
            return continuous_wire(options)
        return cls.from_source(runtime, options)


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
    from palm.system.supervisor.service import CallableSystemService

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
    from palm.system.supervisor.outbox_loop import OutboxLoopService

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
)

OUTBOX_SERVICE = ContinuousServiceDefinition(
    name="outbox",
    order=20,
    register=register_outbox,
)

DEFAULT_CONTINUOUS_DEFINITIONS: tuple[ContinuousServiceDefinition, ...] = (
    WORK_DRAIN_SERVICE,
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
