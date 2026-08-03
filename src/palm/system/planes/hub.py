"""
SystemPlanes — living seat that **consumes** individual planes (0.61).

Same shape as :class:`~palm.system.supervisor.SystemSupervisor`:

| Supervisor | SystemPlanes |
|------------|--------------|
| Continuous services | Reactive planes |
| ``register`` · ``start`` · ``stop`` | ``put`` · ``install`` · ``detach`` |
| ``names`` · ``get`` · ``status`` | ``names`` · ``get`` · ``status`` |

Membership is **what the hub holds**, not a table elsewhere.
**Install policy** lives here (construct · wire collaborators · put).
Boot schedule only says *when*; the hub owns *what it means to have system planes*.
Vitality expands from the live hub.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


class SystemPlanes:
    """Lifecycle home for system planes on one SystemInstance."""

    def __init__(self) -> None:
        self._planes: dict[str, Any] = {}
        self._order: list[str] = []
        # attr / seat aliases → canonical name (e.g. wait_plane → wait)
        self._aliases: dict[str, str] = {}

    # ── membership ───────────────────────────────────────────────────────────

    def put(
        self,
        name: str,
        plane: Any,
        *,
        aliases: tuple[str, ...] | list[str] = (),
    ) -> None:
        """
        Consume a plane instance under *name*.

        Prefer :meth:`install` / :meth:`install_wait` etc. for the default set.
        Replaces an existing member of the same name (detaches the old one).
        """
        key = str(name or "").strip()
        if not key:
            raise ValueError("plane name required")
        if key in self._planes:
            old = self._planes[key]
            detach = getattr(old, "detach", None)
            if callable(detach):
                try:
                    detach()
                except Exception:
                    pass
        else:
            self._order.append(key)
        self._planes[key] = plane
        self._aliases[key] = key
        for alias in aliases:
            a = str(alias or "").strip()
            if a:
                self._aliases[a] = key

    def remove(self, name: str) -> bool:
        """Detach (if possible) and drop a member. Returns whether it existed."""
        key = self._resolve_key(name)
        if key is None or key not in self._planes:
            return False
        plane = self._planes.pop(key)
        self._order = [n for n in self._order if n != key]
        self._aliases = {a: k for a, k in self._aliases.items() if k != key}
        detach = getattr(plane, "detach", None)
        if callable(detach):
            try:
                detach()
            except Exception:
                pass
        return True

    def get(self, name: str) -> Any | None:
        """Plane by canonical name (``wait``) or alias (``wait_plane``)."""
        key = self._resolve_key(name)
        if key is None:
            return None
        return self._planes.get(key)

    def names(self) -> list[str]:
        """Canonical member names in put order."""
        return list(self._order)

    def seat_id(self, name: str) -> str:
        """Observation id for a member (prefer ``*_plane`` alias if registered)."""
        key = self._resolve_key(name)
        if key is None:
            return str(name or "")
        for alias, target in self._aliases.items():
            if target == key and alias.endswith("_plane"):
                return alias
        return f"{key}_plane" if not key.endswith("_plane") else key

    def seat_ids(self) -> list[str]:
        return [self.seat_id(n) for n in self._order]

    def detach(self, name: str | None = None) -> list[str]:
        """
        Detach one member by name, or all members (reverse put order).

        Clears the hub when detaching all.
        """
        if name is not None:
            key = self._resolve_key(name)
            if key is None or key not in self._planes:
                raise KeyError(f"unknown plane: {name}")
            self.remove(key)
            return [key]
        detached: list[str] = []
        for key in list(reversed(self._order)):
            if self.remove(key):
                detached.append(key)
        return detached

    def status(self) -> dict[str, Any]:
        """Public snapshot (raw sampling / doctor)."""
        planes: dict[str, Any] = {}
        for key in self._order:
            plane = self._planes.get(key)
            entry: dict[str, Any] = {
                "name": key,
                "seat_id": self.seat_id(key),
                "attached": plane is not None,
            }
            if plane is not None:
                entry["type"] = type(plane).__name__
            planes[key] = entry
        return {
            "plane_count": len(self._order),
            "registered": list(self._order),
            "seat_ids": self.seat_ids(),
            "planes": planes,
        }

    # ── install (hub owns policy) ────────────────────────────────────────────

    @classmethod
    def ensure_on(cls, runtime: Any) -> SystemPlanes:
        """Return the runtime's planes hub, creating and seating one if absent."""
        hub = get_system_planes(runtime)
        if hub is not None:
            return hub
        hub = cls()
        runtime._planes = hub
        return hub

    def install(
        self,
        runtime: Any,
        options: Mapping[str, Any] | None = None,
        *,
        on_host_session_error: Callable[[BaseException], None] | None = None,
    ) -> list[str]:
        """
        Construct, wire collaborators, and put the default system planes.

        Order: wait → session → work (session inspect may need wait).
        Returns canonical names installed.
        """
        opts = dict(options or {})
        self.install_wait(runtime)
        self.install_session(
            runtime,
            ensure_host=True,
            on_host_session_error=on_host_session_error,
        )
        self.install_work(runtime, opts)
        return list(self._order)

    def install_wait(self, runtime: Any) -> Any:
        """Construct wait plane, wire orchestration/event, put as ``wait``."""
        from palm.system.planes.wait.plane import WaitPlaneService

        orch = getattr(runtime, "orchestration", None)
        if orch is None:
            raise RuntimeError("runtime has no orchestration for wait plane")
        plane = WaitPlaneService()
        plane.attach(
            orchestration=orch,
            event=getattr(runtime, "event", None),
        )
        self.put("wait", plane, aliases=("wait_plane",))
        return plane

    def install_session(
        self,
        runtime: Any,
        *,
        ensure_host: bool = True,
        on_host_session_error: Callable[[BaseException], None] | None = None,
        reuse_existing: bool = True,
    ) -> Any:
        """
        Construct (or re-wire) session plane, put as ``session``.

        Uses storage + instance_manager + get_job + wait plane from runtime/hub.
        """
        from palm.system.planes.session.plane import (
            SessionPlaneService,
            session_get_job_from_runtime,
        )

        wait = self.get("wait")
        if wait is None:
            wait = getattr(runtime, "wait_plane", None)
        im = getattr(runtime, "instance_manager", None)
        get_job = session_get_job_from_runtime(runtime)

        existing = self.get("session")
        if existing is None:
            existing = getattr(runtime, "session_plane", None)
        if reuse_existing and isinstance(existing, SessionPlaneService):
            plane = existing
            plane.attach(
                instance_manager=im,
                get_job=get_job,
                wait_plane=wait,
            )
            if self.get("session") is not plane:
                self.put("session", plane, aliases=("session_plane",))
        else:
            storage = getattr(runtime, "storage", None)
            if storage is None:
                from palm.system.planes.session.plane import SessionPlaneError

                raise SessionPlaneError("runtime has no storage for session plane")
            plane = SessionPlaneService(storage=storage)
            plane.attach(
                instance_manager=im,
                get_job=get_job,
                wait_plane=wait,
            )
            self.put("session", plane, aliases=("session_plane",))

        if ensure_host:
            try:
                plane.ensure_host_session()
            except Exception as exc:
                if on_host_session_error is not None:
                    on_host_session_error(exc)
        return plane

    def install_work(
        self,
        runtime: Any,
        options: Mapping[str, Any] | None = None,
    ) -> Any:
        """Construct work plane, wire storage/submit/able/event, put as ``work``."""
        from palm.system.planes.work.plane import WorkPlaneService, default_submit_flow

        opts = dict(options or {})
        storage = getattr(runtime, "storage", None)
        if storage is None:
            raise RuntimeError("runtime has no storage for work plane")
        max_depth = int(opts.get("work_drain_max_depth", 8) or 8)
        batch_size = int(opts.get("work_drain_batch_size", 10) or 10)
        poll_interval = float(opts.get("work_drain_poll_interval", 1.0) or 1.0)
        plane = WorkPlaneService()
        plane.attach(
            storage=storage,
            submit_flow=default_submit_flow(runtime),
            able=lambda: bool(getattr(runtime, "is_started", False)),
            event=getattr(runtime, "event", None),
            max_depth=max_depth,
            batch_size=batch_size,
            poll_interval=poll_interval,
        )
        self.put("work", plane, aliases=("work_plane",))
        return plane

    def _resolve_key(self, name: str) -> str | None:
        raw = str(name or "").strip()
        if not raw:
            return None
        if raw in self._planes:
            return raw
        return self._aliases.get(raw)


def get_system_planes(runtime: Any) -> SystemPlanes | None:
    """Resolve hub from private ``_planes`` only (never via ``.planes`` property)."""
    hub = getattr(runtime, "_planes", None)
    if isinstance(hub, SystemPlanes):
        return hub
    return None


__all__ = [
    "SystemPlanes",
    "get_system_planes",
]
