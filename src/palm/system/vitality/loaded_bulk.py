"""
Loaded bulk — light structural size map of attached seats (0.61.9).

**Law (ADR-030 / VISION-0.61):**
  - Observation only — no start/continue, no second write path.
  - **Visibility, not shame** — large modules may be valid; we show bulk.
  - Only **loaded** / **attached** things — not a full package tree scan
    (that is genome dogfood later).
  - Cheap: resolve seats + type/module stats + optional LOC of host files.

**Not law:** god-module auto-condemn, health grades, or repo-wide LOC as
vitality truth.
"""

from __future__ import annotations

import sys
from collections.abc import Iterable
from datetime import UTC, datetime
from types import ModuleType
from typing import Any

from palm.system.vitality.capability import CapabilityFragment, SampleContext
from palm.system.vitality.probe import ProbeCatalog
from palm.system.vitality.report import SeatReport
from palm.system.vitality.schema import (
    CAPABILITY_LOADED_BULK,
    KIND_PLANE,
    KIND_SUPERVISOR_SERVICE,
    SEAT_PLANES,
    SEAT_SUPERVISOR,
    STATE_ABSENT,
    supervisor_service_seat_id,
)
from palm.system.vitality.seats import default_probe_catalog
from palm.system.vitality.walk import WalkOptions, walk_result

# Read seat_walk's bag when projection already walked (no double walk).
# Do **not** write that bag — projection extracts seats only from seat_walk.
_BAG_SEAT_REPORTS = "seat_reports"
_BAG_PRIVATE_REPORTS = "_loaded_bulk_reports"


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _public_callable_count(cls: type) -> int:
    """Count non-private callables on *cls* (visibility only)."""
    n = 0
    for name in dir(cls):
        if name.startswith("_"):
            continue
        try:
            attr = getattr(cls, name)
        except Exception:
            continue
        if callable(attr):
            n += 1
    return n


def _module_file_stats(mod: ModuleType) -> dict[str, Any]:
    """Bytes + line count for a loaded module file when path is a ``.py``."""
    path = getattr(mod, "__file__", None)
    out: dict[str, Any] = {
        "module": getattr(mod, "__name__", None),
        "file": path,
    }
    if not path or not str(path).endswith(".py"):
        out["lines"] = None
        out["bytes"] = None
        out["note"] = "no_py_file"
        return out
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        out["bytes"] = len(data)
        # Count lines without decoding failure theater.
        out["lines"] = data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)
    except OSError as exc:
        out["lines"] = None
        out["bytes"] = None
        out["note"] = f"read_error:{type(exc).__name__}"
    return out


def _type_bulk(obj: Any) -> dict[str, Any]:
    cls = type(obj)
    mod_name = getattr(cls, "__module__", None) or ""
    row: dict[str, Any] = {
        "type": getattr(cls, "__qualname__", cls.__name__),
        "module": mod_name,
        "public_callables": _public_callable_count(cls),
    }
    mod = sys.modules.get(mod_name) if mod_name else None
    if mod is not None:
        stats = _module_file_stats(mod)
        row["module_lines"] = stats.get("lines")
        row["module_bytes"] = stats.get("bytes")
        row["module_file"] = stats.get("file")
        if stats.get("note"):
            row["module_note"] = stats["note"]
    else:
        row["module_lines"] = None
        row["module_bytes"] = None
        row["module_note"] = "module_not_in_sys_modules"
    return row


def _resolve_probe_objects(
    instance: Any, catalog: ProbeCatalog
) -> list[tuple[str, str, Any]]:
    """Resolve probe seats to live objects (no status sampling)."""
    out: list[tuple[str, str, Any]] = []
    for probe in catalog.list():
        if probe.resolve is None:
            continue
        try:
            seat = probe.resolve(instance)
        except Exception:
            continue
        if seat is None:
            continue
        out.append((probe.seat_id, probe.kind, seat))
    return out


def _resolve_plane_members(instance: Any) -> list[tuple[str, str, Any]]:
    try:
        from palm.system.subsystems.planes.hub import get_system_planes
    except Exception:
        return []
    hub = get_system_planes(instance)
    if hub is None:
        return []
    out: list[tuple[str, str, Any]] = []
    try:
        names = list(hub.names())
    except Exception:
        return []
    for plane_id in names:
        try:
            plane = hub.get(plane_id)
        except Exception:
            continue
        if plane is None:
            continue
        seat_id = hub.seat_id(plane_id) if callable(getattr(hub, "seat_id", None)) else f"{plane_id}_plane"
        out.append((str(seat_id), KIND_PLANE, plane))
    return out


