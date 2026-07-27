# VISION 0.55.10 — Continue Plane (seat the wait subsystem)

**Status:** ✅ **Done** (slice) — post-exit hardening of [VISION-0.55](VISION-0.55.md); continue plane seated. Follow-ons **0.55.11–0.55.15** closed (latest: [VISION-0.55.15](VISION-0.55.15.md) API collapse).  
**ADR:** [025-reactive-interests](adr/025-reactive-interests.md) still governs the law; this slice is placement, not a new law.  
**Trigger:** CI + architecture review — continue path worked as behavior but lived as a **wiring pile**, not a Palm plane.

> *Start has a plane. Continue must too. One bus, two verbs, two homes.*

---

## 1. Problem (diagnosis)

| Symptom | Cause |
|---------|--------|
| `just ci` deferred-import ratchet red | `waiting_on` / rehydrate bolted in via function-local imports |
| No peer to `WorkDrainService` | free function `bind_wait_matcher_to_runtime` + scatter |
| Dual nested state | wizard child-wait payload **and** `palm.wait.interests` |
| Index unused | production opens interest without index; matcher scans jobs |
| Three “waits” | interest park · child UX · provider `wait_for_job` poll |

**Law is fine** (ADR-025). **Home is missing.**

---

## 2. Intent

| Do | Outcome |
|----|---------|
| **WaitPlaneService** | First-class continue subsystem (lifecycle attach/detach) |
| Wire from `BaseRuntime` only through the plane | No glue free-function as the story |
| One present API for operator surfaces | Top-level imports; doctor/inspect/list share it |
| Rehydrate without deferred try/import | state_ops or plane helper at module level |
| Ratchet deferred-import ceiling down | Immune system green for this seam |
| Document plane vs start plane | EVENT-PLANE / ARCHITECTURE / AGENTS |

### Non-goals (0.55.10)

- Full dual-state collapse (wizard payload → meta only) — may be 0.55.11+  
- Host WorkPlaneCoordinator merge — optional later  
- WorkloadEngine (0.56)  
- Session watches  

---

## 3. Target architecture

```text
                    runtime.event
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
   WaitPlaneService                 WorkDrainService
   (continue)                       (start)
          │                               │
   interest on owner state           WorkIntent store
   match → resume / fail             → submit_flow
```

| Concern | Home |
|---------|------|
| Pure interest + open/close on state | `palm.core.wait` |
| Matcher, signals, policy, index | `palm.common.wait` (internals) |
| **WaitPlaneService** | `palm.common.wait.plane` — public continue façade |
| Runtime wire | `BaseRuntime` holds `wait_plane`, calls `attach`/`detach` |
| Operator present | `palm.common.wait.present` imported at module level by inspect/list/doctor |
| Pattern park | wizard opens interest (existing); later: plane.open_on_job |

---

## 4. Slice plan

| Patch | Deliverable |
|-------|-------------|
| **0.55.10** (this) | Plan + WaitPlaneService + BaseRuntime wire + hoist deferred imports + doctor contributor for neonroot — **done** |
| **0.55.11** (follow) | Single open path via plane + index discipline — **done** |
| **0.55.12** (follow) | Collapse dual nested state / naming docs for three waits — **done** |
| **0.55.13** | Slash `set_child_wait` → `open_nested_park` / interest-only resource phase — **done** |
| **0.55.14** | Plane delivers nested completion; matcher always closes interest — **done** |
| **0.55.15** | Slim public API door; delete tracked/runtime_bind kit — [VISION-0.55.15](VISION-0.55.15.md) — **done** |

Adjust boundaries with STATUS note.

---

## 5. Success criteria (0.55.10)

1. `WaitPlaneService` is the sole attach path for continue matching.  
2. `BaseRuntime.wait_plane` (and `wait_matcher` as thin property if needed) documented.  
3. No function-local `palm.common.wait` imports in inspect / waiting_jobs / diagnostics / instance_sync / system_inspect / assist catalog.  
4. Nested dogfood + matcher tests green.  
5. `guard_deferred` function-local count ≤ previous ceiling after hoist (ratchet down).  
6. VISION/STATUS/ARCHITECTURE name **Continue plane** next to start/work drain.

---

## 6. Complexity filter

Only work that **seats** continue under one service or **removes** scatter qualifies. New features (workload product, session) out of slice.

---

*Start plane drains intents. Continue plane matches interests. Same bus. Two homes.* 🌴⚡
