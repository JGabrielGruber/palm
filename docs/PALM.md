# Palm — System definition

**Status:** Canonical high-level definition.  
**Language:** ASD-STE100 Simplified Technical English (project rule from 0.57).  
**Role:** This file is the **map of Palm as a whole**. Use it first.  
**Detail:** Link out. Do not replace this map with a second full copy.

**Related:** [VISION-0.58](VISION-0.58.md) (session theme **open**) · [ADR-027](adr/027-session-plane.md) · [VISION-0.57](VISION-0.57.md) · [ADR-026](adr/026-palm-system-layer.md) · [WRITING.md](WRITING.md) · [VISION-GROVE](VISION-GROVE.md) · [AGENTS.md](../AGENTS.md) (agent rules only — not a second map) · [ARCHITECTURE.md](../ARCHITECTURE.md) · [STATUS.md](../STATUS.md)

---

## 1. What Palm is

Palm is an **orchestration engine**.

Palm coordinates **work** that must stay **honest**:

- A **definition** says what work may do.
- A **job** is one run of that work.
- An **instance** is the durable record of that run.
- **State** lives on a pluggable blackboard.
- **Control flow** is a **Behavior Tree** (BT), not hidden callbacks.

A person or an agent may:

- start work,
- answer questions mid-flight,
- step back,
- pause and resume later,
- inspect what waits and why.

Palm is **not** only a REST API.  
Palm is **not** only a wizard product.  
Palm is **not** a container platform that happens to run Python.

Palm is a **system**: pure machines, a running kernel shape, plugins, product façades, and thin surfaces.

### 1.1 Operating-system picture

Use this picture to place every new piece:

| OS idea | Palm idea |
|---------|-----------|
| Hardware / ISA | **Core** — pure engines and contracts |
| Kernel | **System** — one running Palm: engines bound, **ports** open, **planes** live |
| Drivers | **Plugins** — patterns, providers, runners, storages |
| Shared libraries | **Shared** — reusable glue that is not the system |
| User programs | **Product** — services for operators and agents |
| Terminals / sockets | **Surfaces** — CLI, HTTP, MCP, WebSocket, … |
| Boot image | **App host** + composition / deployment profiles |
| Files / records | **Definitions** and **instances** |

If a piece has no home in this table, the design is incomplete. Name the home before you add the piece.

---

## 2. What Palm is for

| Aim | Meaning |
|-----|---------|
| **Human-first** | Wizards, choices, backtrack, resume after interruption |
| **Truth-seeking** | Explicit job status, durable instances, visible failures |
| **Agent-operable** | Assist and MCP drive the same work path as a human |
| **Extensible** | New capability by **registry**, not by editing core contracts |
| **Local maturity, Grove horizon** | One Palm is complete; many Palms talk later by the same laws |

Palm optimizes for **long clarity**, not for short cleverness.

---

## 3. Primary concepts

These words are **stable**. Use them with one meaning only.

| Concept | Meaning |
|---------|---------|
| **Definition** | Declared contract of work (flow, process, resource, …). Versionable. |
| **Pattern** | How a flow shape runs (wizard, parallel, pipeline, dag, …). Plugin. |
| **Behavior Tree (BT)** | Control-flow model: nodes tick; composition is explicit. |
| **Job** | Live unit of execution under the orchestration engine. |
| **Instance** | Durable process record for one definition run; survives restart when storage is shared. |
| **Session** | Outside subject (system plane): one coherent external walk; may own **many** instances. |
| **State** | Blackboard data for the run (`BaseState` and schemas). |
| **Resource** | Named way to **speak** to an external or internal system (provider + action). |
| **Provider** | Plugin that implements resource speak. |
| **Workload** | Isolated place for foreign work (run or long service). Not “just another resource.” |
| **Runner** | Plugin that implements a workload runtime (host, neonroot, …). |
| **Event** | Signal on a bus. Completers describe themselves. |
| **Interest** | Explicit want: **start** (trigger) or **continue** (wait). |
| **Port** | Named interface for **effects** the system may perform. |
| **Plane** | System path for one kind of traffic (event, start, continue, session, …). |
| **Surface** | Transport only. |
| **Product** | Operator/agent domain API (policy + envelope). |
| **System** | Running Palm that holds engines and exposes ports. |
| **Shared** | Code reused by many layers that is not system and not product. |

