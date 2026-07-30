# VISION — Session plane (historical queue note)

**Status:** ⚠️ **Superseded** by **[VISION-0.58](VISION-0.58.md)** (theme open at 0.58.0).  
**Do not** plan or implement from this file.

---

## Why this file remains

This note was the **queued** session theme after the 0.55 replan (wait law first).  
It was **watch- and subscription-first**.

**0.58** reframes session as **system glue**:

- bind law (no outside interaction without a session),  
- multi-instance ownership,  
- system home under `palm.system`,  
- watches as later slices on that plane.

Authoritative plan: **[VISION-0.58.md](VISION-0.58.md)** · ADR: **[027-session-plane.md](adr/027-session-plane.md)**.

---

## Historical intent (for archaeology only)

Treat session as a first-class subject: lifecycle, multi-event subscriptions, optional projection — shared by Assist, dashboard, and composition.

| Old slice spirit | Where it goes now |
|------------------|-------------------|
| Plan + ADR | **0.58.0** (done as VISION-0.58 + ADR-027) |
| Events WS / filter by session | **0.58** later watch / WS slices |
| SessionWatch registry | After bind + multi-attach |
| Assist fan-in | Assist dogfood slice |
| Dashboard dogfood | After plane exists (optional) |
| SessionService product | Thin product only; system plane is truth |

---

## Deferred further (unchanged)

Living Library **docs dogfood domain** (DocsService, corpora as process) → after session + workload foundations.

---

*See VISION-0.58. Session is the outside subject. Bind it. Own many instances.* 🌴📡
