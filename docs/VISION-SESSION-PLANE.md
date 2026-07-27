# VISION — Session plane (lifecycle + subscriptions)

**Status:** 📋 **Queued** — after [VISION-0.55](VISION-0.55.md) **Reactive Interests**.  
**Was:** interim plan for minor 0.55; **replanned** July 2026 so wait/start law lands first ([VISION-GROVE](VISION-GROVE.md)).  
**Likely minor:** **0.57+** (or late overlap with workload theme) — lock number at that theme’s `X.0`.

**Sequel context:** [VISION-0.56](VISION-0.56.md) Workload · [VISION-GROVE](VISION-GROVE.md) Grove north star.

---

## Theme

Treat the **session** as a first-class subject: lifecycle, multi-event subscriptions, optional storage projection — shared by Assist, dashboard, and composition.

> *Hermetic run-code proved the loop. Operators and dashboards both need to watch a session live — without each surface inventing wait/poll hacks.*

**Builds on:** [EVENT-PLANE.md](EVENT-PLANE.md) · [VISION-0.55](VISION-0.55.md) wait interest inspect · public event catalog · Assist bind · events WS.

---

## Intent

| Do | Notes |
|----|--------|
| **Session** = durable subject (`instance_id`) with lifecycle | |
| Multi-type **subscriptions** filtered by session/job **and open wait interest** | Grove-shaped |
| One spine for Assist + dashboard + composition | |
| Thin SessionService if product API needs it | |
| Optional storage for projection / watch registry | Not second source of truth vs instance/job |
| Public types + small payloads | |

---

## Surfaces

| Surface | Use |
|---------|-----|
| Assist / Portal | After bind: fan-in progress; turn remains “what next” |
| Dashboard / Explorer | Watch many sessions or waiting fleet |
| Composition / inbound | Precise “when this session finishes” |
| Events WS | Multi-type + `filter.session_id` / wait targets |

---

## Slice sketch (re-lock at theme open)

| Patch | Direction |
|-------|-----------|
| **X.0** | Plan + ADR: session lifecycle, subscription filter, storage optional |
| **X.1** | Events WS / in-process watch: session_id \| job_id \| wait target |
| **X.2** | SessionWatch registry + tests |
| **X.3** | Assist bind → progress/event fan-in |
| **X.4** | Dashboard or REST live waiting dogfood |
| **X.5** | SessionService compose-in + optional projection |

---

## Deferred further

Living Library **docs dogfood domain** (DocsService, corpora as process) → after session + workload foundations.

---

*Session is the human unit of work. Subscribe to its life — including its waits.* 🌴📡
