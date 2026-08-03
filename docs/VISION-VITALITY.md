# VISION — System vitality (queue seed)

**Status:** ✅ **Opened as [VISION-0.61](VISION-0.61.md)** at **0.61.0** · ADR [030](adr/030-system-vitality.md) **Proposed**. This file remains the **seed essay** (horizons, energy lens, capability catalog depth). Theme plan is authoritative for slices.  
**Language:** ASD-STE100 (practical).  
**Map:** [PALM.md](PALM.md) · theme [VISION-0.61](VISION-0.61.md) · supervisor [VISION-0.60](VISION-0.60.md) (**closed**) · [ADR-029](adr/029-system-supervisor.md) · session [VISION-0.58](VISION-0.58.md) · system log [SYSTEM-LOG](SYSTEM-LOG.md) · [BI-015](../TECH-DEBT.md#bi-015) · [OD-001](../TECH-DEBT.md#od-001)  
**North star:** [VISION-GROVE](VISION-GROVE.md)  
**Lens (archive):** [Energy Dissipation Heuristic v1.1](../archive/Energy_Dissipation_Heuristic_v1.1.pdf)  
**Related queue:** [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) (boundary heat) · residual BI / SI / SU · CS-* smells in [TECH-DEBT](../TECH-DEBT.md)

---

## 1. Why this note exists

Palm can answer **structure** questions today:

- Is composition true?  
- Did boot walk?  
- Are planes and supervisor seats present?  
- What did the system log just say?

Palm cannot yet answer **physiology** questions with first-class honesty:

- Is this **living** organism dissipating work usefully?  
- Where is **waste heat** (retries, orphan waits, thrash continues)?  
- **Who** emitted the signal — human, probe agent, system loop, peer?  
- Where is **load** and **bulk** under pressure (queues, CPU/RSS, fat seats)?  
- May we **mutate** definitions from that evidence without harming another emitter class?

**Need statement:** We need health of the **living Palm** (kernel in process).  
Every OS eventually grows a **`top`**: a dynamic real-time view of the running system — summary + what the kernel is managing. Palm should not be less self-aware than that.

We do **not** need full filesystem genome analytics to open the door.  
We **do** want **visibility** (including size and smell of what is loaded) without moralizing or hiding work.

This file names **start → tool → dream**.  
It does **not** open a theme. It does **not** invent a second start/continue path.

---

## 2. Three horizons

| Horizon | Name | Meaning |
|---------|------|---------|
| **Start** | What we already have | Kernel shape live: `SystemInstance` / `BaseRuntime`, planes, ports, supervisor, doctor, system log, emissions, session attribution |
| **Tool** | Living-kernel vitality | Walk the **running** system with Python on seats + emissions; project physiology; present via doctor/assist |
| **Dream** | Healthy evolution | Emission-aware mutation; probe palms; homeostasis; Grove; optional genome dogfood |

**Order:** start is live. **Tool before dream.** Dream without tool is story. Tool without emission identity is noise.

**Priority lock:**

| Need | When |
|------|------|
| **Living Palm vitality** | **Required** — this seed’s tool |
| Probe / mutation / homeostasis | Dream after tool |
| Filesystem / AST / module GC | **Later dogfood** — not kill condition |

### 2.1 Why vitality **first** among queue seeds (growth argument)

Palm’s last seasons paid **structure and intent**:

| We already have | What it captured |
|-----------------|------------------|
| Tests, guards, CI | Spine and layer law do not silently rot |
| Dogfoods, surfaces, assist | How humans and agents **operate** Palm |
| System, session, boot, supervisor | **Homes** for traffic and continuous services |
| Doctor + system log | Anatomy and short tape — not full physiology |

That was necessary. It was also **mostly blind to cost**:

- Further enhancements can land without a live view of lag, heat, bulk, or thrash.  
- Surface weight and dual paths can **kill growth** while tests stay green.  
- Compost themes (surface deflation) and residual BI are real — but ranking them **without** living metrics is still folklore.

**Thesis:** Stop working Palm only by intent and CI. Add **eyes** so growth is tracked, not only asserted.

| Seed | Role relative to vitality |
|------|---------------------------|
| **Vitality first** | Instrument the living body — `top` + emissions + optional bulk |
| Surface deflation | Compost **with evidence** of heat/bulk (better after eyes) |
| Residual BI-* | Pay structural leftovers; vitality may **expose** which BI hurts live |
| Grove / probes | Need a subject that can report health under stress |

**Effort pays off because** every later slice can answer: *did this cost us lag, RSS, wait heat, seat bulk?*  
Without that, themes compound in the dark.

**Not a claim:** vitality replaces deflation or BI paydown.  
**Claim:** vitality is the **reasonable first** queue open so other work is not blind.

---

## 3. Kernel first (living Palm)

Palm has a **kernel**: the system layer — one running machine ([PALM.md](PALM.md) OS picture).

| OS idea | Palm |
|---------|------|
| Kernel | **System** — engines bound, ports open, planes live |
| Concrete | `SystemInstance` · `BaseRuntime` · planes · `SystemSupervisor` · system log |
| Boot image | Host + composition (wires; not the vitality instrument itself) |

### 3.1 Traverse the living body (tool law)

The running kernel is a **Python object graph**. Vitality discovers **what is attached after start**, not what exists in git.

```text
SystemInstance (BaseRuntime)
  ├── ports (e.g. execution)
  ├── planes (wait / work / session / …)     ← report if present
  ├── supervisor → continuous services      ← iterate owned loops
  ├── engines held by system
  ├── system log / ring
  └── boot membership / last_walk facts
            │
            ▼  thin seat report contract + emissions
     vital projection (dynamic fold)
            │
            ▼
     doctor / assist present
```

| Prefer | Avoid |
|--------|--------|
| Walk **seats on this instance** | Hand menu of every package under `src/palm` |
| Composition + supervisor **membership** | Assume drain/outbox always exist |
| Small **report protocol** on seats (`vitality_report` / counters) | Brittle private `__dict__` as law |
| Emissions already fired (jobs, waits, log) | Second write path for the same fact |
| Python on the live graph | Filesystem required for green physiology |

**Principle:** You are **running** Palm. The **kernel is the instrument**.  
No git, no AST, no per-module hand definition required for *this* health.

Cost note: full aggregation can be heavy. Ship thin vitals first. Sample. Window. Do not flood the BT path.

### 3.2 Two kinds of health (do not merge)

| Kind | Question | Need |
|------|----------|------|
| **Living vitality** | How does this **process** process work? | **Palm-palm — we need it** |
| **Genome / codebase** | Is the **source tree** modular? Smelly? | Dogfood **one day** — not this tool bar |

**Rule:** Runtime green ≠ tree clean. Tree clean ≠ flows dissipate well.  
**Rule:** Doctor may later show a **second** section for genome metrics. Never one blended score.

---

## 4. What living vitals measure (examples)

Derived from **live** traffic and seats (discovered, not hardcoded):

- Job yield and terminal class  
- Wait park / clear / orphan / age  
- WorkIntent drain lag and fail (if service present)  
- Outbox lag (if present)  
- Effect retry / provider fail ratio  
- Continues per successful outcome (by `actor_kind` when known)  
- Session bind honesty and attribution fails  
- Supervisor tick success / skip reasons for **owned** services  

Absent capability → **skipped / absent** (boot PhaseSkip honesty), not fake green.

---

## 5. Why this helps Palm development

Vitality is not only operate theatre. It is a **development fitness instrument**.

| Benefit | How |
|---------|-----|
| **Faster truth after change** | After a slice, `top`-like view shows whether drain lag, wait heat, or RSS grew — before folklore |
| **Smell made visible** | Fat seats, deep queues, hot paths surface as numbers, not only PR taste |
| **Bottleneck location** | Split: circulation (supervisor) vs traffic (planes) vs effects (port) vs product chrome |
| **Honest residual debt** | CS-* / SU-* / BI-* gain runtime evidence (“this god-file is also hot under load”) |
| **Safer compost** | Surface deflation and host residual can be ranked by **observed** heat, not only LOC |
| **Theme exit bar** | Dogfood: doctor vitality stable under probe/human walk; no silent thrash |
| **Agent / assist triage** | “What hurts?” becomes a first-class assist path, not source spelunking |
| **Probe feedback** | Small LLMs stress accessibility; living vitals score the subject under that stress |
| **No shame, more light** | Large modules and rich workloads may be valid — we **show** bulk and cost, we do not hide or auto-condemn |

**Stance:** Visibility first. Condemnation never automatic.  
Refactor and Design remain human/agent judgment with evidence.

### 5.1 OS analogy — `top` for Palm

From the usual `top` idea: *dynamic real-time view of a running system* — system summary plus what the kernel manages; configurable; not a second OS.

| `top` (Linux) | Palm vitality (target) |
|---------------|------------------------|
| System summary (load, memory) | Process RSS/CPU (optional), job/wait/intent backlog, emitter partitions |
| Process / thread list | **Seats** the system manages: planes, supervisor services, ports, key engines |
| Configurable columns | Doctor / assist sections; mode-aware depth (`safe` quieter) |
| Limited process manipulation | Homeostasis later (alert, wait, safe knobs) — not kill-9 of jobs by default |
| Persistent user config | Settings / composition — not a hardwired dashboard product |

**Reasonable:** every serious OS exposes live metrics. Palm is a system; it should too.

**Not the goal:** replace OpenTelemetry product, flood BT ticks, or shame every large class.

### 5.2 Smells and bottlenecks — two visibility layers

Do not force one number. Developers need **both**, labeled:

| Layer | Question | Examples | When |
|-------|----------|----------|------|
| **A — Living load** (`top` core) | What is hot **now** in this process? | Drain lag, wait depth, outbox lag, effect fail rate, executor queue, CPU/RSS, tick cost | **Tool bar** |
| **B — Structural bulk** (size map) | What **attached** seats/modules carry weight? | LOC of loaded module, class method count, seat object graph size, registry cardinality | Tool **optional** light pass; full tree scan = dogfood |

**Bottleneck scan (living):**

```text
high wait age + growing interest count     → continue path / definition thrash
drain lag + intent backlog                 → circulation / supervisor / work plane
effect retries + provider fails            → edge I/O, not “Palm is slow”
RSS climb without job yield                → leak or unbounded cache
CPU in supervisor ticks, low completions   → thrash loops / dual path
```

**Smell scan (bulk — visibility only):**

```text
seat's defining module very large          → god-module candidate (CS / SU heat)
class with many public methods             → mixed responsibility candidate
huge registry or many attached surfaces    → composition bulk
```

**Correlation (development gold):**  
“This module is large **and** its seat is hot under load” → compost priority.  
“This module is large **and** cold” → aesthetic debt; still visible, lower urgency.

**Not per-flow vanity alone:** Prefer **resource usage and overall size / seat load** over only “how long did flow X take.”  
Per-definition aggregates remain **optional** design feedback (dream), not the only metric.

### 5.3 Palm aware of itself

```text
  emissions + seat reports + (optional) process resources + (optional) bulk of loaded code
                                    │
                                    ▼
                         vitality projection
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                 doctor          assist          (later) homeostasis
              (human top)     (agent top)         (routine care)
```

Awareness = **continuous ability to answer** “what is my system doing, and where is bulk?”  
Not omniscience. Not auto-rewrite.

---

## 6. Energy lens (short)

Palm is an open system. It **consumes** (intents, inputs, I/O, time) and **emits** (events, waits, log lines, surface answers). Order holds when throughput is useful and entropy is **exported** as visible failure or finished work — not as silent thrash.

| EDH idea | Palm proxy |
|----------|------------|
| Useful dissipation | Completions with intended outcomes; waits that resolve to owner continue |
| Waste heat | Retries, dual paths, orphan interests, abandoned walks, surface bypass |
| Feedback quality | Time and honesty from emission → continue; doctor matches reality |
| Adaptive mutation | Design commit that improves vitals **for the emitter class that hurt** |
| Maladaptive mutation | Optimize one class (e.g. small LLM) while human yield collapses |

Archive essay stays in `archive/`. This vision does **not** claim novel physics. It uses the lens for **placement and policy**.

---

## 7. Emission systems (load-bearing)

Data from **humans** is not data from **LLM probes**.  
Data from **supervisor loops** is not data from **flow taste**.

Every vitality signal must name its **emission system**:

```text
actor_kind · session subject · channel · kind · outcome · time
```

| `actor_kind` (sketch) | Meaning |
|----------------------|---------|
| `human` | Person on CLI / UI / assist |
| `agent` | General agent (MCP power user) |
| `probe` | Declared accessibility / small-model probe |
| `system` | Supervisor, drain, boot, internal |
| `peer` | Other Palm / provider ecology |

**Rule:** Prefer **declared** probe sessions (tag, composition phenotype, assist metadata).  
Do not reverse-engineer “bot vs human” from timing alone.

**Healthy mutation rule:**

> Change the layer the emission system actually stresses.  
> Cite the emitter class on proposals and Design commits.  
> Partition vitals by emitter class. Never blend as one truth.

| Emitter | Prefer to change |
|---------|------------------|
| Probe / small LLM | Assist envelopes, tool density, vocabulary (SU / MCP) |
| Human walk | Definition structure, questions, branches |
| System / supervisor | Loop policy, composition, backlog |
| Provider / peer | Contracts, placement, trust (Grove later) |

---

## 8. Homes (where pieces sit)

Split by purpose. Do not build a god “evolution engine.”

| Concern | Home | Not |
|---------|------|-----|
| **Kernel walk / sense** | Live `SystemInstance`: seats, planes, supervisor services, emissions, system log | Filesystem scan; core pure engines as entry |
| **Seat report contract** | Thin protocol on system seats (planes, continuous services) | Product re-copy of each field |
| **Projection** | System (or thin system helper): discover → fold → vector | Dual status trees |
| **Present** | Product doctor / assist / operate | Second kernel vocabulary (CS-002) |
| **Algorithms (propose)** | Product Design / Assist; optional contributors; probe drivers | Own start/continue |
| **Mutation (commit)** | **Design** for definitions; composition for membership | Supervisor rewrites flows |
| **Continuous pumps** | **SystemSupervisor** | Scorecard owner; mutation authority |
| **Traffic law** | Planes (work / wait / session) | Replaced by vitality |
| **Probe body** | Workload / runner / peer Palm | Inlined into orchestration |
| **Genome / code GC** | Later dogfood (guards today; optional analytics Palm) | **Not** living vitality kill condition |

### 8.1 Supervisor alignment

| Supervisor | Vitality |
|------------|----------|
| Runs work_drain, outbox, inbound | Reads loop lag / fail as **circulation** vitals |
| Prefers system seats | Dual host paths = structural entropy |
| Emits skip/fail to system log | Metrics derive; no parallel story |

Planes legislate. Supervisor pumps. Vitality observes. Design mutates definitions.

---

## 9. Dynamic by law (no hardcode, no dual copy)

Vitality must follow Palm’s **registry + composition + live kernel** spirit.  
Do **not** ship a fixed menu of counters that drifts from what this process actually runs.

### 9.1 What “dynamic” means

| Prefer | Avoid |
|--------|--------|
| **Traverse the living kernel** (seats on `SystemInstance`) | Filesystem walk as physiology |
| **Discover** what is alive (composition, supervisor services, planes attached) | Hardcoded “always show drain / outbox / …” |
| **One emission shape** every seat can speak | Parallel doctor fields hand-maintained next to real loops |
| **Seat report contract** + optional contributors | `if name == "work_drain"` forests in product |
| **Derive** scores from events already emitted | Second write path that re-describes the same fact |
| **Partition** by declared `actor_kind` when present | Guessed categories in presenters |
| **Same lexicon** as system log / doctor pointers (CS-002) | Fourth vocabulary for “health” |

**Composition-aware:** If work_drain is off, do not invent a green drain vital. Report **absent / skipped** from membership (same honesty as boot PhaseSkip).

**Supervisor-aware:** Loop vitals come from **services the supervisor actually owns** — iterate registered continuous services, do not mirror names in a second table.

**Plugin-aware:** New patterns/providers may contribute **optional** vital facets via a small contributor registry (same idea as design / CQRS contributors). Core stays thin.

**Not dynamic law:** Auto-`INSTALLED_*` from package scan. Capability catalog stays intentional.

### 9.2 Single source of truth

```text
  living SystemInstance seats + job/wait/effect emissions
            │  emit / report once
            ▼
     vital projection (read-only fold of discovered sources)
            │
            ▼
     doctor / assist / operate  (present only)
```

| Layer | Duty |
|-------|------|
| **Source** | Owns the fact on the kernel seat (drain lag on drain/supervisor service) |
| **Projection** | Dynamic fold: walk instance → sample → window → vector |
| **Present** | Thin view; no business rules that recompute truth |

**Forbidden duplication:**

- Copying supervisor status into a static product dict that can lie.  
- Hardcoding actor kinds beyond a **small stable enum** + extension map.  
- Hardcoding definition ids or flow names into “health rules.”  
- Re-implementing control_plane_status fields under new names.  
- Requiring a repo checkout to answer “is this Palm healthy?”

**Allowed constants (thin):**

- Stable **field names** for the emission envelope (`actor_kind`, `channel`, `kind`, …).  
- Default **window** / sample rates (overridable by settings).  
- Core `actor_kind` set (`human`, `agent`, `probe`, `system`, `peer`) — extend via registry if needed, do not fork per surface.

### 9.3 Homeostasis without hardwired cures

Routines (dream later) must also be dynamic:

| Prefer | Avoid |
|--------|--------|
| Policy table / definitions / composition flags | `if vital_x > 3: restart_y()` buried in supervisor |
| Named routine definitions (flows or registered handlers) | One-off scripts only the host knows |
| Mode-gated (`safe` forbids auto knobs) | Always-on magic |

Same as the rest of Palm: **capability at the edge**, law in one place, no secret second path.

---

## 10. Tool shape (when a theme opens)

Kill condition sketches — refine in a later VISION-0.X. **`top` for living Palm** is the tool bar.

1. **Walk the live `SystemInstance`** — discover seats that exist after start.  
2. **Layer A (load):** seat reports + emissions + optional process resources (no dual write; no repo required).  
3. **Shared seat report contract** — services/planes report; fold is generic.  
4. **Doctor (or assist) “top”** — summary + seat list; configurable depth by mode; **partition by `actor_kind` when known**.  
5. **Absent membership → skipped**, not green lies.  
6. **Layer B (bulk) optional:** light size of **loaded** seats/modules (visibility) — not a shame score, not required for first green.  
7. **No silent auto-commit** of definitions; no auto-condemn of large modules.  
8. **Heavy paths** optional / sampled; default cheap.  
9. **Out of first tool bar:** full-tree AST, ruff-as-doctor, hand class catalogs, auto-refactor.

Grow from residual **BI-015**, doctor honesty, supervisor seats (0.60).  
Do not wait for Grove or genome dogfood to ship a thin living `top`.

---

## 11. Dream shape (after tool)

| Dream piece | Meaning |
|-------------|---------|
| **Probe palms** | Small LLMs on another Palm walk **assist-first** on the subject; score accessibility yield against living vitals. |
| **Emission-aware Design** | Proposals cite probe vs human partitions; impact checks both. |
| **Homeostasis** | Routines sample **kernel vitals**, alert, wait for human, optional safe knobs — immune/maintenance, not total control. |
| **Grove ecology** | Peer reaction to emissions; org-level vitals language. |
| **Genome dogfood** | Optional: scan tree / import graph / guards as a **separate** Palm app — cool, not physiology. |

**Homeostasis caution:** routine actions that change **composition or loop knobs** need policy and modes (`safe` / `prod`).  
Routine actions that change **definitions** stay behind Design + human/agent commit.

Probe order relative to vitality tool:

- Thin **living** vitals land **without** probes and **without** filesystem.  
- Probes are the best **external** consumer of vitals and emission tags.  
- Full multi-Palm placement is Grove; early probe = process + MCP is enough.

---

## 12. Genome / full tree analytics (later dogfood)

| Idea | Status |
|------|--------|
| `guard_core` / `guard_deferred` today | CI fitness — keep |
| Workloads run ruff / layer metrics / package walk | Cool dogfood |
| Full `pkgutil` / AST “own GC” of modules | Genome observation; complements Layer B |
| Flows present CS/SU debt | Product on TECH-DEBT truth |
| Doctor second section “genome” | Optional; **never blend** with living load score |

**One day** Palm can compost its own tree with eyes open.  
**Need now:** living Palm metrics — **aware of load, bulk of what is attached, and emissions.**

---

## 13. Relation to other seeds

| Seed | Overlap |
|------|---------|
| [Surface deflation](VISION-SURFACE-DEFLATION.md) | Reduces **boundary** entropy so operate vitals are readable |
| Residual **BI-*** | BI-015 catalog/sinks; BI-003 dual root noise; host enrich residual |
| Residual **SI-*** | Attribution and session honesty improve emission identity |
| Residual **SU-*** | Probe thrash often points here first |
| [Grove](VISION-GROVE.md) | Probe/capacity palms; peer emissions; org conversation |
| Workload remainder | Isolation for probes and analytics jobs |

**Not paid here:** user impersonation, plane-store framework, full mesh.

---

## 14. Forbidden

- Vitality as a **plane** that starts or continues work.  
- Algorithms that **silently** rewrite definitions.  
- Supervisor as Design.  
- Blended telemetry without **emission identity**.  
- Claiming **living load** from **static** code metrics alone.  
- Blocking living `top` on full genome dogfood.  
- **Shame scores** that auto-condemn large modules (visibility ≠ guilt).  
- Hiding workload cost to look green.  
- A third observability vocabulary that fights system log / doctor names.  
- **Hardcoded vital menus** that ignore composition / supervisor membership.  
- **Duplicated status trees** (product re-implements what system seats already expose).  
- Magic `if service_name == …` cure paths instead of registered policy.  
- Auto-install capability from package scan.

---

## 15. How to plan (pristine before code)

Vitality is **kernel-grade**. Plan like boot and supervisor: ADR + home table + thin contracts first.  
Do not ship a black-box agent that “just measures.”

### 15.1 Architecture sketch (three layers)

```text
  ┌─────────────────────────────────────────────────────────────┐
  │ PRODUCT — InspectService (today SystemService / SD-007)     │
  │  doctor · top · assist aliases · surface/CQRS business view │
  │  policy / envelope only — no second truth                     │
  └──────────────────────────▲──────────────────────────────────┘
                             │ reads
  ┌──────────────────────────┴──────────────────────────────────┐
  │ SYSTEM — vitality home (not a plane of law)                 │
  │  VitalityProjection: discover seats → fold → snapshot       │
  │  VitalityRegistry: named capabilities (grow here)           │
  │  Seat report protocol on planes / supervisor services       │
  └──────────────────────────▲──────────────────────────────────┘
                             │ reports / emissions
  ┌──────────────────────────┴──────────────────────────────────┐
  │ LIVING SEATS — kernel already there                         │
  │  planes · supervisor loops · ports · system log · membership│
  └─────────────────────────────────────────────────────────────┘

  OPTIONAL tools (registry, not core forever):
    benchmark seat · monitor agent (local workload or remote Palm)
```

| Piece | Home | Must not |
|-------|------|----------|
| Seat counters / emit | Owning seat (plane, continuous service) | Product invent parallel numbers |
| Projection + registry | **`palm.system`** (e.g. `vitality/` or under `log`/inspect seat) | Domain service owning kernel truth |
| Business / surface view | **Product Inspect** (rename from SystemService — pays **SD-007**) | Be named “system” forever |
| Benchmark / monitor tools | Registry capabilities; body may be **workload** or **peer Palm** | Silent inlined magic in BaseRuntime |
| Genome AST tree | Later dogfood | Gate living `top` |

**Law:** Home is **system**. Surface sees **product inspect**. Workloads/remotes are **how some tools run**, not where law lives.

### 15.1a Doctor vs vitality vs inspect (names and intent)

**Shared intent (keep):**  
To act well, Palm (and operators/agents) must **know what is known** — what is attached, what is load, what failed, what is absent.  
That is **self-knowledge for action**. Doctor today carries a piece of that intent. It is not the full intrinsic concept.

**Do not build vitality “on top of doctor.”**  
Do not treat current `doctor()` as the kernel home. Implement **properly in system**; let product **present**. Current doctor may stay as **one report shape** or be thinned later — it still has a place (anatomy / checklist), not as the only eyes.

| Concept | Intent | Home | Dynamic? |
|---------|--------|------|----------|
| **Vitality** (system) | Living physiology — seats, load, emissions, capability fold | **System** projection + registry + seat reports | **Yes** — discover what is alive/enabled |
| **Doctor** (report / verb) | Snapshot **diagnosis**: assembled? wired? known fails? preflight | Product **view** over system facts (+ legacy control_plane glue) | Partial today; should **read** vitality + boot, not own counters |
| **Inspect** (product door) | Operator/agent **API** to see and act (list, cancel, doctor, top, …) | `InspectService` (today SystemService) | Present only |

```text
  self-knowledge (intent)
        │
        ├── VITALITY     system-intrinsic eyes   ← build here properly
        │     (physiology / top / capability fold)
        │
        ├── DOCTOR       one diagnostic view     ← keep concept; thin implementation
        │     (anatomy + checklist + “what’s wrong?”)
        │
        └── INSPECT      product door            ← rename SystemService
              surfaces call this; never own kernel truth
```

**What is “such”?**  
The system-intrinsic thing is **vitality** (or speech: **system observation** / **living metrics**).  
Not a second doctor. Not a domain. Not a plane of law.  
It is the kernel’s **eyes**: dynamic discovery of what the instance knows about itself, so action (human, agent, later homeostasis) can be based on **truthful, current, lineage-bearing** knowledge.

| Term to prefer | When |
|----------------|------|
| **Vitality** | System home, registry, projection, seat reports |
| **Top** / load view | Operator metaphor for the living snapshot |
| **Doctor** | Diagnostic **report** or assist verb (“run doctor”) — may compose vitality + boot + stubs |
| **Inspect** | Product service and surface door |

**Act dynamically based on what we know** means:

1. **Know** via vitality (and boot membership, system log).  
2. **Present** via inspect (doctor view, top view, …).  
3. **Act** via existing law (start/continue, Design, assist, later homeostasis policy) — not via doctor inventing a side path.

**Proper redo:** same *need* as doctor (know so we can act), **different home and mechanism** — intrinsic, registry-dynamic, seat-reported. Ignore doctor as foundation; optionally **rewrite doctor as a consumer** of vitality later.

### 15.2 Not a black box

| Transparent | Black box (forbid) |
|-------------|-------------------|
| Seat reports a known schema | Hidden sampler mutates jobs |
| Registry lists capabilities + maturity | Undocumented “monitor thread” |
| Projection is pure fold of reports + emissions | Side-effecting health daemon as default |
| Doctor shows **sources** (which seat, which capability) | Single green score with no lineage |
| Modes gate cost (`safe` / `test` cheap) | Always-on heavy scrape |

Operator/agent must answer: *what was measured, by whom, from which seat, under which capability?*

### 15.3 Registry (growth is certain)

Vitality will grow. Prepare the home like plugins — **capability registry**, not a closed enum forever.

**Why a registry (not a closed module):**

| Reason | Meaning |
|--------|---------|
| **Growth is certain** | Eyes add tools over years; a fixed `if` forest in projection rots |
| **Membership honesty** | Composition / mode enable capabilities; absent → skipped, not fake green |
| **Maturity truth** | Installed vs intention (same spirit as `INSTALLED_*` / STUBS) |
| **Extension at the edge** | Contributors add facets without editing kernel fold law |
| **Transparent lineage** | Snapshot cites `capability_id` that produced each block |
| **Placement freedom** | Some capabilities run in-process; some place as workload / peer Palm — registry names the *what*, not only the *where* |
| **Not a domain bag** | Registry is for **vitality tools**, not business domains (flows, billing, …) |

**Projection law stays thin:** iterate **enabled** capabilities → each returns a typed fragment → merge → snapshot.  
Capabilities do not own start/continue. They only **observe** (or, for tools, **drive declared load** under policy).

#### Capability catalog — how complete is this list?

| Completeness | Meaning |
|--------------|---------|
| **Known (planned)** | Named below with role and horizon — enough to open a theme without inventing homes later |
| **Possible (horizon)** | Reasonable growth; not kill conditions; registry must not forbid them |
| **Not comprehensive forever** | Market and Palm will invent more eyes; registry is the **slot**, not a frozen product list |
| **Not claimed implemented** | Catalog is **vision**, not code |

##### A — Core observe (first theme bar)

| Id | Role | Inputs (sketch) | Outputs (sketch) |
|----|------|-----------------|------------------|
| `seat_walk` | Discover attached seats; fold reports | `SystemInstance`, membership | Seat list, absent/skipped, per-seat counters |
| `emission_window` | Sample recent job/wait/intent/effect outcomes | Events, rings, optional journal window | Yield, wait heat, fail classes; `actor_kind` when known |

##### B — Optional observe (same theme or immediate next)

| Id | Role | Notes |
|----|------|--------|
| `process_resources` | Process RSS/CPU/threads | Stdlib first; optional extra; mode-gated cost |
| `loaded_bulk` | Size map of **loaded** seats/modules | Layer B light — visibility, not shame |
| `boot_membership` | Re-present last boot walk / PhaseSkip as vital context | May alias system log / boot facts — no dual story |
| `system_log_tail` | Recent system-log lines as operate tape | BI-015 neighbor; present, not second bus |
| `supervisor_loops` | Explicit fold of supervisor-owned continuous services | May be part of `seat_walk` if services already report |

##### C — Active tools (later; registry-ready)

| Id | Role | Placement |
|----|------|-----------|
| `benchmark` | Controlled load recipe; compare vitals under stress | In-process light or **workload** |
| `monitor_agent` | Long watch; threshold → alert / wait / assist note | **Local workload** or **remote Palm** |
| `probe_drive` | Declared accessibility walk (small LLM / scripted assist) | Peer/workload; scores via emissions + subject vitals |
| `diff_snapshot` | Compare two vitality snapshots (before/after slice) | Pure fold on stored snapshots — great for dev |
| `export_snapshot` | Emit snapshot to sink (JSON file, optional) | BI-015-ish; not OTel product |

##### D — Genome / compost (dogfood; not living bar)

| Id | Role |
|----|------|
| `genome_scan` | Package/import/AST walk of tree |
| `guard_mirror` | Surface guard_core/deferred results into inspect |
| `debt_link` | Map hot seats ↔ TECH-DEBT ids (CS/SU) when known |

##### E — Possible later (do not forbid; do not build yet)

| Id | Role |
|----|------|
| `session_vitality` | Aggregate by session subject (multi-instance walks) |
| `definition_vitality` | Per-definition aggregates for Design feedback |
| `peer_vitality` | Ingest peer Palm snapshots (Grove) |
| `homeostasis_policy` | Named routines that **read** vitals and act under mode policy |
| `otel_bridge` | Optional export bridge — never replace Palm lineage |
| `custom_contributor` | Plugin-registered facet (pattern/provider-specific counters) |

**Minimum to claim “eyes open”:** A (`seat_walk` + thin `emission_window`) + product present.  
**Minimum to claim “registry ready”:** register A–B ids; C–E may be stubs or absent.

**Registry rules (Palm spirit):**

- Composition / mode may enable capabilities (membership honesty).  
- Intention vs installed maturity if a tool is experimental.  
- Contributors may register **optional** facets (same pattern as design/CQRS).  
- Core projection stays thin: **iterate registry → run enabled → merge**.  
- **Do not** put business domains in this registry.

### 15.4 Tools: benchmark seat & monitor agent

Not required to open the theme. Design so they **fit** later without rewrite.

| Tool | What it is | Placement |
|------|------------|-----------|
| **Benchmark seat** | Declared load recipe; measures subject before/after or under stress | System capability; run body via **workload** or inline light for dogfood |
| **Monitor agent** | Watches vitals over time; alerts / opens wait / assist note | Capability; **local Palm workload** or **remote Palm** (Grove spirit) that only **reads** inspect/vitality APIs |

**ohohoho oh boy is correct:** monitor-as-workload is dogfood of 0.56 + vitality.  
Remote monitor is Grove rehearsal — same genome, continuous interface (assist/MCP/doctor), not a private scrape wire.

**Rule:** Tools **consume** projection; they do not own a second metric law.

### 15.4a Dynamic tools — first-class Palm, not workarounds

**Question:** Will tools be truly dynamic and treated properly, or will we invent hacks so we can “monitor everything”?

**Answer we commit to:** evolve Palm so vitality is a **proper system concern**. Refuse a culture of workarounds.

| First-class (required) | Workaround (forbid as path of record) |
|------------------------|----------------------------------------|
| Seats **report** via a shared protocol | Scrape private attributes / `__dict__` as law |
| Projection **discovers** enabled capabilities | Hardcoded list of every module to “cover” |
| Tools registered, mode/composition gated | Undocumented threads, monkey-patches, import hooks |
| Monitor/benchmark use **assist / inspect / ports** | Parallel debug HTTP only the monitor knows |
| Emissions already on job path | Second write path “for metrics only” |
| Absent seat → skipped | Fake green by probing dead code paths |
| Remote monitor = peer Palm + continuous interface | SSH into process / pdb in prod as design |
| Growth = new registry capability | Growth = another `if name ==` in BaseRuntime |

**Dynamic means:**

1. **What is alive** — only seats and capabilities present after start (membership).  
2. **What is enabled** — composition + mode + registry maturity.  
3. **What is reported** — protocol fragments, same shape for core and tools.  
4. **Where tools run** — in-process, workload, or remote Palm — without changing **what** is measured (projection law).  
5. **What agents see** — inspect/doctor/assist; no secret side channel as the real API.

**Dynamic does not mean:**

- Reflect on every object in the heap and call it health.  
- Auto-instrument every domain service with magic.  
- “Monitor everything” by bypassing planes and ports.  
- Evolve the kernel only when a workaround fails.

**Proper evolution (preferred pressure):**

| Gap | Proper fix | Not |
|-----|------------|-----|
| Seat has no counters | Add report method on that seat | Product guesses from logs alone |
| New continuous service | Supervisor owns it → appears in walk | Special-case name in doctor |
| Need long watch | `monitor_agent` capability + workload/peer | Cron + curl recipe only |
| Need stress | `benchmark` capability under policy | Manual thrash with no snapshot lineage |
| Need agent access | Inspect + assist aliases | New private MCP scrape tools |

**Theme bar:** if a metric cannot be obtained without a workaround, either **extend the seat contract** (proper) or **do not claim** that metric in vitality (honest).  
Do not ship the workaround as the architecture.

**Palm already treats other concerns this way:** ports for effects, planes for traffic, registries for plugins, supervisor for loops. Vitality is the same discipline for **eyes**.

### 15.5 Product rename — InspectService (pair, not block)

| Today | Pain | Target speech |
|-------|------|----------------|
| `palm.services.system` / `SystemService` | Collides with **system layer** (**SD-007**) | **InspectService** (or `services.inspect`) — doctor, top, cancel/list operator views |

**Pairing with vitality:**

- Product inspect = **business rule view** for surfaces (Explorer, assist, MCP).  
- System vitality = **kernel truth**.  
- Rename can be **same theme** (early slice) or **immediate follow** — do not leave two names forever.  
- Host attribute `host.system` → `host.inspect` (migration alias temporary if needed).

Vitality does **not** live in product. Product only **presents**.

### 15.6 Suggested theme slices (when open — not open yet)

Pristine order; one purpose per slice:

| Slice | Deliverable | Kill |
|-------|-------------|------|
| **0.plan** | VISION-0.X + ADR (homes, registry, non-goals, Inspect rename policy) | Names locked |
| **.1** | Seat report protocol + walk discover on `SystemInstance` | Empty phenotype shows absent seats honestly |
| **.2** | `VitalityProjection` + registry core (`seat_walk`) | Doctor section `vitality` / `top` from projection only |
| **.3** | Thin `emission_window` + `actor_kind` when present | Partition or “unknown” explicit |
| **.4** | InspectService rename (SD-007) + surface/assist door | No dual product name; business view over system seat |
| **.5** | Optional `process_resources` / light `loaded_bulk` | Off by default or mode-gated |
| **.6+** | Benchmark / monitor agent capability stubs + workload dogfood | Registry grows; still transparent |
| **exit** | ADR Accepted; docs; residual named | `just check` green |

**Out of first theme:** genome AST app, auto Design from vitals, Grove mesh, shame scores.

### 15.7 ADR seeds (when open)

Lock in ADR (or VISION-0.X decisions):

1. Vitality is **system observation**, not a plane and not product truth.  
2. Projection is **dynamic discovery** + **registry**, not domain hardcode.  
3. Product door is **Inspect** (rename SystemService).  
4. Tools (benchmark, monitor) are **registered capabilities**; placement may be workload/peer.  
5. Emission identity required for mutation-facing aggregates.  
6. Modes control cost; `safe`/`test` stay cheap.  
7. No silent job mutation from vitality.

### 15.8 Market rarity (why purpose is exciting)

Most software ships dashboards **outside** the kernel, or APM glued on. Few treat **self-physiology** as a first-class system seat with:

- the same **layer laws** as the rest of the OS picture,  
- **registry growth** without dual paths,  
- **human + agent** operate surface,  
- later **Palm-on-Palm** monitors.

Palm already has the hard parts (planes, supervisor, session, honest catalog).  
Vitality is giving the organism **eyes** that match its structure — not bolting Prometheus and calling it culture.

Purpose is allowed. Fear of “not how the market does it” is not a Palm law.

---

## 16. Open questions (ponder before open theme)

1. Package path: `palm.system.vitality` vs seat under `system.log` / `system.inspect`?  
2. Minimal seat report schema (fields, versioning).  
3. Registry key names and composition flags for capabilities.  
4. InspectService rename blast radius (host, assist, MCP, Explorer) — same theme or immediate next?  
5. Process metrics: stdlib only vs optional extra.  
6. First theme sense-only vs include empty benchmark/monitor **registry stubs**.  
7. Name in UI: *vitality* · *top* · *inspect* — one lexicon.  
8. How monitor agent authenticates to subject (session bind, service session).  

---

## 17. Spirit

> **Doctor is anatomy. Supervisor is circulation. The kernel is the body. Vitality is Palm’s `top` — dynamic view of the living system. Inspect is the product door. Registry is how eyes grow. Tools may run as workloads or peer palms — they never own a second truth. Design is mutation with consent. Visibility shows bulk and load; it does not hide work or auto-condemn size. Purpose is allowed.**

**Start** is built (kernel, planes, supervisor, log).  
**Plan** locks homes, registry, inspect rename, non-black-box law.  
**Tool** = living metrics, pristine and dynamic.  
**Dream** = probes, homeostasis, Grove monitors, genome dogfood.  
**Development** gets eyes — so growth is not blind.

---

*Seed essay. Theme open: [VISION-0.61](VISION-0.61.md) · [ADR-030](adr/030-system-vitality.md). Prefer tool before dream. Prefer live kernel walk over hardcode. Prefer registry over closed box. Prefer Inspect product name over SystemService collision. Prefer proper eyes over workaround architecture.*
