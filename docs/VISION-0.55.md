# VISION 0.55 — Reactive Interests (wait + trigger law)

**Status:** 📋 **Open** — `0.55.0` plan (this document + [ADR-025](adr/025-reactive-interests.md)).  
**Theme:** Make **start** and **continue** first-class under one reactive law — completers emit self-events; Palm matches **trigger interest** → WorkIntent and **wait interest** → resume. Nested flow cutover; second wait kind stub; inspect/doctor. Grove-shaped foundation.

> *Two verbs, one bus. Completers speak of themselves. Palm starts or continues.*

**ADR:** [025-reactive-interests.md](adr/025-reactive-interests.md) — **accept with 0.55.0**.  
**North star:** [VISION-GROVE](VISION-GROVE.md) §4 (Law of Reactive Interests).  
**Builds on:** [EVENT-PLANE](EVENT-PLANE.md) · [WORK-DRAIN](WORK-DRAIN.md) · nested child-wait · [VISION-0.54](VISION-0.54.md).  
**Sequel:** [VISION-0.56](VISION-0.56.md) Workload (place + peer; `kind=workload` waits) · [VISION-SESSION-PLANE](VISION-SESSION-PLANE.md) (queued watches).

**Replan note:** Former “0.55 Session plane” moved to [VISION-SESSION-PLANE.md](VISION-SESSION-PLANE.md) so the **law** lands before multi-surface watches and full workload product.

---

## 1. Why this theme now

| Pressure | Response |
|----------|----------|
| Nested flow “child reaches up to parent” | **Wait interest** on owner + event match |
| Long hermetic / future workload steps need park, not lock | Same continue path |
| WorkIntent plane already strong for **start** | Elevate as peer verb; shared event catalog |
| Grove needs remote peers later | Local law first: self-events + local interest |
| 0.56 WorkloadLeaf needs a socket | Second wait kind stub in 0.55 |

Without 0.55, workload and session risk inventing private resume paths.

---

## 2. Intent

| Do | Outcome |
|----|---------|
| **Law** of two verbs (start / continue) | Documented, tested, constitution-linked |
| **Wait interest** on parked job + instance | Durable, inspectable `{ kind, target_id, … }` |
| **Matcher** on `runtime.event` | Normative unpark / fail-owner policy |
| **Nested flow** on the wait plane | First production kind (`job` / child job target) |
| **WorkIntent / triggers** remain start path | Documented sibling; doctor shows both |
| **Second kind stub** (`workload` target + fake emit) | Proves grammar for 0.56 |
| Surfaces: inspect, list waiting, doctor, Assist fields | Humans/agents see *why* parked |
| Restart + idempotency | Long-term support |

---

## 3. Architecture (target)

```text
                    runtime.event
         (job.* · flow.session.* · resource.* · stub workload.*)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     Wait matcher                      Trigger path
     (open waits by target)            (TriggerRegistry / inbound)
              │                               │
              ▼                               ▼
     resume_job / fail                 WorkIntentStore → drain
     (owner job)                       → submit_flow (new job)
              │
              ▼
     Pattern yields WAITING_* / park
     interest on job + instance state
```

| Layer | Home |
|-------|------|
| Wait interest types + pure helpers | `palm/core/` and/or thin pure module (no I/O) |
| Open / index / match / complete + resume policy | `palm/common/` (e.g. `common/wait/` or graduate `child_wait`) |
| Bus subscription + host wire | Runtime hooks / workplane sibling |
| Nested flow adapter | Wizard bridges — open wait, no parent-resume in completer |
| Start path | Existing `WorkDrainService` + triggers + inbound |

**Completers** (child job, stub workload): emit self-lifecycle only.  
**Waiters**: open interest, park.  
**Palm**: match.

---

## 4. Wait interest contract (**locked 0.55.1**)

Serializable on owner job/instance state under key **`palm.wait.interests`**
(list of interest dicts). Module: [`palm.core.wait`](../src/palm/core/wait/).

```text
WaitInterest {
  v: 1                               # WAIT_INTEREST_SCHEMA_VERSION
  kind: "job" | "workload" | …       # WAIT_KIND_JOB | WAIT_KIND_WORKLOAD | …
  target_id: str                     # child job_id, workload_id, …
  opened_at: str                     # ISO-8601 UTC
  policy: { on_target_failed: "fail_owner" | "leave" }
  meta: { step_slug?, output_key?, … }  # pattern UX (opaque)
}
```

Helpers (pure, no I/O): `open_wait_interest` / `close_wait_interest` /
`list_wait_interests` / `open_wait_on_job` / `close_wait_on_job` /
`make_job_wait` / `make_workload_wait`.

