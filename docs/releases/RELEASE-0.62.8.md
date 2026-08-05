# Release 0.62.8 — Multi-claimer work drain (theme close)

**Date:** 2026-08-04  
**Package version:** `0.62.8` (`palmengine`)  
**Theme:** [VISION-0.62](../vision/closed/VISION-0.62.md) · [ADR-031](../adr/031-multi-claimer-work-drain.md) **Accepted**  
**Map:** [PALM.md](../PALM.md)  
**Migration:** [MIGRATION-0.62](../migrations/MIGRATION-0.62.md)  
**Previous stamp:** `0.61.13`

---

## Highlights

Palm has **safe in-process capacity** on the start path and the job-drive path.

- **Exclusive claim** — `claimed_by` / `lease_until` · reclaim · store lock (**SD-017**)  
- **Multi-claimer drain** — N plane workers (default 1) under supervisor  
- **Exclusive job drive** — orchestration membership lock · one drive owner per job  
- **QueuedScheduler pool** — `queued_workers` / `PALM_QUEUED_WORKERS` (default 1)  
- **Vitality proof** — `work_cycle` multi-claimer (`workers=K`)  
- **Honest residual** — multi-process shared claim needs CAS (**SD-019**)

**0.62 is closed.** Defaults remain single-worker. Claim pool and drive pool are independent knobs. Pools improve **overlap**, not “all host cores for Python patterns.”

---

## Upgrade

```bash
pip install -U palmengine==0.62.8
# or from this repo:
uv sync
```

Read [MIGRATION-0.62](../migrations/MIGRATION-0.62.md).

Optional concurrency:

```bash
export PALM_WORK_DRAIN_WORKERS=2   # claimers
export PALM_QUEUED_WORKERS=4       # job-drive pool (daemon/server)
```

---

## Breaking

Mild / pre-1.0:

- WorkIntent durable claim fields (`claimed_by`, `lease_until`).  
- Exclusive claim API requires claimer identity.  
- Double-drive of the same job is refused (`drive_job` → `False`).  
- **One continuous drain owner per work-intent store** until SD-019.

---

## Slice summary (0.62.0 → 0.62.8 + exit)

| Slice | Summary |
|-------|---------|
| 0.62.0 | Plan + ADR-031 Proposed + debt rows |
| 0.62.1 | Exclusive claim model (`claimed_by` / `lease_until` · store lock) |
| 0.62.2 | Reclaim / visibility timeout |
| 0.62.3 | Plane tick claimer identity + reclaim on poll · status heat |
| 0.62.4 | N drain workers (default 1) · settings |
| 0.62.5 | Drive-path honesty named (claim ≠ host cores) |
| 0.62.6 | Benchmark `work_cycle` multi-claimer (`workers=K`) |
| 0.62.7 | Orchestration exclusive drive + QueuedScheduler pool |
| 0.62.8 | **Theme exit** · ADR-031 Accepted · residual **SD-019** named · stamp |
| exit | José judged capacity proper (2026-08-04) |
