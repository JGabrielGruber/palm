# VISION 0.55 — Session plane (lifecycle + subscriptions)

**Status:** 📋 **Queued** — after [VISION-0.54](VISION-0.54.md) hermetic jobs dogfood.  
**Sequel:** [VISION-0.56](VISION-0.56.md) Workload plane (WorkloadEngine + runtimes) — session plane should land first for watches; late overlap OK.  
**Theme:** Treat the **session** as a first-class subject: lifecycle, multi-event subscriptions, optional storage projection — shared by Assist, dashboard, and composition.

> *Hermetic run-code proved the loop. Operators and dashboards both need to watch a session live — without each surface inventing wait/poll hacks.*

**ADR:** plan at `0.55.0` (session subscription contract; storage boundaries).  
**Builds on:** [EVENT-PLANE.md](EVENT-PLANE.md) · public event catalog (0.42) · Assist bind (0.32) · events WS (0.42).

---

## Intent

| Do | Don’t |
|----|--------|
| **Session** = durable subject (`instance_id`) with lifecycle | Firehose all jobs to every client |
| Multi-type **subscriptions** filtered by session/job | One-off Portal-only hacks |
| One spine for **Assist + dashboard + composition** | Separate “chat bus” vs “ops bus” |
| Thin **SessionService** (watch/list/projection) if product API needs it | God service owning orchestration |
| Optional **storage** for session projection / watch registry | Second source of truth vs instance/job |
| Public types + small payloads (ids, status, step) | Stream full stdout/bodies on the bus |

---

## Why now (after 0.54.10)

Dogfooding `hermetic-run-code` exposed the gap: long resource steps, Portal mid-wait, dashboard/ops wanting the same story. Fixes for auto-advance are necessary but not sufficient — Palm needs a **session subscription** primitive.

---

## Surfaces (same model)

| Surface | Use |
|---------|-----|
| **Assist / Portal** | After bind: fan-in progress; turn remains “what next” |
| **Dashboard / Explorer** | Watch many sessions or waiting fleet |
| **Composition / inbound** | Precise “when this session finishes” |
| **Events WS** | Generic multi-type + `filter.session_id` |

Not HTTP SSE as the product contract (WS + in-process handlers). MCP may stay poll/meta-tool.

---

## Slice sketch (lock at 0.55.0)

| Patch | Direction |
|-------|-----------|
| **0.55.0** | Plan + ADR: session lifecycle states, subscription filter, storage optional |
| **0.55.1** | Events WS / in-process watch: `filter.session_id` \| `job_id` |
| **0.55.2** | SessionWatch registry (common or execution) + tests |
| **0.55.3** | Assist bind → optional progress/event fan-in |
| **0.55.4** | Dashboard or REST “live waiting” dogfood |
| **0.55.5** | SessionService compose-in + optional projection store |

---

## Deferred (was interim 0.55)

**Living Library docs dogfood domain** (DocsService, corpora as process) → later minor (e.g. 0.56) after session plane lands. Static 0.52 tooling stays.

---

## Non-goals

- Replacing instance repository / job orchestration  
- Full CMS or docs product in this theme  
- Unfiltered global event dump to Portal  

---

## Depends on

- 0.54 hermetic jobs + run-code dogfood  
- Event plane: orchestration bus for job/flow lifecycle  
- Public event catalog  

## Horizon

Session plane is how humans **watch and walk** journeys. Long-term multi-palm presence and org-scale Assist routing aim at [**The Grove**](VISION-GROVE.md) (Palm Organization north star). Prefer subscription shapes that can later filter by session **and** open wait interest.

---

*Session is the human unit of work. Subscribe to its life.* 🌴📡
