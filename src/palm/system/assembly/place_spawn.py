"""Place spawn port — hands that can grow bodies for ENSURE place (0.63.14).

In-process ledger (0.63.11) marks ready. This port is the **structure hand** that
may later OS-spawn or workload-place. Floor default is in-process success so
embedded definition stays green. Fail closed when a registered strategy refuses.

Not Grove. Not product job path. Structure assemble / place-book only.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, runtime_checkable

PlaceSpawnState = Literal["ready", "failed", "gone"]


@dataclass(frozen=True, slots=True)
class PlaceSpawnResult:
    """Outcome of one ensure/release attempt against a place body."""

    state: PlaceSpawnState
    reason: str = ""
    handle: Any = None
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "reason": self.reason,
            "handle": self.handle,
            "payload": dict(self.payload),
        }


@runtime_checkable
class PlaceSpawnPort(Protocol):
    """Spawn / release place bodies for assembly effect intents."""

    def ensure(self, place_id: str, *, payload: Mapping[str, Any] | None = None) -> PlaceSpawnResult:
        """Ensure a place body exists; return ready or failed."""
        ...

    def release(self, place_id: str) -> PlaceSpawnResult:
        """Release a place body; return gone (or failed if stuck)."""
        ...


@dataclass
class InProcessPlaceSpawn:
    """Default hands: no OS body — ensure means present-in-ledger ready."""

    def ensure(
        self, place_id: str, *, payload: Mapping[str, Any] | None = None
    ) -> PlaceSpawnResult:
        key = str(place_id or "").strip()
        if not key:
            return PlaceSpawnResult(state="failed", reason="empty_place_id")
        return PlaceSpawnResult(state="ready", reason="in_process")

    def release(self, place_id: str) -> PlaceSpawnResult:
        return PlaceSpawnResult(state="gone", reason="in_process")


#: Callable strategy: place_id, payload → result
PlaceEnsureFn = Callable[[str, Mapping[str, Any]], PlaceSpawnResult]
PlaceReleaseFn = Callable[[str], PlaceSpawnResult]


@dataclass
class RegisteredPlaceSpawn:
    """Route place ids to registered ensure/release strategies (growth OS/workload).

    Unregistered places fall through to ``fallback`` (default in-process).
    Prefix routes (e.g. ``os:``) match when no exact id is registered.
    """

    ensures: dict[str, PlaceEnsureFn] = field(default_factory=dict)
    releases: dict[str, PlaceReleaseFn] = field(default_factory=dict)
    #: prefix → ensure fn (longest prefix wins among matches)
    prefix_ensures: dict[str, PlaceEnsureFn] = field(default_factory=dict)
    prefix_releases: dict[str, PlaceReleaseFn] = field(default_factory=dict)
    fallback: PlaceSpawnPort = field(default_factory=InProcessPlaceSpawn)
    handles: dict[str, Any] = field(default_factory=dict)

    def register(
        self,
        place_id: str,
        *,
        ensure: PlaceEnsureFn | None = None,
        release: PlaceReleaseFn | None = None,
    ) -> None:
        key = str(place_id or "").strip()
        if not key:
            return
        if ensure is not None:
            self.ensures[key] = ensure
        if release is not None:
            self.releases[key] = release

    def register_prefix(
        self,
        prefix: str,
        *,
        ensure: PlaceEnsureFn | None = None,
        release: PlaceReleaseFn | None = None,
    ) -> None:
        p = str(prefix or "")
        if not p:
            return
        if ensure is not None:
            self.prefix_ensures[p] = ensure
        if release is not None:
            self.prefix_releases[p] = release

    def _match_prefix(
        self, place_id: str, table: dict[str, Any]
    ) -> Any | None:
        best: str | None = None
        for prefix in table:
            if place_id.startswith(prefix) and (best is None or len(prefix) > len(best)):
                best = prefix
        return table.get(best) if best is not None else None

    def ensure(
        self, place_id: str, *, payload: Mapping[str, Any] | None = None
    ) -> PlaceSpawnResult:
        key = str(place_id or "").strip()
        if not key:
            return PlaceSpawnResult(state="failed", reason="empty_place_id")
        body = dict(payload or {})
        fn = self.ensures.get(key) or self._match_prefix(key, self.prefix_ensures)
        if fn is not None:
            result = fn(key, body)
            if result.state == "ready" and result.handle is not None:
                self.handles[key] = result.handle
            return result
        return self.fallback.ensure(key, payload=body)

    def release(self, place_id: str) -> PlaceSpawnResult:
        key = str(place_id or "").strip()
        if not key:
            return PlaceSpawnResult(state="gone", reason="empty_place_id")
        fn = self.releases.get(key) or self._match_prefix(key, self.prefix_releases)
        if fn is not None:
            result = fn(key)
            self.handles.pop(key, None)
            return result
        self.handles.pop(key, None)
        return self.fallback.release(key)


def fail_closed_os_ensure(
    place_id: str, payload: Mapping[str, Any]
) -> PlaceSpawnResult:
    """Refuse unless body handle or spawnable argv (illegal fake OS body).

    Prefer :class:`OsProcessRegistry` via :func:`os_prefix_spawn_port` for real
    process spawn. This pure helper still accepts pre-supplied handles.
    """
    handle = payload.get("handle") or payload.get("process") or payload.get("pid")
    if handle is not None:
        return PlaceSpawnResult(
            state="ready",
            reason="os_body_provided",
            handle=handle,
            payload=dict(payload),
        )
    if _argv_from_payload(payload):
        # Pure helper does not spawn — point callers at OsProcessRegistry.
        return PlaceSpawnResult(
            state="failed",
            reason="os_spawn_use_registry",
            payload={"place_id": place_id, **dict(payload)},
        )
    return PlaceSpawnResult(
        state="failed",
        reason="os_spawn_not_configured",
        payload={"place_id": place_id, **dict(payload)},
    )


def _argv_from_payload(payload: Mapping[str, Any]) -> list[str] | None:
    raw = payload.get("argv")
    if raw is not None:
        if isinstance(raw, str):
            import shlex

            parts = shlex.split(raw)
            return parts or None
        if isinstance(raw, (list, tuple)):
            parts = [str(x) for x in raw]
            return parts or None
    command = payload.get("command")
    if command:
        import shlex

        parts = shlex.split(str(command))
        return parts or None
    return None


@dataclass
class OsProcessRegistry:
    """Real OS process bodies for assembly place ensure (0.63.15).

    Structure assemble / place-book only — not the product job path. Tracks :class:`subprocess.Popen`
    by place id; release terminates the process group when possible.
    """

    processes: dict[str, Any] = field(default_factory=dict)

    def ensure(
        self, place_id: str, payload: Mapping[str, Any] | None = None
    ) -> PlaceSpawnResult:
        key = str(place_id or "").strip()
        if not key:
            return PlaceSpawnResult(state="failed", reason="empty_place_id")
        body = dict(payload or {})

        # Pre-supplied body (tests / external supervisor).
        handle = body.get("handle") or body.get("process") or body.get("pid")
        if handle is not None and not _argv_from_payload(body):
            return PlaceSpawnResult(
                state="ready",
                reason="os_body_provided",
                handle=handle,
                payload=body,
            )

        # Already running?
        existing = self.processes.get(key)
        if existing is not None:
            poll = getattr(existing, "poll", lambda: None)()
            if poll is None:
                pid = getattr(existing, "pid", None)
                return PlaceSpawnResult(
                    state="ready",
                    reason="os_process_already",
                    handle=pid,
                    payload={"place_id": key},
                )
            self.processes.pop(key, None)

        argv = _argv_from_payload(body)
        if not argv:
            return PlaceSpawnResult(
                state="failed",
                reason="os_spawn_not_configured",
                payload={"place_id": key, **body},
            )

        import subprocess

        try:
            proc = subprocess.Popen(
                argv,
                cwd=body.get("cwd") or None,
                env=body.get("env") if isinstance(body.get("env"), dict) else None,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except OSError as exc:
            return PlaceSpawnResult(
                state="failed",
                reason="os_spawn_error",
                payload={"place_id": key, "error": str(exc), **body},
            )

        self.processes[key] = proc
        return PlaceSpawnResult(
            state="ready",
            reason="os_process_spawned",
            handle=proc.pid,
            payload={"place_id": key, "pid": proc.pid, "argv": list(argv)},
        )

    def release(self, place_id: str) -> PlaceSpawnResult:
        key = str(place_id or "").strip()
        if not key:
            return PlaceSpawnResult(state="gone", reason="empty_place_id")
        proc = self.processes.pop(key, None)
        if proc is None:
            return PlaceSpawnResult(state="gone", reason="os_not_tracked")
        poll = getattr(proc, "poll", lambda: 0)()
        if poll is None:
            import os
            import signal
            import subprocess

            pid = getattr(proc, "pid", None)
            try:
                if pid is not None:
                    os.killpg(pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError, OSError):
                try:
                    proc.terminate()
                except OSError:
                    pass
            try:
                proc.wait(timeout=2.0)
            except (subprocess.TimeoutExpired, OSError):
                try:
                    if pid is not None:
                        os.killpg(pid, signal.SIGKILL)
                    else:
                        proc.kill()
                except (ProcessLookupError, PermissionError, OSError):
                    pass
                try:
                    proc.wait(timeout=1.0)
                except (subprocess.TimeoutExpired, OSError):
                    pass
        return PlaceSpawnResult(
            state="gone",
            reason="os_process_released",
            handle=getattr(proc, "pid", None),
        )


def os_prefix_spawn_port(
    registry: OsProcessRegistry | None = None,
) -> RegisteredPlaceSpawn:
    """Port where ``os:`` places spawn real processes when argv/command given.

    Without argv/handle: fail closed (``os_spawn_not_configured``).
    """
    reg = registry if registry is not None else OsProcessRegistry()
    port = RegisteredPlaceSpawn()
    port.register_prefix(
        "os:",
        ensure=lambda pid, payload: reg.ensure(pid, payload),
        release=lambda pid: reg.release(pid),
    )
    # Keep registry reachable for tests / shutdown.
    port.handles["__os_registry__"] = reg  # type: ignore[index]
    return port


__all__ = [
    "InProcessPlaceSpawn",
    "OsProcessRegistry",
    "PlaceEnsureFn",
    "PlaceReleaseFn",
    "PlaceSpawnPort",
    "PlaceSpawnResult",
    "PlaceSpawnState",
    "RegisteredPlaceSpawn",
    "fail_closed_os_ensure",
    "os_prefix_spawn_port",
]
