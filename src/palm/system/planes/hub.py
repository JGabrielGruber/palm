"""
SystemPlanes — living seat that **consumes** individual planes (0.61).

Same shape as :class:`~palm.system.supervisor.SystemSupervisor`:

| Supervisor | SystemPlanes |
|------------|--------------|
| Continuous services | Reactive planes |
| ``register`` · ``start`` · ``stop`` | ``put`` · ``detach`` |
| ``names`` · ``get`` · ``status`` | ``names`` · ``get`` · ``status`` |

Membership is **what the hub holds**, not a table elsewhere.
Boot constructs each plane and ``put``s it. Vitality expands from the hub.
"""

from __future__ import annotations

from typing import Any


class SystemPlanes:
    """Lifecycle home for system planes on one SystemInstance."""

    def __init__(self) -> None:
        self._planes: dict[str, Any] = {}
        self._order: list[str] = []
        # attr / seat aliases → canonical name (e.g. wait_plane → wait)
        self._aliases: dict[str, str] = {}

    def put(
        self,
        name: str,
        plane: Any,
        *,
        aliases: tuple[str, ...] | list[str] = (),
    ) -> None:
        """
        Consume a plane instance under *name*.

        Does not construct or attach the plane to the runtime — caller does that.
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
