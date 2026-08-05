# Release 0.59.8 — System boot (theme close)

**Date:** 2026-08-01  
**Package version:** `0.59.8` (`palmengine`)  
**Theme:** [VISION-0.59](../vision/closed/VISION-0.59.md) · [ADR-028](../adr/028-system-boot.md) **Accepted**  
**Map:** [PALM.md](../PALM.md)  
**Migration:** [MIGRATION-0.59](../migrations/MIGRATION-0.59.md)  
**Previous stamp:** `0.58.20`

---

## Highlights

Palm has a **true boot schedule** and **truthful composition**.

- **Two schedules** — host + system phase tables walked in code  
- **CompositionProfile** — sole membership switch on the migrated path (services / surfaces / capabilities)  
- **Boot modes** — `safe` / `test` / `dev` / `prod` + shape presets; `ApplicationHost.for_mode`  
- **SystemLog** — ordered boot narrative (seats live; richer catalog residual)  
- **Break / harvest** — dual work_drain OR removed; residual **BI-*** named  

**0.59 is closed** for start control + membership truth. Residual **BI-*** remain (dual root, suite force, work start home, surface chrome, log catalog).

---

## Upgrade

```bash
pip install -U palmengine==0.59.8
# or from this repo:
uv sync
```

Read [MIGRATION-0.59](../migrations/MIGRATION-0.59.md) for membership gates and `for_mode`.

---

## Breaking

Mild / pre-1.0:

- Capability gates no longer OR deployment at phase time for work_drain.  
- Modes can skip recover / background.  
- Dead test DAG `options={"name": "quick"}` does not build (use spine wizard).

---

## Slice summary (0.59.0 → 0.59.8 + exit)

| Slice | Summary |
|-------|---------|
| 0.59.0 | Plan + ADR-028 Proposed + BI seed |
| 0.59.1 | Boot inventory + characterization |
| 0.59.1a | SystemLog basic |
| 0.59.2 | Stub schedule + BootMode |
| 0.59.3 | System schedule walked |
| 0.59.4 | Host schedule walked |
| 0.59.5 | Composition membership truth |
| 0.59.6 | Mode dogfood (`safe`/`test`) |
| 0.59.7 | Shape dogfood (dev/prod/cli/mcp/worker/server) |
| 0.59.8 | Residual cleanup (fixture + dead spine) |
| **exit** | ADR Accepted · SD-014 closed · migration · stamp `0.59.8` |

---

## Next

- Residual **BI-*** when touched (not a blank theme promise)  
- [VISION-SURFACE-DEFLATION](../vision/VISION-SURFACE-DEFLATION.md) for surface chrome  
- Grove / multi-Palm ([VISION-GROVE](../vision/VISION-GROVE.md)) when local control is enough  
