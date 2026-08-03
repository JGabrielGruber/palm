"""
PlaneDefinition — participation law at the edge (0.61 / SD-015).

**Registry extension:** each plane package owns how it is constructed and
wired. :class:`~palm.system.planes.hub.SystemPlanes` only holds definitions,
orders install, and consumes the resulting instance (``put``).

**ISP / DIP (CS-008+):** definitions depend on :class:`InstallContext` ports,
not on a runtime bag. The system instance exposes
:meth:`~palm.system.runtime.base.BaseRuntime.plane_wire` (or any
:class:`PlaneWireSource`) to build that context once.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from palm.system.planes.hub import SystemPlanes


@runtime_checkable
class PlaneWireSource(Protocol):
    """
    Narrow surface for plane install (ISP).

    Implemented by the system instance (``BaseRuntime.plane_wire``).
    Install law must not dig a god bag for attributes.
    """

    def plane_wire(
        self,
        *,
        options: Mapping[str, Any] | None = None,
        on_host_session_error: Callable[[BaseException], None] | None = None,
        reuse_existing: bool = True,
        get_session_plane: Callable[[], Any | None] | None = None,
    ) -> InstallContext: ...


@dataclass
class InstallContext:
    """
    Collaborator ports + knobs for one hub install pass.

    Built via :meth:`from_source` or :meth:`PlaneWireSource.plane_wire`.
    Plane definitions use *ctx* only — never a full runtime bag.
    """

    options: Mapping[str, Any] = field(default_factory=dict)
    on_host_session_error: Callable[[BaseException], None] | None = None
    reuse_existing: bool = True
    orchestration: Any = None
    event: Any = None
    storage: Any = None
    instance_manager: Any = None
    get_job: Callable[[str], Any | None] | None = None
    submit_flow: Callable[[str, dict[str, Any]], Any] | None = None
    able: Callable[[], bool] | None = None

    @classmethod
    def from_source(
        cls,
        source: Any,
        options: Mapping[str, Any] | None = None,
        *,
        on_host_session_error: Callable[[BaseException], None] | None = None,
        reuse_existing: bool = True,
        get_session_plane: Callable[[], Any | None] | None = None,
    ) -> InstallContext:
        """
        Build ports from a *source* that exposes named collaborators.

        Prefer ``source.plane_wire(...)`` when the source implements
        :class:`PlaneWireSource`. This method is the shared extraction body.
        """
        from palm.system.planes.session.plane import make_get_job
        from palm.system.planes.work.plane import make_submit_flow

        orch = getattr(source, "orchestration", None)
        get_job_fn = getattr(source, "get_job", None)
        if not callable(get_job_fn):
            get_job_fn = None

        def _session_plane() -> Any | None:
            if get_session_plane is not None:
                return get_session_plane()
            return getattr(source, "session_plane", None)

        submit = getattr(source, "submit_flow", None)
        if not callable(submit):
            submit_flow = None
        else:

            def _submit(
                flow_id: str,
                metadata: dict[str, Any] | None = None,
                state: Any = None,
            ) -> Any:
                return submit(flow_id, metadata=metadata, state=state)

            submit_flow = make_submit_flow(
                submit=_submit,
                get_session_plane=_session_plane,
            )

        def _able() -> bool:
            return bool(getattr(source, "is_started", False))

        return cls(
            options=dict(options or {}),
            on_host_session_error=on_host_session_error,
            reuse_existing=reuse_existing,
            orchestration=orch,
            event=getattr(source, "event", None),
            storage=getattr(source, "storage", None),
            instance_manager=getattr(source, "instance_manager", None),
            get_job=make_get_job(get_job=get_job_fn, orchestration=orch),
            submit_flow=submit_flow,
            able=_able,
        )

    @classmethod
    def from_runtime(
        cls,
        runtime: Any,
        options: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ) -> InstallContext:
        """Compat alias for :meth:`from_source` (prefer ``runtime.plane_wire``)."""
        plane_wire = getattr(runtime, "plane_wire", None)
        if callable(plane_wire):
            return plane_wire(options=options, **kwargs)
        return cls.from_source(runtime, options, **kwargs)


# install(hub, ctx) -> plane instance (already put on hub)
PlaneInstallFn = Callable[["SystemPlanes", InstallContext], Any]


@dataclass(frozen=True)
class PlaneDefinition:
    """
    How one plane becomes a hub member.

    * ``name`` — canonical membership key (``wait``, ``session``, ``work``)
    * ``aliases`` — attr / seat ids (``wait_plane``, …)
    * ``order`` — lower installs first
    * ``install`` — construct, wire from *ctx*, ``hub.put``; return plane
    """

    name: str
    aliases: tuple[str, ...]
    order: int
    install: PlaneInstallFn
    after: tuple[str, ...] = ()

    def seat_id(self) -> str:
        for a in self.aliases:
            if a.endswith("_plane"):
                return a
        return f"{self.name}_plane"


__all__ = [
    "InstallContext",
    "PlaneDefinition",
    "PlaneInstallFn",
    "PlaneWireSource",
]
