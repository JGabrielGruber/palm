# VISION — The Grove (Palm Organization)

**Status:** 🌴 **North star** — multi-theme horizon, not a single minor plan.  
**Role:** Steer growth and complexity so near-term themes compound into a **grove of Palms** that talk through organization flows, reactive interests, and shared genome.  
**Does not replace:** per-minor [VISION-0.X](VERSIONING.md) plans. Those remain the execution rhythm; this document is the **territory they aim toward**.

> *Palm grows where the sun meets the sea. A grove is many palms, one light, continuous conversation.*

**Related near themes:** [VISION-0.55](VISION-0.55.md) session · [VISION-0.56](VISION-0.56.md) workload · [EVENT-PLANE](EVENT-PLANE.md) · [WORK-DRAIN](WORK-DRAIN.md) · [ADR-024](adr/024-workload-engine.md) · [PHILOSOPHY](../PHILOSOPHY.md)

---

## 1. Intent

Palm today is a coherent **single organism**: pure core, definitions and instances, work plane (start), nested waits (continue), Assist, composition phenotypes.

The Grove is Palm at **organization scale**:

| Scale | What it is |
|-------|------------|
| **One Palm** | Local orchestration — flows, jobs, instances, providers, workloads |
| **Many Palms** | User palms, service palms, capacity palms (GPU, CI, vault) |
| **Organization** | Trust, catalog, placement, shared flows — the paths between trees |
| **Conversation** | How they integrate: **org flows + events + reactive interests**, not N×N glue APIs |

**Aim:** software participates in a living conversation. Surfaces shrink because **participation recycles** the same genome (flows, waits, triggers, providers, Assist). Integration becomes **continuous interface**, not a frozen pairwise adapter.

---

## 2. Picture

```text
                    Palm Organization
           catalog · trust · placement · shared flows
                              │
     ┌────────────┬───────────┼───────────┬────────────┐
     ▼            ▼           ▼           ▼            ▼
  User A       User B     Service Σ    Service Π     Capacity
  Palm         Palm       Palm         Palm          Palm
  flows        flows      interface    interface     workloads
  datasets     …          as flows     as flows      GPU / CI
  dashboards
     │            │           │           │            │
     └────────────┴───────────┴───────────┴────────────┘
              talk via org flows · events · interests
              speak via providers · place via workloads
              walk via session / handoff / peer runtime
```

- **Each user Palm** holds personal journeys, datasets, dashboards, local Assist memory.  
- **Each service Palm** is a living partner: flows *are* the interface; events *are* progress; waits *are* readiness.  
- **Organization** holds allowlists, shared definition revisions, placement policy, identity of peers.  
- **Walking between palms** means following **interest and session** across nodes — start work there, continue when a remote target speaks — not bespoke RPC for every pair.

---

## 3. Continuous interface (vs integrative glue)

| Integrative (classic) | Continuous (Grove) |
|-----------------------|---------------------|
| Service freezes an API | Service Palm **runs** versioned flows |
| Consumer writes an adapter | Consumer **arms triggers** and **opens waits** |
| Change breaks glue | Contracts evolve as **definitions + events + migration** |
| O(N²) surfaces | O(N) **participation** in one conversation grammar |

**Continuous interface:** the conversation *is* the integration — human-drivable mid-flight, compensatable, inspectable, the same on every node.

Recycling is structural: wizard, DAG, wait, trigger, provider, workload, Assist are **one genome**; only **definitions, placement, and trust** change per palm.

---

## 4. The Law of Reactive Interests

*Foundation of local maturity and of the Grove. Completers speak of themselves; Palm continues or creates work by matching interest to signal.*

### 4.1 Two verbs, one bus

| Verb | Interest | Meaning |
|------|----------|---------|
| **Start** | **Trigger interest** | Signal matches a **rule** → **create or enqueue** work (`WorkIntent` → drain → job). |
| **Continue** | **Wait interest** | Signal matches a **target** → **resume** work that already exists (parked job). |