def _resolve_supervisor_services(instance: Any) -> list[tuple[str, str, Any]]:
    supervisor = getattr(instance, "supervisor", None)
    if supervisor is None:
        return []
    names_fn = getattr(supervisor, "names", None)
    get_fn = getattr(supervisor, "get", None)
    if not callable(names_fn):
        return []
    out: list[tuple[str, str, Any]] = []
    try:
        names = list(names_fn())
    except Exception:
        return []
    for name in names:
        service = get_fn(name) if callable(get_fn) else None
        if service is None:
            continue
        out.append(
            (supervisor_service_seat_id(str(name)), KIND_SUPERVISOR_SERVICE, service)
        )
    return out


def _collect_attached(
    instance: Any, catalog: ProbeCatalog | None
) -> list[tuple[str, str, Any]]:
    cat = catalog if catalog is not None else default_probe_catalog()
    by_id: dict[str, tuple[str, str, Any]] = {}
    for seat_id, kind, obj in _resolve_probe_objects(instance, cat):
        by_id[seat_id] = (seat_id, kind, obj)
    # Membership expansions — same spirit as seat_walk, resolve-only.
    for seat_id, kind, obj in _resolve_plane_members(instance):
        by_id[seat_id] = (seat_id, kind, obj)
    for seat_id, kind, obj in _resolve_supervisor_services(instance):
        by_id[seat_id] = (seat_id, kind, obj)
    return list(by_id.values())


def _ensure_seat_reports(
    instance: Any, ctx: SampleContext
) -> list[SeatReport]:
    for key in (_BAG_SEAT_REPORTS, _BAG_PRIVATE_REPORTS):
        cached = ctx.bag.get(key)
        if isinstance(cached, list) and cached and isinstance(cached[0], SeatReport):
            return list(cached)
    # Own walk for composition counts only — private bag so projection seats
    # still require seat_walk (ADR-030 fold lineage).
    options = ctx.walk_options if isinstance(ctx.walk_options, WalkOptions) else None
    result = walk_result(instance, options)
    ctx.bag[_BAG_PRIVATE_REPORTS] = list(result.reports)
    return list(result.reports)


def _composition_counts(instance: Any, reports: list[SeatReport]) -> dict[str, Any]:
    """Registry / membership cardinality — composition bulk, not shame."""
    by_kind: dict[str, int] = {}
    present = 0
    for r in reports:
        by_kind[r.kind] = by_kind.get(r.kind, 0) + 1
        if r.present:
            present += 1

    planes_n: int | None = None
    try:
        from palm.system.subsystems.planes.hub import get_system_planes

        hub = get_system_planes(instance)
        if hub is not None:
            planes_n = len(list(hub.names()))
    except Exception:
        planes_n = None

    services_n: int | None = None
    supervisor = getattr(instance, "supervisor", None)
    if supervisor is not None and callable(getattr(supervisor, "names", None)):
        try:
            services_n = len(list(supervisor.names()))
        except Exception:
            services_n = None

    probe_n = len(default_probe_catalog().list())
    try:
        from palm.system.vitality.seats_registry import default_vitality_registry

        cap_n = len(default_vitality_registry())
    except Exception:
        cap_n = None

    return {
        "seat_report_count": len(reports),
        "present_seat_count": present,
        "absent_seat_count": sum(1 for r in reports if r.state == STATE_ABSENT),
        "by_kind": by_kind,
        "planes_registered": planes_n,
        "supervisor_services_registered": services_n,
        "vitality_probe_count": probe_n,
        "vitality_capability_count": cap_n,
        "hub_seats_present": {
            SEAT_PLANES: any(r.seat_id == SEAT_PLANES and r.present for r in reports),
            SEAT_SUPERVISOR: any(
                r.seat_id == SEAT_SUPERVISOR and r.present for r in reports
            ),
        },
    }


