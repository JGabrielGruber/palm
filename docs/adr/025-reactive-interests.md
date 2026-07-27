# ADR-025: Reactive Interests (wait + trigger)

## Status

**Accepted** — with **0.55.0** (canonical plan: [VISION-0.55](../VISION-0.55.md)).  
**North star:** [VISION-GROVE](../VISION-GROVE.md) §4.  
Supplements [EVENT-PLANE](../EVENT-PLANE.md) and existing work-drain / child-wait practice; does not remove WorkIntent.

## Context

1. Palm already has a strong **start** path: definition/inbound/schedule triggers → **WorkIntent** → drain → new job ([WORK-DRAIN](../WORK-DRAIN.md), host workplane).
2. **Continue** for nested flows exists as wizard child-wait: parent parks; completion often **reaches up** via parent job id on the child and `ChildCompletionHook` → `resume_parent_after_child`. Effective, but inverted: the completer knows the waiter.
3. Long steps (hermetic run-code, future workloads) need **park without locking** the process; blocking invoke is not the Grove shape.
4. [VISION-GROVE](../VISION-GROVE.md) requires: completers emit self-events; interest is explicit; Palm matches — so later peer palms need only trust + target id + events.
5. Former 0.55 “Session plane” is deferred ([VISION-SESSION-PLANE](../VISION-SESSION-PLANE.md)); watches must sit **on** this law, not before it.
6. Workload plane ([VISION-0.56](../VISION-0.56.md), [ADR-024](024-workload-engine.md)) needs a **wait kind socket**, not a second resume engine.

## Decision

### D1 — Two verbs on the orchestration bus

| Verb | Interest | Action |
|------|----------|--------|
| **Start** | Trigger interest (rule/binding/schedule) | Enqueue **WorkIntent** → drain → new job |
| **Continue** | Wait interest (on owner job + instance) | **resume_job** / fail owner per policy |

Both consume **`runtime.event`**. Same event may trigger both verbs.

### D2 — Completers announce themselves only

Lifecycle subjects emit self-describing events (`job_id` / target id, status, small payload). They do not own parent-resume logic as the normative path.

### D3 — Wait interest is durable on the waiter

Open wait records `{ kind, target_id, … }` on the parked owner job/instance. Matcher finds interest by target and resumes or fails the owner. Optional index by `target_id` is an implementation detail.

### D4 — Nested flow is the first wait kind

Target kind for child jobs (e.g. `job` + child `job_id`). Migrate nested wizard wait onto open-wait + matcher. Compatibility dual-path allowed briefly during 0.55; normative unpark is the matcher by theme close.

### D5 — WorkIntent remains the start unit

No merge of “resume” into WorkIntent kinds for v1. Triggers/inbound/schedules stay the start plane. 0.55 documents and doctors both paths as peers under the Law.

### D6 — Second kind stub in 0.55

A minimal `workload` (or equivalent) wait kind + synthetic lifecycle events proves extension. Full WorkloadEngine remains **0.56**.

### D7 — Layering

| Concern | Home |
|---------|------|
| Pure interest shape / validation | core-friendly pure types |
| Open / match / complete / policy | `palm/common` (wait coordination) |
| Bus wire, resume call | runtime hooks / host workplane |
| Pattern UX (prompts, step meta) | patterns (wizard first) |
| Start queue | existing work drain |

Core stays free of wizard and workload SDKs.

### D8 — Surfaces and Grove

Inspect, list-waiting, doctor, and Assist expose open wait interest. Designs must allow later filters by session **and** wait target ([VISION-SESSION-PLANE](../VISION-SESSION-PLANE.md), Grove walk).

## Consequences

### Positive

- One grammar for async continue; workload and peers plug in as kinds.  
- Removes long-term need for completer→waiter wiring.  
- Aligns start (already mature) with continue (now first-class).  
- Steers complexity toward [VISION-GROVE](../VISION-GROVE.md).

### Trade-offs

- Migration cost for nested flow characterization tests.  
- Dual-path complexity until cutover slices finish.  
- Must define fail/cancel and idempotent resume carefully.

### Follow-ons

- **0.56** WorkloadEngine emits real `workload.*`; leaf opens wait.  
- **Session plane** subscribes to same bus + wait fields.  
- Optional later: remote target ids across peer palms (trust theme).

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Only improve ChildCompletionHook | Keeps inverted dependency; poor Grove fit |
| WorkIntent kind `resume_job` for all continues | Confuses start queue with park/resume; weak instance affinity |
| Session plane before wait law | Watches without a clear wait model; reorder risk |
| Full workload engine inside 0.55 | Scope explosion; ADR-024 stays 0.56 |

## Checklist (theme exit — see VISION-0.55 §7)

- [x] Wait interest contract + pure open/close (`palm.core.wait`, 0.55.1)  
- [x] Matcher + resume/fail policy on bus (`palm.common.wait`, 0.55.2)  
- [x] Nested flow opens wait interest (dual-path with ChildCompletionHook, 0.55.3)  
- [x] Matcher normative for nested flow (BaseRuntime wire + job scan, 0.55.4)  
- [x] Doctor/inspect/list-waiting expose waiting_on (0.55.5)  
- [x] Wait interest on instance across restart (0.55.6 rehydrate + dogfood)  
- [x] Second kind stub (`workload` emit ready/fail, 0.55.7)  
- [x] Doctor/inspect both verbs (reactive_interests section, 0.55.5)  
- [x] Constitution docs EVENT-PLANE / WORK-DRAIN / AGENTS / ARCHITECTURE (0.55.8)  
- [x] Theme exit 0.55.9 — dual-path time-box + [MIGRATION-0.55](../migrations/MIGRATION-0.55.md)  
- [x] Wait/matcher characterization green at exit  

## Theme status

**Law closed** with **0.55.9** (inverted unpark removed). **0.55.10** seats structure as **`WaitPlaneService`** (continue plane peer of work-drain) — [VISION-0.55.10](../VISION-0.55.10.md).

## References

- [VISION-0.55](../VISION-0.55.md) · [VISION-GROVE](../VISION-GROVE.md) · [VISION-0.56](../VISION-0.56.md) · [VISION-SESSION-PLANE](../VISION-SESSION-PLANE.md)  
- [EVENT-PLANE](../EVENT-PLANE.md) · [WORK-DRAIN](../WORK-DRAIN.md) · [ADR-024](024-workload-engine.md)  