Both listen on the **orchestration event plane** (`runtime.event`). Neither locks the process.

### 4.2 Completers announce themselves

A completer (job, workload, peer subject, …):

1. Lives its own lifecycle.  
2. Emits a **self-describing** event (who I am, what status I reached).  
3. Does not know or invoke its waiters.  

### 4.3 Interest is explicit and owned

**Wait interest**

- Owned by a **job** (and durable **instance**).  
- Opened when parking: kind + target id (+ policy).  
- Closes when satisfied, failed per policy, or owner ends.  
- Survives restart with the owner.

**Trigger interest**

- Owned by a **rule** (definition metadata, inbound binding, schedule).  
- Armed while loaded; may fire many times → many new jobs.  
- Firing produces **WorkIntent**; drain starts work when able.

### 4.4 Palm matches; Palm acts

- **Wait matcher:** event about target T → resume/fail owners waiting on T.  
- **Trigger matcher:** event matches rule → enqueue start.  
- Same event may do both; verbs stay distinct.  
- Matching is **Palm’s** duty (common/host), not the completer’s.

### 4.5 Start path / continue path

```text
Start:     rule armed → event → WorkIntent → drain → new job
Continue:  job opens wait → parks → target emits → matcher → resume owner
```

### 4.6 Creed (short)

1. Two verbs: **start** and **continue**.  
2. One bus: **orchestration events**.  
3. Completers speak **only of themselves**.  
4. Wait interest lives on the **job**; trigger interest on the **rule**.  
5. Palm **matches** interest to signal.  
6. Start becomes **WorkIntent**, then a new job.  
7. Continue **resumes** a parked job.  
8. Durable, explicit, inspectable — never locked in a call stack.  
9. New capabilities are **new kinds**, not new laws.  
10. Across palms, the same law: remote targets are still **self-events + local interest**.

---

## 5. Building blocks (map near work to the Grove)

| Block | Grove role | Near steer |
|-------|------------|------------|
| **Reactive interests** | Social contract of every node and of the mesh | Extract wait plane; event-match resume; keep WorkIntent as start |
| **Event plane** | Nervous system | Stable public payloads; runtime bus for lifecycle |
| **Work plane** | Deferred **start** | Triggers, inbound, schedules, drain — already strong |
| **Session plane (0.55)** | Human unit of walk/watch | Subscribe to journey life; later multi-node presence |
| **Workload plane (0.56)** | Place body of work (incl. `runtime=palm`) | Isolation ≠ I/O; peer placement; ownership |
| **Definitions + revisions** | Shared language of the org | Catalog pin; instance pin; Design evolve |
| **Providers / blueprints** | **Speak** after READY | Continuous consume, not parallel service APIs |
| **Composition profiles** | Phenotypes: user / service / edge / server | One genome, many shapes |
| **Assist** | Meta-surface per palm | Same drive loop; later org routing of “which palm holds this?” |
| **Trust / mesh** | Garden wall | Allowlists, max hops, authn of peers (0.56 sketches) |

Complexity that **serves the Grove** is welcome. Complexity that invents a **second integration grammar** fights the Grove.

---

## 6. Walking between palms

Modes (all under the Law):

| Mode | Idea |
|------|------|
| **Handoff** | Trigger starts work on palm B; A **waits** on B’s terminal/ready event |
| **Delegation** | Workload `runtime=palm` places isolation on a peer; events/handles return |
| **Affinity** | Logical session stays coherent; steps start/continue on peers by policy |
| **Presence** | Assist on A observes/drives a subject hosted on B (thin surface, remote subject) |

Walking is **following interest and session**, not ad-hoc remote procedure for every pair.

---

## 7. Complexity steering (how to decide)

When proposing a feature, ask:

