# VISION — The Grove (Palm Organization)

**Status:** 🌴 **North star** — multi-theme horizon, not a single minor plan.  
**Role:** Steer growth and complexity so near-term themes compound into a **grove of Palms** that talk through organization flows, reactive interests, and shared genome.  
**Does not replace:** per-minor [VISION-0.X](../VERSIONING.md) plans. Those remain the execution rhythm; this document is the **territory they aim toward**.  
**Does not block:** local courage. Near work is [VISION-ASSEMBLY](VISION-ASSEMBLY.md) (organism truth, tree of places) and the closed system seasons. Grove is **not** a gate you must pass before Palm may scale a process tree.

> *Palm grows where the sun meets the sea. A grove is many palms, one light, continuous conversation.*  
> *Tree first. Organization when the verbs are boring.*

**Related near themes:** [VISION-0.55](closed/VISION-0.55.md) **Reactive Interests** · [VISION-0.56](VISION-0.56.md) workload · [VISION-SESSION-PLANE](closed/VISION-SESSION-PLANE.md) · [EVENT-PLANE](../EVENT-PLANE.md) · [WORK-DRAIN](../WORK-DRAIN.md) · [ADR-025](../adr/025-reactive-interests.md) · [ADR-024](../adr/024-workload-engine.md) · [PHILOSOPHY](../../PHILOSOPHY.md)

**Near structure (before full org crown):**  
1. [VISION-ASSEMBLY](VISION-ASSEMBLY.md) — organism truth; tree; home up; optional **assembly seed** for base business structure  
2. [VISION-TUNNELS](VISION-TUNNELS.md) — trusted reach; neighborhood; mesh *feel*, tree *law*  
3. **This file** — multi-Palm organization and continuous interface  

Assembly + tunnels make a grove of processes honest without mesh self-discovery as the first law.

---

## 1. Intent

Palm today is a coherent **single organism**: pure core, definitions and instances, work plane (start), nested waits (continue), Assist, composition phenotypes.

The Grove is Palm at **many-organism scale** — still **one genome**.

**Updated meaning (after assembly / tunnels seeds):**

| Older Grove speech | Refined meaning |
|--------------------|-----------------|
| Organization as only a flat multi-Palm catalog | **Organization** = recursive **support** (or light center over support) that may have **realm** children; DNA + projection; home up — [VISION-ASSEMBLY](VISION-ASSEMBLY.md) §7 |
| Mesh of peers as first integration | **Hop home** for meaning; **tunnels** for trusted reach — [VISION-TUNNELS](VISION-TUNNELS.md) |
| Scale = more Palms talking | Scale = **vertical** authority + **horizontal** place book, then conversation |

| Scale | What it is |
|-------|------------|
| **One Palm** | Local orchestration — flows, jobs, instances, providers, place book |
| **Tree of places** | Light center, supports, work/resource places; multi-process controlled |
| **Many Palms / orgs** | Several supports or trees; user, service, capacity phenotypes |
| **Grove conversation** | Trust, shared definitions, **org flows + events + interests** — continuous interface |
| **Reach** | Trusted paths so neighborhoods talk without dual ownership |

**Aim:** software participates in a living conversation. Surfaces shrink because **participation recycles** the same genome. Integration becomes **continuous interface**, not frozen pairwise adapters — **after** home and places are honest.

---

## 2. Picture

**Logical (vertical) — recursive support**

```text
              Root light center
                     │
              Org support (DNA · project realms)
              ┌──────┴──────┐
              ▼             ▼
           Realm A       Realm B · …
           (sub-support) (sub-support)
              │
         truth home · local ground
              │
         hop home for meaning
```

**Physical (horizontal) — place book under any node**

```text
   work places · resource places · peer processes
   (same host or many hosts — readiness in the book)
```

**Conversation (Grove crown — when verbs are boring)**

```text
   org flows · events · interests · Assist
   speak via providers · place via workloads
   walk via session / handoff · optional tunnels for path
```

- **User / service / capacity palms** remain phenotypes of the same genome.  
- **Organization** holds allowlists and shared revisions **and** is assemblable as support DNA.  
- **Walking between palms** follows interest and session — and **home** when truth is contested.  
- **Multi-org** is natural: more recursive supports, not a second product.

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
| **Reactive interests (0.55)** | Social contract of every node and of the mesh | Wait plane; event-match resume; WorkIntent as start |
| **Event plane** | Nervous system | Stable public payloads; runtime bus for lifecycle |
| **Work plane** | Deferred **start** | Triggers, inbound, schedules, drain — already strong |
| **Session plane** (**0.58** open) | Outside subject / walk glue (multi-instance) | [VISION-0.58](closed/VISION-0.58.md) · bind + attach + watch |
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

Execution order still follows [VERSIONING](../VERSIONING.md) minors. This is **compass heading**:

| Season spirit | Outcome toward Grove | Theme |
|---------------|----------------------|--------|
| **Reactive interests** | Local start/continue true; nested flow on event match; second wait kind stub | **[0.55](closed/VISION-0.55.md)** open |
| **Workload plane** | Place work; peer palm runtime; ownership; real `workload.*` events | **[0.56](VISION-0.56.md)** queued |
| **Session plane** | Humans walk and watch the same subject; multi-instance | [VISION-0.58](closed/VISION-0.58.md) open |
| **Peer dogfood** | Two Palms: handoff + wait + place | later |
| **Org catalog + trust** | Named organization, shared definitions, allowlists | later |
| **User / service phenotypes** | Composition profiles for multi-user and service palms | later |
| **Continuous service interfaces** | Service products ship as Palm participation by default | later |

Near minors **must** cite this document when a slice choice is “local only” vs “Grove-shaped.” **0.55** implements §4 of the Law.

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
