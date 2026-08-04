# Living Library — on-disk contract (0.52)

Palm’s knowledge house under `docs/`. Layers are law ([ADR-021](adr/021-living-library.md), [VISION-0.52](VISION-0.52.md)).

## SOURCE (humans edit; generators never overwrite)

| Path | Role |
|------|------|
| Repo root constitution | `README`, `AGENTS`, `PHILOSOPHY`, `STATUS`, `TECH-DEBT`, `ARCHITECTURE`, `DEVELOPMENT`, `SCOPE`, `CHANGELOG` — header version stamps on ARCHITECTURE / DEVELOPMENT / SCOPE sync via `scripts/sync_version.py` (0.52.4) |
| **`docs/PALM.md`** | **Canonical high-level system map** (0.57+) — read first for layer purpose |
| **`docs/SYSTEM-LOW-LEVEL.md`** | Low-level system design (package, ports, moves) for 0.57 |
| **`TECH-DEBT.md` (root)** | Live debt (SD/SU/ST/CS/CF-*); archive era in `docs/audit/TECH-DEBT-ERA-0.45.md` |
| **`docs/STUBS.md`** | Intention catalog — purpose without fake implementations |
| `docs/wiki/` | Human narrative — guides & concepts |
| `docs/adr/` | Decisions — index [adr/README.md](adr/README.md); **ADR or explicit waive** (AGENTS §5) |
| `docs/migrations/`, `docs/releases/` | Point-in-time notes |
| `docs/VERSIONING.md` | Version scheme + **theme discipline** (floor · growth · exit; **José** decides) |
| `docs/VISION-*.md` | Theme plans (optional later move to `docs/vision/`) — **0.61** vitality **closed**: [VISION-0.61.md](VISION-0.61.md) · seed essay [VISION-VITALITY](VISION-VITALITY.md) · **0.60** supervisor: [VISION-0.60.md](VISION-0.60.md) · queue: [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) · **0.58** session: [VISION-0.58.md](VISION-0.58.md) · **0.57** system: [VISION-0.57.md](VISION-0.57.md) |
| `docs/llms.txt`, `docs/mcp.txt`, `docs/MCP.md`, `docs/skills/` | Agent progressive disclosure |
| Landing assets | `docs/index.html`, `docs/styles/`, `docs/images/` (today). Intended home: `docs/site/` after assemble (0.52.7) — see [site/README.md](site/README.md) |

## BUILD (only the builder writes)

| Path | Role |
|------|------|
| `docs/_build/` | Artifact tree — **gitignored**. Produced by `just docs-build` / `scripts/docs_build.py` (0.52.6+). |
| `docs/_build/deploy/` | **Assembled canopy** for static hosts (landing + wiki + reference + inventory). Point Cloudflare assets here after build. |

Do not hand-edit under `_build/`. Do not commit generated inventories (gitignore). Edge deploy is not coupled to “copy raw `docs/`” — adjust the host; the genome stays SOURCE.

## MIRRORS (derived; `docs-check` enforces)

| Source | Destinations |
|--------|----------------|
| `docs/llms.txt`, `docs/mcp.txt`, `docs/skills/palm/**` | `src/palm/runtimes/mcp/data/…`, `.grok/skills/palm/…` |

Sync: `just docs-sync-mirrors` or `just bump-version` ([PD-031](../TECH-DEBT.md) closed 0.52.1).

## SURFACES (consume artifacts / SOURCE, do not invent a second truth)

- **Cloudflare** — assembled canopy `docs/_build/deploy` after `just docs-build` (wrangler assets; adjust host build command as needed).
- **MCP / agents** — `palm://…` and skill mirrors over the same genome.
- **Hermetic rebuild (0.53+)** — NeonRoot + palm-docs / palm-ci ([VISION-0.53](VISION-0.53.md), [ci/README.md](../ci/README.md)).
- **Hermetic jobs / DAG (0.54)** — definition-driven work; tools only via neonroot ([VISION-0.54](VISION-0.54.md)).
- **Docs dogfood domain (0.55)** — optional Living Library business process + DocsService ([VISION-0.55](VISION-0.55.md)).
- **Horizon:** DB adapters in NeonRoot images (PD-022).

## Wiki map

Start at [wiki/index.md](wiki/index.md).
