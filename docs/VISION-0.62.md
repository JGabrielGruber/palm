# VISION 0.62 — Multi-claimer work drain (execution capacity)

**Status:** ✅ **Theme closed** at **0.62.8** (exit).  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [PALM.md](PALM.md) — read first.  
**ADR:** [031-multi-claimer-work-drain.md](adr/031-multi-claimer-work-drain.md) **Accepted**.  
**Migration:** [MIGRATION-0.62](migrations/MIGRATION-0.62.md) · **Release:** [RELEASE-0.62.8](releases/RELEASE-0.62.8.md).  
**Theme law:** [VERSIONING.md](VERSIONING.md) (floor · growth · exit judgment) · [AGENTS.md](../AGENTS.md) §6b.  
**Debt paid:** [SD-017](../TECH-DEBT.md#sd-017) ✅ · [SD-018](../TECH-DEBT.md#sd-018) ✅ · residual [SD-019](../TECH-DEBT.md#sd-019) · neighbors BI-013 residual · BI-009 · SD-016.  
**Prior closed:** [VISION-0.61](VISION-0.61.md) vitality · [VISION-0.60](VISION-0.60.md) supervisor + work plane.  
**Queue later:** [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) · Grove · workload remainder · storage CAS.  
**North star:** [VISION-GROVE](VISION-GROVE.md).  
**Work drain law:** [WORK-DRAIN](WORK-DRAIN.md).

**Exit judgment (2026-08-04):** José judged in-process capacity proper — exclusive claim + reclaim, multi-claimer drain, exclusive job drive + Queued pool, vitality 1 vs K, residual multi-process CAS named. Theme closed; not empty checklist.

---

## 1. Goal

Give Palm a **safe concurrent start path** on the existing work plane.

| Piece | Role |
|-------|------|
| **Exclusive claim** | Only one claimer owns a due `WorkIntent` at a time |
| **Reclaim / lease** | Stuck `claimed` work returns after visibility timeout |
| **Multi-claimer drain** | N continuous workers under supervisor (default **1**) |
| **Vitality proof** | `work_cycle` and friends show **1 vs K** without double-submit |

**Host** stays packaging.  
**Planes** still carry start/continue.  
**Supervisor** still runs continuous loops.  
**Vitality only observes** — it does not schedule claimers.

### 1.1 Ambition and floor

| Concept | Meaning |
|---------|---------|
| **Floor** | Claim is exclusive and reclaimable, even with one drain worker. Same claim API for `workers=1`. |
| **Growth line** | N workers, drive-path concurrency, knobs, benchmarks — **paid** under theme. |
| **Exit** | ✅ José’s judgment (2026-08-04) — capacity proper; residual honest (**SD-019**). |

Do not kill ambition to satisfy dead process notes.  
Do not ship permanent workarounds to stay “thin.”  
Break what is ugly. Pay debt when feasible. Name the rest.

### 1.2 Success (theme intent)

- Two claimers cannot take the same intent.  
- Worker death does not leave work claimed forever.  
- Continuous drain has **one owner**: system work plane + supervisor (plane-only).  
- `palm benchmark work_cycle` can prove **1 vs K** with honest counters.  
- Multi-process shared claim is **named residual** if unpaid ([SD-019](../TECH-DEBT.md#sd-019)).

This theme is **not** full surface compost.  
This theme is **not** Grove mesh.  
This theme is **not** “threads use all host cores.”

---

## 2. Why now

1. **Work plane + supervisor** are live ([VISION-0.60](VISION-0.60.md)). Start law has a home.  
2. **Host dual drain** is gone — multi-claimer attaches to **one** owner only.  
3. **Vitality + benchmarks** exist ([VISION-0.61](VISION-0.61.md)) — eyes can prove 1 vs K.  
4. **Code was single-claimer by construction** — exclusive claim + multi-claimer drain + (0.62.7) exclusive job drive + Queued pool close the in-process capacity spine.  
5. Further growth without exclusive claim ships dual-claim corruption as architecture.

**Thesis:** Capacity starts with **safe claim**, then **N workers**, not with pool size theater.

---

## 3. Non-goals (subject of other seeds — not forever bans)

| Out of this theme’s *subject* | Relation |
|-------------------------------|----------|
| Full surface purge (SU-*) | [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) |
| Grove multi-Palm mesh | Scale-out; not shared pending index |
| Full SD-016 seat DI cleanup | Boy-scout on touch; not theme gate |
| BI-003 packaging seats / delete ServerContext | Packaging residual; dual types stay |
| Workload placement remainder as home | Heavy CPU home is workloads — complement, not this theme |
| User plane | Separate seed |
| `BaseBackend` CAS / multi-process claim pool | [SD-019](../TECH-DEBT.md#sd-019) residual |

**Forbidden always (layer law):**

- Second start path (host drain resurrection for “speed”).  
- `workers>1` without exclusive claim + reclaim.  
- Vitality as a plane that starts work.  
- Product claim that in-process threads = all host cores.  
- Fake green when multi-claimer is unsafe.  
- Closed menu of worker peers in schedule prose (registry extension spirit).

---

## 4. Principles

Bind to [PALM.md](PALM.md), [ADR-025](adr/025-reactive-interests.md), [ADR-029](adr/029-system-supervisor.md), [ADR-030](adr/030-system-vitality.md), and ADR-031.

1. **One start path** — work plane only.  
2. **Exclusive claim before multi-claimer** — floor is safety, not pool size.  
3. **Reclaim is first-class** — no stuck claimed forever.  
4. **Supervisor runs continuous workers** — does not invent claim law.  
5. **Default workers=1** — same API as N.  
6. **Registry extension** — worker set from definition/options, not schedule menus.  
7. **Seat DI** — natural paths use interfaces/subsystems ([SD-016](../TECH-DEBT.md#sd-016) boy-scout).  
8. **Vitality proves** — 1 vs K; honest `processed` vs `submit_ok`.  
9. **Honest capacity** — claim pool ≠ host cores; workloads own heavy CPU.  
10. **Pay or name** — multi-process CAS residual if unpaid.  
11. **One continuous drain owner per work-intent store** until SD-019 is paid.  
12. **STE** for theme docs.  
13. **Theme exit is José’s judgment** when capacity is proper.

**Spirit:** Safe claim under concurrency beats a large pool that lies.

---

## 5. Lexicon

| Term | Meaning | Home |
|------|---------|------|
| **Claim** | Transition due intent `pending` → `claimed` for one claimer | Work intent store |
| **Claimer** | Stable id of the worker that holds the lease | Store + plane tick |
| **Lease / visibility timeout** | Time after which another claimer may reclaim | Store |
| **Reclaim** | Expired lease → `pending` again | Store |
| **Multi-claimer** | N concurrent claimers on one process, one store | Work plane + supervisor |
| **Drain worker** | Continuous loop that claims and submits when able | Supervisor / plane |
| **Drive path** | Job execution after submit (`submit_flow` → scheduler) | Orchestration |
| **Claim pool** | Scale of exclusive claimers | Not “host cores” |

**Rule:** Speak **claim / lease / reclaim / claimer**.  
Do not call thread count “multi-core Palm” without workloads or processes.

### 5.1 Three layers (do not conflate)

| Layer | Meaning | 0.62 stance |
|-------|---------|-------------|
| **In-process multi-claimer** | N threads, one system instance, one store | **Theme subject** (after exclusive claim) |
| **Multi-runtime same host** | Kernel roles / registry — not a shared claim pool by law | One drain owner per store |
| **Multi-process shared store** | Two OS processes, same durable keys | **SD-019 residual** — needs storage CAS |

---

## 6. Target shape

```text
  SUPERVISOR
    work_drain (1..K continuous workers)
         │ each: able? → work_plane.tick(limit=…)
         ▼
  WORK PLANE
    enqueue · coalesce · tick_schedules · tick
         │
         ▼
  WorkIntentStore
    claim_due(limit, claimer_id) → exclusive lease
    reclaim_expired(now)
    ack / fail (owner-aware when multi-claimer on)
         │
         ▼
  submit_flow → job start (drive path; concurrency growth)
```

**Invariants:**

- One start law (WorkIntent → drain → job). No second host queue.  
- Claim exclusivity **before** `work_drain_workers=N` as success.  
- `workers=1` uses the same claim API.  
- Vitality observes; it does not schedule claimers.

### 6.1 Claim API (floor)

| Operation | Role |
|-----------|------|
| `claim_due(limit, *, claimer_id, now=…, lease_seconds=…)` | Exclusive lease for due pending intents |
| `reclaim_expired(*, now=…)` | Expired leases → pending |
| `ack` / `fail` | Complete or retry; owner-aware when multi-claimer on |

Durable fields (core `WorkIntent`): `claimed_by`, `lease_until` (names lock in code).  
In-process atomicity: store lock (or single-writer mutex) around claim/ack/fail/index.  
Later multi-process: same fields; CAS on backend ([SD-019](../TECH-DEBT.md#sd-019)).

### 6.2 Continuous workers (growth)

| Option | Shape | Prefer |
|--------|--------|--------|
| **A** | Plane owns worker count; N threads each tick + exclusive store | **First** |
| **B** | N supervisor members from one definition | If plane ownership is wrong |
| **C** | One claimer + N submit workers | Only after exclusive batch claim holds |

Default **`work_drain_workers=1`**.  
Settings/composition resolve knobs without triple-override chaos ([BI-009](../TECH-DEBT.md#bi-009)).

### 6.3 Drive path (growth — **0.62.7 paid**)

Floor required **safe claim** only. Growth paid concurrent **job drive** without rewriting orchestration law:

| Path | Law |
|------|-----|
| Orchestration map | `RLock` membership |
| Drive slice | `begin_drive` / `end_drive` — one owner per job |
| `drive_job` | Acquires exclusive drive; drop duplicate queue items |
| QueuedScheduler | Worker **pool** (`workers=N`, default **1**) |
| Settings | `queued_workers` / `PALM_QUEUED_WORKERS` |

| Path | Behavior |
|------|----------|
| InlineScheduler | Drive on caller; exclusive drive still holds if multi-threaded |
| QueuedScheduler N | Up to N **different** jobs drive at once; serial **per job** |

Honesty: claim pool + drive pool improve **overlap** under I/O/wait. They are **not** “all host cores for Python patterns” — workloads / processes remain the CPU home.

### 6.4 Benchmarks (dogfood)

Reuse vitality truth from 0.61:

- `system.vitality.run_benchmark` · `InspectService.benchmark` · `palm benchmark`  
- Default recipe `work_cycle` — honest `processed` vs `submit_ok`

| Proof | Intent |
|-------|--------|
| `work_cycle` workers=1 | Baseline |
| `work_cycle` workers=K | Throughput + no double-ack + queue empty |
| Reclaim recipe | Lease expire → reclaim → process |
| Contention | Coalesce + multi-claim no lost/dup jobs |

### 6.5 GIL / cores (product truth)

- Multi-claimer improves **start-queue throughput** under I/O-bound and wait-heavy work.  
- CPU-bound steps use **workloads / processes / peer Palm**.  
- Success yardstick: wall clock + correctness under K — not CPU% theater on one process.

---

## 7. Ordered work (guide — not a coffin)

Slices stay **one purpose each**. Numbers may merge, split, or extend.  
Theme stays open while José still needs proper capacity.

| Order | Slice spirit | Result |
|------:|--------------|--------|
| **0** | Plan + map + ADR | **0.62.0** — this file · ADR-031 Proposed · debt rows |
| **1** | Exclusive claim model | `claimed_by` / `lease_until` · store claim API · two claimers never share one intent |
| **2** | Reclaim / visibility timeout | Expired lease → pending · storm tests |
| **3** | Plane tick uses claimer identity | Stable claimer id · reclaim on poll · status heat |
| **4** | N drain workers | `work_drain_workers` default 1 · plane/supervisor worker set |
| **5** | Drive-path honesty | Pay concurrent submit safety **or** name residual |
| **6** | Benchmark proof | 1 vs K · reclaim · contention recipes |
| **7** | Concurrent job drive | Orchestration lock · exclusive drive · Queued pool · **0.62.7** |
| **8** | Docs + residual + exit | WORK-DRAIN · MIGRATION · SD-019 named · **0.62.8** |
| **exit** | José judges | ✅ ADR Accepted · residual named · stamp `0.62.8` |

**Hard rule:** Do not ship `workers>1` as “done” before exclusive claim + reclaim.

---

## 8. Debt budget

| ID | Title | Stance |
|----|-------|--------|
| [SD-017](../TECH-DEBT.md#sd-017) | Claim not exclusive | **Pay floor** |
| [SD-018](../TECH-DEBT.md#sd-018) | Single-claimer by construction | **Pay growth** or name drive residual |
| [SD-019](../TECH-DEBT.md#sd-019) | Multi-process / multi-runtime shared claim needs CAS | **Name residual** |
| BI-013 residual | Session enrich + catalog packaging | Boy-scout if on path |
| BI-009 | Settings / profile / options | New knobs go through resolver |
| SD-016 | Ambient system DI | Boy-scout on new install paths |
| SI-014 | Plane-store framework | Do not pay whole; keep claim API clean |

**Already paid (do not re-litigate):** BI-013 home · plane-only drain · CS-006 · SD-015 · vitality eyes.

---

## 9. Multi-process decision (plan law)

**Do not support multi-process shared claim first.**

| Question | Answer |
|----------|--------|
| Support multi-process first? | **No.** Needs backend CAS Palm does not have yet. |
| Impact on multi-claim structure? | **Low** if durable claimer/lease fields exist; **high** if exclusivity is only a process lock with no lease shape. |
| Impact of ignoring multi-process this theme? | **Low** for one process + N workers + benchmarks. **Name** single drain owner per store. |

Shape floor so later CAS is a plug-in, not a rewrite.

---

## 10. Green bar

- Declared modes stay green on `just check` per slice.  
- Concurrent claim tests when claim lands.  
- `just guard-core` if core `WorkIntent` changes.  
- `just docs-check` when theme docs/version change.  
- No host drain dual path.

---

## 11. Risks

| Risk | Mitigation |
|------|------------|
| Orchestration rewrite scope creep | Floor = claim only; drive residual named |
| Coalesce + multi-claim races | Explicit tests in early slices |
| BI-009 knob explosion | Few knobs: workers, lease TTL, existing poll/batch/depth |
| “Done” at N threads without reclaim | Exit needs reclaim proof |
| Multi-process claimed too early | SD-019 residual; in-process first |

---

## 12. Exit judgment

José closes the theme when:

1. Exclusive claim + reclaim hold under concurrent claimers. ✅  
2. Default path stays correct at `workers=1`. ✅  
3. N workers (when shipped) are safe where claimed. ✅  
4. Vitality (or equivalent) can show honest 1 vs K. ✅  
5. Residual multi-process is **named**, not hidden. ✅ **SD-019**  
6. ADR-031 Accepted. ✅  
7. Spine green on declared modes. ✅  

**Exit is not** residual-zero or every growth row checked.

**Theme closed** at `0.62.8` (2026-08-04).  
**Not paid in 0.62:** multi-process shared claim CAS (**SD-019**); full seat DI (**SD-016**); surface deflation; Grove.

---

*Palm grows where the sun meets the sea.*  
*Safe claim. Honest pools. Residual named.*
