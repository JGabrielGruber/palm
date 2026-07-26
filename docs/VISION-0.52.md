# VISION 0.52 — The Living Library

**Status:** 🟢 **Open (0.52.0)** — plan + [ADR-021](adr/021-living-library.md). Execution starts at 0.52.1.  
**Theme:** Knowledge architecture for Palm: *one genome of truth, many surfaces that serve it.*  
**Debt line:** TECH-DEBT **T6** (docs-as-code) — PD-019, PD-020, PD-021, PD-031 — plus intentional growth beyond the register.  
**Sibling conventions:** [VERSIONING.md](VERSIONING.md), [AGENTS.md](../AGENTS.md) §5, [PHILOSOPHY.md](../PHILOSOPHY.md).  
**Sequel:** **0.53** — build the library *with Palm* (pipeline dogfood), not a shell around `just`.

> *Palm grows where the sun meets the sea.*  
> Documentation is not a pile of leaves at the root — it is the **canopy**: how light reaches others.  
> Structure the canopy first; a thin builder is enough. Teaching the tree to *be* the builder is the next season.

---

## True intent

Palm already has a pure core, registry-driven edges, and multi-shape runtimes. Its **knowledge** has not kept the same discipline:

- Root markdown sprawl (~50+ living files, RELEASE/MIGRATION overlapping CHANGELOG).
- Version stamps and mirrors lag (PD-019, PD-031).
- ADR gaps (PD-020).
- Website is a beautiful handcrafted landing page (`docs/index.html` + Tailwind + Cloudflare assets) — not yet a library.
- Agent surfaces (`llms.txt`, `mcp.txt`, skill mirrors) are parallel truths that drift.

**0.52 makes documentation a first-class Palm concern** — not by bolting a heavy static-site monorepo on the side, but by applying Palm grammar:

| Palm law | Living Library analogue |
|----------|-------------------------|
| Core purity | **Source of truth** is narrow and explicit (hand prose + code-derived inventories) |
| Register downward | Builders **read** registries and packages; they do not invent parallel APIs |
| Composition × deployment | **What knowledge exists** vs **where it is served** (SSR, Cloudflare, MCP, offline) |
| Early structure, honest stubs | Shelves exist before every shelf is full |
| Minimal magic | **Simple builder** (`just docs-build` + small stdlib/scripts) — no mkdocs/Sphinx tax in 0.52 |

### Two seasons of dogfood (do not blur them)

| Minor | Builder | Intent |
|-------|---------|--------|
| **0.52** | `just docs-build` — thin, boring, good enough | Shelves, gates, static vs built, serve assembled artifacts |
| **0.53** | **A Palm pipeline** that *is* the build (orchestration, steps, durable instance) | Capability pressure on Palm itself — inefficient on purpose as a learning gym |

0.52 must **not** invest in a polished Python docs platform that 0.53 would throw away. Prefer dumb copies, JSON inventories, and a few HTML stubs over external doc frameworks.

The long arc after structure: **Docs as a service domain**, mountable as a surface. 0.52 may leave a **read-only stub**; it does not ship a fat Docs god-service.

---

## Thesis — three layers, not one folder

```
                    ┌─────────────────────────────────────┐
   SURFACES         │  Cloudflare Pages · SSR Explorer     │
   (deployment)     │  MCP palm://docs · CLI · offline zip │
                    └──────────────────▲──────────────────┘
                                       │ serve / mount
                    ┌──────────────────┴──────────────────┐
   BUILD            │  0.52: just docs-build (thin)        │
   (metabolism)     │  0.53: Palm pipeline (dogfood)       │
                    └──────────────────▲──────────────────┘
                                       │ read
                    ┌──────────────────┴──────────────────┐
   SOURCE           │  Hand wiki · constitution · ADRs     │
   (genome)         │  Code: packages, CQRS, MCP inventory │
                    └─────────────────────────────────────┘
```

1. **SOURCE (genome)** — what is true. Hand-authored narrative + machine-readable inventories from code.  
2. **BUILD (metabolism)** — deterministic SOURCE → **artifact tree**.  
3. **SURFACES (phenotypes)** — how artifacts are served.

Confusing these three is how docs rot. 0.52 names them and keeps them separate on disk.

---

## On-disk structure (the shelf plan)

### Root — constitution only

| File | Role |
|------|------|
| `README.md` | Front door |
| `AGENTS.md` | Constitution for builders |
| `PHILOSOPHY.md` | Spirit |
| `STATUS.md` | Living status ledger |
| `TECH-DEBT.md` | Debt ledger |
| `ARCHITECTURE.md` | Map |
| `DEVELOPMENT.md` | How to tend |
| `SCOPE.md` | Boundaries |
| `CHANGELOG.md` | Temporal spine |

Point-in-time and deep guides move under `docs/`.

### `docs/` — library house

```text
docs/
  wiki/                 # narrative (human-first)
    index.md
    guides/
    concepts/           # stubs OK
  adr/
  vision/               # optional later migrate of VISION-0.X.md
  migrations/           # from root MIGRATION-*.md
  releases/             # from root RELEASE-*.md
  llms.txt / mcp.txt / mcp-card.txt / MCP.md / skills/
  site/                 # landing soul (index.html, styles/, images/)
  _build/               # BUILD output only (prefer gitignore + CI/assemble)
  VERSIONING.md
  VISION-0.52.md
  audit/                # not public canopy by default
  superpowers/          # internal plans — not public canopy
```

