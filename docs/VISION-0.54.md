# VISION 0.54 — The Library Pipeline (docs as a Palm dataset)

**Status:** 🟢 **Open (0.54.0)** — plan refined: storage-backed library + DocsService + multi-corpus resources.  
**ADR:** [023-library-pipeline.md](adr/023-library-pipeline.md)  
**Depends on:** [VISION-0.52](VISION-0.52.md) (SOURCE / BUILD / SURFACE) · [VISION-0.53](VISION-0.53.md) (neonroot · **landed**) · [ADR-011](adr/011-local-document-resources.md) (tiered hot/cold KV)  
**Not:** `subprocess(["just", …])` dogfood · DocsService that only `open()`s local `_build` · one god image / god resource

> *0.52 named the library. 0.53 gave it hermetic hands. 0.54 publishes the canopy into Palm’s own storage and serves it as a living product.*

---

## True intent

The Living Library is **not a folder we serve**. It is a **revisioned product** Palm:

1. **Produces** hermetically (resources — often `neonroot`, sometimes pure `kv`/`file` copy),  
2. **Publishes** into **Palm storage** (hot/cold KV — same durability stack as the rest of the engine),  
3. **Queries** via **DocsService** (API / Assist / MCP / later SSR),  
4. **Optionally exports** a pin to disk or Cloudflare (`_build` / edge = phenotype, not source of truth).

Disk `docs/` remains **SOURCE** (humans edit markdown, hand landing page).  
Storage holds **published corpora** (the live docs).  
Rebuild cleanly = new revision + pin, not mutate a magically shared directory.

---

## Three planes

```text
                    ┌─────────────────────────────────────┐
   SERVE            │  DocsService · REST · MCP · Assist   │
   (query/present)  │  list / get / status / rebuild()     │
                    └──────────────────▲──────────────────┘
                                       │ read pin + blobs
                    ┌──────────────────┴──────────────────┐
   STORE            │  Palm storage — namespace library/*   │
   (durable truth)  │  tiered KV hot/cold · revisions      │
                    └──────────────────▲──────────────────┘
                                       │ publish (write)
                    ┌──────────────────┴──────────────────┐
   PRODUCE          │  Resources per corpus (not one god)  │
   (hermetic build) │  neonroot · kv · file · …            │
                    └─────────────────────────────────────┘
```

| Plane | Owns | Does not own |
|-------|------|----------------|
| **PRODUCE** | Generators in runners; resource defs | Serving HTTP |
| **STORE** | Blobs + manifests + current pin | Tailwind / Node |
| **SERVE** | Catalog, get page, trigger rebuild flow | Hand-editing SOURCE |

---

## Corpora (distinct resources, few images)

**Images** = tooling phenotypes (`palm-docs`, later slim inventory image).  
**Resources** = products you publish.

| Corpus id | Producer (sketch) | Stored product |
|-----------|-------------------|----------------|
| `wiki` | Normalize/copy SOURCE wiki (light; may skip container) | pages + index |
| `api` | Public packages / signatures inventory | tree JSON (+ optional HTML later) |
| `sdk` | Services, composition vocabulary, registries | structured JSON |
| `mcp` | MCP tool catalog (assist/full surfaces) | tool rows |
| `adr` | ADR index + bodies | pages + index |
| `site` | Landing + CSS (palm-docs + Tailwind) | static assets / hashed blobs |

Each corpus → **ResourceDefinition**(s) e.g. `docs-corpus-wiki-publish`, `docs-corpus-mcp-publish`.  
Pipeline/wizard: rebuild **one** or **all** — composition of resources.

No god resource that “builds the entire internet.”

---

## Storage layout (sketch — lock in 0.54.x)

Namespace **`library`** (tiered KV when durable host storage):

```text
library/meta/current                 → { revision, corpora: { wiki: r1, api: r1, … }, built_at }
library/revisions/{rev}/manifest     → full build record (generators, palm version)
library/{corpus}/{rev}/{path…}       → blob + content metadata
library/{corpus}/latest              → optional alias → rev (or only global current pin)
```

- **Append-friendly:** new rev, then flip `meta/current` (definition-revision spirit, 0.24).  
- **Hot:** indexes and current pin.  
- **Cold:** full bodies and older revs.  
- **Clean rebuild:** produce into new rev; pin only on success of the graph (or pin partial corpus revs if we allow per-corpus pins — prefer global pin v0 for simplicity).

