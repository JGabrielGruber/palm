# Component — structure management

**Status:** Intended description (living).  
**Theme seed:** [VISION-ASSEMBLY](../../vision/VISION-ASSEMBLY.md) · honesty [§0](../../vision/VISION-ASSEMBLY.md#0-progress-honesty-2026-08-08).  
**Terms:** [glossary §2](../../glossary.md#2-structure-management-organism-ready).  
**Lifecycle:** [views/lifecycle.md](../../views/lifecycle.md).

---

## 1. Job

Between **machine up** (boot) and **business runs** (job path), Palm needs one care: **organism ready**.

**Structure management** owns desired structure for this process: what may exist, reconcile toward it, **materialize** membership, publish **admission**.

It is **not** a second job orchestrator. It is **not** product or surface implementation. It is **not** host dig as structure API.

Analogy (teaching only): local **compose + init** for Palm’s own plugins, product, surfaces, and system capabilities — see [appendix/metaphor.md](../../appendix/metaphor.md) for retired kingdom language.

---

## 2. Two layers: engine (core) vs manager (system)

This split is intentional and must stay clean.

```text
  Structure definition (data)
           │
           ▼
  ┌─────────────────────────────┐
  │  Structure reconciler       │  CORE — pure
  │  (engine)                   │  definition + observations
  │  → status + effect intents  │  → no I/O, no install
  └─────────────┬───────────────┘
                │ intents / status
                ▼
  ┌─────────────────────────────┐
  │  Structure manager          │  SYSTEM — impure
  │  resolve sources            │  load definition
  │  apply effect hands         │  materialize membership
  │  fold observations          │  publish admission on shell
  └─────────────┬───────────────┘
                │
                ▼
         Admission (may business run?)
```

| Piece | Layer | Package home (intended / lag) | Duty |
|-------|--------|-------------------------------|------|
| **Structure definition** | Data | `palm.core.assembly` types (lag name) | Declarative desired structure + membership sections |
| **Structure reconciler** | **Core** | `palm.core.assembly` · **AssemblyEngine** | Pure tick: intents + status. No packages install. No provider I/O. |
| **Effect port / hands** | **System** | `palm.system.assembly` | Apply intents (places, policy, …); return observations |
| **Structure manager** | **System** | seat + loop + resolvers + materialize | Orchestrates reconcile **and** real-world membership; publishes admission |
| **Admission** | Published on shell | snapshot from status | Fail-closed gate for business that needs ground |

**Yes:** core has the **engine** (reconciler).  
**Yes:** system has the **manager** (seat, loop, hands, materialize, resolvers).  
The manager **uses** the engine; it does not reimplement pure reconcile in product.

**As-built lag:** system seat + assemble loop + admission are real; **membership materialize** (install only what definition lists; no freelanced host soup) is the deep remaining work. Admission walls are the **dashboard** half.

---

## 3. Structure definition (membership shape)

Intended: definition carries **sections** of membership units (names open; spirit like `INSTALLED_APPS`):

| Section (intended) | Examples of units |
|--------------------|-------------------|
| **capabilities** | journal, outbox, work_drain, … |
| **plugins** | patterns, providers, storages, runners, … |
| **products** | assist, execution façades, domain services, … |
| **surfaces** | cli, rest, mcp, ssr, … |
| **refuse / places / role** | structure policy and place book intent |

Each unit may eventually carry a **membership source** (`local` | `provider` | …).  
Manager materializes units; it does not become their business logic.

---

## 4. How membership is obtained (resolvers)

One **materialize** step; pluggable **source resolvers**:

| Source | Meaning | When |
|--------|---------|------|
| **local** | Python packages / definition already on this system | **First build** |
| **provider** | Palm provider **provides** definition packages over Palm protocol | Multi-process / support home |
| **cache / replicate** | Provide once → store local → later boots use **local** | Far future (supporter replication) |

Remote is **provide**, not freestyle download-as-architecture.  
Download-to-disk is a **replication mode of provide**, not a rival story.

See glossary: membership source, structure source resolver, definition package, provide.

---

## 5. What the manager controls (and does not)

| Controls | Does not control |
|----------|------------------|
| Whether plugins / products / surfaces / capabilities **may exist** here | Their internal business or transport protocols |
| Wire / install only allowed units | Job path orchestration |
| Places and structure effect intents | Customer flow definitions as structure |
| Publish admission | Authn/authz product policy |
| Reassemble under new definition | Grove mesh (later seeds) |

Roles at scale (later): thin orchestrator, support **serves** definitions, worker **uses** a definition cut — same manager, different definition content and sources.

---

## 6. Relationship to host and product

- **Host** seeds which definition to load and wires once; after load, definition + manager are structure law.  
- **Product / surfaces** are clients: ports + admission; no composition-root dig for readiness.  
- **Boot** brings the machine up; manager runs as the structure-ready care (phase after system ready enough to assemble).

---

## 7. Progress honesty

| Built (roughly) | Deeper remaining |
|-----------------|------------------|
| Reconciler + status + admission | Full membership **materialize** (plugins / product / surfaces) |
| Fail-closed doors on many business paths | Definition as install set beyond `work_drain` |
| DNA `capabilities` + manager materialize of **`work_drain`** | Other capability units still host/composition |
| Seed map (mode/env → definition id) | Provider source resolver; cache/replicate |
| Place hands (partial) | Structure as sole owner of freelanced bootstrap soup |

First implementation cut (capabilities / `work_drain`; theme stamp open): [appendix/structure-materialize-cut.md](../../appendix/structure-materialize-cut.md).

---

## 8. Diagrams (to add)

- Component context: boot → structure management → job path / surfaces  
- Sequence: load definition → resolve → materialize → tick → admit  
- Package: `core.assembly` vs `system.assembly` (see [c4-code](../../c4-code/README.md))