---

## 4. Path of one unit of work

This path is the spine. Ports and planes exist **for** this path.

```text
1. Definition exists in the catalog
        │  (optional: Design propose → impact → commit → revision)
        ▼
2. Someone submits work
        │  product / surface / nested pattern / WorkIntent drain
        ▼
3. System materializes a pattern from the definition
        │  (BT + leaves bound to ports / engines today)
        ▼
4. Orchestration accepts a Job
        │  instance may be created or resumed
        ▼
5. Scheduler drives the job (inline or queued)
        │  BT ticks
        │  ├── ask human/agent  → wait for input
        │  ├── invoke resource  → effect (speak)
        │  ├── start workload   → effect (isolate) + optional wait
        │  ├── open wait interest → park until event matches
        │  └── transform / branch / child flow …
        ▼
6. Completer emits self-events on runtime.event
        │
        ├── Start path:  trigger matches → WorkIntent → new job
        └── Continue path: wait matches → resume or fail owner
        ▼
7. Terminal status
        │  persist instance; compensate if needed; projections update
        ▼
8. Operator or agent may inspect, resume, or design the next change
```

### 4.1 Job status (honest lifecycle)

A job moves through explicit statuses (orchestration).  
Typical shape: **pending → running → waiting → running → terminal**  
Terminal means success, failure, or cancelled — not a silent hang.

**Waiting** is first-class. Waiting may mean:

- human or agent input,
- child work,
- external signal,
- workload readiness or completion.

### 4.2 Two clients on the same spine

| Client | Role on the path |
|--------|------------------|
| **Graph (pattern / BT)** | Ticks the job. Needs fast, injectable **ports**. |
| **Operator / agent / HTTP** | Starts and drives from outside. Needs product + CQRS + **same ports**. |

Truth is the **job path**.  
Product is not a second engine.  
Raw engines as the only graph API is an incomplete contract.

---

## 5. What Palm contains

### 5.1 Core — pure machines (`palm.core`)

Core has **no** imports from other Palm packages.

| Engine / area | Purpose |
|---------------|---------|
| **BehaviorTreeEngine** | Run BT nodes and patterns |
| **OrchestrationEngine** | Job lifecycle, drive, hooks, results |
| **ContextEngine** | Scopes and state wiring |
| **StorageEngine** | Persistence backend coordination |
| **ResourceEngine** | Invoke providers (speak) |
| **EventEngine** | In-process event bus |
| **AuthEngine** | Auth primitives and principals |
| **TransformEngine** | Data transform rules |
| **Wait** (types) | Pure continue-interest vocabulary |
| **Work** (types) | Pure start-plane intent types |
| **WorkloadEngine** | Pure workload lifecycle (place / exec / status / stop) |

Core also holds **registries** (pattern, provider, storage, …) as pure registration points.  
Higher layers **register downward** into them.

### 5.2 Definitions and instances

| Package | Purpose |
|---------|---------|
| **`palm.definitions`** | Flow, process, resource, schema, dashboard contracts |
| **`palm.instances`** | Durable process instance, snapshots, status history |

Definitions may **revise** (append-only history).  
Instances **pin** a revision and hold resume state.  
**Design** (product) proposes and commits definition change. It does not replace the catalog.

### 5.3 Plugins — register, do not fork core

| Plugin family | Purpose | Package |
|---------------|---------|---------|
| **Patterns** | Control-flow shapes (wizard, parallel, pipeline, dag, …) | `palm.patterns` |
| **Providers** | Speak backends (rest, kv, file, palm, neonroot-as-provider legacy, …) | `palm.providers` |
| **Runners** | Workload isolation backends (host, neonroot, …) | `palm.runners` |
| **Storages** | Storage backends (memory, filesystem, postgres, …) | `palm.storages` |

Each plugin family follows an **app + registry** layout.  
Capability is added at the edge. Core contracts stay stable.

**Flagship pattern today:** **wizard** — interactive steps, validation, backtrack, commit, resource and workload leaves.  
Other patterns exist at different maturity. Maturity is not the same as purpose.

### 5.4 System — the running Palm

**Purpose:** Hold engines for **one** started runtime, expose **ports**, run **planes**, accept definition-driven jobs.

**Today (honest):** This role is **split**:

