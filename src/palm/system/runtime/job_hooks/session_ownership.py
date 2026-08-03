"""Attach process instances to the system session plane (0.58.4).

Runs after instance persistence creates the durable record. Does not resume
jobs — only labels ownership via :meth:`SessionPlaneService.attach_instance`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from palm.core.orchestration.hooks import JobHookAdapter

if TYPE_CHECKING:
    from palm.core.orchestration.engine import OrchestrationEngine
    from palm.core.orchestration.job import Job
    from palm.system.subsystems.planes.session.plane import SessionPlaneService


class SessionOwnershipHook(JobHookAdapter):
    """When job metadata carries ``session_id``, attach ``instance_id`` on the plane.

    ``get_plane`` is lazy so the hook can be registered before the session plane
    is constructed on :meth:`~palm.system.runtime.base.BaseRuntime.start`.
    """

    def __init__(
        self,
        get_plane: Callable[[], SessionPlaneService | None] | None = None,
    ) -> None:
        self._get_plane = get_plane

    def bind_plane_getter(
        self, get_plane: Callable[[], SessionPlaneService | None]
    ) -> None:
        self._get_plane = get_plane

    def on_job_submitted(self, engine: OrchestrationEngine, job: Job) -> None:
        self._maybe_attach(job)

    def on_job_status_changed(
        self,
        engine: OrchestrationEngine,
        job: Job,
        result: Any = None,
    ) -> None:
        # Re-attach is idempotent; covers create-on-first-status if submit missed.
        self._maybe_attach(job)

    def _maybe_attach(self, job: Job) -> None:
        if self._get_plane is None:
            return
        plane = self._get_plane()
        if plane is None:
            return
        meta = job.metadata or {}
        sid_raw = meta.get("session_id")
        iid_raw = meta.get("instance_id")
        if sid_raw is None or iid_raw is None:
            return
        sid = str(sid_raw).strip()
        iid = str(iid_raw).strip()
        if not sid or not iid:
            return
        try:
            if plane.get(sid) is None:
                # Open under the known id so attach does not invent a different subject.
                plane.open(session_id=sid, metadata={"via": "job_path"})
            plane.attach_instance(sid, iid)
        except Exception:
            # Ownership is best-effort for job path; never break orchestration.
            return


__all__ = ["SessionOwnershipHook"]
