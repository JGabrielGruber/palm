# VISION 0.55.15 — Continue plane API collapse

**Status:** ✅ **Done** (slice) — post-exit hardening after [VISION-0.55.10](VISION-0.55.10.md)–0.55.14.  
**ADR:** [025-reactive-interests](../../adr/025-reactive-interests.md) still governs the law; this slice is **subtraction**, not new law.  
**Trigger:** Continue plane maturity report — usable and truthful, still a **kit** (~public barrel re-exports everything).

> *One production door. Pure core for engines and tests. Hide the leftover kit.*

---

## 1. Problem

| Smell | Reality after 0.55.14 |
|-------|------------------------|
| God-barrel `__init__` | Plane + tracked + runtime_bind + stub + deliver + signals + … |
| Dual open helpers | `open_tracked_wait` overlaps `plane.open_on_job` |
| Compat wire | `bind_wait_matcher_to_runtime` — no production callers left |
| Easy misuse | Kit symbols look as first-class as the plane |

Law and nested delivery are fine. Maturity needs a **small public surface**.

---

## 2. Intent

| Do | Outcome |
|----|---------|
| Slim `palm.common.wait` package exports | Production door only |
| Delete `tracked` + `runtime_bind` | No dual open / legacy matcher bind |
| Keep `access.*` | Register-downward open when code has job/state, not a plane ref (delegates to plane) |
| Stub / matcher / deliver | Submodule imports only — not package root |
| Docs | MIGRATION + EVENT-PLANE name the door |

### Non-goals

- Kind deliver registry (P2) — **done in [0.55.16](VISION-0.55.16.md)**  
- Kill resource poll fallback (P3)  
- Host workplane peer (P4)  
- Test folder tidy (P4)  
- Rename `child_wait` / invoke-wait modules  

---

## 3. Public API (locked)

```text
palm.core.wait          pure WaitInterest + open/close on state (engines, unbound tests)
palm.common.wait        package root:
  WaitPlaneService
  bind_wait_plane_to_runtime
  get_wait_plane
  open_interest_on_job / close_interest_on_job
  open_interest_for_state / close_interest_for_state
  find_job_for_state
  waiting_on_* / summarize_waiting_on

Internals (import submodule):
  plane, access, matcher, index, present, rehydrate,
  signals, policy, deliver, workload_stub
```

**Production open path:** `plane.open_on_job` or `access.open_interest_*` (plane when bound, pure state otherwise).  
**Do not** open via ad-hoc index helpers in product code.

---

## 4. Success criteria

1. Package `__all__` is the slim door above (characterization test).  
2. No `tracked.py` / `runtime_bind.py`.  
3. Matcher / durability / nested / plane tests green.  
4. Deferred-import ceiling does not rise.  
5. MIGRATION-0.55 documents the collapse.

---

## 5. Complexity filter

Only work that **removes** public surface or **redirects** callers to the plane qualifies. No new features.

---

*Start plane drains intents. Continue plane matches interests. Same bus. One door each.* 🌴⚡
