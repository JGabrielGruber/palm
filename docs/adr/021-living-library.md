# ADR-021: The Living Library — knowledge as SOURCE / BUILD / SURFACE (0.52)

## Status

**Accepted** — July 2026 (0.52.0, theme: **The Living Library**).  
Planned in [VISION-0.52](../VISION-0.52.md). Implements TECH-DEBT **T6** direction (docs-as-code) with a longer product arc (docs as service; Palm-pipeline build in **0.53**).

## Context

Palm’s code architecture is layered, registry-driven, and multi-surface. Its **documentation** is not:

- Root markdown sprawl (RELEASE/MIGRATION vs CHANGELOG; PD-021).
- Version stamps and skill/MCP mirrors lag (PD-019, PD-031).
- ADR discipline incomplete (PD-020).
- The public site is a strong handcrafted landing page, not a library of truth with a clear build.
- Agent progressive surfaces (`llms.txt`, `mcp.txt`, skills) drift from the same facts.

A natural product destination is **docs as a Palm service** (queryable, SSR-served, MCP-exposed) and — further — **building the library with Palm itself** (pipeline dogfood). Doing that without first separating **what is true**, **what is built**, and **what is served** would create a second god-object and two truths.

## Decision

### 1. Theme

**0.52 = The Living Library** — structure knowledge so one genome feeds many surfaces.

### 2. Three-layer law

| Layer | Meaning | Examples |
|-------|---------|----------|
| **SOURCE** | Hand genome + code-as-inventory input | `docs/wiki/`, `docs/adr/`, constitution at root, package registries |
| **BUILD** | Deterministic transform → artifacts | `just docs-build` → `docs/_build/` |
| **SURFACE** | How artifacts are delivered | Cloudflare assets, future SSR `/docs`, MCP `palm://docs`, CLI |

**Invariant:** generators and builders **never write into hand SOURCE paths**. Mirrors (MCP data, `.grok` skills) are derived and gated by `docs-check`.

### 3. On-disk constitution

- **Root** keeps only living constitution: README, AGENTS, PHILOSOPHY, STATUS, TECH-DEBT, ARCHITECTURE, DEVELOPMENT, SCOPE, CHANGELOG.
- **Point-in-time** RELEASE/MIGRATION notes live under `docs/releases/` and `docs/migrations/`.
- **Wiki** narrative under `docs/wiki/`; landing soul under `docs/site/` (or current `docs/index.html` until relocated without behavior change).
- **Artifacts** under `docs/_build/` (prefer gitignored; build in CI or before deploy).

### 4. Builder simplicity (0.52)

- **Required:** `just docs-build` that copies static wiki (and assemble steps) and emits at least one **stdlib / in-repo script** inventory (e.g. MCP tools, service domains).
- **Forbidden as required deps in 0.52:** mkdocs, Sphinx, Material, pdoc, or other heavy doc frameworks.
- Polish API HTML is optional and must not block T6 cleanup.

### 5. Palm-pipeline dogfood is 0.53

- **0.53** will explore building the library **using Palm** (pipeline / orchestration as the build graph) to pressure engine capabilities.
- **Not** a Palm step that shells out to `just docs-build` and calls it dogfood.
- 0.52 therefore **must not over-invest** in a Python-only docs platform that 0.53 would replace; keep the 0.52 builder thin and replaceable.

### 6. Docs as a service (timing)

- Late 0.52 may add a **composition-gated, read-only** facade (list/get artifacts) and/or a thin SSR route — stubs OK.
- Rebuild-as-command, CMS, and multi-author wiki are out of scope for 0.52.
- Surfaces mount the **same artifact tree**; they do not re-author content.

### 7. Landing page

The handcrafted product story (`index.html` / site) **stays**. Wiki and reference attach beside it; they do not replace the brand page with a generic theme.

### 8. History / AI trailers

- No required `Co-Authored-By` for paid AI tooling.
- Stripping historical trailers is an **opt-in** maintainer operation (filter-repo + force-push), not a silent default of 0.52.

## Consequences

- **Positive.** Docs become navigable and gateable (T6); static vs built is honest; Cloudflare and future SSR share one assembled truth; 0.53 has a clear contract (replace thin BUILD, keep SOURCE/SURFACE law).
- **Risk.** File moves break links — mitigate with `git mv`, link check in `docs-check`, and one declutter slice.
- **Risk.** A too-clever 0.52 builder wastes effort before Palm-pipeline dogfood — mitigated by decision 4–5.
- **Bounded.** No full Docs CMS; no mandatory history rewrite; no heavy framework lock-in.

## Alternatives considered

- **Adopt mkdocs-material immediately.** Rejected for 0.52 — good canopy, wrong cost before shelf cleanup and before 0.53 may redefine BUILD as a Palm pipeline.
- **Docs only as Cloudflare static forever.** Insufficient — agents and SSR need the same genome; service/surface path must stay open.
- **Palm flow wrapping `just` in 0.52.** Rejected — not real dogfood; confuses “orchestration product” with “shell recipe.”
- **Rewrite all history to drop Claude trailers as part of declutter.** Rejected as default — orthogonal, destructive; policy first.

## References

- [VISION-0.52](../VISION-0.52.md)  
- [TECH-DEBT.md](../../TECH-DEBT.md) T6 (PD-019…021, PD-031)  
- [VERSIONING.md](../VERSIONING.md)  
- [PHILOSOPHY.md](../../PHILOSOPHY.md)  
