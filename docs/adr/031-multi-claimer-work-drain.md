# ADR-031 — Multi-claimer work drain (exclusive claim first)

**Status:** Accepted  
**Date:** 2026-08-04  
**Theme:** [VISION-0.62](../VISION-0.62.md) (**closed** at `0.62.8`)  
**Map:** [PALM.md](../PALM.md)  
**Migration:** [MIGRATION-0.62](../migrations/MIGRATION-0.62.md) · **Release:** [RELEASE-0.62.8](../releases/RELEASE-0.62.8.md)  
**Debt:** [SD-017](../../TECH-DEBT.md#sd-017) ✅ · [SD-018](../../TECH-DEBT.md#sd-018) ✅ · residual [SD-019](../../TECH-DEBT.md#sd-019)  
**Related:** [ADR-025](025-reactive-interests.md) · [ADR-029](029-system-supervisor.md) · [ADR-030](030-system-vitality.md) · [WORK-DRAIN](../WORK-DRAIN.md)

---

## Context

1. Palm has **reactive interests** ([ADR-025](025-reactive-interests.md)): start (WorkIntent) and continue (wait).  
2. **Work plane + supervisor** own start traffic and continuous drain ([ADR-029](029-system-supervisor.md)). Host dual drain is removed.  
3. **Vitality** can run load recipes ([ADR-030](030-system-vitality.md)) — `work_cycle` is the real start-path story.  
4. At theme open, `WorkIntentStore.claim_due` was **not exclusive**: read entry → set `claimed`. No `claimed_by`, no lease, no reclaim.  
5. Continuous drain was **one thread** with serial `submit_flow`. QueuedScheduler was one job-drive worker.  
6. Palm needed **capacity** on the start path without inventing a second queue or lying about host cores.  
7. Pre-1.0 may break ugly shapes when homes are wrong. Theme exit is **José’s judgment**.

---

## Decision

### D1 — Exclusive claim is the floor

Multi-claimer **starts with exclusive claim and reclaim**, not with `workers=N`.

| Floor | Growth |
|-------|--------|
| `claim_due` exclusive (`pending` → `claimed` for one claimer) | N continuous drain workers |
| Lease / visibility timeout + `reclaim_expired` | Drive-path concurrency as proven |
| Same API at `workers=1` | Benchmark 1 vs K |

Do **not** ship `work_drain_workers>1` as success before exclusive claim + reclaim hold.

### D2 — One start owner

Continuous drain remains on **system work plane + supervisor** only.

| Prefer | Avoid |
|--------|--------|
| Plane tick + supervised workers | Host `WorkDrainService` resurrection |
| Fail closed if plane unattached | Second start queue “for performance” |

### D3 — Durable claim shape

`WorkIntent` (core) carries claim identity:

| Field | Role |
|-------|------|
| `claimed_by` | Claimer id holding the lease |
| `lease_until` | When another claimer may reclaim |

Store API (names lock in code):

```text
claim_due(limit, *, claimer_id, now=None, lease_seconds=...) -> list[WorkIntent]
reclaim_expired(*, now=None) -> int
```

In-process atomicity uses a store lock (or single-writer mutex) around claim/ack/fail/index.  
Core stays pure; store I/O stays system.

### D4 — Default workers = 1

| Knob | Default | Meaning |
|------|---------|---------|
| `work_drain_workers` | **1** | Continuous drain loops (name may lock) |
| Existing poll / batch / depth | Unchanged spirit | Storm guards stay |

New knobs resolve through settings/composition without triple-override chaos ([BI-009](../../TECH-DEBT.md#bi-009)).

### D5 — Worker set home (prefer plane-owned count)

**Preferred first shape:** work plane owns worker count; N threads each call `tick` against the exclusive store.

Supervisor still **registers** `work_drain` as one continuous service (or one definition that configures N).  
Do not open-code a closed menu of peers in boot schedule prose ([CS-006](../../TECH-DEBT.md#cs-006) spirit / registry extension).

### D6 — Multi-process / multi-runtime is residual

| Layer | Stance |
|-------|--------|
| In-process multi-claimer | Theme subject after exclusive claim |
| Multi-runtime roles (`worker_count`) | Not a shared claim pool; **one continuous drain owner per work-intent store** |
| Multi-process shared durable store | [SD-019](../../TECH-DEBT.md#sd-019) — needs storage CAS; **not floor** |

Do **not** implement `BaseBackend` CAS in this theme unless José expands scope.  
Shape claim fields so later CAS is a plug-in, not a rewrite.

### D7 — Drive path (growth after claim floor)

Floor does **not** require parallel job drive. Floor requires **safe claim**.

Growth (0.62.7) pays concurrent **job drive** without rewriting orchestration:

| Law | Shape |
|-----|--------|
| Membership | `OrchestrationEngine` `RLock` on `_jobs` |
| Exclusive drive | `begin_drive` / `end_drive` — one owner per job |
| Drive entry | `drive_job` acquires; duplicate queue items no-op |
| Queued pool | `QueuedScheduler(workers=N)` · `queued_workers` / `PALM_QUEUED_WORKERS` (default **1**) |

Serial **per job**; parallel **across jobs**. Claim pool and drive pool are independent knobs.

### D8 — Honest capacity (GIL)

In-process multi-claimer + Queued **N** improve **start-queue and job-drive overlap** under I/O-bound and wait-heavy work.  
It is **not** a product promise that one Python process uses all host CPU cores.  
Heavy CPU stays in **workloads / processes / peer Palms**.

### D9 — Vitality proves capacity

Use existing vitality benchmark path (`work_cycle` and extensions) for **1 vs K**, reclaim, and contention.  
Vitality does **not** schedule claimers.

### D10 — Exit is José’s judgment

When exclusive claim + reclaim hold, workers (if shipped) are safe where claimed, proof is honest, residual is named, and declared green bars hold — **José** accepts this ADR and closes the theme.

---

## Consequences

### Positive

- Multi-claimer becomes extension of exclusive claim, not a rewrite.  
- One start path stays true.  
- Benchmarks already in house can dogfood capacity.  
- Multi-process residual is honest (SD-019).

### Negative / cost

- Core `WorkIntent` schema grows claim fields.  
- Store paths need lock discipline and reclaim tests.  
- Drive exclusivity + pool add concurrency discipline (hooks/re-entrancy still product care).  
- Two processes on one store remain unsupported until SD-019.

### Risks if ignored

- Flipping `workers=N` without exclusive claim corrupts the queue.  
- Treating multi-runtime as multi-claimer double-drains shared storage.  
- Claiming “multi-core” without workloads lies to operators.

---

## Alternatives considered

| Alternative | Why not |
|-------------|---------|
| Multi-process CAS first | Wrong rung; backend has no atomic claim; delays in-process floor |
| Host drain pool parallel to plane | Dual start path; undoes 0.60 residual pay |
| Only thread pool, no lease fields | Blocks reclaim and multi-process later |
| Vitality schedules workers | Eyes must not start work ([ADR-030](030-system-vitality.md)) |
| N QueuedScheduler workers as floor | Drive path ≠ claim exclusivity; optional growth |

---

## Status notes

- **0.62.0** — plan + this ADR **Proposed**.  
- **0.62.1–0.62.3** — exclusive claim + reclaim (**SD-017** ✅).  
- **0.62.4–0.62.6** — N drain workers + honesty + bench.  
- **0.62.7** — orchestration exclusive drive + Queued pool (**SD-018** ✅).  
- **0.62.8** — theme exit · José judged capacity proper · this ADR **Accepted**. Residual: **SD-019**.
