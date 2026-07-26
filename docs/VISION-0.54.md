# VISION 0.54 — The Library Pipeline (Palm builds the canopy)

**Status:** 🟢 **Open (0.54.0)** — plan + [ADR-023](adr/023-library-pipeline.md).  
**Theme:** Build the Living Library with a **Palm definition** (pipeline-first) whose steps are **resources** — especially `neonroot` — not a shell that calls `just`.  
**Depends on:** [VISION-0.52](VISION-0.52.md) (SOURCE / BUILD / SURFACE) · [VISION-0.53](VISION-0.53.md) (neonroot provider + palm-ci / palm-docs · **landed**).  
**Not:** `subprocess(["just", "docs-build"])` dressed as dogfood.

> *0.52 named the library. 0.53 gave it honest hands. 0.54 teaches the hands a sequence.*  
> *The same hands can later hold Postgres and Mongo — Palm orchestrates; runners isolate.*

---

## True intent

Palm already has:

| Layer | Reality |
|-------|---------|
| **Genome** | `docs/wiki`, constitution, ADRs ([LIBRARY](LIBRARY.md)) |
| **Thin metabolism** | `scripts/docs_build.py` / `just docs-build` |
| **Hermetic hands** | `provider: neonroot` · `spawn` · `--output` · palm-docs image |

What is missing is a **named, durable, operator-facing sequence** that *is* Palm:

```text
operator / Assist / CLI
        ↓
  flow: rebuild-living-library   (or similar)
        ↓
  resource: neonroot-health          (optional preflight)
  resource: neonroot-spawn-docs-css  (optional; --output CSS)
  resource: neonroot-spawn-docs-build (+ --output _build)
  resource / gate: inventory present
        ↓
  SUCCEEDED — canopy artifacts on host (via NeonRoot export)
```

Dogfood pressure: multi-step resources, state between steps, failure surfaces, Assist loop, resume story for long spawns.

---

## Pipeline shape (locked by ADR-023)

| Decision | Choice |
|----------|--------|
| **Pattern** | **Pipeline** (linear resource + transform/gate steps) — default for rebuild |
| **Wizard** | Optional later for interactive “which steps?” — not required for 0.54.1 |
| **Work unit** | Keep `scripts/docs_build.py` and Tailwind CLI **inside** palm-docs (0.52/0.53) |
| **Host artifacts** | NeonRoot `--output` maps (already in recipes); resource params carry the same |
| **just recipes** | Remain for humans; Palm path is **peer metabolism**, not replacement |

### Resource graph (v0)

| Step | Resource / action | Image | Notes |
|------|-------------------|-------|--------|
| 0 | `neonroot-health` | — | Soft preflight; fail fast if CLI missing |
| 1 | spawn CSS *(optional)* | palm-docs | seed `docs/`, output `styles/output.css` |
| 2 | spawn docs_build | palm-docs | seed git-archive or narrow tree; output `docs/_build` |
| 3 | gate | file or inventory JSON | Assert `_build/deploy/index.html` exists on host |

Exact definition IDs land in 0.54.1 under `examples/definitions/` (or a small pack).

---

## Slice sequence

| Patch | Scope | MIGRATION? |
|-------|--------|------------|
| **0.54.0** | Plan (this doc) + ADR-023 | — |
| **0.54.1** | Flow definition + neonroot resource steps (publishable example) | no |
| **0.54.2** | Characterization / e2e — mock spawn or neonroot-if-present | no |
| **0.54.3** | Assist discover / operator entry for “rebuild library” | no |
| **0.54.4** | Failure semantics — spawn non-zero, missing image, missing CLI | no |
| **0.54.5** | Docs: LIBRARY + DEVELOPMENT — two metabolisms; STATUS close | no |

Optional sub-slices: compensation for failed mid-pipeline (usually N/A for pure build); Explorer deep-link.

---

## Horizon — beyond the library (not this minor)

Sovereign Runners unlock **orchestrating work that is not Palm itself**. Documented so debt and future minors have a north star:

### Postgres / Mongo (and GraphQL) providers — future vision

Today ([TECH-DEBT](../TECH-DEBT.md) **T7 / PD-022 / PD-023 / PD-030**):

- `providers/postgres`, `storages/postgres`, `storages/mongodb` are **stubs or untested**
- Extras `postgres=[]` / `mongodb=[]` leave drivers unpinned
- Shipping “installed but empty” is dishonest (PD-023)

**Target pattern** (post-0.54 theme candidate, e.g. **0.55 Adapter Runners** or T7 minor):

```text
Palm flow / CI definition
  → neonroot.spawn(image=palm-postgres-test, seed=git-archive, command=pytest tests/adapters/…)
  → or compose: start DB in image, run provider round-trips, export junit/coverage via --output
```

| Principle | Application |
|-----------|-------------|
| **Core purity** | Drivers stay out of `palm.core`; providers remain edges |
| **Hermetic truth** | Real Postgres/Mongo in **tool images**, not “hope host has docker-compose” |
| **Composition** | `composition.has("neonroot")` + optional `enable_*` for adapter images |
| **Honest install** | Pin extras when real; gate experimental until green (PD-023) |
| **Same grammar as docs** | Resource steps + spawn + output — Library Pipeline is the **template** |

0.54 does **not** implement adapter images. It **proves the orchestration grammar** on docs so T7 can copy the pattern without inventing a second engine.

Related futures (even later): GraphQL provider tests, audit image (`palm-audit`), multi-service demos.

---

## Explicit non-goals (0.54)

- Full DocsService CMS / multi-author wiki  
- Replacing Cloudflare hosting with Palm  
- Implementing postgres/mongo round-trips (horizon only)  
- Deleting `just docs-build`  
- Perfect efficiency  

---

## Exit criteria

- A Palm **flow definition** rebuilds (or verifies rebuild of) the Living Library canopy via **neonroot resources**
- Host gets artifacts through **NeonRoot `--output`**, not bind-mount folklore  
- Assist/CLI can start the flow without inventing a one-off tool  
- Docs state **just vs Palm** metabolisms clearly  
- Horizon note for DB adapters via runners is in STATUS / TECH-DEBT direction  
- Suite green; no fake dogfood  

---

## Spirit check

- **Register downward** — new flow is a definition, not host surgery  
- **Truth-seeking** — spawn failures surface as instance/job truth  
- **Dogfood** — Palm uses Palm + NeonRoot the way users will for any external system  
- **Unlock** — grammar for “orchestrate beyond Palm” without waiting for perfect adapters  

---

*One genome of knowledge. Hermetic hands. A pipeline that is Palm.* 🌴📚  
*Next horizons: databases that finally run where they belong — in runners, under Palm’s story.*
