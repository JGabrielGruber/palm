"""
InstallInterface / SystemInstall — collaborator interface for subsystem install (0.61).

Peer of :class:`~palm.system.interfaces.execution.ExecutionPort`:

| Interface | Role |
|-----------|------|
| **execution** | How work *runs* effects |
| **install** | How boot / planes / supervisor *see* collaborators |

The install board is a **living interface seat** on the system instance.
Boot **binds** named ports explicitly. Subsystem install does not dig a
runtime bag or take ``Any`` scrapers.

**DI law:** inject interfaces and subsystems — not the system instance.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Protocol, runtime_checkable

_UNSET: Any = object()


@runtime_checkable
class InstallInterface(Protocol):
    """
    Named collaborator surface for system install.

    Implementations: :class:`SystemInstall` on the system instance.
    """

    @property
    def orchestration(self) -> Any: ...

    @property
    def event(self) -> Any: ...

    @property
    def storage(self) -> Any: ...

    @property
    def instance_manager(self) -> Any: ...

    @property
    def get_job(self) -> Callable[[str], Any | None] | None: ...

    @property
    def submit(self) -> Callable[..., Any] | None: ...

    @property
    def able(self) -> Callable[[], bool] | None: ...

    @property
    def outbox_store(self) -> Any: ...

    @property
    def outbox_processor(self) -> Any: ...

    @property
    def work_plane(self) -> Any: ...

    @property
    def event_journal(self) -> Any: ...

    @property
    def projections(self) -> Any: ...


class SystemInstall:
    """
    Mutable install board — filled by explicit :meth:`bind`, not by bag scrape.

    Holds collaborators for plane install and continuous service register.
    """

    __slots__ = (
        "_orchestration",
        "_event",
        "_storage",
        "_instance_manager",
        "_get_job",
        "_submit",
        "_able",
        "_admission_able",
        "_outbox_store",
        "_outbox_processor",
        "_work_plane",
        "_event_journal",
        "_event_journal_sub",
        "_projections",
    )

    def __init__(self) -> None:
        self._orchestration: Any = None
        self._event: Any = None
        self._storage: Any = None
        self._instance_manager: Any = None
        self._get_job: Callable[[str], Any | None] | None = None
        self._submit: Callable[..., Any] | None = None
        self._able: Callable[[], bool] | None = None
        self._admission_able: Callable[[], bool] | None = None
        self._outbox_store: Any = None
        self._outbox_processor: Any = None
        self._work_plane: Any = None
        self._event_journal: Any = None
        self._event_journal_sub: Any = None
        self._projections: Any = None

    # ── read surface (InstallInterface) ─────────────────────────────────────

    @property
    def orchestration(self) -> Any:
        return self._orchestration

    @property
    def event(self) -> Any:
        return self._event

    @property
    def storage(self) -> Any:
        return self._storage

    @property
    def instance_manager(self) -> Any:
        return self._instance_manager

    @property
    def get_job(self) -> Callable[[str], Any | None] | None:
        return self._get_job

    @property
    def submit(self) -> Callable[..., Any] | None:
        return self._submit

    @property
    def able(self) -> Callable[[], bool] | None:
        return self._able

    @property
    def admission_able(self) -> Callable[[], bool] | None:
        """Ready query for continue (wait plane). Not work-drain membership."""
        return self._admission_able

    @property
    def outbox_store(self) -> Any:
        return self._outbox_store

    @property
    def outbox_processor(self) -> Any:
        return self._outbox_processor

    @property
    def work_plane(self) -> Any:
        return self._work_plane

    @property
    def event_journal(self) -> Any:
        """Append-only journal attached by the journal hand. Not a loop."""
        return self._event_journal

    @property
    def event_journal_sub(self) -> Any:
        """Interceptor subscription for drop-on-omit. Not a product slot."""
        return self._event_journal_sub

    @property
    def projections(self) -> Any:
        """Core projections attached by the projections hand. Not a loop."""
        return self._projections

    # ── explicit bind ────────────────────────────────────────────────────────

    def bind(
        self,
        *,
        orchestration: Any = _UNSET,
        event: Any = _UNSET,
        storage: Any = _UNSET,
        instance_manager: Any = _UNSET,
        get_job: Callable[[str], Any | None] | None | object = _UNSET,
        submit: Callable[..., Any] | None | object = _UNSET,
        able: Callable[[], bool] | None | object = _UNSET,
        admission_able: Callable[[], bool] | None | object = _UNSET,
        outbox_store: Any = _UNSET,
        outbox_processor: Any = _UNSET,
        work_plane: Any = _UNSET,
        event_journal: Any = _UNSET,
        event_journal_sub: Any = _UNSET,
        projections: Any = _UNSET,
    ) -> SystemInstall:
        """
        Bind named ports. Omitted kwargs are left unchanged.

        Pass ``None`` to clear a slot. This is the only legal write path.
        """
        if orchestration is not _UNSET:
            self._orchestration = orchestration
        if event is not _UNSET:
            self._event = event
        if storage is not _UNSET:
            self._storage = storage
        if instance_manager is not _UNSET:
            self._instance_manager = instance_manager
        if get_job is not _UNSET:
            self._get_job = get_job  # type: ignore[assignment]
        if submit is not _UNSET:
            self._submit = submit  # type: ignore[assignment]
        if able is not _UNSET:
            self._able = able  # type: ignore[assignment]
        if admission_able is not _UNSET:
            self._admission_able = admission_able  # type: ignore[assignment]
        if outbox_store is not _UNSET:
            self._outbox_store = outbox_store
        if outbox_processor is not _UNSET:
            self._outbox_processor = outbox_processor
        if work_plane is not _UNSET:
            self._work_plane = work_plane
        if event_journal is not _UNSET:
            self._event_journal = event_journal
        if event_journal_sub is not _UNSET:
            self._event_journal_sub = event_journal_sub
        if projections is not _UNSET:
            self._projections = projections
        self._push_start_ports()
        return self

    def start_ports_bound(self) -> bool:
        """True when work_drain start ports are on this board."""
        return self._work_plane is not None and self._submit is not None and self._able is not None

    def _push_start_ports(self) -> None:
        """Plane reads submit/able from this board — bind is the only writer."""
        plane = self._work_plane
        if plane is None:
            return
        if self._submit is not None:
            setter = getattr(plane, "set_submit_flow", None)
            if callable(setter):
                setter(self._submit)
            else:
                plane._submit_flow = self._submit
        set_able = getattr(plane, "set_able", None)
        if callable(set_able):
            set_able(self._able)

    def status(self) -> dict[str, Any]:
        """Public snapshot (vitality / doctor)."""
        return {
            "orchestration": self._orchestration is not None,
            "event": self._event is not None,
            "storage": self._storage is not None,
            "instance_manager": self._instance_manager is not None,
            "get_job": self._get_job is not None,
            "submit": self._submit is not None,
            "able": self._able is not None,
            "admission_able": self._admission_able is not None,
            "outbox_store": self._outbox_store is not None,
            "outbox_processor": self._outbox_processor is not None,
            "work_plane": self._work_plane is not None,
            "event_journal": self._event_journal is not None,
            "projections": self._projections is not None,
            "start_ports": self.start_ports_bound(),
        }

    def require_orchestration(self) -> Any:
        if self._orchestration is None:
            raise RuntimeError("system install: orchestration not bound")
        return self._orchestration

    def require_storage(self) -> Any:
        if self._storage is None:
            raise RuntimeError("system install: storage not bound")
        return self._storage

    def require_submit(self) -> Callable[..., Any]:
        if self._submit is None:
            raise RuntimeError("system install: submit not bound")
        return self._submit


def continuous_context_from_install(
    install: InstallInterface,
    options: Mapping[str, Any] | None = None,
) -> Any:
    """Build continuous install context from InstallInterface (no runtime bag)."""
    from palm.system.subsystems.supervisor.definition import ContinuousWireContext

    return ContinuousWireContext(
        options=dict(options or {}),
        work_plane=install.work_plane,
        outbox_processor=install.outbox_processor,
        outbox_store=install.outbox_store,
    )


# ── temporary aliases (remove when callers migrate) ──────────────────────────

WirePort = InstallInterface
SystemWire = SystemInstall
continuous_context_from_wire = continuous_context_from_install


__all__ = [
    "InstallInterface",
    "SystemInstall",
    "continuous_context_from_install",
    # aliases
    "WirePort",
    "SystemWire",
    "continuous_context_from_wire",
]
