"""SystemSupervisor — register and run continuous system services (0.60.1).

Empty registry is valid: boot wires the seat; later slices register services.
"""

from __future__ import annotations

from typing import Any

from palm.system.supervisor.service import SystemService


class SystemSupervisor:
    """Lifecycle home for continuous services on one system instance."""

    def __init__(self) -> None:
        self._services: dict[str, SystemService] = {}
        self._running: set[str] = set()

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

    def seat_report(self) -> dict[str, Any]:
        """Native vitality seat report (0.61.1+) — supervisor physiology."""
        from palm.system.vitality.schema import (
            KIND_SUPERVISOR,
            LINEAGE_NATIVE,
            SEAT_REPORT_SCHEMA,
            SEAT_SUPERVISOR,
            STATE_OK,
        )

        return {
            "schema": SEAT_REPORT_SCHEMA,
            "seat_id": SEAT_SUPERVISOR,
            "kind": KIND_SUPERVISOR,
            "present": True,
            "state": STATE_OK,
            "load": {
                "service_count": len(self._services),
                "running_count": len(self._running),
                "running": sorted(self._running),
                "registered": sorted(self._services),
            },
            "notes": [],
            "lineage": LINEAGE_NATIVE,
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
