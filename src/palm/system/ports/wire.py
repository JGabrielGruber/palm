"""
WirePort / SystemWire — collaborator surface for install (0.61).

Peer of :class:`~palm.system.ports.execution.ExecutionPort`:

| Port | Role |
|------|------|
| **execution** | How work *runs* effects |
| **wire** | How boot / planes / supervisor *see* collaborators |

The wire is a **living seat** on the system instance. Boot **binds** named
ports explicitly. Install does not dig a runtime bag or take ``Any`` scrapers.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Protocol, runtime_checkable

_UNSET: Any = object()


@runtime_checkable
class WirePort(Protocol):
    """
    Named collaborator surface for system install.

    Implementations: :class:`SystemWire` on the system instance.
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


class SystemWire:
    """
    Mutable wire board — filled by explicit :meth:`bind`, not by bag scrape.

    Holds collaborators for plane install and continuous service wire.
    """

    __slots__ = (
        "_orchestration",
        "_event",
        "_storage",
        "_instance_manager",
        "_get_job",
        "_submit",
        "_able",
        "_outbox_store",
        "_outbox_processor",
        "_work_plane",
    )

    def __init__(self) -> None:
        self._orchestration: Any = None
        self._event: Any = None
        self._storage: Any = None
        self._instance_manager: Any = None
        self._get_job: Callable[[str], Any | None] | None = None
        self._submit: Callable[..., Any] | None = None
        self._able: Callable[[], bool] | None = None
        self._outbox_store: Any = None
        self._outbox_processor: Any = None
        self._work_plane: Any = None

    # ── read surface (WirePort) ──────────────────────────────────────────────

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
    def outbox_store(self) -> Any:
        return self._outbox_store

    @property
    def outbox_processor(self) -> Any:
        return self._outbox_processor

    @property
    def work_plane(self) -> Any:
        return self._work_plane

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
        outbox_store: Any = _UNSET,
        outbox_processor: Any = _UNSET,
        work_plane: Any = _UNSET,
    ) -> SystemWire:
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
        if outbox_store is not _UNSET:
            self._outbox_store = outbox_store
        if outbox_processor is not _UNSET:
            self._outbox_processor = outbox_processor
        if work_plane is not _UNSET:
            self._work_plane = work_plane
        return self

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
            "outbox_store": self._outbox_store is not None,
            "outbox_processor": self._outbox_processor is not None,
            "work_plane": self._work_plane is not None,
        }

    def require_orchestration(self) -> Any:
        if self._orchestration is None:
            raise RuntimeError("system wire: orchestration not bound")
        return self._orchestration

    def require_storage(self) -> Any:
        if self._storage is None:
            raise RuntimeError("system wire: storage not bound")
        return self._storage

    def require_submit(self) -> Callable[..., Any]:
        if self._submit is None:
            raise RuntimeError("system wire: submit not bound")
        return self._submit


def continuous_context_from_wire(
    wire: WirePort,
    options: Mapping[str, Any] | None = None,
) -> Any:
    """Build continuous install context from a wire (no runtime bag)."""
    from palm.system.supervisor.definition import ContinuousWireContext

    return ContinuousWireContext(
        options=dict(options or {}),
        work_plane=wire.work_plane,
        outbox_processor=wire.outbox_processor,
        outbox_store=wire.outbox_store,
    )


__all__ = [
    "SystemWire",
    "WirePort",
    "continuous_context_from_wire",
]
