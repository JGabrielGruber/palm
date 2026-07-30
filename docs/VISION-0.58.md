# VISION 0.58 — Session plane (system glue)

**Status:** 🚧 **Theme open** — through **0.58.18** (session operate + surface_view v2).  
**Close plan:** remaining slices **0.58.19–0.58.20** + **exit** named below (§6).  
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

### 4.3 Session owns surface context (0.58.14+)

**Law:** the **session** (via product **SessionService**) **owns** what surfaces need to operate.  
Surfaces do **not** invent dual slots (`active_system_*` + `active_assist_*` + private plane access) as truth.

**BoundSurface** (name locked in 0.58.14) is the surface handle shaped by the session door:

```text
BoundSurface
  session_id     # system subject (sess-… | sess-svc-…)
  instance_id    # continue focus under that session (or None)
  kind           # outside | service | host
  origin         # optional: mcp | cli | work-drain:{flow} | …
  metadata       # session-context facts (see §4.4) — not job blackboard
```

| Who | Owns |
|-----|------|
| **Session plane** | Record, attach list, exclusive ownership, active focus, service origins |
| **SessionService** | Bind / BoundSurface / enrich / gate / surface_view / session metadata |
| **Surface** | Transport of bind proof (cookie, header, WS, CLI slot); **not** a second identity model |
| **Job / instance** | Run state, waits, orchestration — job metadata stays **run** facts |

### 4.4 Session context metadata vs job metadata

Not everything belongs on **job** metadata.

| Home | Holds | Examples |
|------|-------|----------|
| **Session context metadata** | Walk / surface / attribution facts that outlive one job | `kind`, `origin`, last surface, UI prefs, client labels, “current walk” tags |
| **Job / instance metadata** | Facts of **this run** | definition id, pattern, wait interests, depth, per-run seed |
| **EventContext** | Moment of emit / effect | session_id + job_id + instance_id for inheritance |

**Rule:** if a fact is about **who is walking** or **how the outside subject is bound**, put it on the **session**.  
**Rule:** if a fact is about **this orchestration unit**, put it on the **job/instance**.  
**Rule:** do not duplicate ownership graphs into job meta — plane attach list is truth.

This is the seat for **BoundSurface** and for cleaning dual CLI/MCP context later (0.58.14+).

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
| **Product** | **SessionService** (0.58.12) — surface door. **BoundSurface** (0.58.14+) — session-owned surface context. Assist stays envelope; continue via instance under bound session |
| **Session metadata** | Walk/surface/attribution on session record (0.58.14+); job meta stays run facts only |
| **Watches** | Filter events and open waits by session (after bind + multi-attach work) |

**Server surface:** bind may look like a **cookie** (or header / WS bind op). That is transport. The plane is the truth.

---

## 6. Ordered work

Slices stay **one purpose each**. Numbers lock at execution; spirit is fixed.

### 6.1 Done (0.58.0–0.58.13)

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
| **14** | BoundSurface + session metadata | Session owns surface context; plane + SessionService metadata API — **0.58.14** ✅ (SI-016 seat) |
| **15** | Strict attribution | Start always sessioned; continue requires owner; bare orphan refuse — **0.58.15** ✅ (SI-015 residual) |
| **16** | Inherit-or-service | Reactive start inherits signal session or service origin — **0.58.16** ✅ (SI-011) |
| **17** | Single kit door + dogfood | `resolve_session_service` only; CLI/MCP/WS BoundSurface — **0.58.17** ✅ |

### 6.2 Remaining — close plan (lock order; implement one purpose each)

| Order | Slice | Spirit | Pays / residual | Done when |
|------:|-------|--------|-----------------|-----------|
| **14** | **BoundSurface + session metadata** | Session **controls** surface context. Product type: `session_id` + `instance_id` + `kind` + `origin` + session metadata API. Prefer session-context meta over stuffing walk facts into job meta. SessionService: `bind_surface` / `surface_from_*` / get-set session metadata. | Foundation for SI-001/006/010 usage; §4.3–4.4 · SI-016 seat | ✅ Surfaces hold one BoundSurface; session metadata round-trips on plane record |
| **15** | **Strict attribution policy** | When plane ready: **start** always has system session (outside or service); **continue** requires bound system session + owned instance (resolve allowed). Kill bare-instance happy path (SI-015 residual). Optional compat flag only if tests need a short window. | SI-015 residual ✅ | ✅ No product continue without attribution when plane attached (`PALM_SESSION_STRICT_ATTRIBUTION`) |
| **16** | **Inherit-or-service start** | Reactive WorkIntent: if signal carries session → inherit; else `ensure_service_session(origin)` (`work-drain:…` / `inbound:…` / `schedule:…`). Finish SI-011. Workloads still inherit job session only. | SI-011 ✅; SI-009 edge | ✅ Automated start always attributed; parent walks not stolen when context present |
| **17** | **Single kit door + surface dogfood** | Kit public helper → **SessionService** only (`resolve_session_service`). CLI / MCP / WS prefer BoundSurface; drop dual plane fallbacks on dogfood paths. | SI-005/006 partial; dual-path debt | ✅ Dogfood surfaces do not call `session_plane` for product verbs |
| **18** | **Session operate + surface_view v2** | Product verbs under session: focus (`set_active`), list owned waiting, cancel-owned (drive execution under gate — no private resume), richer `surface_view` (kind/origin/waiting/refs). Optional CQRS/catalog session queries (SI-007). | SI-007 partial; multi-instance operable | ✅ Operator can act on a session walk without inventing edge code |
| **19** | **Product vocabulary rename** | Paths / envelopes / grammar: continue segment is `instance` (or clear `instance_id`); `session_id` only system subject. Assist/MCP tools + REST aligned. Class names `FlowSession` may stay as thin handles (SI-002). | SI-001, SI-005 | Public contracts match 0.58.9 law; no silent instance-as-session on touched paths |
| **20** | **Docs, skill, residual honesty** | MCP skill + MCP.md + wiki: session ≠ instance; BoundSurface; service sessions. Explorer/SSR bind when cheap (SI-010); else **name residual** for SU-*. | SI-012; SI-010 honesty | Agents learn truth; STATUS residual SI list ready for exit |
| **exit** | **Theme exit** | Map true; residual SI honest; **SD-008 closed**; **ADR-027 Accepted**; `just check` green. | SD-008; ADR | Theme closed in STATUS/CHANGELOG |

