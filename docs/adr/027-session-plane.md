# ADR-027 — Session plane (system glue, multi-instance)

**Status:** Proposed  
**Date:** 2026-07-30  
**Theme:** [VISION-0.58](../VISION-0.58.md)  
**Map:** [PALM.md](../PALM.md)  
**Supersedes (plan only):** watch-first sketch in [VISION-SESSION-PLANE](../VISION-SESSION-PLANE.md)

---

## Context

1. Palm has a named **system** layer ([ADR-026](026-palm-system-layer.md)): engines, ports, planes.  
2. **Event**, **work** (start), **wait** (continue), and **workload** planes exist or are scouting. **Session** has no system home (**SD-008**).  
3. Product and surfaces already use the word **session**. In code, `session_id` almost always **is** `instance_id`. That alias is a development shortcut, not architecture.  
4. Growth needs a subject that can hold **many instances** (many jobs over a walk): Assist continuity, cancel owned work, watches, later Grove affinity.  
5. Palm is not in production. We may break the alias. We must not invent a second resume law.  
6. Server bind can stay simple (cookie / header / WS bind). Transport is not the plane.

---

## Decision

### D1 — Session is a system plane

Session lifecycle and ownership live under **`palm.system`** (target package: `palm.system.planes.session`).  
Product services may expose thin handles. Product is **not** the source of session truth.

### D2 — Three distinct concepts

| Concept | Meaning |
|---------|---------|
| **Session** | Outside subject: one coherent external conversation / walk |
| **Instance** | Durable process record for a definition run |
| **Job** | Live orchestration unit |

A session may attach **zero or more** instances over time (**multi-instance**).  
Do not encode permanent 1:1 as law.

### D3 — Outside interaction binds a session

Surfaces (MCP, WS, HTTP, interactive CLI, composition edges that represent operator journeys) **create or bind** a session before they drive work.  
Bind transport may be cookie-like on the server. The plane still owns the record.

### D4 — Not a second continue path

Start remains **work plane**. Continue remains **wait plane** ([ADR-025](025-reactive-interests.md)).  
Session may **attribute**, **list**, and **watch** open waits and events. Session does **not** resume jobs by a private hook.

### D5 — Store is allowed and expected

The session plane may use a **store** (in-memory and/or durable via host storage).  
The store holds session records and attach lists. It is **not** a second job blackboard.  
A shared “every plane has one store framework” is **out of scope** for this ADR; design per plane until a later theme.

### D6 — Capable model from the start

Multi-instance attach, lifecycle (open / active / closed), and bind are in the **first** system design.  
Watches and rich product UI may come later in the same theme. They must not force a weak 1:1 core.

### D7 — Break aliases; record residual

Replace `session_id == instance_id` lies on paths the theme touches.  
List remaining consumers in [TECH-DEBT.md](../../TECH-DEBT.md) as **SI-*** (session impact).  
No long-lived dual-path shims for comfort.

### D8 — Not the user plane

No multi-user identity product, org presence, or Grove mesh in this decision.  
Optional opaque metadata on the session record is enough for later phenotypes.

---

## Consequences

### Positive

- One glue subject for surfaces, workloads, waits, and future walk.  
- Honest multi-instance growth.  
- Clear home next to other planes.  
- Server bind stays simple (cookie-like).

### Negative / cost

- Widespread rename and rebind of product/surface APIs.  
- Tests and dogfood that assumed session ≡ instance must change.  
- Temporary breakage until slices land (pre-1.0 accepted).

### Neutral

- Assist and FlowSession can remain **handles** after rebind.  
- `flow.session.*` event names may stay; payloads must gain real session attribution when ready.

---

## Alternatives considered

| Option | Why rejected |
|--------|----------------|
| Keep session ≡ instance | Blocks multi-instance and ownership; confuses Grove walk |
| Session only as product SessionService | Repeats dual-path; no system seat (fails ADR-026) |
| Watch-only theme first | Leaves bind law and multi-attach weak |
| Full user plane now | Scope explosion; not required for glue |
| Shared plane-store framework first | Blocks delivery; store per plane is enough now |

---

## Follow-up

- [x] Execute [VISION-0.58](../VISION-0.58.md) slices through **0.58.8** (bind + dogfood + WS + watches/fan-in).  
- [ ] Close **SD-008** at theme exit when residual SI honest.  
- [ ] Pay remaining **SI-*** (rename, explorer, docs) when edges are touched.  
- [ ] Accept this ADR at theme exit (or earlier if law is stable in code).

---

## References

- [ADR-025](025-reactive-interests.md) · [ADR-026](026-palm-system-layer.md) · [ADR-024](024-workload-engine.md)  
- [VISION-0.58](../VISION-0.58.md) · [VISION-GROVE](../VISION-GROVE.md) · [EVENT-PLANE](../EVENT-PLANE.md)  
- Live debt: [TECH-DEBT.md](../../TECH-DEBT.md)