| Piece | Holds |
|-------|--------|
| **`BaseRuntime`** | Engines, start wiring, executor, wait plane attach, outbox hooks |
| **Parts of `palm.common`** | Wait plane service, work drain, workload bootstrap, runtime hooks, definition executor |
| **`RuntimeHost` protocol** | Incomplete: orchestration + event + resource only |
| **`PalmKernel`** | Storage, instance manager, **runtime registry** — multi-runtime infra, not the effect port table |

**Target:** One clear **system** boundary. Same purpose. Cleaner home. Named ports.

#### Ports

A **port** is a named effect surface.  
Graphs and product both bind ports.

| Effect family | Meaning | Notes |
|---------------|---------|--------|
| **Resource / speak** | Invoke provider actions | Dual path today (leaf → engine; service → engine) |
| **Workload / isolate** | Start, exec, stop, status | Scouted in 0.56; must share the port model |
| **Job / drive** | Submit, drive, input, inspect as system allows | Orchestration-facing; keep explicit |

A port is **not** CQRS alone.  
A port is **not** one engine class name as the public graph contract.  
A port is **not** “everything is a flow.”

#### Planes

A **plane** is system traffic of one kind.

| Plane | Verb / role | Home (intent) |
|-------|-------------|----------------|
| **Event** | Signals; completers speak of self | `runtime.event` (orchestration bus) |
| **Work (start)** | Trigger → WorkIntent → new job | Work drain / start plane |
| **Wait (continue)** | Interest → resume or fail parked work | Wait plane |
| **Session** (0.58) | Outside subject: bind, multi-instance walk, watch | System `planes.session` (seat + multi-attach 0.58.2); thin product later |
| **Workload** | Isolation lifecycle events and placement | Workload engine + runners |

**Host bus** (`host.event`) is for host coordination (start, shutdown, outbox process).  
**Do not** put job lifecycle only on the host bus. See [EVENT-PLANE](EVENT-PLANE.md).

#### Reactive law (start and continue)

1. Completers emit **self-events**.  
2. Palm matches **interest**.  
3. **Start** creates or enqueues work.  
4. **Continue** resumes work that already exists.  
5. Same bus may feed both verbs. Verbs stay distinct.

This law is **system law**. It is not a feature flag.  
Detail: [VISION-GROVE](VISION-GROVE.md) §4 · [ADR-025](adr/025-reactive-interests.md).

### 5.5 Shared — not the system dump

**Purpose:** Reusable coordination and libraries that:

- many layers need,
- are not a product domain,
- are not the running kernel itself.

**Examples of true shared work:** transform rule packs, schema helpers, persistence repositories used by system and product, CQRS bus **primitives**, small operator view helpers.

**Today (honest):** `palm.common` holds **shared and system together**. That mix is the main structural debt of the middle layer.

| In common today | Likely class |
|-----------------|--------------|
| `BaseRuntime`, wait plane, work drain | **System** |
| Definition executor, plans, hooks | **System** (or system-adjacent) |
| Transform builtins, some resolvers | **Shared** |
| CQRS buses | **Shared primitive**; wiring is host/product |
| Operator presenters | **Shared support** for product/surfaces — watch bulk |
| Full product domains | **Must not** live here |

**Rule:** If you do not know where code goes, do not put it in shared by default. Name system, product, or plugin first.

### 5.6 Product — userland (`palm.services`)

**Purpose:** Domains for operators and agents.  
Policy, validation, envelopes, CQRS contributors.  
Then call **system ports** (target). Today many paths call engines on a resolved runtime.

| Domain | Purpose |
|--------|---------|
| **Definitions** | Catalog read/write of definitions |
| **Design** | Propose → impact → commit definition change |
| **Execution** | Run flows, processes, provider invoke, workloads |
| **Assist** | Meta-surface: discover, drive, present next step |
| **System** (product name) | Doctor / health style operator queries — **not** the kernel layer |
| **Analytics** | Datasets and dashboards |

**Name clash (tell the truth):**  
Product package `palm.services.system` is **operator system info**.  
**System layer** in this map is the **kernel shape**.  
Do not confuse the two. Prefer “product SystemService” vs “system layer” in speech.

**CQRS** is how many edges ask product.  
CQRS is transport and schema discipline.  
CQRS is not the definition of all Palm power.

### 5.7 Surfaces (`palm.runtimes`)

