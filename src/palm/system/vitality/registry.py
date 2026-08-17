"""
VitalityRegistry — capability catalog for living-kernel eyes (0.61.2).

Eyes grow by registering capabilities, not by editing BaseRuntime forever.
Enablement is dynamic (composition / mode / maturity); ids are intentional.

This is **not** the seat probe catalog (:mod:`palm.system.vitality.probe`).
Probes discover attachments; this registry catalogs observe/tool capabilities.
"""

from __future__ import annotations

import threading
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from palm.system.vitality.capability import VitalityCapability
from palm.system.vitality.schema import MATURITY_INTENTION


@dataclass
class VitalityRegistry:
    """Thread-safe registry of :class:`VitalityCapability` entries.

    Enablement is tracked separately from registration so composition can
    disable expensive or intention capabilities without unregistering them.
    """

    _caps: dict[str, VitalityCapability] = field(default_factory=dict)
    _enabled: dict[str, bool] = field(default_factory=dict)
    _lock: threading.RLock = field(default_factory=threading.RLock, repr=False)

    def register(
        self,
        capability: VitalityCapability,
        *,
        replace: bool = True,
        enabled: bool | None = None,
    ) -> None:
        """Add or replace a capability.

        Parameters
        ----------
        enabled:
            Explicit enable flag. When omitted, uses
            ``default_enabled`` only if maturity is installed; intention
            defaults to disabled unless *enabled* is True.
        """
        if not isinstance(capability, VitalityCapability):
            raise TypeError("capability must be VitalityCapability")
        with self._lock:
            if not replace and capability.id in self._caps:
                raise KeyError(f"capability already registered: {capability.id}")
            self._caps[capability.id] = capability
            if enabled is not None:
                self._enabled[capability.id] = bool(enabled)
            else:
                if capability.maturity == MATURITY_INTENTION:
                    self._enabled[capability.id] = False
                else:
                    self._enabled[capability.id] = bool(capability.default_enabled)

    def unregister(self, capability_id: str) -> bool:
        key = str(capability_id or "").strip()
        with self._lock:
            self._enabled.pop(key, None)
            return self._caps.pop(key, None) is not None

    def get(self, capability_id: str) -> VitalityCapability | None:
        with self._lock:
            return self._caps.get(str(capability_id or "").strip())

    def contains(self, capability_id: str) -> bool:
        with self._lock:
            return str(capability_id or "").strip() in self._caps

    def enable(self, capability_id: str) -> None:
        key = str(capability_id or "").strip()
        with self._lock:
            if key not in self._caps:
                raise KeyError(f"unknown capability: {key}")
            self._enabled[key] = True

    def disable(self, capability_id: str) -> None:
        key = str(capability_id or "").strip()
        with self._lock:
            if key not in self._caps:
                raise KeyError(f"unknown capability: {key}")
            self._enabled[key] = False

    def is_enabled(self, capability_id: str) -> bool:
        key = str(capability_id or "").strip()
        with self._lock:
            if key not in self._caps:
                return False
            return bool(self._enabled.get(key, False))

    def list(self) -> list[VitalityCapability]:
        with self._lock:
            items = list(self._caps.values())
        return sorted(items, key=lambda c: (c.order, c.id))

    def enabled(self) -> list[VitalityCapability]:
        with self._lock:
            items = [
                c
                for cid, c in self._caps.items()
                if self._enabled.get(cid, False)
            ]
        return sorted(items, key=lambda c: (c.order, c.id))

    def ids(self) -> list[str]:
        return [c.id for c in self.list()]

    def enabled_ids(self) -> list[str]:
        return [c.id for c in self.enabled()]

    def catalog(self) -> list[dict[str, Any]]:
        """Inspect-friendly catalog rows (no sampling)."""
        rows: list[dict[str, Any]] = []
        with self._lock:
            for cap in sorted(self._caps.values(), key=lambda c: (c.order, c.id)):
                rows.append(
                    {
                        "id": cap.id,
                        "role": cap.role,
                        "maturity": cap.maturity,
                        "enabled": bool(self._enabled.get(cap.id, False)),
                        "default_enabled": cap.default_enabled,
                        "cost": cap.cost,
                        "description": cap.description,
                        "tags": list(cap.tags),
                        "order": cap.order,
                    }
                )
        return rows

    def extend(
        self,
        capabilities: Iterable[VitalityCapability],
        *,
        replace: bool = True,
    ) -> VitalityRegistry:
        for cap in capabilities:
            self.register(cap, replace=replace)
        return self

    def clone(self) -> VitalityRegistry:
        out = VitalityRegistry()
        with self._lock:
            out._caps = dict(self._caps)
            out._enabled = dict(self._enabled)
        return out

    def merge(self, other: VitalityRegistry, *, replace: bool = True) -> VitalityRegistry:
        out = self.clone()
        for cap in other.list():
            out.register(
                cap,
                replace=replace,
                enabled=other.is_enabled(cap.id),
            )
        return out

    def __len__(self) -> int:
        with self._lock:
            return len(self._caps)

    def __contains__(self, capability_id: object) -> bool:
        if not isinstance(capability_id, str):
            return False
        return self.contains(capability_id)


__all__ = [
    "VitalityRegistry",
]
