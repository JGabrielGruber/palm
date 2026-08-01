"""Supervised continuous service contract (0.60.1)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SystemService(Protocol):
    """One continuous duty the supervisor may start and stop."""

    @property
    def name(self) -> str:
        """Stable service id (e.g. ``work_drain``, ``outbox``, ``inbound``)."""
        ...

    def start(self) -> None:
        """Begin continuous run. Idempotent when already running."""
        ...

    def stop(self) -> None:
        """End continuous run. Idempotent when already stopped."""
        ...

    def status(self) -> dict[str, Any]:
        """Doctor-oriented snapshot for this service."""
        ...


class CallableSystemService:
    """Adapter: wrap start/stop/status callables as a :class:`SystemService`."""

    def __init__(
        self,
        name: str,
        *,
        start: Callable[[], None] | None = None,
        stop: Callable[[], None] | None = None,
        status: Callable[[], dict[str, Any]] | None = None,
    ) -> None:
        self._name = str(name or "").strip()
        if not self._name:
            raise ValueError("system service name required")
        self._start = start
        self._stop = stop
        self._status = status
        self._running = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_running(self) -> bool:
        return self._running

    def start(self) -> None:
        if self._running:
            return
        if self._start is not None:
            self._start()
        self._running = True

    def stop(self) -> None:
        if not self._running:
            return
        if self._stop is not None:
            self._stop()
        self._running = False

    def status(self) -> dict[str, Any]:
        base: dict[str, Any] = {
            "name": self._name,
            "running": self._running,
        }
        if self._status is not None:
            extra = self._status()
            if isinstance(extra, dict):
                base.update(extra)
                base["name"] = self._name
                base["running"] = self._running
        return base


__all__ = ["CallableSystemService", "SystemService"]
