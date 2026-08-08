"""Place spawn port — hands that can grow bodies for ENSURE place (0.63.14).

In-process ledger (0.63.11) marks ready. This port is the **structure hand** that
may later OS-spawn or workload-place. Floor default is in-process success so
embedded DNA stays green. Fail closed when a registered strategy refuses.

Not Grove. Not product job path. Assembly household only.
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
    """Honest OS pretender purge: refuse unless payload supplies a body handle.

    Real process spawn is growth; this wall names the hand and fails closed
    when no body is provided — no soft-ready place.
    """
    handle = payload.get("handle") or payload.get("process") or payload.get("pid")
    if handle is not None:
        return PlaceSpawnResult(
            state="ready",
            reason="os_body_provided",
            handle=handle,
            payload=dict(payload),
        )
    return PlaceSpawnResult(
        state="failed",
        reason="os_spawn_not_configured",
        payload={"place_id": place_id, **dict(payload)},
    )


def os_prefix_spawn_port() -> RegisteredPlaceSpawn:
    """Port where ``os:`` places fail closed unless body payload is supplied."""
    port = RegisteredPlaceSpawn()
    port.register_prefix("os:", ensure=fail_closed_os_ensure)
    return port


__all__ = [
    "InProcessPlaceSpawn",
    "PlaceEnsureFn",
    "PlaceReleaseFn",
    "PlaceSpawnPort",
    "PlaceSpawnResult",
    "PlaceSpawnState",
    "RegisteredPlaceSpawn",
    "fail_closed_os_ensure",
    "os_prefix_spawn_port",
]
