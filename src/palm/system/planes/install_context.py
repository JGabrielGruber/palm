"""
InstallContext — snapshot of wire ports for one plane-install walk.

Built only from :class:`~palm.system.ports.wire.SystemWire` (or an explicit
constructor for tests). Never from ``getattr`` on an arbitrary bag.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from palm.system.ports.wire import SystemWire, WirePort


def make_get_job(
    *,
    direct: Callable[[str], Any | None] | None = None,
    orchestration: Any | None = None,
) -> Callable[[str], Any | None]:
    """Compose job lookup from explicit ports (no runtime bag)."""

    def resolve(job_id: str) -> Any | None:
        jid = str(job_id)
        if direct is not None:
            try:
                return direct(jid)
            except Exception:
                pass
        orch = orchestration
        if orch is None:
            return None
        jobs = getattr(orch, "jobs", None)
        if isinstance(jobs, dict):
            return jobs.get(jid)
        get = getattr(orch, "get_job", None)
        if callable(get):
            try:
                return get(jid)
            except Exception:
                return None
        return None

    return resolve


@dataclass
class InstallContext:
    """
    Collaborator ports for one :meth:`~SystemPlanes.install` pass.

    Plane definitions take only this context — never a system instance bag.
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
    def from_wire(
        cls,
        wire: WirePort,
        *,
        options: Mapping[str, Any] | None = None,
        on_host_session_error: Callable[[BaseException], None] | None = None,
        reuse_existing: bool = True,
        get_session_plane: Callable[[], Any | None],
    ) -> InstallContext:
        """
        Snapshot *wire* into install ports.

        *get_session_plane* is supplied by the hub (membership), not scraped
        from a bag. Work submit is composed here from ``wire.submit``.
        """
        from palm.system.planes.work.plane import make_submit_flow

        orch = wire.orchestration
        if orch is None and isinstance(wire, SystemWire):
            orch = wire.require_orchestration()
        elif orch is None:
            raise RuntimeError("system wire: orchestration not bound")

        direct = wire.get_job
        get_job = make_get_job(direct=direct, orchestration=orch)

        raw_submit = wire.submit
        if raw_submit is None and isinstance(wire, SystemWire):
            raw_submit = wire.require_submit()
        elif raw_submit is None:
            raise RuntimeError("system wire: submit not bound")

        def _submit(
            flow_id: str,
            metadata: dict[str, Any] | None = None,
            state: Any = None,
        ) -> Any:
            return raw_submit(flow_id, metadata=metadata, state=state)

        submit_flow = make_submit_flow(
            submit=_submit,
            get_session_plane=get_session_plane,
        )
        able = wire.able if wire.able is not None else (lambda: False)

        return cls(
            options=dict(options or {}),
            on_host_session_error=on_host_session_error,
            reuse_existing=reuse_existing,
            orchestration=orch,
            event=wire.event,
            storage=wire.storage,
            instance_manager=wire.instance_manager,
            get_job=get_job,
            submit_flow=submit_flow,
            able=able,
        )


__all__ = [
    "InstallContext",
    "make_get_job",
]