---

## DocsService (domain API)

Composition: `services` includes **`"docs"`** (extend `ServiceName` when implemented).

| Method / concern | Behavior |
|------------------|----------|
| `list_corpora` / `list(corpus, rev?)` | Catalog from storage pin |
| `get(corpus, path, rev?)` | Blob + metadata |
| `status` | Current revision, per-corpus health, last build |
| `rebuild(corpus \| all)` | Submit pipeline / resource graph — **does not** shell `just` |
| Present | Assist views, MCP `palm://docs/…` progressive cards |

**Out of scope for DocsService:** multi-author CMS, editing SOURCE markdown, owning NeonRoot CLI details (resource engine does).

`GET /v1/docs` OpenAPI hub today is **unrelated** — keep name collision in mind (`/v1/library` or `/v1/api/docs/library` when REST lands).

---

## Pipeline shape (ADR-023)

| Decision | Choice |
|----------|--------|
| Pattern | **Pipeline** v0 (linear publish graph) |
| Steps | Resources: health → per-corpus publish → pin current |
| Work units | Generators inside images / stdlib scripts; Palm orchestrates |
| Host `_build` / Cloudflare | **Optional export phenotype** after pin (`--output` or export resource) |
| `just docs-*` | Peer metabolism for humans; not the product truth |

### Graph (v0)

```text
neonroot-health?
  → publish wiki      → storage
  → publish mcp/api   → storage   (can parallel later)
  → publish site/css  → storage
  → pin meta/current
  → (optional) export pin → docs/_build/deploy for edge
```

---

## Slice sequence

| Patch | Scope |
|-------|--------|
| **0.54.0** | Plan (this doc) + ADR-023 refined ✅ |
| **0.54.1** ✅ | Storage schema + publish helpers (`palm.common.library`, pin) |
| **0.54.2** ✅ | Wiki corpus publish SOURCE → storage (`publish_wiki_corpus`, `just library-publish-wiki`) |
| **0.54.3** ✅ | **DocsService** stub: list/get/status/rebuild(`wiki`) over pin |
| **0.54.4** ✅ | Library provider + `rebuild-living-library` resource graph (wizard steps) |
| **0.54.5** | Characterization tests (mock neonroot / memory KV) |
| **0.54.6** | Assist / MCP progressive `palm://docs/…` or discover |
| **0.54.7** | Optional edge export phenotype; LIBRARY/DEVELOPMENT dual metabolism docs |
| **0.54.8** | Second corpus (mcp or api) — proves multi-resource model |

---

## Horizon (not this minor)

### Postgres / Mongo / GraphQL (T7 / PD-022)

Same grammar: **produce under isolation, result is Palm-truth or green tests** — not “hope the laptop has Docker.”

```text
Palm flow
  → neonroot.spawn(palm-postgres-test, pytest adapter suite)
  → pin extras when honest; gate placeholders (PD-023)
```

Library Pipeline is the **template** for adapter runners.

### Later library growth

Search, full API HTML, SSR surface `docs_ssr`, multi-rev browse UI, analytics *about* the library (page counts) as a true analytics dataset.

---

## Explicit non-goals (0.54)

- Full CMS / multi-author wiki in storage as SOURCE  
- Replacing git SOURCE with only KV  
- Implementing real DB adapters  
- One container that builds every corpus forever  
- Deleting `just docs-build`  

---

## Exit criteria

- At least one corpus is **published into Palm storage** and readable via **DocsService**  
- Rebuild path is a **Palm definition / resource graph**, not `just` inside a step  
- Pin/revision story is explicit and testable  
- Multi-corpus *shape* is proven (second corpus or clear extension point)  
- Edge/`_build` is documented as export, not live truth  
- Horizon for DB adapters recorded in TECH-DEBT / PROVIDER-APPS  
- Suite green  

---

## Spirit check

- **Register downward** — corpora and DocsService at the edges  
- **Storage is memory** — hot/cold, not ad-hoc files for live serve  
- **Hermetic produce** — runners build; Palm stores and serves  
- **Dataset, not folder** — revisioned product with clean rebuild  
- **Unlock** — same hands hold docs today and databases tomorrow  

---

*The canopy is published, not merely rendered. Palm remembers what it published.* 🌴📚