**Implement rule:** do not skip 14 before 15–17 (BoundSurface is the seat).  
**Implement rule:** 19 is safer after 14–17 (rename with a real context object).  
**Implement rule:** 20 may land early on touch; must be complete before exit.  
**Not in close plan:** user plane, impersonation (D11), SI-014 plane-store framework, Grove mesh.

**Rule:** Do not ship “session is still just instance_id with a new name.”  
**Rule:** Do not invent session-resume that bypasses the wait plane.  
**Rule:** Session owns surface context; job meta is not a second session store.

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

1. [x] [PALM.md](PALM.md) shows session plane as **live** (not queued).  
2. [x] System package owns session plane (types, lifecycle, multi-attach).  
3. [ ] External entry on dogfood surfaces **requires** bind or create (strict policy **0.58.15**).  
4. [ ] `session_id` is not a silent alias of `instance_id` on dogfood paths (**0.58.19**).  
5. [x] Assist / MCP happy path uses the plane / SessionService.  
6. [x] BoundSurface + session metadata home live (**0.58.14**); [x] kit single door (**0.58.17**).  
7. [x] Automated start attributed (inherit-or-service **0.58.16**).  
8. [ ] SD-008 closed; residual SI/SU listed (**0.58.20** + exit).  
9. [ ] ADR-027 Accepted (exit).  
10. [ ] Path we touch stays testable (`just check`).

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
| **plan** | **Close plan locked (docs):** §4.3 BoundSurface / session owns surface context; §4.4 session vs job metadata; §6.2 remaining **0.58.14–0.58.20** + exit. No code in this plan row. |
| **0.58.14** | **BoundSurface + session metadata:** product `BoundSurface` (`session_id`, `instance_id`, `kind`, `origin`, metadata snapshot); SessionService `bind_surface` / `surface_from_*` / `get_metadata` / `merge_metadata` / `replace_metadata`; plane `get_metadata` / `merge_metadata` / `replace_metadata`; `surface_view` includes `bound_surface`. SI-016 seat (surface dogfood remains 0.58.17). |
| **0.58.15** | **Strict attribution:** plane `require_continue_attribution` + `SessionAttributionError`; SessionService `strict_attribution` (settings `session_strict_attribution` / `PALM_SESSION_STRICT_ATTRIBUTION`); gate injects owner from reverse index; bare orphan refuse on rewrite; product unknown id defers to 404; handoff auto-start inherits system session; assist product door unshadowed (`product_session` / `_session`). SI-015 residual closed. |
| **0.58.16** | **Inherit-or-service reactive start (SI-011):** triggers copy system `session_id` from event signal into WorkIntent; `SessionService.enrich_reactive_start` / `inherit_or_service_session` / `reactive_origin`; work-drain submit inherits parent walk or uses `work-drain:` / `schedule:` / `inbound:` service sessions; never random outside `sess-…` for reactive. Workloads still inherit job session only. |
| **0.58.17** | **Single kit door + surface dogfood:** kit `resolve_session_service` / `require_session_service` as only product door; `resolve_session_plane` system/tests only. MCP operator, WS assist/events, MCP in-process, CLI use SessionService + BoundSurface; no product plane dual-path. SI-005/006/016 partial (path rename → 0.58.19). |
| **0.58.18** | **Session operate + surface_view v2:** product `focus` / `clear_focus` / `list_owned_waiting` / `cancel_owned` / `cancel_all_owned` (system cancel under owner gate; no private resume); `surface_view` v2 (waiting, refs.job_id, actions catalog); operator paths `system/session/{id}/view|focus|cancel`. SI-007 partial (full CQRS contributor still optional). |

---

*Session is the outside subject. Bind it. Own many instances. Active is focus, not a pass. Session owns surface context. Grow Palm on one glue.* 🌴📡
