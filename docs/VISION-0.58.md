# VISION 0.58 — Session plane (system glue)

**Status:** 🚧 **Theme open** — through **0.58.13** (service / origin sessions).  
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
| Unified system boot phase table / composition as sole host truth | Real debt **[SD-014](../TECH-DEBT.md#sd-014)** — later theme; not this session theme |
| Keep `session_id == instance_id` forever | Development simplification; **break** for truth |
| Long-lived compat shims | Pre-1.0; delete dual paths |

---

## 4. Principles

Bind to [PALM.md](PALM.md) and ADR-027.

1. **Session is system traffic** — home under `palm.system`, not product as truth.  
2. **Session ≠ instance ≠ job** — three concepts.  
3. **Multi-instance is law** — one session may attach many instances over time.  
4. **Exclusive ownership** — one instance has at most one owning session (reverse index).  
5. **Active is focus, not a pass** — `active_instance_id` picks continue **inside** the owner attach list only.  
6. **Surfaces bind** — cookie-like on HTTP is enough for server; MCP/CLI/WS carry the same bind idea. Do not invent a second identity stack.  
7. **Product stays thin** — Assist / FlowSession are handles and policy over the plane.  
8. **Reactive law stays** — start/continue only via work + wait planes.  
9. **Capable, not weak** — store and multi-attach when needed; no 1:1 permanent trap.  
10. **Break for truth** — document impact (SI-*); pay in order; no paper over.  
11. **STE** for theme docs.

**Spirit:** Palm already waited for this seat. Deliver it properly. Do not fear the break.

### 4.1 Ownership vs active focus (0.58.10)

These are **two different laws**. Do not collapse them.

| Concept | Meaning | Enforced where |
|---------|---------|----------------|
| **Owner session** | Session that **owns** the instance (attach + reverse index) | Plane: attach refuses dual owner; one instance → one session |
| **Active instance** | Continue **focus** among instances this session already owns | Plane: `active_instance_id` on the record; resolve prefers it |

```text
sess-A owns inst-1, inst-2     active → inst-2
sess-B cannot attach inst-1    (already owned by A)
sess-B cannot set_active(inst-1)
resolve(sess-A) → only inst-1 | inst-2
resolve(sess-B) → never inst-1
```

**Active is not a workaround** to drive instances under a session that does not own them.  
Cross-session drive is **out of law**.

**Intended continue path:**

1. Surface **binds** `session_id` (system subject).  
2. Plane **resolves** continue instance: active → open wait → last attached (all on attach list).  
3. Or client passes `instance_id` that **belongs** to the bound session.  
4. **Owner gate (0.58.11 / SI-015):** when a system session is bound, refuse continue if the instance is not on that attach list (`require_owned_instance`).  
5. Continue still goes through the **wait plane** (no session-private resume).

**Refuse:** bound session S + instance I when I is not attached to S — **enforced** at rewrite + product continue (0.58.11).  
**Residual:** bare `instance_id` with **no** bound system session still skips the gate (legacy tooling until SI-001 / surface bind complete).

### 4.2 Outside bind vs service session (0.58.13)

| Kind | Who | Id shape | When |
|------|-----|----------|------|
| **Outside session** | Human / agent surface (MCP, HTTP, CLI, WS) | `sess-{uuid}` via **bind** | Each outside walk |
| **Service session** | Automated / internal start (work drain, schedules, host) | Stable `sess-svc-{origin}` | Same origin reuses one owner |
| **Host session** | Runtime seat | `sess-svc-host` | Opened at runtime start |

**Policy:**

1. Outside interaction still **binds** (D3).  
2. Automated **start** is not “no session” — it uses a **service session** so attach, cancel, and watch stay honest (SI-011).  
3. Prefer **origin** grouping (`work-drain:{flow}`) over one mega root for all automation.  
4. Workloads **inherit** the job’s session (EventContext / metadata). Do not invent a parallel workload session type.  
5. Active focus on a service session is legal but often weak (many scheduled instances); operators should set focus or pass `instance_id` when continuing service-owned work.

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
| **Session record** | Stable `session_id`, lifecycle, metadata, ordered `instance_ids`, **`active_instance_id`** focus (0.58.10) |
| **Ownership** | Reverse index: instance → owner session; exclusive attach |
| **Store** | Plane may use a store (memory first; durable when host storage allows). Same idea as instance manager — **not** a second source of job truth |
| **Bind** | Surface connection / request / client context points at `session_id` |
| **Product** | **SessionService** (0.58.12) — surface door over the plane: bind, continue target, submit enrich, journey, event filter. Assist stays envelope; continue via instance under bound session |
| **Watches** | Filter events and open waits by session (after bind + multi-attach work) |

**Server surface:** bind may look like a **cookie** (or header / WS bind op). That is transport. The plane is the truth.

---

## 6. Ordered work

Slices stay **one purpose each**. Numbers lock at execution; spirit is fixed.

| Order | Slice spirit | Result |
|------:|--------------|--------|
| **0** | Plan + map + ADR + debt impact | This file, ADR-027, PALM/STATUS/TECH-DEBT — **0.58.0** ✅ |
| **1** | System seat | Types + plane module + lifecycle API on system instance — **0.58.1** ✅ |
| **2** | Store + multi-attach | Session record persists; attach/detach instances (0..N) — **0.58.2** ✅ |
| **3** | Bind law on entry | Touched surfaces resolve session; kill silent instance-only happy paths where theme touches — **0.58.3** ✅ |
| **4** | Job path link | Create/attach instance under session; events can filter by session — **0.58.4** ✅ |
| **5** | Wait / inspect | Session → open waits / journey view (no private resume hooks) — **0.58.5** ✅ |
| **6** | Assist + MCP dogfood | palm_assist bind path uses system session — **0.58.6** ✅ (product session_id still instance handle) |
| **7** | WS / cookie-like bind | Same contract; delete one-off reconnect hacks — **0.58.7** ✅ |
| **8** | Watches / fan-in | Multi-type subscribe by session — **0.58.8** ✅ |
| **9** | Vocabulary slash | One name: `session_id` = system; `instance_id` = continue; delete duals — **0.58.9** ✅ |
| **10** | Active instance on record | Plane-owned `active_instance_id`; resolve prefers focus — **0.58.10** ✅ |
| **11** | Owner gate on continue | Bound session must own instance (SI-015) — **0.58.11** ✅ |
| **12** | Product SessionService | Surface door: no reinvent plane access; helpers for other services — **0.58.12** ✅ |
| **13** | Service / origin sessions | Automated start (work drain) + host seat use stable service sessions — **0.58.13** ✅ (SI-011 partial) |
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

### 7.1 Growth later (do not break ownership law)

**0.58 does not ship multi-user identity.** Optional session metadata is enough for now ([ADR-027](adr/027-session-plane.md) D8).

When a **user plane** (or admin product) exists, maturity must **extend** ownership — not dissolve it:

| Need | Wrong approach | Right approach (seed) |
|------|----------------|------------------------|
| Support agent helps a human mid-flow | Let agent session drive foreign `instance_id` | **Impersonate / act-as** the **owning** session (or a granted delegate), with audit |
| Admin inspects any instance | Drop owner checks on product paths | Elevated **inspect** role; write still under owner session or explicit grant |
| Shared team walk | Two sessions own one instance | Shared **session membership** or **delegate tokens** — still one owner record, many principals |
| Grove peer affinity | Peer invents a second owner | Peer carries owner `session_id`; local plane is truth |

**Session impersonation (future theme seed):** a principal is allowed to **bind or act as** an existing session under policy (user, role, grant, time bound). The plane still sees one owner session and one attach list. Impersonation is **identity policy**, not “session B owns instance of session A.”

Record: [TECH-DEBT.md](../TECH-DEBT.md) later-theme seeds · **SI-015** paid at **0.58.11** (bare-instance residual noted).

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
| Active used as foreign pass | Active only on attach list; SI-015 owner gate (0.58.11) |
| Second resume path | AGENTS / ADR: wait plane only for continue |
| Theme too large | Hard slice order; watches last |
| Store over-design | Session store first; shared plane-store framework later |
| Surface cookie drama | Treat cookie as bind transport; plane owns truth |
| Soften ownership for “admin UX” | Prefer impersonation / grant themes later; do not dual-own instances |

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
| **0.58.1** | System seat: `planes.session` types + lifecycle; **StorageEngine** store; `BaseRuntime.session_plane` |
| **0.58.2** | Multi-attach: `attach_instance` / `detach_instance` / `session_for_instance`; reverse key `palm:session:by_instance:*`; OPEN→ACTIVE on first attach; one instance → one session |
| **0.58.3** | Bind law: `SessionPlaneService.bind` / `require_open` / `SessionBind`; `ApplicationHost.bind_session`; CLI `active_system_session_id` distinct from product assist/instance |
| **0.58.4** | Job path: `ProcessInstance.session_id`; job metadata `session_id`; `SessionOwnershipHook` plane attach; `EventContext.session_id` + `flow.session.*` payload fields |
| **0.58.5** | Journey: `SessionPlaneService.inspect` / `list_waiting`; host `inspect_session`; no session-resume path |
| **0.58.6** | Dogfood: `FlowExecutionService` auto-bind system session on submit; Assist start dogfood |
| **0.58.7** | WS/cookie bind: `op: bind` + `X-Palm-Session` / `palm_session` cookie → session plane; flow create Set-Cookie; fix name-vs-id create (`todo-builder`) |
| **0.58.8** | Watches: plane `event_matches` / `make_event_filter`; Events WS fan-in; `resolve_continue_instance` + path rewrite; `system/session/{id}` inspect; workload owner session from EventContext |
| **0.58.9** | **Vocabulary slash:** edge + job meta `session_id` = system subject only; continue handle = `instance_id`; delete `system_session_id` / `palm_session_id` duals; plane resolve when only session given; product internal paths still resolve `sess-…` (SI-001 residual class names) |
| **0.58.10** | **Active instance:** `SessionRecord.active_instance_id`; set on attach; `set_active_instance` / `clear_active_instance`; `resolve_continue_instance` = active → waiting → last; inspect/bind expose focus. **Docs:** ownership exclusive; active = focus only; residual bare-instance gate = SI-015; future impersonation seed (user plane) without dual-own |
| **0.58.11** | **Owner gate (SI-015):** `owns_instance` / `require_owned_instance` / `InstanceNotOwnedError`; operator rewrite + flows/assist continue gate when system `session_id` bound; host `require_session_owns_instance`; WS `session_owner` error code. Path instance is authoritative (not replaced by plane focus). Bare instance without bound session remains residual. |
| **0.58.12** | **Product SessionService:** `palm.services.session.SessionService` as surface door (bind, continue_target, enrich_submit_body, surface_view, event filter, owner gate helpers). Host `session` slot; composition core includes session; flows/assist/MCP prefer service over scattered plane access. Plane remains law — service does not resume. SI-001 path/handle rename still residual. |
| **0.58.13** | **Service / origin sessions (SI-011 partial):** stable `sess-svc-{origin}` for automated start; well-known host `sess-svc-host` at runtime start; work drain enriches `work-drain:{target}`; `SessionService.ensure_service_session` / `enrich_submit_body(origin=…)`. Outside surfaces still mint random `sess-…`. **Not** one junk-drawer root for all jobs. Workloads inherit job session (no separate workload session type). |

---

*Session is the outside subject. Bind it. Own many instances. Active is focus, not a pass. Grow Palm on one glue.* 🌴📡