- Owner job **parks** (existing lifecycle: e.g. `WAITING_FOR_INPUT` or documented park status) with interest present.  
- Matcher (0.55.2+): on event for `target_id` + kind → **resume** or **fail** owner per policy.  
- Optional target→owners **index** for O(1) match (may start as scan of live jobs).  
- PatternStatus: keep or generalize `WAITING_FOR_CHILD` as external wait (document; rename optional later).

---

## 5. Start path (affirm existing)

Unchanged architecture, first-class in this theme’s **story**:

```text
rule / inbound / schedule → WorkIntent → drain → new job
```

0.55 work: catalog alignment, doctor, docs — not a rewrite of WorkIntent.

---

## 6. Slice plan (lock at 0.55.0)

| Patch | Deliverable | Hardens |
|-------|-------------|---------|
| **0.55.0** | This VISION + ADR-025 accepted; STATUS/AGENTS/Grove links; session plane parked in VISION-SESSION-PLANE | Theme open |
| **0.55.1** | Wait interest type + open/close on job/state helpers + unit tests — **done** (`palm.core.wait`) | Contract |
| **0.55.2** | Matcher on `runtime.event` + resume/fail policy + contract tests — **done** (`palm.common.wait`) | Reaction |
| **0.55.3** | Nested flow **opens wait** when child starts; dual-path OK with existing hook — **done** | Migration |
| **0.55.4** | Normative unpark = matcher; ChildCompletionHook thin/compat; characterization green — **done** | Cutover |
| **0.55.5** | Inspect / Assist / list-waiting / doctor expose `waiting_on` — **done** | Surfaces |
| **0.55.6** | Instance rehydrate + restart mid-wait test; double-event idempotency — **done** | Durability |
| **0.55.7** | Second kind stub (`workload`) + emit ready/fail + contract test — **done** | Grove / 0.56 socket |
| **0.55.8** | EVENT-PLANE + WORK-DRAIN + AGENTS/ARCHITECTURE; trigger↔wait catalog — **done** | Constitution |
| **0.55.9** | Compat cleanup (or time-box), MIGRATION note if inspect breaks, theme exit | Close |

Execution starts at **0.55.1**. Adjust slice boundaries only with STATUS note.

---

## 7. Success criteria (theme exit)

1. Nested compositional wait dogfood works with **matcher** as normative unpark.  
2. Completer path does not require child to call parent resume APIs.  
3. Wait interest visible in inspect / list waiting / doctor.  
4. Restart mid-wait recovers interest and can still complete.  
5. Double completion does not double-corrupt owner.  
6. Target fail policy defined and tested for nested job kind.  
7. Second kind stub green (open wait → fake event → resume).  
8. Trigger → WorkIntent → new job still green; docs name both verbs.  
9. `just check` green; docs-check when surfaces change.  
10. [VISION-GROVE](VISION-GROVE.md) §4 reflected in ARCHITECTURE/AGENTS short form.

---

## 8. Non-goals (this minor)

- Full WorkloadEngine / runners / neonroot-as-runtime (→ **0.56**)  
- Full SessionService / WS watch product (→ [VISION-SESSION-PLANE](VISION-SESSION-PLANE.md))  
- Multi-palm org mesh / trust fabric (→ Grove later seasons)  
- Replacing WorkIntent with waits or waits with intents  
- Streaming multi-MB logs on the bus  

---

## 9. Relationship to Grove & neighbors

| Document | Relation |
|----------|----------|
| [VISION-GROVE](VISION-GROVE.md) | North star; 0.55 implements §4 law locally |
| [VISION-0.56](VISION-0.56.md) | Consumes wait kind `workload`; place/peer |
| [VISION-SESSION-PLANE](VISION-SESSION-PLANE.md) | Watches same events + open waits |
| [EVENT-PLANE](EVENT-PLANE.md) | Bus contract |
| [WORK-DRAIN](WORK-DRAIN.md) | Start verb |

**Complexity filter:** every 0.55.N slice must strengthen start, continue, match, inspect, or durability under the Law — or it is out of theme.

---

## 10. Open decisions (close during 0.55.1–0.55.4)

1. ~~Exact state key / serialization version for wait interest.~~ **Closed 0.55.1:** `palm.wait.interests` list; `v: 1`; pure types in `palm.core.wait`.  
2. JobStatus: reuse `WAITING_FOR_INPUT` vs introduce single park label (prefer **reuse + interest fields** unless Assist demands more).  
3. Fail policy defaults for nested job — **default locked:** `on_target_failed=fail_owner` (`leave` available). Nested cutover may refine.  
4. How long dual-path (hook + matcher) lasts (prefer gone by 0.55.4–0.55.9).  
5. Package name for matcher/coordination: prefer **`palm.common.wait`** in 0.55.2 (core stays pure interest + state_ops; graduate `child_wait` onto it later).

---

*Start with rules. Continue with waits. Match on the bus. Grow kinds without growing laws.* 🌴⚡