| Kind | Examples | Rule |
|------|----------|------|
| **Static (source)** | `wiki/**`, `adr/**`, `site/index.html`, constitution at root | Humans edit; generators never overwrite |
| **Built (artifact)** | `_build/**`, inventory JSON, assembled deploy tree | Only the builder writes |
| **Mirrors** | `mcp/data/*`, `.grok/skills/*` | Derived; `docs-check` enforces (PD-031) |

---

## Builder philosophy (0.52) — simple is enough

**In scope for `just docs-build`:**

- Create/clean `docs/_build/`
- Copy static wiki (and optionally site assets) into the artifact tree
- Emit **one or two** registry-truthful inventories (e.g. MCP tool list, service domain names) via a **small script** under `scripts/` — stdlib + existing Palm imports if cheap
- Optionally assemble a flat deploy directory Cloudflare already understands

**Out of scope for 0.52 builder:**

- mkdocs, Sphinx, pdoc, Material, Node doc toolchains as *required* deps  
- Perfect API HTML for every module  
- A Palm flow that shells out to `just` (that is not dogfood — that is a wrapper)  
- Replacing the handcrafted landing page with a theme engine  

If a step needs a heavy tool, **stub the shelf** and leave the real work for 0.53’s pipeline pressure or a later polish patch.

---

## Long arc (destination phenotypes)

### Docs as a service (late 0.52 stub OK; full life later)

```text
CompositionProfile
  services:  { …, "docs" }       # list/get library paths; no fat CMS
  surfaces:  { …, "docs_ssr" }   # mount /docs when ready
```

| Piece | When |
|-------|------|
| Thin `DocsService` (list/get artifacts) | 0.52 late, optional stub |
| SSR / MCP `palm://docs` | 0.52 if cheap; else 0.53+ |
| Cloudflare assembled publish | 0.52 (evolve current wrangler assets) |
| **Palm pipeline that builds the library** | **0.53** |

### What 0.52 must not do

- HTML templates inside `ApplicationHost`  
- DocsService as a second host  
- Heavy doc frameworks “because professional”  
- History rewrite in the same patch as file moves  
- Fake dogfood (`just` inside a Palm step) presented as 0.53 work

### Honest stubs

- Empty `docs/wiki/concepts/` with a one-line “shelf reserved”  
- Inventory JSON with a short HTML index  
- Read-only docs facade without rebuild API  

---

## Slice sequence

| Patch | Slice | Closes / intent |
|-------|--------|-----------------|
| **0.52.0** | **Plan** — this VISION + ADR-021 | Theme open |
| **0.52.1** | **Gates green** — `docs-check` + skill/mcp mirrors on bump (PD-031) | Safety net |
| **0.52.2** | **Root declutter** — RELEASE → `docs/releases/`, MIGRATION → `docs/migrations/` (PD-021) | Clean floor |
| **0.52.3** | **Shelf tree** — `docs/wiki/` (+ stubs), static vs `_build` contract; optional `docs/site/` without behavior change | Structure |
| **0.52.4** | **Stamp completeness** — SYNC ARCHITECTURE / DEVELOPMENT / SCOPE (PD-019) | Docs-as-code |
| **0.52.5** | **ADR hygiene** — index, 013 note, AGENTS rule (PD-020) | Discipline |
| **0.52.6** | **Builder v0** — `just docs-build`: copy wiki + one inventory into `_build/` (stdlib/scripts only) | Thin metabolism |
| **0.52.7** | **Assemble & edge** — deploy bundle for Cloudflare from assembled tree | Surface: CDN |
| **0.52.8** | **In-process stub** *(optional)* — composition-gated list/get of artifacts | Docs-as-service bud |
| **0.52.9** | **Agent map** *(optional)* — deeper llms / `palm://docs` over same SOURCE | Progressive disclosure |
| **0.52.10** | **History policy** *(optional)* — DEVELOPMENT note on AI trailers; rewrite runbook only if maintainer opts in | Hygiene |

**Explicitly not in 0.52:** Palm-native docs pipeline → **[VISION-0.53]** when opened.

---

## Decisions (locked in ADR-021)

1. Theme name: **The Living Library**.  
2. SOURCE / BUILD / SURFACE law; generators never write the hand genome.  
3. `_build/` prefer **gitignore + build on demand/CI**; commit only if deploy forces it.  
4. **0.52 builder stays thin** — no required external doc frameworks.  
5. **0.53** owns Palm-pipeline dogfood (build *with* Palm, not wrap `just`).  
6. Landing page soul stays handcrafted.  
7. AI Co-Authored-By not required; history rewrite opt-in only.

---

## Out of scope (this minor)

- 0.53 Palm pipeline builder  
- Full CMS / multi-author wiki auth  
- 100% API reference coverage  
- Mandatory history rewrite  
- Observability / T5 work  

---

## Exit criteria

- Root is constitution-scale (sprawl closed or residual files justified).  
- `just docs-check` green; mirrors update on version bump.  
- `just docs-build` produces a known `_build` tree (copy + ≥1 inventory) without new heavy deps.  
- Wiki shelves exist; Cloudflare (or documented path) can publish an **assembled** library.  
- Path to Docs service / SSR is written and unblocked — implementation may be stub.  
- T6 PD-019…021, PD-031 closed or explicitly deferred in TECH-DEBT.  
- STATUS + CHANGELOG name The Living Library; 0.53 called out as pipeline dogfood season.

---

## Spirit check

- **Names** layers before tools.  
- **Cleans** the forest floor so growth is visible.  
- **Builds** with something boring and honest in 0.52.  
- **Reserves** the real dogfood — Palm *as* the builder — for 0.53.  
- **Leaves stubs** that tell the truth.

---

*One genome of knowledge. A thin metabolism. Many surfaces. The library lives — and next season, Palm tends it itself.* 🌴📚