**Purpose:** Map a wire protocol to product (or a controlled system entry).  
Stay thin.

| Surface family | Examples |
|----------------|----------|
| Embedded | In-process library runtime |
| Daemon | Long-lived worker |
| Server | HTTP, Explorer SSR, WebSocket assist |
| CLI | Terminal commands and REPL |
| MCP | Agent tools and resources |

Surfaces must not invent a second semantic model.

### 5.8 App host (`palm.app`)

**Purpose:** Compose a **phenotype** of Palm and boot it.

| Piece | Role |
|-------|------|
| **PalmKernel** | Infra: shared storage, instance manager, runtime registry |
| **ApplicationHost** | Roles, CQRS wiring, recovery, service façades, workers |
| **Composition / deployment profiles** | Declare shape (embedded, server, all-in-one, …) |
| **Settings** | Configuration |

The host is **not** a second port table.  
The host **wires** system instances and product.

### 5.9 Reliability and truth aids

These are part of Palm’s honesty, not optional polish:

| Aid | Role |
|-----|------|
| **Instance persistence** | Resume after restart |
| **State snapshots** | Bounded history for inspect (optional) |
| **Outbox** | Reliable event publication |
| **Compensation** | Undo on failed commit paths where registered |
| **Projections** | Read models for status and dashboards |
| **Doctor** | Health and registry visibility |

---

## 6. Layers — purpose table

Each top-level part has **one purpose**.

| Layer | Purpose (one sentence) | Must not |
|-------|------------------------|----------|
| **Core** | Pure engines and contracts | Import outside `palm.core` |
| **System** | Running Palm: bind engines, ports, planes | Be a product domain or a surface |
| **Shared** | Reusable non-system, non-product glue | Absorb “no home” code |
| **Plugins** | Extend by registry | Own host lifecycle or product envelopes |
| **Product** | Operator/agent domains over ports | Hold engines as the public truth |
| **Surfaces** | Transport adapters | Call engine class names as policy |
| **App host** | Boot and compose phenotypes | Replace system ports |
| **Definitions / instances** | Contracts and durable records | Execute effects |

### 6.1 Names (current truth)

| Name | Role now | Residual |
|------|----------|----------|
| `PalmKernel` | Infra: storage + system-instance registry | Not the effect API |
| `BaseRuntime` | **System instance** under `palm.system.runtime` | Import from `palm.system` |
| `RuntimeHost` | Thin legacy protocol for executions | Prefer `SystemInstance` + ports |
| `PatternBuildContext` | Carries `execution` port (+ engines for unit tests) | Engine fields for tests only |
| `ExecutionService.*` | Product over **ports** for effects | list/doctor residual |
| `palm.system` | System home: runtime, planes, ports | — |
| `palm.common` | Shared libraries (plans, CQRS, transforms, …) | — |
| `palm.kits` | Surface kits (`server`, …) | SD-011 ✅ |
| `services.system` | Doctor/health **product** | Do not call it the kernel |

---

## 7. How Palm grows

| You want to add… | You add it as… |
|------------------|----------------|
| New pure algorithm or engine | **Core** |
| New effect family | **System port** (+ core engine if pure) |
| New isolation backend | **Runner** plugin |
| New speak backend | **Provider** plugin |
| New control-flow shape | **Pattern** plugin |
| New storage backend | **Storage** plugin |
| New operator domain | **Product** service + CQRS |
| New transport | **Surface** |
| New deployment shape | **Composition / deployment profile** |
| New event reaction | **Trigger or wait interest** on the event plane — not a private hook web |

**Growth rule:** extend **kinds** and **registries**.  
Do not invent a second integration grammar.

---

## 8. Grove (horizon, not the local map)

[VISION-GROVE](VISION-GROVE.md) is the **multi-Palm** north star:

- many Palms (user, service, capacity),
- talk by flows, events, and interests,
- same genome, different placement and trust.

**This file** defines **one Palm**.  
Grove does not replace local system structure.  
Local system structure makes Grove possible later.

---

## 9. Laws

