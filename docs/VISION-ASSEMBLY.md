# VISION — Assembly (organism truth · tree scale)

**Status:** 📋 **Queue seed** — named **2026-08-05**. Not an open minor. José may open a theme when the floor is ready.  
**Language:** ASD-STE100 (practical).  
**Map:** [PALM.md](PALM.md) · [VERSIONING.md](VERSIONING.md) (floor · growth · exit · **José** decides)  
**Spine we keep:** [VISION-0.57](VISION-0.57.md)+ system · [VISION-0.56](VISION-0.56.md) workload scout · [VISION-0.55](VISION-0.55.md) reactive · [VISION-0.62](VISION-0.62.md) capacity  
**Horizon:** [VISION-GROVE](VISION-GROVE.md) (multi-Palm org — later) · surface compost [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md)  
**Debt touchpoints:** workload remainder · [SD-019](../TECH-DEBT.md#sd-019) · [SD-016](../TECH-DEBT.md#sd-016) · host/profile glue · catalog wire residual  

---

## 1. Why this note exists

Palm can boot a **system**. Palm can run **business** (flows, start, continue).  
Between those two cares, structure is still **glue**: profiles, host enrich, catalog load order, soft “definitions ready,” future spawn scripts.

That glue multiplies when Palm scales past one process.

This file names the **missing steward** and the **tree-shaped scale** that workloads and multi-process must serve.  
It does **not** open a theme. It does **not** replace boot, orchestration, or the workload plane.

**Duty:** write the structure Palm will grow into — realistic, named, honest about what we cannot do yet.  
**Posture (from 0.57+):** plan the home; engine then alternate path; validate; migrate; clean. Prefer 80/20. Complete what is open. Put debt where a theme can own it. Prefer proper over hot glue.

Palm is **experimental** and **pre-1.0**. There is **no long-term support** promise. See [README](../README.md). Break for truth.

---

## 2. The missing care (lifecycle)

| Care | Owner today | Job |
|------|-------------|-----|
| **System up** | Boot + seats + supervisor | Machine lives: planes, ports, continuous loops |
| **Organism ready** | **Missing home** (scattered glue) | Definitions and ground are real; topology intent holds; business may start honestly |
| **Business runs** | Orchestration + work/wait planes | Flows, jobs, start, continue |
| **Places exist** | Workload plane (scout) | Named bodies: spawn or adopt; health; stop |

**Assembly** is the name for **organism ready**.

| Prefer | Avoid |
|--------|--------|
| One steward after system, before business | Stuff assembly into boot forever |
| One steward that loads **authoritative** plan | Encode every role only as profile flags |
| Workload as **place book** | Workload as second orchestrator |
| Flows as **business rules** only | Encode cluster topology as a customer flow |

**Coordinator (lifecycle sense):** assembly coordinates *becoming* Palm.  
**Orchestration (engine sense):** runs business once assembly truth holds.  
Do not fight the word “orchestrator” as a **profile role** (light center). That role is topology. Assembly is the **lifecycle phase**.

---

## 3. Normative terms

Define once. Reuse.

| Term | Meaning |
|------|---------|
| **Assembly definition** | Declarative DNA: role, truth home, required places, refuse rules, projection rules, seat intent. Single truth when loaded from authority. |
| **Assembly engine** | Pure interpreter of assembly definition → assembly status + requested effects (via ports). Not sockets. Not OS spawn. Not business jobs. |
| **Truth home** | Place that is **authoritative** for durable meaning this process projects (definitions, store faces, ground). |
| **Projection** | Local view of authoritative state. Cache or index allowed. Source of truth stays at truth home. |
| **Invalidate** | Drop or seal projection when truth home is not ready. Refuse work that needs that truth. |
| **Place book** | Workload registry of named places (spawn or adopt). Lifecycle + readiness. |
| **Control home** | Who assigns work and whose surfaces this process uses for control (may equal truth home or sit above it). |
| **Light center** | Composition **rule**: refuse heavy job body and/or durable ground on purpose; place weight; stay efficient. Not “unable.” |
| **Work place** | Place whose role is to execute work the light center will not carry. |
| **Support place** | Place whose role is to hold durable ground or other weight the center will not hold. |
| **Tree topology** | Each node depends **up** for authority/control. Not full mesh first. |
| **Profile** | Local bootstrap seed and defaults. Authority may override structure via assembly definition. |

**Invocation** (call another Palm’s door) ≠ **projection** (represent their truth as part of *our* readiness).

---

## 4. Law (intent)

1. **Boot** cares for the **system**.  
2. **Assembly** cares for **organism truth** so business can be honest.  
3. **Orchestration** cares for **business rules** after organism truth holds.  
4. **Workload** cares for **places** (inventory of bodies). Assembly **requests** places; it does not reimplement runners.  
5. **Authoritative first, then the rest.** Truth-home place ready → load or refresh assembly definition and projections → finish seating/binding → then drain and flows that need that truth.  
6. **Truth home is a place in the book.** Without readiness, projection is faith. With it: not ready → invalidate → do not pretend.  
7. **Tree first.** Home points up. Relays may exist later with hop limits. Full mesh and rich middleman proxy are **Grove growth**, not the entry ticket.  
8. **Do not kill what works.** All-in-one Palm remains valid. Light center is a **chosen rule**, not the only shape.  
9. **Business BT ≠ assembly tree.** Same grammar may tick assembly (ensure / gate / leaf). Different subject. Different home.  
10. **Pre-1.0:** break glue; name residual; no LTS theater.

---

## 5. Workload refined (scale without a second panic)

Workload is not only “run a container.”

| Workload is | Workload is not |
|-------------|-----------------|
| Named places and availability | Claim law for WorkIntents (that is work plane + store) |
| Spawn **or adopt** | The assembly definition itself |
| Gate: dependency down → do not start that work yet | A second business orchestrator |
| How multi-process (local and remote) becomes **controlled** | Magic concurrency without readiness |

**Multi-process and network process** become real when places are in the book and assembly (or business) **uses only what is tracked**.  
Palm does not need a new lock religion first. It needs **place readiness** and **projection honesty**.

In-process multi-claimer capacity remains [0.62](VISION-0.62.md). Multi-writer shared store remains [SD-019](../TECH-DEBT.md#sd-019). Assembly does not erase that residual.

**Light center dogfood (profile rule, not universal law):** ensure support place + work place; project from support; then Palm-as-known. The center may still place ordinary workloads (e.g. postgres) without every dependency becoming its own Palm — avoid abstraction hell.

---

## 6. Profiles and dynamic structure

Profiles today capture part of assembly (roles, flags, deployment shape). Keep them as **seeds**.

With assembly:

1. Process boots far enough to find authority (or run all-in-one local DNA).  
2. Authority ready → load **assembly definition**.  
3. Assembly engine (or steward) defines what this Palm **will have**.  
4. System finishes assemble to that plan.  
5. Business works.

Structure becomes **data-driven from one truth**. Glue of “if profile then install…” moves into definition + engine, then migrates off host spaghetti.

---

## 7. Tree of processes (near scale)

```text
        Light center (optional rule)
        control + claim + surfaces
                 │
     places / readiness (workload book)
        ┌────────┴────────┐
        ▼                 ▼
  Support place      Work place(s)
  (truth home)       (job body)
        │
   projection up when ready
```

- Worker may use center as **control home**.  
- Truth home may be support place, or center after it projects. Choose explicitly in definition; do not blur.  
- Mid nodes that only **propagate** authority are not required to be thin “worker profile.” Any Palm may depend on another Palm.  
- Organization and realms stay [Grove](VISION-GROVE.md) vision. They do not block assembly floor.

**Cluster slogan elsewhere:** master/workers.  
**Palm slogan:** genome + roles + place book + assembly. Workers are full genome under a rule, not dumb slaves.

---

## 8. What other systems do (lineage, not copy)

| Elsewhere | Palm mapping |
|-----------|--------------|
| K8s desired state + readiness | Assembly definition + place readiness |
| OTP supervision / start phases | Tree topology + assemble then serve |
| Config/service discovery join | Projection from truth home |
| OSGi resolve/start levels | Definition-driven seats |
| Workflow products’ worker fleets | Often **ops outside** the product soul |

Palm’s rare packaging: **assembly** next to **orchestration** and **workload**, in a BT-native organism. The *need* is common. The *named organ* is the ambition.

---

## 9. Growth path (when José opens a theme)

Same rhythm as system seasons: **engine → alternate path → validate → migrate → clean**.

| Stage | Spirit |
|-------|--------|
| **Floor** | Assembly definition artifact + pure interpret/status; one alternate path (e.g. light center or all-in-one DNA); truth-home place in book; invalidate when down; business gated on definition-ready |
| **Growth** | Profiles as seeds only; more place kinds; worker projection; adopt external places; tickable assembly plan (BT grammar, **not** business flow domain); vitality/inspect shows assembly status |
| **Later / Grove** | Multi-host tree, hop limits, proxy-through-center, org crown |
| **Non-goals for first theme** | Full mesh; replace orchestration; force every boot to fork support+worker; CAS multi-process claim (SD-019 unless natural); surface purge |

**80/20:** one real definition-ready path beats a perfect cluster brochure.

**Boy scout:** when assembly touches host glue or catalog wire, move truth toward assembly definition — do not only relocate menus ([AGENTS §1.1](../AGENTS.md)).

---

## 10. What we keep (spine)

Do not redesign these to invent assembly:

- Job path and pure core  
- Start / continue (work plane + wait plane)  
- Session law  
- Workload plane foundation (place / exec / runners)  
- Supervisor continuous seats  
- Vitality + Inspect  
- In-process exclusive claim (0.62)  
- Registry extension and seat DI direction  

Assembly **removes future glue** and **absorbs scattered become-Palm glue**. It does not erase the seasons that made the tree possible.

---

## 11. Horizon (dream, not floor)

Palm is a strong home for **datasets**, **training automation**, and **workloads** that run TinyML or larger models. Those bodies are places in the book. Assembly and light-center rules keep the center efficient so small runtimes can live well under Palm.

Dream after tool: organism DNA from authority, workers and support places as honest branches, business flows that train and serve without lying when ground is down.

---

## 12. Honesty and honor

| Do | Do not |
|----|--------|
| Name what we cannot ship yet | Fake green for absent assembly |
| Plan debt into a theme home | Hot-glue mid-slice with no residual row |
| Prefer completing open intent | Leave half-homes because speed felt good |
| Say experimental / no LTS out loud | Imply enterprise support pre-1.0 |
| Increase start cost for structure | Pay forever in glue when speed matters most |

Palm did not always know what it wanted. Past code is history and teacher — not always the prime example.  
**Duty now:** know better, do what we can, say what we cannot, plan the opportunistic moment. That is organic. That is honorable.

---

## 13. Success picture (for a future theme exit — not a checklist today)

1. A reader can point to **assembly** as the steward between boot and business.  
2. An assembly definition can shape what a process has without open-coded profile soup for that path.  
3. Truth home is tracked; down means invalidate; dependent work does not pretend.  
4. Workload remains the place book; business flows remain business.  
5. All-in-one still works; light center is optional rule.  
6. Docs and ADR match code; residual named; José judges exit.

---

## 14. Open decisions (close when theme opens)

1. Package home: `palm.core.assembly` vs system-first steward then core extract.  
2. Assembly definition storage and how authority serves it.  
3. Worker truth home: center only vs support place direct.  
4. How much BT grammar on day one vs linear ensure plan.  
5. Relation to existing DeploymentProfile / composition flags (seed map).  
6. ADR number when theme opens (append-only).

---

## 15. One sentence

**After the system is up, assembly makes the organism true from authoritative DNA and tracked places; only then business runs — so Palm scales as a tree of named places without mesh theater or glue as architecture.**

---

*Seed essay. Not a theme open. Prefer tool before dream. Prefer place readiness before multi-writer myth. Prefer honor over sparks.*  
*José decides when this becomes a minor.*
