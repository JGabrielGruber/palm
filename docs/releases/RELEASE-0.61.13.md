# Release 0.61.13 — Living-kernel vitality (theme close)

**Date:** 2026-08-04  
**Package version:** `0.61.13` (`palmengine`)  
**Theme:** [VISION-0.61](../vision/closed/VISION-0.61.md) · [ADR-030](../adr/030-system-vitality.md) **Accepted**  
**Map:** [PALM.md](../PALM.md)  
**Migration:** [MIGRATION-0.61](../migrations/MIGRATION-0.61.md)  
**Previous stamp:** `0.60.9`

---

## Highlights

Palm has **first-class eyes** on the living system process.

- **`palm.system.vitality`** — seat discovery, seat reports, projection + registry  
- **Inspect door** — `InspectService` presents top / vitality / benchmark (**SD-007**)  
- **Doctor & host status demoted** — anatomy / packaging residual (**OD-001**, **CS-002**)  
- **Load eyes** — `process_resources`, `loaded_bulk`, `benchmark` (human CLI units)  
- **Neighbor residuals paid under theme** — plane-only work drain; shared product packaging (BI-003 floor)

**0.61 is closed.** Residual BI-015, SD-016, enrich/catalog packaging, surface deflation, and `monitor_agent` remain later work — not unfinished eyes.

---

## Upgrade

```bash
pip install -U palmengine==0.61.13
# or from this repo:
uv sync
```

Read [MIGRATION-0.61](../migrations/MIGRATION-0.61.md).

---

## Breaking

Mild / pre-1.0:

- Prefer `host.inspect` over product `SystemService` as the operate door.  
- Doctor reports are `legacy_doctor` anatomy packaging; living counters come from vitality.  
- Host triple-status methods are packaging residual, not load law.  
- Host `WorkDrainService` removed — use `runtime.work_plane` only.

---

## Slice summary (0.61.0 → 0.61.13 + exit)

| Slice | Summary |
|-------|---------|
| 0.61.0 | Plan + ADR-030 Proposed |
| 0.61.1 | Seat report + dynamic walk |
| 0.61.2 | Projection + registry (`seat_walk`) |
| 0.61.3 | Emission window + actor_kind |
| 0.61.4 | InspectService rename (SD-007) |
| 0.61.5 | Inspect top/vitality present |
| 0.61.6 | Doctor demotion (OD-001) |
| 0.61.7 | Host status compost (CS-002) |
| 0.61.8 | `process_resources` |
| 0.61.9 | `loaded_bulk` |
| 0.61.10 | `benchmark` tool |
| 0.61.11 | Inspect + CLI present for benchmark |
| 0.61.12 | Human CLI units + deeper recipes |
| 0.61.13 | BI-003 product packaging floor + **theme exit** |
| exit | ADR-030 Accepted · residual named · stamp `0.61.13` |
