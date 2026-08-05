# Release 0.58.20 — Session plane (theme close)

**Date:** 2026-07-30  
**Package version:** `0.58.20` (`palmengine`)  
**Theme:** [VISION-0.58](../vision/closed/VISION-0.58.md) · [ADR-027](../adr/027-session-plane.md) **Accepted**  
**Map:** [PALM.md](../PALM.md)  
**Migration:** [MIGRATION-0.58](../migrations/MIGRATION-0.58.md)  
**Previous stamp:** `0.57.14`

---

## Highlights

Palm has a **true session plane** in the system layer.

- **Outside subject** — `session_id` (`sess-…` / service `sess-svc-…`); multi-instance attach; exclusive ownership  
- **Continue handle** — `instance_id`; path segment **`instance`** (legacy `session` may parse)  
- **BoundSurface** + **SessionService** — product door; kit `resolve_session_service`  
- **Active = focus only** — not a foreign pass; continue via **wait plane**  
- **Strict attribution** + **inherit-or-service** reactive start  
- **Operate** — focus, list waiting, cancel-owned under gate  
- **Agents taught** — skill / MCP / wiki: session ≠ instance  

**0.58 is closed** for structure. Residual **SI-*** / **SU-*** remain. Surface compost is named, not paid: [VISION-SURFACE-DEFLATION](../vision/VISION-SURFACE-DEFLATION.md).

---

## Upgrade

```bash
pip install -U palmengine==0.58.20
# or from this repo:
uv sync
```

Read [MIGRATION-0.58](../migrations/MIGRATION-0.58.md) for vocabulary and attribution breaks.

---

## Breaking

Yes — product paths and envelopes separate system `session_id` from continue `instance_id`. Soft-land on parse/alias is temporary. Pre-1.0 truth over comfort.

---

## Slice summary (0.58.0 → 0.58.20 + exit)

| Slice | Summary |
|-------|---------|
| 0.58.0 | Plan + ADR-027 + SI inventory |
| 0.58.1–5 | Plane seat → multi-attach → bind → job path → inspect |
| 0.58.6–8 | Dogfood → WS/cookie → watches / system journey |
| 0.58.9–11 | Vocabulary slash → active focus → owner gate |
| 0.58.12–13 | SessionService → service/origin sessions |
| 0.58.14–18 | BoundSurface → strict → inherit-or-service → kit door → operate |
| 0.58.19 | Product path rename (`instance`) |
| 0.58.20 | Docs/skill + residual honesty |
| **exit** | ADR Accepted · SD-008 closed · migration · stamp · surface vision named |

---

## Next

- Residual **SI-002** family / **SU-*** — optional; [VISION-SURFACE-DEFLATION](../vision/VISION-SURFACE-DEFLATION.md)  
- **[SD-014](../../TECH-DEBT.md#sd-014)** boot phases — later theme  
- Other named dogfoods / API·SDK docs when they unlock value  
- Grove / multi-Palm north star ([VISION-GROVE](../vision/VISION-GROVE.md))  
