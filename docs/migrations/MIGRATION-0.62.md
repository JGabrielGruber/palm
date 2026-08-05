# Migration — 0.62 Multi-claimer work drain

**Theme:** [VISION-0.62](../vision/closed/VISION-0.62.md) (**closed**) · **ADR:** [031](../adr/031-multi-claimer-work-drain.md) **Accepted**  
**Map:** [PALM.md](../PALM.md) · **Release:** [RELEASE-0.62.8](../releases/RELEASE-0.62.8.md) · **Work drain:** [WORK-DRAIN](../WORK-DRAIN.md)

Palm is pre-1.0. This theme makes the **start path** and **job-drive path** safe under in-process concurrency. Defaults stay single-worker. Multi-process shared claim is **not** supported.

## Prefer

| Goal | Use |
|------|-----|
| Exclusive claim | `WorkIntentStore.claim_due(..., claimer_id=…, lease_seconds=…)` |
| Reclaim stuck claims | `reclaim_expired` (plane tick does this on poll) |
| Multi-claimer drain | `PALM_WORK_DRAIN_WORKERS` / `work_drain_workers` (default **1**) |
| Concurrent job drive (daemon/server) | `PALM_QUEUED_WORKERS` / `queued_workers` (default **1**) |
| Capacity proof | `palm benchmark work_cycle` · `run_benchmark(..., workers=K)` |
| One start path | System **work plane** only — no host drain |

## Behavior changes

| Was | Now |
|-----|-----|
| `claim_due` non-exclusive (read → set claimed) | Exclusive lease (`claimed_by` / `lease_until`) + store lock |
| No reclaim | `reclaim_expired` + visibility timeout |
| One drain thread by construction | N plane claimer threads (default 1) |
| QueuedScheduler one drive worker | Worker **pool** (default 1); exclusive drive per job |
| Orchestration job map unlocked | Membership `RLock` + `begin_drive` / `end_drive` |
| Double-queue could double-drive | `drive_job` no-ops if another owner holds drive |

## Settings / env

| Knob | Default | Role |
|------|---------|------|
| `work_drain_workers` / `PALM_WORK_DRAIN_WORKERS` | **1** | Continuous claimers |
| `work_drain_lease_seconds` / `PALM_WORK_DRAIN_LEASE_SECONDS` | **60** | Claim visibility timeout |
| `queued_workers` / `PALM_QUEUED_WORKERS` | **1** | QueuedScheduler drive pool |

Independent knobs. Raising claimers does **not** raise drive workers, and the reverse.

## Product law (until SD-019)

**One continuous drain owner per work-intent store.**  
Do not run two OS processes (or two continuous drain owners) against the same durable work keys.

| Safe | Unsafe |
|------|--------|
| One process, `work_drain_workers=K`, `queued_workers=N` | Two processes, same store, both draining |
| Multiple surfaces that only enqueue | Multi-runtime as a “shared claim pool” |

## Breaking / mild (pre-1.0)

- Core `WorkIntent` serializes `claimed_by` / `lease_until` (durable shape).  
- `claim_due` signature requires claimer identity for exclusive lease (callers pass claimer id).  
- Concurrent `drive_job` on the same job: second caller gets `False` (conflict), not a second drive.  
- Defaults unchanged (workers=1) — opt-in concurrency.

## Honesty

| Promise | Truth |
|---------|-------|
| Multi-claimer | Safer/faster **start-queue** under overlap |
| Queued N | Concurrent drive of **different** jobs |
| Host cores for Python patterns | **Not** this theme — workloads / processes |

## Tests

| Prefer | Avoid |
|--------|--------|
| Concurrent claim tests (two claimers, one intent) | Treating thread count as multi-core |
| Multi-worker drain + exclusive drive overlap | Dual continuous drain on one store in CI |
| `work_cycle` with `workers=K` | Calling fail-drain “success” |

## Residual after theme close

| Open | Kind |
|------|------|
| **SD-019** | Multi-process / multi-runtime shared claim needs storage CAS |
| **SD-016** | Ambient seat DI (boy-scout) |
| Surface deflation | [VISION-SURFACE-DEFLATION](../vision/VISION-SURFACE-DEFLATION.md) |
| Grove | Multi-Palm mesh (not shared claim index) |