def _rank_modules(module_rows: Iterable[dict[str, Any]], *, limit: int = 12) -> list[dict[str, Any]]:
    rows = [dict(r) for r in module_rows]
    rows.sort(
        key=lambda r: (
            -(r.get("lines") or 0),
            -(r.get("seat_count") or 0),
            str(r.get("module") or ""),
        )
    )
    return rows[: max(1, limit)]


def sample_loaded_bulk(instance: Any, ctx: SampleContext) -> CapabilityFragment:
    """Optional observe: light bulk of attached seats / their modules."""
    if ctx.bag.get("loaded_bulk_skip"):
        return CapabilityFragment.skipped(
            CAPABILITY_LOADED_BULK,
            "bag:loaded_bulk_skip",
            meta={"capability": CAPABILITY_LOADED_BULK},
        )

    reports = _ensure_seat_reports(instance, ctx)
    attached = _collect_attached(instance, None)

    seats: list[dict[str, Any]] = []
    modules: dict[str, dict[str, Any]] = {}

    for seat_id, kind, obj in attached:
        bulk = _type_bulk(obj)
        seats.append(
            {
                "seat_id": seat_id,
                "kind": kind,
                **bulk,
            }
        )
        mod_name = bulk.get("module") or ""
        if not mod_name:
            continue
        entry = modules.setdefault(
            mod_name,
            {
                "module": mod_name,
                "lines": bulk.get("module_lines"),
                "bytes": bulk.get("module_bytes"),
                "file": bulk.get("module_file"),
                "seat_ids": [],
                "seat_count": 0,
                "max_public_callables": 0,
            },
        )
        entry["seat_ids"].append(seat_id)
        entry["seat_count"] = len(entry["seat_ids"])
        pub = int(bulk.get("public_callables") or 0)
        if pub > int(entry.get("max_public_callables") or 0):
            entry["max_public_callables"] = pub
        # Prefer known lines/bytes if a later seat fills them.
        if entry.get("lines") is None and bulk.get("module_lines") is not None:
            entry["lines"] = bulk["module_lines"]
            entry["bytes"] = bulk.get("module_bytes")
            entry["file"] = bulk.get("module_file")

    module_list = list(modules.values())
    for m in module_list:
        m["seat_ids"] = sorted(m["seat_ids"])

    ranked = _rank_modules(module_list)
    lines_known = [m["lines"] for m in module_list if isinstance(m.get("lines"), int)]
    composition = _composition_counts(instance, reports)

    # Largest public surface among attached types (visibility, not grade).
    max_pub = 0
    max_pub_seat: str | None = None
    for s in seats:
        pub = int(s.get("public_callables") or 0)
        if pub > max_pub:
            max_pub = pub
            max_pub_seat = s.get("seat_id")

    summary = {
        "attached_object_count": len(seats),
        "unique_module_count": len(modules),
        "modules_with_lines": len(lines_known),
        "total_module_lines": sum(lines_known) if lines_known else None,
        "max_module_lines": max(lines_known) if lines_known else None,
        "max_public_callables": max_pub,
        "max_public_callables_seat": max_pub_seat,
        "top_modules": [
            {
                "module": m["module"],
                "lines": m.get("lines"),
                "seat_count": m.get("seat_count"),
            }
            for m in ranked[:5]
        ],
        "composition": {
            "present_seat_count": composition["present_seat_count"],
            "planes_registered": composition["planes_registered"],
            "supervisor_services_registered": composition[
                "supervisor_services_registered"
            ],
            "vitality_capability_count": composition["vitality_capability_count"],
        },
        "sources": ["seat_resolve", "module_file", "composition_counts"],
    }

    notes: list[str] = []
    if not seats:
        notes.append("no_attached_objects")
    if not lines_known:
        notes.append("module_lines_unavailable")
    notes.append("visibility_not_shame")

    data: dict[str, Any] = {
        "seats": seats,
        "modules": ranked,
        "composition": composition,
        "summary": summary,
        "sample_ts": _now_iso(),
        "meta_law": "visibility_not_shame",
    }

    return CapabilityFragment.ok(
        CAPABILITY_LOADED_BULK,
        data,
        notes=notes,
        meta={
            "capability": CAPABILITY_LOADED_BULK,
            "sample_source": "attached_seats+loaded_modules",
        },
    )


__all__ = [
    "sample_loaded_bulk",
]
