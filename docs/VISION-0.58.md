# VISION 0.58 — Session plane (system glue)

**Status:** 🚧 **Theme open** at **0.58.0** (plan only).  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [PALM.md](PALM.md) — read first.  
**ADR:** [027-session-plane.md](adr/027-session-plane.md) **Proposed** (accept at theme exit or when law is stable in code).  
**Prior:** [VISION-0.57](VISION-0.57.md) system home (**closed**) · [VISION-0.55](VISION-0.55.md) reactive law · [VISION-SESSION-PLANE](VISION-SESSION-PLANE.md) (**superseded** by this file).  
**Debt:** [TECH-DEBT.md](../TECH-DEBT.md) — **SD-008** in theme · **SI-*** impact inventory.  
**North star:** [VISION-GROVE](VISION-GROVE.md).

---

## 1. Goal

Give Palm a **true session plane** in the **system** layer.

**Session** is the **outside subject**.  
No outside interaction runs without a session behind it.  
All surfaces **bind** a session.  
One session may own **many instances** (and their jobs).  
Session is the **glue** for Palm growth — not a weak alias for `instance_id`.

**Success:**

- [PALM.md](PALM.md) names session as a live plane with clear purpose.  
- System code has a home: `palm.system.planes.session` (path locked in early slices).  
- Surfaces and product **bind**; they do not invent lifecycle or private resume.  
- Multi-instance ownership is in the model from the start (capable, not weak).  
- Residual impact is listed in tech debt for later chew (SI-*).

This theme is **not** the user plane.  
This theme is **not** Grove multi-Palm mesh.  
This theme is **structure + bind law + multi-instance capability**.

---

## 2. Why now

1. **0.57** named the system and left **SD-008** open on purpose.  
2. Product words (`session_id`, Assist, FlowSession) already mean “conversation,” but they **collapse to `instance_id`**. That lie blocks growth.  
3. Workload, wait, and Grove walk need a **real subject** for affinity, cancel, and watch.  
4. Palm is **not** in production. We may break aliases. We must not ship more workarounds.  
5. The old queued note ([VISION-SESSION-PLANE](VISION-SESSION-PLANE.md)) was **watch-first**. We need **bind-first, multi-instance, system home**.

---

## 3. Non-goals

| Out of scope for 0.58 | Why |
|-----------------------|-----|
| Full multi-user / identity product | User plane later |
| Full dashboard fleet product | After plane exists |
| Grove peer mesh | Needs local session first |
| Replace wait / work / event laws | Session labels and groups; does not second-resume |
| Perfect plane-store framework for all planes | Note the need; do not block on a shared store framework |
| Keep `session_id == instance_id` forever | Development simplification; **break** for truth |
| Long-lived compat shims | Pre-1.0; delete dual paths |

---

## 4. Principles

Bind to [PALM.md](PALM.md) and ADR-027.

1. **Session is system traffic** — home under `palm.system`, not product as truth.  
2. **Session ≠ instance ≠ job** — three concepts.  
3. **Multi-instance is law** — one session may attach many instances over time.  
4. **Surfaces bind** — cookie-like on HTTP is enough for server; MCP/CLI/WS carry the same bind idea. Do not invent a second identity stack.  
5. **Product stays thin** — Assist / FlowSession are handles and policy over the plane.  
6. **Reactive law stays** — start/continue only via work + wait planes.  
7. **Capable, not weak** — store and multi-attach when needed; no 1:1 permanent trap.  
8. **Break for truth** — document impact (SI-*); pay in order; no paper over.  
9. **STE** for theme docs.

**Spirit:** Palm already waited for this seat. Deliver it properly. Do not fear the break.

---

## 5. Target shape

```text
Surface (MCP / WS / HTTP / CLI / composition edge)
        │  always: create or bind Session
        ▼
Session plane (system)     ← lifecycle, attach list, watch hooks
        │  owns 0..N instances (and thus jobs)
        ▼
Job path (spine)
  Definition → Pattern → Job ↔ Instance → effects → events
        │
        ├─ Work plane (start)
        ├─ Wait plane (continue)
        └─ Workload plane (place; owner.session_id becomes real)
```

