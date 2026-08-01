# VISION 0.60 — System Supervisor + Work Plane

**Status:** 📋 **Theme open** at **0.60.0** (plan).  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [PALM.md](PALM.md) — read first.  
**ADR:** [029-system-supervisor.md](adr/029-system-supervisor.md) **Proposed**.  
**Debt:** [BI-013](../TECH-DEBT.md) (pay) · host workplane / inbound / outbox continuous re-home · dual-root attach (**BI-003** edges).  
**Prior closed:** [VISION-0.59](VISION-0.59.md) boot · [VISION-0.58](VISION-0.58.md) session · [VISION-0.57](VISION-0.57.md) system · [VISION-0.55](VISION-0.55.md) reactive law.  
**Queue later:** [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) · user plane · Grove.  
**North star:** [VISION-GROVE](VISION-GROVE.md).

---

## 1. Goal

Make **`SystemInstance` complete for reactive work**.

| Seat | Role |
|------|------|
| **Work plane** | Start traffic: store, schedules, triggers, enqueue, tick |
| **Wait plane** | Continue traffic (already on system) |
| **Session plane** | Attribution (already on system) |
| **Supervisor** | Continuous services: lifecycle, mode gates, status |
| **Inbound (system)** | Required contract into the work plane + supervised workers |
| **Execution path** | Job start (and resume) as system effects |

**Host** stays packaging: composition, product, surfaces.  
Host does **not** own start law or continuous loops.

**Success:**

- A started system arms triggers, accepts inbound, drains in background, starts and continues jobs, attributes session.  
- Truth does **not** require `WorkPlaneCoordinator` or host-only drain.  
- Doctor and system log report supervisor + plane status.  
- Residual chrome is named; spine stays honest.

This theme pays structural debt so Palm can grow.  
It is **not** surface compost.  
It is **not** Grove mesh.

---

## 2. Why now

1. **Reactive law** is landed (0.55). **Wait** is a system plane. **Start** data lives under `planes/work`; continuous drain still sits on the host.  
2. **Session** (0.58) attributes reactive start; the wire still passes through host product edges.  
3. **Boot** (0.59) gave schedules, modes, and membership. Continuous seats still hang on host phases only.  
4. **BI-013** names the residual: work start on host workplane. True owner is system.  
5. Inbound, outbox poll, and work drain share one kind of problem: **continuous system service**.  
6. Lean runtimes, dual root, and later surfaces need a **complete local organism**.

---

## 3. Non-goals

| Out of scope for 0.60 | Why |
|-----------------------|-----|
| Full surface purge (explorer / MCP dual stack) | [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) |
| Merge wait into WorkIntent kinds | [ADR-025](adr/025-reactive-interests.md) — two verbs stay distinct |
| User plane | Later seed |
| Grove multi-Palm remote interests | Needs local completeness first |
| Full workload placement remainder | Only edges that touch supervisor / ports |
| One global middleware list | HTTP ≠ job hooks ≠ plane law ≠ supervisor loops |
| Fake-success chrome always green mid-theme | Declared green bar only |

---

## 4. Principles

Bind to [PALM.md](PALM.md), [ADR-025](adr/025-reactive-interests.md), [ADR-028](adr/028-system-boot.md), and ADR-029.

1. **Reactive interests** — one law; two verbs (start and continue).  
2. **Planes** carry traffic. **Supervisor** carries continuous run.  
3. **Inbound is required** on system — signal → WorkIntent is not optional host furniture.  
4. **Background drain** is a supervised service over `work_plane.tick`.  
5. **Job start** is a system effect. Product is a façade.  
6. **Composition and mode** choose membership. System owns the seats.  
7. **System schedule** grows seats (`supervisor.wire`, `background.start`, …).  
8. **Host thins** — coordinators become delegates or leave.  
9. **Break / harvest** — same posture as 0.59 when paths move.  
10. **STE** for theme docs.

**Spirit:** A complete system node beats a clever host bag.

---

## 5. Target shape

### 5.1 Seats on SystemInstance

```text
SystemInstance
  .event
  .work_plane          # start  (WorkPlaneService)
  .wait_plane          # continue (exists)
  .session_plane       # exists
  .supervisor          # continuous services
       work_drain  → work_plane.tick
       outbox      → processor
       inbound     → workers → enqueue
  .execution / executor / engines
```

### 5.2 Vocabulary

| Term | Meaning |
|------|---------|
| **Work plane** | Start traffic seat |
| **Wait plane** | Continue traffic seat |
| **Supervisor** | Lifecycle and status for continuous system services |
| **System service** (supervised) | One loop or worker set (`work_drain`, `outbox`, `inbound`, …) |
| **Inbound contract** | System API: enqueue path + worker lifecycle feeding the work plane |
| **Host** | Composition root, product, surfaces |

### 5.3 Boot (system schedule growth)

Illustrative seats (ids lock in early slices):