| Question | Prefer if yes |
|----------|----------------|
| Does it strengthen **start** or **continue** under the Law? | Aligns with Grove |
| Does a **completer** only emit self-events? | Aligns |
| Is interest **explicit and durable** on job or rule? | Aligns |
| Can a **second palm** later be only trust + target id + same events? | Aligns |
| Does it add a **pairwise adapter** that only two systems understand? | Reconsider — prefer flow/event/interest |
| Does it teach core about remote HTTP/org topology? | Keep out of core — adapters/register down |
| Does it duplicate WorkIntent for “resume”? | Prefer wait interest + resume |
| Does it duplicate wait hooks for “start”? | Prefer trigger + WorkIntent |

**Growth rule:** extend **kinds** (wait kind, intent kind, runtime, provider) and **catalog**. Preserve **verbs** and **layering**.

**Debt rule:** special-case “child calls parent” and long **blocking invoke** are interim organisms; the Grove needs them **graduated** into the Law (see near themes).

---

## 8. Growth seasons (compass, not schedule)

Execution order still follows [VERSIONING](VERSIONING.md) minors. This is **compass heading**:

| Season spirit | Outcome toward Grove |
|---------------|----------------------|
| **Reactive interests** | Local start/continue boring and true; nested flow on event match; second wait kind stubable |
| **Session plane** | Humans watch the same interests; walk is observable |
| **Workload plane** | Place work; peer palm runtime; ownership; events for ready/stop |
| **Peer dogfood** | Two Palms: handoff + wait + place |
| **Org catalog + trust** | Named organization, shared definitions, allowlists |
| **User / service phenotypes** | Composition profiles for multi-user and service palms |
| **Continuous service interfaces** | Service products ship as Palm participation by default |

Near minors (0.55, 0.56, and any **Reactive interests** theme opened before or beside them) should **cite this document** when a slice choice is “local only” vs “Grove-shaped.”

---

## 9. Dogfood of the Grove (destination image)

A living dogfood might look like:

1. **Org** “Palm Engine” with shared flow catalog and peer allowlist.  
2. **User palms** — each maintainer’s flows, datasets, dashboards.  
3. **Service palms** — e.g. CI capacity, docs build, design assist — interfaces as flows.  
4. Work **starts** via org triggers (schedule, inbound, peer terminal).  
5. Work **continues** via wait interest on remote job/workload ready.  
6. Heavy steps **place** on capacity palms (`runtime=palm` / hermetic).  
7. Humans **Assist** on their palm and occasionally **walk** a session that spans peers.  
8. New capability joins by **publishing a palm phenotype**, not a new integration product.

That dogfood is **years of seasons**, not one patch. It is the **fitness function** for architecture: if a design cannot eventually appear in this picture, question it.

---

## 10. Non-goals of this document

- Not a substitute for `VISION-0.X.0` planning releases.  
- Not a mandate to build multi-tenant SaaS in the next minor.  
- Not a requirement that every feature be multi-node on day one.  
- Not a second product brand — **Palm** remains the genome; **Organization / Grove** is scale.

---

## 11. Affirmations

1. Palm is **grown** — the Grove is organic scale of the same plant.  
2. **One genome, many palms** — composition and catalogs, not forks.  
3. **Two verbs** everywhere — start and continue.  
4. **Completers are free**; **interest is Palm’s memory of care**.  
5. **Definitions** are the shared language; **instances** are lived journeys.  
6. **Workloads place**; **providers speak**; **events inform**; **interests decide**.  
7. **Continuous interface** reduces surfaces and recycles participation.  
8. **Complexity serves conversation** — or it is pruned.  
9. Near themes are **root and trunk**; the Grove is the **canopy we grow into**.  
10. The map yields to the territory — but this map is where we **point the seasons**.

---

## 12. One sentence

> **The Grove is many Palms in one organization, talking through shared flows and reactive interests, so integration is continuous conversation — and every near theme should deepen start, continue, place, speak, or trust toward that canopy.**

---

*Steering document for growth and complexity. Tend the roots (interests, events, session, workload); the grove follows.* 🌴🌳
