# ADR-029 — System supervisor + work plane on SystemInstance

**Status:** Accepted  
**Date:** 2026-08-01  
**Accepted:** 2026-08-01 (theme exit `0.60.9`)  
**Theme:** [VISION-0.60](../vision/closed/VISION-0.60.md) (**closed**)  
**Map:** [PALM.md](../PALM.md)  
**Debt:** [BI-013](../../TECH-DEBT.md) ✅ closed at exit · residual host product wire  
**Release:** [RELEASE-0.60.9](../releases/RELEASE-0.60.9.md) · [MIGRATION-0.60](../migrations/MIGRATION-0.60.md)  
**Related:** [ADR-025](025-reactive-interests.md) · [ADR-026](026-palm-system-layer.md) · [ADR-027](027-session-plane.md) · [ADR-028](028-system-boot.md) · [WORK-DRAIN](../WORK-DRAIN.md)

---

## Context

1. Palm has **reactive interests** ([ADR-025](025-reactive-interests.md)): start (WorkIntent) and continue (wait).  
2. **Wait** is a first-class system plane on `BaseRuntime`.  
3. **Work** durable store and schedules live under `palm.system.planes.work`. Continuous drain, trigger wire, and inbound still live under `palm.app.host.workplane`.  
4. **Outbox** processor wires on system; the poll thread still lives on the host.  
5. **Boot** ([ADR-028](028-system-boot.md)) has host and system schedules. Background work drain is a **host** phase only.  
6. **Session** ([ADR-027](027-session-plane.md)) attributes reactive start; enrich still runs on host submit edges.  
7. Palm needs a **complete SystemInstance**: reactive traffic and continuous loops without host coordinators as owners of truth.  
8. Palm is pre-1.0. Structural churn is acceptable when homes are named.

---

## Decision

### D1 — Planes carry reactive traffic

| Plane | Verb | Role |
|-------|------|------|
| **Work plane** | Start | Triggers, schedules, enqueue, tick → new job |
| **Wait plane** | Continue | Interest match → resume / fail |

Verbs stay distinct. Do not encode resume as a WorkIntent kind.

### D2 — Supervisor carries continuous run

Introduce **`SystemSupervisor`** (name may lock as `runtime.supervisor`) on each system instance.

| Duty | Meaning |
|------|---------|
| Register | Continuous **system services** (`work_drain`, `outbox`, `inbound`, …) |
| Lifecycle | Start, stop, join on shutdown |
| Gates | Mode and composition membership |
| Status | Doctor / control / system log |

The supervisor does **not** invent start or continue law.  
It **runs** plane and processor APIs on a schedule or worker set.

### D3 — Work plane service on system

`WorkPlaneService` attaches on the system schedule (with wait and session).

| API spirit | Meaning |
|------------|---------|
| `attach` / `detach` | Bind store, schedules, event triggers, submit/able |
| `enqueue` | Accept WorkIntent |
| `tick` | Claim due intents (and optional schedules) |
| reload triggers | Arm rules from catalog feed |

Background drain is **not** a separate law owner.  
It is a supervised service that calls `work_plane.tick`.

### D4 — Inbound is a required system contract

Inbound (resource metadata → WorkIntent) is **system** traffic into the work plane.

| Part | Owner |
|------|-------|
| Enqueue contract | System (work plane / inbound collaborator) |
| Workers (poll / stream / debounce flush) | Supervised system service |
| HTTP routes / surface mount | Surfaces and kits — thin adapters |

Host must not be the only place that can accept inbound start.

### D5 — Job start is a system effect

Drain submits new jobs through the **system** path (executor and/or ExecutionPort job-start).  
Product execution services remain façades over the same path.  
Session attribution uses session plane law on that path.

### D6 — Host is packaging

| Host may | Host must not |
|----------|----------------|
| Walk composition root | Own work start law |
| Wire product and surfaces | Be the only continuous drain owner |
| Request background via mode/composition | Hide inbound as private coordinator glue |

Host coordinators thin to delegates or leave as slices land.

### D7 — System schedule seats

Grow system phases for supervisor wire and background start (ids lock in theme).  
Modes may skip background (safe / test). Composition selects which services register.

### D8 — Package homes

| Concern | Home |
|---------|------|
| Work plane | `palm.system.planes.work` |
| Supervisor | `palm.system.supervisor` (or `runtime` submodule) |
| Inbound contract | system (exact package in slice) |
| Continuous outbox | supervisor service over existing processor |
| Thin host handoff | `palm.app.host` |

### D9 — Break / harvest

Same method as [ADR-028](028-system-boot.md) D8 when moving paths.  
Spine and reactive law regressions fix in-theme.

---

## Consequences

### Positive

- SystemInstance can react without ApplicationHost as law owner.  
- One home for continuous loops (drain, outbox, inbound workers).  
- Clear map: planes = traffic; supervisor = continuous run.  
- Surfaces and product can thin against stable system contracts.  
- BI-013 and related tangles get a pay path.

### Cost

- Package and boot churn.  
- ExecutionPort / product submit rebind.  
- Dual-root and test hosts must attach new seats.  
- Temporary dual path only with slice id and kill condition.

### Neutral

- Wait plane stays; it does not fold into the start queue.  
- Surface deflation remains a later theme.

---

## Alternatives considered

| Option | Why not chosen as the main path |
|--------|----------------------------------|
| Host remains true owner of drain forever | Blocks hostless system and dual-root honesty |
| Merge wait into work queue | Breaks ADR-025; confuses start and continue |
| Plane owns threads with no supervisor | Duplicates lifecycle for outbox, inbound, drain |
| Supervisor replaces planes | Mixes traffic law with continuous run |
| Inbound stays host-only optional | Incomplete start plane; surfaces stay fat |

---

## Follow-up (theme)

- [x] Execute [VISION-0.60](../vision/closed/VISION-0.60.md) slices (0.60.1–0.60.9).  
- [x] Accept this ADR at theme exit.  
- [x] Update [PALM.md](../PALM.md), STATUS, TECH-DEBT, [MIGRATION-0.60](../migrations/MIGRATION-0.60.md).  
- [x] Host re-exports for inbound; product enrich path residual named.

---

## References

- Live code: `palm.system.planes.work`, `palm.system.planes.wait`, `palm.app.host.workplane`, host `background.work_drain` phase.  
- [VISION-0.60](../vision/closed/VISION-0.60.md) · [TECH-DEBT.md](../../TECH-DEBT.md) BI-013.