| Piece | Target |
|-------|--------|
| **Session record** | Stable `session_id`, lifecycle, metadata, list of attached `instance_id`s |
| **Store** | Plane may use a store (memory first; durable when host storage allows). Same idea as instance manager — **not** a second source of job truth |
| **Bind** | Surface connection / request / client context points at `session_id` |
| **Product** | Thin SessionService later if needed; Assist stays envelope |
| **Watches** | Filter events and open waits by session (after bind + multi-attach work) |

**Server surface:** bind may look like a **cookie** (or header / WS bind op). That is transport. The plane is the truth.

---

## 6. Ordered work

Slices stay **one purpose each**. Numbers lock at execution; spirit is fixed.

| Order | Slice spirit | Result |
|------:|--------------|--------|
| **0** | Plan + map + ADR + debt impact | This file, ADR-027, PALM/STATUS/TECH-DEBT — **0.58.0** |
| **1** | System seat | Types + plane module + lifecycle API on system instance |
| **2** | Store + multi-attach | Session record persists; attach/detach instances (0..N) |
| **3** | Bind law on entry | Touched surfaces resolve session; kill silent instance-only happy paths where theme touches |
| **4** | Job path link | Create/attach instance under session; events can filter by session |
| **5** | Wait / inspect | Session → open waits / journey view (no private resume hooks) |
| **6** | Assist + MCP dogfood | palm_assist bind path uses system session |
| **7** | WS / cookie-like bind | Same contract; delete one-off reconnect hacks |
| **8+** | Watches / fan-in | Multi-type subscribe by session (old watch sketch) |
| **exit** | Theme exit | Map true; SD-008 closed; residual SI/SU honest; ADR Accepted |

**Rule:** Do not ship “session is still just instance_id with a new name.”  
**Rule:** Do not invent session-resume that bypasses the wait plane.

---

## 7. Relation to other themes

| Theme | Role |
|-------|------|
| **0.55** | Start / continue law — keep; session does not replace it |
| **0.56** | Workload ownership / cancel hooks become **consumers** of session |
| **0.57** | System home — session plane sits **in** it |
| **Old VISION-SESSION-PLANE** | Watch sketches only; **superseded** |
| **Grove** | Walk and affinity need this plane first |

---

## 8. Debt

| Register | Role |
|----------|------|
| [TECH-DEBT.md](../TECH-DEBT.md) | **SD-008** active in theme; **SI-*** impact inventory (chew later without full context) |
| SU-* | Surface bulk remains optional; bind paths pay when touched |

Add SI rows when analysis finds a consumer that must change later.  
Do not hide impact only in chat.

---

## 9. Risks

| Risk | Mitigation |
|------|------------|
| Collapse to instance again | Multi-attach in model from slice 2; tests refuse 1:1-only law |
| Second resume path | AGENTS / ADR: wait plane only for continue |
| Theme too large | Hard slice order; watches last |
| Store over-design | Session store first; shared plane-store framework later |
| Surface cookie drama | Treat cookie as bind transport; plane owns truth |

---

## 10. Exit criteria

Theme **0.58** closes when:

1. [ ] [PALM.md](PALM.md) shows session plane as **live** (not queued).  
2. [ ] System package owns session plane (types, lifecycle, multi-attach).  
3. [ ] External entry on dogfood surfaces **requires** bind or create.  
4. [ ] `session_id` is not a silent alias of `instance_id` on those paths.  
5. [ ] Assist / MCP happy path uses the plane.  
6. [ ] SD-008 closed; residual SI/SU listed.  
7. [ ] ADR-027 Accepted.  
8. [ ] Path we touch stays testable (`just check`).

---

## 11. Context preservation (agents)

At **each chunk**, update:

- [STATUS.md](../STATUS.md) — slice table, decisions, purpose, spirit  
- This VISION patch log  
- [TECH-DEBT.md](../TECH-DEBT.md) if new residual appears  

After compact, an agent reads: **STATUS → VISION-0.58 → ADR-027 → TECH-DEBT SI-*** → PALM.md.

---

## 12. Patch log

| Patch | What |
|-------|------|
| **0.58.0** | Plan + ADR-027 Proposed + map/STATUS/debt + supersede VISION-SESSION-PLANE + SI impact inventory |

---

*Session is the outside subject. Bind it. Own many instances. Grow Palm on one glue.* 🌴📡
