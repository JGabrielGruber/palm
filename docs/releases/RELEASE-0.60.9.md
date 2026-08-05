# Release 0.60.9 — System supervisor + work plane (theme close)

**Date:** 2026-08-01  
**Package version:** `0.60.9` (`palmengine`)  
**Theme:** [VISION-0.60](../vision/closed/VISION-0.60.md) · [ADR-029](../adr/029-system-supervisor.md) **Accepted**  
**Map:** [PALM.md](../PALM.md)  
**Migration:** [MIGRATION-0.60](../migrations/MIGRATION-0.60.md)  
**Previous stamp:** `0.59.8`

---

## Highlights

Palm’s **SystemInstance** owns reactive start and continuous services.

- **Work plane** — `runtime.work_plane` enqueue / tick / triggers / schedules  
- **Supervisor** — continuous `work_drain`, `outbox`, `inbound`  
- **Session attribution** on system default submit (inherit-or-service)  
- **Inbound** home under `palm.system.planes.work`  
- **Host** prefers system seats; packaging remains for product enrich and surfaces  

**0.60 is closed** for hostless reactive completeness. Residual host product wire and surface compost remain later seeds.

---

## Upgrade

```bash
pip install -U palmengine==0.60.9
# or from this repo:
uv sync
```

Read [MIGRATION-0.60](../migrations/MIGRATION-0.60.md).

---

## Breaking

Mild / pre-1.0:

- System phase table gains `system.supervisor.wire` and `system.background.start`.  
- Background skip reason may be `no_background_services_enabled` when neither drain nor outbox is enabled.  
- Prefer `palm.system.planes.work.inbound` (host re-export kept).

---

## Slice summary (0.60.0 → 0.60.9 + exit)

| Slice | Summary |
|-------|---------|
| 0.60.0 | Plan + ADR-029 Proposed |
| 0.60.1 | SystemSupervisor seat |
| 0.60.2 | WorkPlaneService attach |
| 0.60.3 | System job start default |
| 0.60.4 | Session attr on system path |
| 0.60.5 | Supervised work_drain |
| 0.60.6 | OutboxLoopService |
| 0.60.7 | Catalog reload_from_repository |
| 0.60.8 | Inbound on system |
| 0.60.9 | Lean seats without host |
| exit | ADR Accepted · BI-013 closed · stamp `0.60.9` |
