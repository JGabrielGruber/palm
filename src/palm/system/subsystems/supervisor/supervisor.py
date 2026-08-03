"""SystemSupervisor — register and run continuous system services (0.60.1).

Empty registry is valid: boot wires the seat; later slices register services.
Install walks :class:`~palm.system.subsystems.supervisor.definition.ContinuousServiceDefinition`
at the edge (CS-006).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from palm.system.subsystems.supervisor.definition import (
    DEFAULT_CONTINUOUS_DEFINITIONS,
    ContinuousServiceDefinition,
    ContinuousWireContext,
)
from palm.system.subsystems.supervisor.service import SystemService


class SystemSupervisor:
    """
    Continuous-services subsystem — lifecycle home on one shell.

    Satisfies :class:`~palm.system.subsystems.protocol.Subsystem`
    (``names`` / ``get`` / ``status``).
    """

    def __init__(
        self,
        definitions: Sequence[ContinuousServiceDefinition] | None = None,
    ) -> None:
        self._services: dict[str, SystemService] = {}
        self._running: set[str] = set()
        self._definitions: tuple[ContinuousServiceDefinition, ...] = (
            tuple(definitions)
            if definitions is not None
            else DEFAULT_CONTINUOUS_DEFINITIONS
        )

    def register(self, service: SystemService) -> None:
        """Add or replace a service by name. Does not auto-start."""
        name = str(getattr(service, "name", "") or "").strip()
        if not name:
            raise ValueError("system service name required")
        if name in self._running:
            # Replace while running: stop old first.
            old = self._services.get(name)
            if old is not None:
                try:
                    old.stop()
                finally:
                    self._running.discard(name)
        self._services[name] = service

    def unregister(self, name: str) -> bool:
        """Stop (if running) and remove. Returns whether a service was removed."""
        key = str(name or "").strip()
        if key not in self._services:
            return False
        if key in self._running:
            try:
                self._services[key].stop()
            finally:
                self._running.discard(key)
        del self._services[key]
        return True

    def get(self, name: str) -> SystemService | None:
        return self._services.get(str(name or "").strip())

    def names(self) -> list[str]:
        return sorted(self._services)

    def definitions(self) -> tuple[ContinuousServiceDefinition, ...]:
        """Install catalog this supervisor walks (not live membership)."""
        return self._definitions

    def install(
        self,
        install: Any | None = None,
        options: Mapping[str, Any] | None = None,
        *,
        ctx: ContinuousWireContext | None = None,
    ) -> list[str]:
        """
        Walk continuous definitions; each may ``register`` a service.

        *install* is :class:`~palm.system.interfaces.install.InstallInterface` (or a
        ContinuousWireContext). Prefer the system install seat — not a bag.

        Returns names registered after the walk.
        """
        install_ctx = ctx
        if install_ctx is None:
            if install is None:
                raise ValueError("install interface or ContinuousWireContext required")
            if isinstance(install, ContinuousWireContext):
                install_ctx = install
            else:
                from palm.system.interfaces.install import continuous_context_from_install

                install_ctx = continuous_context_from_install(install, options)
        for defn in sorted(self._definitions, key=lambda d: (d.order, d.name)):
            defn.register(self, install_ctx)
        return list(self.names())

    def start(self, name: str | None = None) -> list[str]:
        """Start one service by name, or all registered. Returns started names."""
        if name is not None:
            key = str(name).strip()
            if key not in self._services:
                raise KeyError(f"unknown system service: {key}")
            return self._start_one(key)
        started: list[str] = []
        for key in sorted(self._services):
            started.extend(self._start_one(key))
        return started

    def stop(self, name: str | None = None) -> list[str]:
        """Stop one service by name, or all running (reverse name order)."""
        if name is not None:
            key = str(name).strip()
            if key not in self._services:
                raise KeyError(f"unknown system service: {key}")
            return self._stop_one(key)
        stopped: list[str] = []
        for key in sorted(self._running, reverse=True):
            stopped.extend(self._stop_one(key))
        return stopped

    def status(self) -> dict[str, Any]:
        """Doctor-oriented snapshot of the supervisor and each service."""
        services: dict[str, Any] = {}
        for key in sorted(self._services):
            svc = self._services[key]
            try:
                snap = dict(svc.status() or {})
            except Exception as exc:
                snap = {
                    "name": key,
                    "running": key in self._running,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            snap.setdefault("name", key)
            snap.setdefault("running", key in self._running)
            services[key] = snap
        return {
            "service_count": len(self._services),
            "running_count": len(self._running),
            "running": sorted(self._running),
            "registered": sorted(self._services),
            "services": services,
        }

    def _start_one(self, key: str) -> list[str]:
        if key in self._running:
            return []
        self._services[key].start()
        self._running.add(key)
        return [key]

    def _stop_one(self, key: str) -> list[str]:
        if key not in self._running:
            return []
        try:
            self._services[key].stop()
        finally:
            self._running.discard(key)
        return [key]


__all__ = ["SystemSupervisor"]