```text
system.planes.attach          # wait, session, work
system.supervisor.wire        # register services from options / membership
system.ready
system.background.start       # mode may skip (safe / test)
```

Host may still request phenotype. Supervisor lives on the system instance.

### 5.4 Package homes (intent)

| Concern | Home (target) |
|---------|----------------|
| Work plane service | `palm.system.planes.work` |
| Wait plane | `palm.system.planes.wait` (exists) |
| Supervisor | `palm.system.supervisor` (or under `runtime`) |
| Inbound system contract | `palm.system.planes.work` collaborator or `palm.system.inbound` |
| Job start on port | `palm.system.ports.execution` + executor |
| Host thin handoff | `palm.app.host` delegates only |

System schedule must not import product or surfaces.

---

## 6. Ordered work

Slices stay **one purpose each**. Numbers may gain `a`/`b` sub-slices.

| Order | Slice spirit | Result |
|------:|--------------|--------|
| **0** | Plan + map + ADR | This file · ADR-029 Proposed · STATUS · PALM pointer · BI-013 theme — ✅ **0.60.0** |
| **1** | Supervisor seat | Registry, start/stop/status, boot hooks; empty services OK — ✅ **0.60.1** |
| **2** | Work plane service | `WorkPlaneService` · `runtime.work_plane` · attach · tick/enqueue over existing store — ✅ **0.60.2** |
| **3** | System job start | Drain submits via executor / ExecutionPort (product façade later) |
| **4** | Session-safe start | Reactive attribution on system path (0.58 law, system wire) |
| **5** | Supervised work drain | Background loop · system phase · mode skip |
| **6** | Outbox continuous | Supervisor owns poll; host thread path thins |
| **7** | Catalog feed · triggers | Reload arms on work plane |
| **8** | Inbound system contract | Required enqueue + supervised workers |
| **9** | Host deflate · dual root | Coordinators thin; lean roots attach planes + supervisor |
| **exit** | ADR Accepted · debts closed or residual named · stamp · migration if needed | |

---

## 7. Debt this theme pays

| Debt / tangle | Theme action |
|---------------|--------------|
| **BI-013** | Work start + continuous drain on system |
| Host `WorkPlaneCoordinator` as law owner | Deflate to delegate or remove |
| Outbox processor on system / thread on host | Continuous under supervisor |
| Inbound host-only (CF-011 family) | System contract |
| **BI-003** edges | Dual root attaches same system seats where spawn exists |
| ExecutionPort without job start | Expand as slices need |

Surface SU-* and full suite force (BI-007) stay residual unless a slice touches them.

---

## 8. Mid-theme green bar

| Track | Mid-theme | Exit |
|-------|-----------|------|
| Spine (`safe` / `test` + job path) | Green (or recover same slice) | Green |
| Explicit `tick` work path | Green early | Green |
| Background drain modes | May lag | Green on declared modes |
| Inbound contract | After slice 8 | Green dogfood |
| Host coordinator removal | May lag | Done or residual named |
| Heavy surfaces | May fail; harvest only | Not full green required |

Each slice states which modes are in the green bar.

---

## 9. Success criteria

- [ ] `runtime.work_plane` attached on system start.  
- [ ] `runtime.supervisor` owns continuous services (at least work drain; outbox as sliced).  
- [ ] Inbound is a system contract; workers supervised.  
- [ ] Job start from drain uses system path (product façade only).  
- [ ] Session attribution works on reactive start without host-only law.  
- [ ] Host workplane is thin or gone; law tests run host-thin or hostless.  
- [ ] Doctor / control status reports supervisor + planes.  
- [ ] PALM names supervisor and work plane seats.  
- [ ] BI-013 closed; residual named.  
- [ ] ADR-029 Accepted at exit.  
- [ ] Spine green on declared modes.

---

## 10. How to update this file

- Mark slices done with ✅ and patch id.  
- Lock package paths and phase ids as they land.  
- Do not paste a second full map — link [PALM.md](PALM.md).  
- At exit: status closed, release/migration links, residual debt.

---

## 11. Related

| Doc | Role |
|-----|------|
| [PALM.md](PALM.md) | System map |
| [ADR-029](adr/029-system-supervisor.md) | Supervisor + work plane decisions |
| [ADR-025](adr/025-reactive-interests.md) | Start / continue law |
| [ADR-027](adr/027-session-plane.md) | Session attribution |
| [ADR-028](adr/028-system-boot.md) | Schedules · modes · membership |
| [WORK-DRAIN.md](WORK-DRAIN.md) | Start path ops (update as home moves) |
| [EVENT-PLANE.md](EVENT-PLANE.md) | Bus catalog |
| [TECH-DEBT.md](../TECH-DEBT.md) | BI-013 and residuals |
| [STATUS.md](../STATUS.md) | Active theme |
| [VISION-GROVE](VISION-GROVE.md) | Horizon |
| [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) | Later surface compost |

---

*Complete the local node. Then the Grove has a place to stand.*
