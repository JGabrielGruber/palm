"""Boot walk context — shared seats for phase handlers (0.59.2+ / seat DI)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BootContext:
    """
    Mutable seat bag for one schedule walk (boot DI container).

    **Law:** handlers take seats from this context. They do not dig the
    system instance as ambient DI when a seat is already published.

    | Field | After phase |
    |-------|-------------|
    | ``shell`` | walk start (system instance owns seats) |
    | ``event`` / ``resource`` / ``workload`` / ``auth`` / ``context_engine`` | ``system.engines.init`` |
    | ``storage`` | ``system.storage.select`` |
    | ``outbox_store`` / ``outbox_processor`` | ``system.outbox.wire`` |
    | ``orchestration`` / ``instance_manager`` | ``system.hooks.install`` |
    | ``install`` | ``system.install.bind`` |
    | ``planes`` | ``system.planes.attach`` |
    | ``supervisor`` | ``system.supervisor.wire`` |

    Keep free of product types so ``palm.system.boot`` stays pure.
    Host-side handlers may hang collaborators on ``extras``.
    """

    schedule: str
    mode: str | None = None
    runtime: str | None = None
    """Log / identity name of the runtime (string), not the shell object."""
    shell: Any = None
    """System instance that owns seats (assembly target)."""

    # ── engine / collaborator seats (published as phases init them) ─────────
    event: Any = None
    resource: Any = None
    workload: Any = None
    auth: Any = None
    context_engine: Any = None
    storage: Any = None
    orchestration: Any = None
    instance_manager: Any = None
    outbox_store: Any = None
    outbox_processor: Any = None

    # ── interface + subsystem seats ─────────────────────────────────────────
    install: Any = None
    """InstallInterface after bind phase."""
    planes: Any = None
    """Planes subsystem after attach phase."""
    supervisor: Any = None
    """Supervisor subsystem after wire phase."""

    extras: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.extras.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.extras[key] = value

    def publish(self, **seats: Any) -> None:
        """Publish named seats onto this context (boot DI)."""
        for name, value in seats.items():
            if not hasattr(self, name):
                raise AttributeError(f"BootContext has no seat field {name!r}")
            setattr(self, name, value)

    def require_shell(self) -> Any:
        """Return the system instance shell; fail if the walk has no owner."""
        if self.shell is None:
            raise RuntimeError(
                "boot walk requires ctx.shell (system instance); "
                "BaseRuntime.start sets shell=self before walk_schedule"
            )
        return self.shell


__all__ = ["BootContext"]
