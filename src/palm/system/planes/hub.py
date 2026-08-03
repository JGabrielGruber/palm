"""
SystemPlanes — living seat that **consumes** individual planes (0.61).

Same shape as :class:`~palm.system.supervisor.SystemSupervisor`:

| Supervisor | SystemPlanes |
|------------|--------------|
| Continuous services | Reactive planes |
| ``register`` · ``start`` · ``stop`` | ``put`` · ``install`` · ``detach`` |
| ``names`` · ``get`` · ``status`` | ``names`` · ``get`` · ``status`` |

Membership is **what the hub holds**.
**Install law** lives on :class:`~palm.system.planes.definition.PlaneDefinition`
at the edge (SD-015 / registry extension). The hub only **walks** definitions,
orders them, and ``put``s results.

Boot schedule only says *when* (``ensure_on`` + ``install``).
Vitality expands from the live hub.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from palm.system.planes.catalog import (
    DEFAULT_PLANE_DEFINITIONS,
    definition_by_name,
)
from palm.system.planes.definition import InstallContext, PlaneDefinition


class SystemPlanes:
    """Lifecycle home for system planes on one SystemInstance."""

    def __init__(
        self,
        definitions: Sequence[PlaneDefinition] | None = None,
    ) -> None:
        self._planes: dict[str, Any] = {}
        self._order: list[str] = []
        # attr / seat aliases → canonical name (e.g. wait_plane → wait)
        self._aliases: dict[str, str] = {}
        defs = (
            tuple(definitions)
            if definitions is not None
            else DEFAULT_PLANE_DEFINITIONS
        )
        self._definitions: tuple[PlaneDefinition, ...] = defs
        self._definitions_by_name: dict[str, PlaneDefinition] = {
            d.name: d for d in defs
        }

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

        Prefer :meth:`install` / :meth:`install_named` (definition at edge).
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

    def definitions(self) -> tuple[PlaneDefinition, ...]:
        """Install catalog this hub walks (not live membership)."""
        return self._definitions

    def seat_id(self, name: str) -> str:
        """Observation id for a member (prefer ``*_plane`` alias if registered)."""
        key = self._resolve_key(name)
        if key is None:
            return str(name or "")
        defn = self._definitions_by_name.get(key)
        if defn is not None:
            return defn.seat_id()
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
            "definition_names": [d.name for d in self._sorted_definitions()],
            "planes": planes,
        }

    # ── install (walk definitions) ───────────────────────────────────────────

    @classmethod
    def ensure_on(
        cls,
        runtime: Any,
        definitions: Sequence[PlaneDefinition] | None = None,
    ) -> SystemPlanes:
        """Return the runtime's planes hub, creating and seating one if absent."""
        hub = get_system_planes(runtime)
        if hub is not None:
            return hub
        hub = cls(definitions=definitions)
        runtime._planes = hub
        return hub

    def install(
        self,
        runtime: Any,
        options: Mapping[str, Any] | None = None,
        *,
        on_host_session_error: Callable[[BaseException], None] | None = None,
        reuse_existing: bool = True,
        ctx: InstallContext | None = None,
    ) -> list[str]:
        """
        Walk registered :class:`PlaneDefinition`\\s in order; each installs itself.

        Ports come from *ctx* (or :meth:`InstallContext.from_runtime`).
        Returns canonical names installed (live membership after walk).
        """
        wire = ctx or self._wire_from(
            runtime,
            options,
            on_host_session_error=on_host_session_error,
            reuse_existing=reuse_existing,
        )
        for defn in self._sorted_definitions():
            defn.install(self, wire)
        return list(self._order)

    def install_named(
        self,
        name: str,
        runtime: Any,
        options: Mapping[str, Any] | None = None,
        *,
        on_host_session_error: Callable[[BaseException], None] | None = None,
        reuse_existing: bool = True,
        ctx: InstallContext | None = None,
    ) -> Any:
        """Install one plane by name or alias via its edge definition."""
        defn = self._lookup_definition(name)
        if defn is None:
            raise KeyError(f"unknown plane definition: {name}")
        wire = ctx or self._wire_from(
            runtime,
            options,
            on_host_session_error=on_host_session_error,
            reuse_existing=reuse_existing,
        )
        return defn.install(self, wire)

    def _wire_from(
        self,
        source: Any,
        options: Mapping[str, Any] | None,
        *,
        on_host_session_error: Callable[[BaseException], None] | None,
        reuse_existing: bool,
    ) -> InstallContext:
        """Prefer :meth:`PlaneWireSource.plane_wire`; else :meth:`InstallContext.from_source`."""
        kwargs = {
            "options": options,
            "on_host_session_error": on_host_session_error,
            "reuse_existing": reuse_existing,
            "get_session_plane": lambda: self.get("session"),
        }
        plane_wire = getattr(source, "plane_wire", None)
        if callable(plane_wire):
            return plane_wire(**kwargs)
        return InstallContext.from_source(source, **kwargs)

    # Thin aliases for bind helpers / tests (delegate to definitions)
    def install_wait(self, runtime: Any, *, ctx: InstallContext | None = None) -> Any:
        return self.install_named("wait", runtime, ctx=ctx)

    def install_session(
        self,
        runtime: Any,
        *,
        ensure_host: bool = True,
        on_host_session_error: Callable[[BaseException], None] | None = None,
        reuse_existing: bool = True,
        ctx: InstallContext | None = None,
    ) -> Any:
        # ensure_host is always done by session definition when install runs;
        # swallow path uses on_host_session_error (None → silent).
        _ = ensure_host
        return self.install_named(
            "session",
            runtime,
            on_host_session_error=on_host_session_error,
            reuse_existing=reuse_existing,
            ctx=ctx,
        )

    def install_work(
        self,
        runtime: Any,
        options: Mapping[str, Any] | None = None,
        *,
        ctx: InstallContext | None = None,
    ) -> Any:
        return self.install_named("work", runtime, options, ctx=ctx)

    def _sorted_definitions(self) -> list[PlaneDefinition]:
        return sorted(self._definitions, key=lambda d: (d.order, d.name))

    def _lookup_definition(self, name: str) -> PlaneDefinition | None:
        key = str(name or "").strip()
        if key in self._definitions_by_name:
            return self._definitions_by_name[key]
        found = definition_by_name(key, self._definitions)
        return found

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
