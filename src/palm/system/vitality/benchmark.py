"""
Benchmark tool — controlled load recipe + snapshot diff (0.61.10+).

**Law (ADR-030 / VISION-VITALITY §15.4):**
  - Registered **tool** capability — consumes projection; no second metric law.
  - ``snapshot₀ → recipe → snapshot₁ → diff`` (RSS/CPU · seats · emissions · bulk).
  - Nested samples are **observe-only** (tools disabled) so this never re-enters.
  - **default_enabled=False** — everyday ``project()`` must not thrash.
  - Recipes use real seats (work plane, walk, log) — not vanity status loops alone.

**Not law:** vanity per-flow timings alone; health grades; silent job mutation
for product paths (benchmark may enqueue disposable intents and drain them).
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from typing import Any

from palm.system.vitality.capability import CapabilityFragment, SampleContext
from palm.system.vitality.schema import (
    CAPABILITY_BENCHMARK,
    CAPABILITY_EMISSION_WINDOW,
    CAPABILITY_LOADED_BULK,
    CAPABILITY_PROCESS_RESOURCES,
    COST_MODERATE,
    ROLE_TOOL,
)

# Recipe id → description (catalog honesty).
RECIPE_IDLE: str = "idle"
RECIPE_PULSE: str = "pulse"
RECIPE_WALK: str = "walk"
RECIPE_LOG_FILL: str = "log_fill"
RECIPE_WORK_CYCLE: str = "work_cycle"
RECIPE_PROJECT_STRESS: str = "project_stress"

KNOWN_RECIPES: frozenset[str] = frozenset(
    {
        RECIPE_IDLE,
        RECIPE_PULSE,
        RECIPE_WALK,
        RECIPE_LOG_FILL,
        RECIPE_WORK_CYCLE,
        RECIPE_PROJECT_STRESS,
    }
)

# Default: real start-plane path so CLI deltas mean something.
DEFAULT_RECIPE: str = RECIPE_WORK_CYCLE
DEFAULT_ITERATIONS: int = 10
MAX_ITERATIONS: int = 500

# Disposable target — not a real flow; tick fails honestly and drains queue.
_BENCHMARK_FLOW_TARGET: str = "__vitality.benchmark.no_flow"

_BAG_RECIPE = "benchmark_recipe"
_BAG_ITERATIONS = "benchmark_iterations"
_BAG_SKIP = "benchmark_skip"
_BAG_ACTIVE = "_vitality_benchmark_active"
_BAG_STORE_FULL = "benchmark_store_full_snapshots"
_BAG_WORKERS = "benchmark_workers"


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _iterations(ctx: SampleContext) -> int:
    raw = ctx.bag.get(_BAG_ITERATIONS, DEFAULT_ITERATIONS)
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_ITERATIONS
    return max(0, min(MAX_ITERATIONS, n))


def _recipe_id(ctx: SampleContext) -> str:
    raw = str(ctx.bag.get(_BAG_RECIPE) or DEFAULT_RECIPE).strip().lower()
    if raw in KNOWN_RECIPES:
        return raw
    return DEFAULT_RECIPE


def _run_idle(_instance: Any, n: int) -> dict[str, Any]:
    """Control recipe — measures sample noise only."""
    return {"kind": RECIPE_IDLE, "ops": 0, "requested": n}


def _run_pulse(instance: Any, n: int) -> dict[str, Any]:
    """Light thrash: work_plane.status when attached, else tiny CPU ticks."""
    work = getattr(instance, "work_plane", None)
    status_fn = getattr(work, "status", None) if work is not None else None
    ops = 0
    path = "cpu_tick"
    if callable(status_fn):
        path = "work_plane.status"
        for _ in range(n):
            status_fn()
            ops += 1
    else:
        for _ in range(n):
            # Deterministic micro-load — not a timer vanity race.
            _ = sum(range(200))
            ops += 1
    return {"kind": RECIPE_PULSE, "ops": ops, "path": path, "requested": n}


def _run_walk(instance: Any, n: int) -> dict[str, Any]:
    """Repeat seat walk — stresses discovery / sample path."""
    from palm.system.vitality.walk import walk_result

    ops = 0
    last_present = None
    for _ in range(n):
        result = walk_result(instance)
        ops += 1
        last_present = result.present_count
    return {
        "kind": RECIPE_WALK,
        "ops": ops,
        "requested": n,
        "last_present_count": last_present,
    }


def _run_log_fill(_instance: Any, n: int) -> dict[str, Any]:
    """Declared emission stress — system log only; actor_kind=probe."""
    from palm.system.log import get_system_log

    slog = get_system_log()
    ops = 0
    for i in range(n):
        slog.info(
            "vitality.benchmark.pulse",
            f"benchmark log_fill {i}",
            actor_kind="probe",
        )
        ops += 1
    return {"kind": RECIPE_LOG_FILL, "ops": ops, "requested": n, "channel": "system_log"}


def _workers_from_bag(bag: Mapping[str, Any] | None) -> int:
    if not bag:
        return 1
    raw = bag.get(_BAG_WORKERS, 1)
    try:
        return max(1, min(32, int(raw)))
    except (TypeError, ValueError):
        return 1


def _run_work_cycle(
    instance: Any, n: int, *, workers: int = 1
) -> dict[str, Any]:
    """Real start-plane path: enqueue WorkIntents, then tick to drain.

    Targets a missing flow so submit fails honestly (no silent product job).
    Peak pending is recorded in recipe_meta — the story when before/after
    pending returns to ~0 after drain.

    When ``workers>1`` (0.62.6), concurrent claimers call ``tick`` with
    distinct claimer ids (exclusive claim proof). Drive path may still
    serialize under GIL — claim correctness is the story, not host cores.
    """
    from palm.core.work import WorkIntent

    work = getattr(instance, "work_plane", None)
    if work is None or not getattr(work, "is_attached", False):
        # Honest fallback — still a recipe result, not a fake green work path.
        base = _run_pulse(instance, n)
        base["fallback"] = "pulse"
        base["note"] = "work_plane_unavailable"
        return base

    enqueue_fn = getattr(work, "enqueue", None)
    tick_fn = getattr(work, "tick", None)
    status_fn = getattr(work, "status", None)
    if not callable(enqueue_fn) or not callable(tick_fn):
        base = _run_pulse(instance, n)
        base["fallback"] = "pulse"
        base["note"] = "work_plane_no_enqueue_tick"
        return base

    run_token = uuid.uuid4().hex[:12]
    enqueued = 0
    for i in range(n):
        intent = WorkIntent(
            kind="run_flow",
            target=_BENCHMARK_FLOW_TARGET,
            payload={
                "_vitality_benchmark": True,
                "i": i,
                "run": run_token,
            },
            # Unique coalesce so N means N intents (not one).
            coalesce_key=f"vitality.benchmark.work_cycle.{run_token}.{i}",
        )
        rid = enqueue_fn(intent)
        if rid:
            enqueued += 1

    peak_pending: int | None = None
    if callable(status_fn):
        try:
            peak_pending = int((status_fn() or {}).get("pending") or 0)
        except Exception:
            peak_pending = None

    claim_workers = max(1, int(workers))
    submit_ok = 0
    processed = 0
    ticks = 0
    t0 = time.perf_counter()

    if claim_workers <= 1:
        # Drain until empty or safety bound (batch may be small).
        max_ticks = max(3, (enqueued // 5) + 5)
        for _ in range(max_ticks):
            ticks += 1
            pending_before = None
            if callable(status_fn):
                try:
                    pending_before = int((status_fn() or {}).get("pending") or 0)
                except Exception:
                    pending_before = None
            try:
                done = int(tick_fn(limit=max(enqueued, 10)) or 0)
            except Exception:
                done = 0
            submit_ok += done
            pending_now = None
            if callable(status_fn):
                try:
                    pending_now = int((status_fn() or {}).get("pending") or 0)
                except Exception:
                    pending_now = None
            if pending_before is not None and pending_now is not None:
                processed += max(0, pending_before - pending_now)
            if pending_now == 0:
                break
    else:
        import threading

        stop = threading.Event()
        lock = threading.Lock()

        def _claimer_loop(claimer_id: str) -> None:
            nonlocal submit_ok, ticks
            while not stop.is_set():
                try:
                    done = int(
                        tick_fn(
                            limit=1,
                            claimer_id=claimer_id,
                            reclaim=True,
                        )
                        or 0
                    )
                except Exception:
                    done = 0
                with lock:
                    ticks += 1
                    submit_ok += done
                if callable(status_fn):
                    try:
                        if int((status_fn() or {}).get("pending") or 0) == 0:
                            return
                    except Exception:
                        pass
                if done == 0:
                    time.sleep(0.001)

        threads = [
            threading.Thread(
                target=_claimer_loop,
                args=(f"bench-{i}",),
                daemon=True,
            )
            for i in range(claim_workers)
        ]
        for th in threads:
            th.start()
        deadline = time.monotonic() + max(2.0, enqueued * 0.05 + 1.0)
        while time.monotonic() < deadline:
            if callable(status_fn):
                try:
                    if int((status_fn() or {}).get("pending") or 0) == 0:
                        break
                except Exception:
                    pass
            time.sleep(0.01)
        stop.set()
        for th in threads:
            th.join(timeout=1.0)
        if callable(status_fn):
            try:
                pending_now = int((status_fn() or {}).get("pending") or 0)
            except Exception:
                pending_now = None
            if peak_pending is not None and pending_now is not None:
                processed = max(0, peak_pending - pending_now)

    wall_ms = (time.perf_counter() - t0) * 1000.0

    pending_after = None
    if callable(status_fn):
        try:
            pending_after = int((status_fn() or {}).get("pending") or 0)
        except Exception:
            pending_after = None

    return {
        "kind": RECIPE_WORK_CYCLE,
        "ops": enqueued,
        "requested": n,
        "enqueued": enqueued,
        # submit_ok = successful flow starts (0 when target flow is missing).
        "submit_ok": submit_ok,
        # processed = intents cleared from pending (ok or fail-ack).
        "processed": processed,
        "ticks": ticks,
        "peak_pending": peak_pending,
        "pending_after": pending_after,
        "workers": claim_workers,
        "wall_ms": round(wall_ms, 3),
        "path": "work_plane.enqueue+tick",
        "target": _BENCHMARK_FLOW_TARGET,
        "note": (
            "missing_flow_fails_on_tick_by_design; processed clears queue"
            + (
                "; multi_claimer exclusive claim proof"
                if claim_workers > 1
                else ""
            )
        ),
    }


def _run_project_stress(instance: Any, n: int) -> dict[str, Any]:
    """Repeat observe-only projection — measures eyes cost under self-load."""
    ops = 0
    last_seats = None
    for _ in range(n):
        # Fresh context each time — no bag carry between samples.
        snap = _project_observe(instance, SampleContext())
        ops += 1
        last_seats = (getattr(snap, "summary", None) or {}).get("present_count")
    return {
        "kind": RECIPE_PROJECT_STRESS,
        "ops": ops,
        "requested": n,
        "path": "vitality.project_observe",
        "last_present_count": last_seats,
    }


_RECIPES: dict[str, Callable[[Any, int], dict[str, Any]]] = {
    RECIPE_IDLE: _run_idle,
    RECIPE_PULSE: _run_pulse,
    RECIPE_WALK: _run_walk,
    RECIPE_LOG_FILL: _run_log_fill,
    RECIPE_WORK_CYCLE: _run_work_cycle,
    RECIPE_PROJECT_STRESS: _run_project_stress,
}


def extract_load_points(snapshot: Any) -> dict[str, Any]:
    """Pure fold: comparable load points from a vitality snapshot.

    Consumes projection fragments — does not invent parallel counters.
    """
    points: dict[str, Any] = {
        "sample_ts": getattr(snapshot, "sample_ts", None),
    }
    summary = getattr(snapshot, "summary", None) or {}
    if isinstance(summary, Mapping):
        points["seat_count"] = summary.get("seat_count")
        points["seat_present"] = summary.get("present_count")

    frag_fn = getattr(snapshot, "fragment", None)
    if not callable(frag_fn):
        # dict-shaped snapshot support
        fragments = getattr(snapshot, "fragments", None)
        if isinstance(fragments, Mapping):
            def frag_fn(cid: str) -> Any:  # type: ignore[misc]
                return fragments.get(cid)
        else:
            return points

    pr = frag_fn(CAPABILITY_PROCESS_RESOURCES)
    if pr is not None and getattr(pr, "present", False):
        data = getattr(pr, "data", None) or {}
        s = data.get("summary") if isinstance(data, Mapping) else None
        if isinstance(s, Mapping):
            points["rss_kb"] = s.get("primary_rss_kb")
            points["rss_kind"] = s.get("primary_rss_kind")
            points["threads"] = s.get("threads_active")
            points["cpu_user_s"] = s.get("cpu_user_s")
            points["cpu_system_s"] = s.get("cpu_system_s")

    em = frag_fn(CAPABILITY_EMISSION_WINDOW)
    if em is not None and getattr(em, "present", False):
        data = getattr(em, "data", None) or {}
        if isinstance(data, Mapping):
            s = data.get("summary")
            if isinstance(s, Mapping):
                points["emission_count"] = s.get("emission_count")
                by_actor = s.get("by_actor_kind")
                if isinstance(by_actor, Mapping):
                    points["emission_probe"] = by_actor.get("probe")
                    points["emission_system"] = by_actor.get("system")
            heat = data.get("heat")
            if isinstance(heat, Mapping):
                points["work_pending"] = heat.get("pending")
                points["work_trigger_count"] = heat.get("trigger_count")

    bulk = frag_fn(CAPABILITY_LOADED_BULK)
    if bulk is not None and getattr(bulk, "present", False):
        data = getattr(bulk, "data", None) or {}
        s = data.get("summary") if isinstance(data, Mapping) else None
        if isinstance(s, Mapping):
            points["bulk_attached"] = s.get("attached_object_count")
            points["bulk_module_lines"] = s.get("total_module_lines")
            points["bulk_unique_modules"] = s.get("unique_module_count")

    return points


def diff_load_points(
    before: Mapping[str, Any], after: Mapping[str, Any]
) -> dict[str, Any]:
    """Pure numeric delta fold — before/after/delta per comparable key."""
    keys = sorted(set(before) | set(after))
    out: dict[str, Any] = {}
    for key in keys:
        if key in {"sample_ts", "rss_kind"}:
            out[key] = {"before": before.get(key), "after": after.get(key)}
            continue
        va = before.get(key)
        vb = after.get(key)
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            out[key] = {"before": va, "after": vb, "delta": vb - va}
        else:
            out[key] = {"before": va, "after": vb, "delta": None}
    return out


def _project_observe(instance: Any, ctx: SampleContext) -> Any:
    """Nested projection: installed observe only — never tools."""
    from palm.system.vitality.projection import ProjectionOptions, VitalityProjection
    from palm.system.vitality.seats_registry import default_vitality_registry

    reg = default_vitality_registry().clone()
    tool_ids: list[str] = []
    for cap in reg.list():
        if cap.role == ROLE_TOOL or cap.id == CAPABILITY_BENCHMARK:
            reg.disable(cap.id)
            tool_ids.append(cap.id)
    return VitalityProjection(reg).sample(
        instance,
        ProjectionOptions(
            mode=ctx.mode,
            walk_options=ctx.walk_options,
            stamp=True,
            extra_disable=frozenset(tool_ids),
        ),
    )


def sample_benchmark(instance: Any, ctx: SampleContext) -> CapabilityFragment:
    """Tool capability: recipe thrash between two observe projections."""
    if ctx.bag.get(_BAG_SKIP):
        return CapabilityFragment.skipped(
            CAPABILITY_BENCHMARK,
            "bag:benchmark_skip",
            meta={"capability": CAPABILITY_BENCHMARK},
        )
    if ctx.bag.get(_BAG_ACTIVE):
        return CapabilityFragment.skipped(
            CAPABILITY_BENCHMARK,
            "reentrant_benchmark",
            meta={"capability": CAPABILITY_BENCHMARK},
        )

    recipe = _recipe_id(ctx)
    # Unknown bag recipe falls back — note when caller passed garbage.
    requested = str(ctx.bag.get(_BAG_RECIPE) or recipe).strip().lower()
    notes: list[str] = []
    if requested not in KNOWN_RECIPES and ctx.bag.get(_BAG_RECIPE) is not None:
        notes.append(f"unknown_recipe_fallback:{requested}->{recipe}")

    iterations = _iterations(ctx)
    runner = _RECIPES[recipe]
    ctx.bag[_BAG_ACTIVE] = True
    t0 = time.perf_counter()
    try:
        before_snap = _project_observe(instance, ctx)
        before_points = extract_load_points(before_snap)

        t_recipe0 = time.perf_counter()
        try:
            if recipe == RECIPE_WORK_CYCLE:
                recipe_meta = _run_work_cycle(
                    instance,
                    iterations,
                    workers=_workers_from_bag(ctx.bag),
                )
            else:
                recipe_meta = runner(instance, iterations)
        except Exception as exc:
            return CapabilityFragment.error(
                CAPABILITY_BENCHMARK,
                f"recipe:{type(exc).__name__}: {exc}",
                meta={
                    "capability": CAPABILITY_BENCHMARK,
                    "recipe": recipe,
                    "iterations": iterations,
                },
            )
        recipe_ms = (time.perf_counter() - t_recipe0) * 1000.0

        after_snap = _project_observe(instance, ctx)
        after_points = extract_load_points(after_snap)
        diff = diff_load_points(before_points, after_points)
    finally:
        ctx.bag.pop(_BAG_ACTIVE, None)
    total_ms = (time.perf_counter() - t0) * 1000.0

    summary = {
        "recipe": recipe,
        "iterations": iterations,
        "recipe_ops": (recipe_meta or {}).get("ops"),
        "recipe_ms": round(recipe_ms, 3),
        "total_ms": round(total_ms, 3),
        "deltas": {
            k: v.get("delta")
            for k, v in diff.items()
            if isinstance(v, Mapping) and v.get("delta") is not None
        },
    }

    data: dict[str, Any] = {
        "recipe": recipe,
        "recipe_meta": recipe_meta,
        "iterations": iterations,
        "before": before_points,
        "after": after_points,
        "diff": diff,
        "summary": summary,
        "sample_ts": _now_iso(),
        "timing": {
            "recipe_ms": round(recipe_ms, 3),
            "total_ms": round(total_ms, 3),
        },
        "known_recipes": sorted(KNOWN_RECIPES),
    }
    if ctx.bag.get(_BAG_STORE_FULL):
        # Opt-in full snapshots — heavy; default keeps only load points.
        data["before_snapshot"] = before_snap.to_dict()
        data["after_snapshot"] = after_snap.to_dict()

    notes.append("consumes_projection")
    notes.append("tools_excluded_from_nested_sample")

    return CapabilityFragment.ok(
        CAPABILITY_BENCHMARK,
        data,
        notes=notes,
        meta={
            "capability": CAPABILITY_BENCHMARK,
            "role": ROLE_TOOL,
            "cost": COST_MODERATE,
            "sample_source": "observe_project+recipe+diff",
        },
    )


def run_benchmark(
    instance: Any,
    *,
    recipe: str = DEFAULT_RECIPE,
    iterations: int = DEFAULT_ITERATIONS,
    mode: str | None = None,
    store_full_snapshots: bool = False,
    workers: int = 1,
) -> CapabilityFragment:
    """Public dogfood entry — run without enabling the tool on every project.

    ``workers`` (0.62.6) — concurrent claimers for ``work_cycle`` only.
    """
    ctx = SampleContext(mode=mode)
    ctx.bag[_BAG_RECIPE] = recipe
    ctx.bag[_BAG_ITERATIONS] = iterations
    ctx.bag[_BAG_WORKERS] = max(1, int(workers))
    if store_full_snapshots:
        ctx.bag[_BAG_STORE_FULL] = True
    return sample_benchmark(instance, ctx)


__all__ = [
    "DEFAULT_ITERATIONS",
    "DEFAULT_RECIPE",
    "KNOWN_RECIPES",
    "MAX_ITERATIONS",
    "RECIPE_IDLE",
    "RECIPE_LOG_FILL",
    "RECIPE_PROJECT_STRESS",
    "RECIPE_PULSE",
    "RECIPE_WALK",
    "RECIPE_WORK_CYCLE",
    "diff_load_points",
    "extract_load_points",
    "run_benchmark",
    "sample_benchmark",
]