1. **One purpose per module.** If two purposes fit, split.  
2. **Core stays pure.**  
3. **Register downward.**  
4. **The job path is the spine.** Features must say where they sit on that path.  
5. **Effects use named ports.** Graphs and product share them.  
6. **Planes are system.** Product may expose; product does not own.  
7. **Product is userland.** Policy and envelopes, then ports.  
8. **Surfaces stay thin.**  
9. **Shared is not a dump.**  
10. **Completers emit self-events.** Palm starts or continues by interest.  
11. **Waiting is first-class.** Do not hide waits in call stacks.  
12. **Definitions declare; instances remember; jobs run.**  
13. **Coherence is enforced** (guards, CI).  
14. **Break for truth before 1.0.** Record residual debt. Do not keep a structural lie for comfort.  
15. **Incomplete maps are false maps.** When structure changes, update this file in the same theme of work.

---

## 10. Documentation rule

From theme **0.57** onward:

- Write new and revised project docs in **ASD-STE100** ([WRITING.md](WRITING.md)).  
- Prefer short sentences and one idea per sentence.  
- Use the **same word** for the same idea (see §3).  
- Prefer active voice and tables.  
- Do not add marketing text.  
- **Link this map.** Do not paste a second full map into AGENTS or README.

---

## 11. Where to look next

| Need | Open |
|------|------|
| **This map** | `docs/PALM.md` |
| System low-level (package, ports, moves) | [SYSTEM-LOW-LEVEL](SYSTEM-LOW-LEVEL.md) |
| Live debt (SD/SU/ST/CS) | [TECH-DEBT.md](../TECH-DEBT.md) |
| Intention stubs | [STUBS.md](STUBS.md) |
| Debt archive (PD era) | [audit/TECH-DEBT-ERA-0.45.md](audit/TECH-DEBT-ERA-0.45.md) |
| Theme plan | [VISION-0.57](VISION-0.57.md) |
| Structural ADR | [ADR-026](adr/026-palm-system-layer.md) |
| Start / continue law | [VISION-0.55](VISION-0.55.md) · [ADR-025](adr/025-reactive-interests.md) |
| Event buses | [EVENT-PLANE](EVENT-PLANE.md) |
| Start drain | [WORK-DRAIN](WORK-DRAIN.md) |
| Workload scout | [VISION-0.56](VISION-0.56.md) · [ADR-024](adr/024-workload-engine.md) |
| Session plane (theme open) | [VISION-0.58](VISION-0.58.md) · [ADR-027](adr/027-session-plane.md) |
| Multi-Palm horizon | [VISION-GROVE](VISION-GROVE.md) |
| Dense layer detail | [ARCHITECTURE.md](../ARCHITECTURE.md) |
| Agent rules | [AGENTS.md](../AGENTS.md) — points here for structure |
| Version and theme status | [STATUS.md](../STATUS.md) |
| Spirit | [PHILOSOPHY.md](../PHILOSOPHY.md) |

If a document fights this map, **this map wins** until an ADR changes it.

---

## 12. Truth about completeness

A map that only names **pain** is incomplete.  
A map that only names **ideals** without today is also incomplete.

| Area | State |
|------|--------|
| Core purity and engines | **Real and strong** |
| Definitions, instances, resume | **Real** |
| BT + orchestration job path | **Real** — spine of Palm |
| Patterns / providers / storages registries | **Real** |
| Wizard and Assist product loops | **Real** (product maturity varies by surface) |
| Reactive start / continue law | **Landed** (0.55) |
| Workload pure engine + leaf direction | **Scout** (0.56) — enough to force this map |
| Named system layer in packages | **Live** — `palm.system` holds BaseRuntime, ports, planes, executions, job hooks (**0.57 closed**) |
| Unified execution port | **Live** — product + graphs + edges for effects and catalog inspect |
| Shared vs system split in tree | **Deflated** (0.57.6–13); kits exposed (`palm.kits.server`); plans DTO shared |
| Live debt register | **Real** — residual **SU-*** / **SD-008** (in 0.58) / **SI-*** — [TECH-DEBT.md](../TECH-DEBT.md) · [STUBS.md](STUBS.md) |
| Surface thinness | **Law** — bulk/bypass as SU-* (~14k server LOC; optional paydown) |
| Session plane | **Theme open 0.58** — [VISION-0.58](VISION-0.58.md) · multi-instance system glue (not user plane) |
| Grove multi-Palm | **Horizon** — not local incomplete |

**Incomplete structure is stated here on purpose.**  
Hiding it would make the map a lie.

---

*Palm grows where the sun meets the sea.*  
*Name the whole tree. Then grow the branch.*
