"""
Probe catalog — extensible discovery seeds for seat walk (0.61.1).

A **probe** is one intentional way to look for a seat on a live instance.
Probes are *not* a closed product menu: composition attaches seats; probes
only know *how* to observe known attach points and custom extensions.

This is **not** :class:`VitalityRegistry` (capability fold — 0.61.2).
Probes answer: *what seats might be on this graph?*
The registry answers: *which observe/tool capabilities are enabled?*
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

from palm.system.vitality.report import SeatReport

# instance -> attached seat object or None
SeatResolver = Callable[[Any], Any | None]
# (instance, seat_object) -> SeatReport
SeatReporter = Callable[[Any, Any], SeatReport]
# instance alone when no object resolution (e.g. process log)
InstanceReporter = Callable[[Any], SeatReport]

AbsentPolicy = Literal["report", "omit"]


@dataclass(frozen=True)
class SeatProbe:
    """One discovery seed for the vitality walk.

    Parameters
    ----------
    seat_id:
        Stable attachment id (e.g. ``wait_plane``, ``supervisor.outbox``).
    kind:
        Seat kind (plane · supervisor · port · …).
    resolve:
        Map instance → attached object, or ``None`` when not present.
        When ``resolve`` is ``None``, :attr:`report_instance` must be set
        (instance-level seats such as process system log).
    report:
        Build a report from ``(instance, seat)`` when the seat is present.
        If omitted, the walk prefers native ``seat_report()`` then fails
        closed to a degraded presence-only report.
    report_instance:
        Build a report from the instance alone (no resolved object).
    when_absent:
        ``report`` → emit honest ``absent``; ``omit`` → skip silently
        (use for optional experimental probes).
    order:
        Lower runs earlier. Same order keeps registration order.
    tags:
        Free labels for filtering (e.g. ``core``, ``optional``, ``process``).
    description:
        Human note for docs / inspect later.
    """

    seat_id: str
    kind: str
    resolve: SeatResolver | None = None
    report: SeatReporter | None = None
    report_instance: InstanceReporter | None = None
    when_absent: AbsentPolicy = "report"
    order: int = 100
    tags: tuple[str, ...] = ()
    description: str = ""

    def __post_init__(self) -> None:
        sid = str(self.seat_id or "").strip()
        if not sid:
            raise ValueError("SeatProbe.seat_id required")
        object.__setattr__(self, "seat_id", sid)
        kind = str(self.kind or "").strip() or "other"
        object.__setattr__(self, "kind", kind)
        if self.resolve is None and self.report_instance is None:
            raise ValueError(
                f"SeatProbe {sid!r} needs resolve and/or report_instance"
            )


@dataclass
class ProbeCatalog:
    """Thread-safe registry of :class:`SeatProbe` discovery seeds.

    Default Palm seeds live in :func:`default_probe_catalog`. Callers may
    clone, extend, or replace for tests and future composition profiles.
    """

    _probes: dict[str, SeatProbe] = field(default_factory=dict)
    _order_seq: int = 0
    _lock: threading.RLock = field(default_factory=threading.RLock, repr=False)

    def register(self, probe: SeatProbe, *, replace: bool = True) -> None:
        """Add or replace a probe by ``seat_id``."""
        if not isinstance(probe, SeatProbe):
            raise TypeError("probe must be SeatProbe")
        with self._lock:
            if not replace and probe.seat_id in self._probes:
                raise KeyError(f"probe already registered: {probe.seat_id}")
            self._probes[probe.seat_id] = probe
            self._order_seq += 1

    def unregister(self, seat_id: str) -> bool:
        with self._lock:
            return self._probes.pop(str(seat_id or "").strip(), None) is not None

    def get(self, seat_id: str) -> SeatProbe | None:
        with self._lock:
            return self._probes.get(str(seat_id or "").strip())

    def contains(self, seat_id: str) -> bool:
        with self._lock:
            return str(seat_id or "").strip() in self._probes

    def list(self) -> list[SeatProbe]:
        """Probes sorted by ``order``, then seat_id."""
        with self._lock:
            items = list(self._probes.values())
        return sorted(items, key=lambda p: (p.order, p.seat_id))

    def seat_ids(self) -> list[str]:
        return [p.seat_id for p in self.list()]

    def with_tag(self, tag: str) -> list[SeatProbe]:
        t = str(tag or "").strip()
        return [p for p in self.list() if t in p.tags]

    def extend(self, probes: Iterable[SeatProbe], *, replace: bool = True) -> ProbeCatalog:
        """Register many probes; return self for chaining."""
        for p in probes:
            self.register(p, replace=replace)
        return self

    def clone(self) -> ProbeCatalog:
        """Deep-enough copy: new catalog, same probe objects (frozen)."""
        out = ProbeCatalog()
        with self._lock:
            out._probes = dict(self._probes)
            out._order_seq = self._order_seq
        return out

    def merge(self, other: ProbeCatalog, *, replace: bool = True) -> ProbeCatalog:
        """Return a new catalog with *other* layered on top of *self*."""
        out = self.clone()
        for p in other.list():
            out.register(p, replace=replace)
        return out

    def __len__(self) -> int:
        with self._lock:
            return len(self._probes)

    def __contains__(self, seat_id: object) -> bool:
        if not isinstance(seat_id, str):
            return False
        return self.contains(seat_id)


def attr_resolver(*names: str) -> SeatResolver:
    """Resolve the first non-None attribute among *names* on the instance."""

    attrs = tuple(str(n) for n in names if str(n).strip())

    def _resolve(instance: Any) -> Any | None:
        for name in attrs:
            if hasattr(instance, name):
                value = getattr(instance, name)
                if value is not None:
                    return value
        return None

    return _resolve


def private_attr_resolver(*names: str) -> SeatResolver:
    """Resolve private/public attrs (e.g. ``_last_boot_walk`` / property)."""

    attrs = tuple(str(n) for n in names if str(n).strip())

    def _resolve(instance: Any) -> Any | None:
        for name in attrs:
            value = getattr(instance, name, None)
            if value is not None:
                return value
        return None

    return _resolve


def first_resolver(*resolvers: SeatResolver) -> SeatResolver:
    """Resolve with the first resolver that returns non-None."""

    fns = tuple(resolvers)

    def _resolve(instance: Any) -> Any | None:
        for fn in fns:
            value = fn(instance)
            if value is not None:
                return value
        return None

    return _resolve


def fixed_probes(probes: Sequence[SeatProbe]) -> ProbeCatalog:
    """Build a catalog from an explicit sequence."""
    return ProbeCatalog().extend(probes)


__all__ = [
    "AbsentPolicy",
    "InstanceReporter",
    "ProbeCatalog",
    "SeatProbe",
    "SeatReporter",
    "SeatResolver",
    "attr_resolver",
    "first_resolver",
    "fixed_probes",
    "private_attr_resolver",
]
