# Living Library — on-disk contract (0.52)

Palm’s knowledge house under `docs/`. Layers are law ([ADR-021](adr/021-living-library.md), [VISION-0.52](vision/closed/VISION-0.52.md)).

## SOURCE (humans edit; generators never overwrite)

| Path | Role |
|------|------|
| Repo root constitution | `README`, `AGENTS`, `PHILOSOPHY`, `STATUS`, `TECH-DEBT`, `ARCHITECTURE`, `DEVELOPMENT`, `SCOPE`, `CHANGELOG` — header version stamps on ARCHITECTURE / DEVELOPMENT / SCOPE sync via `scripts/sync_version.py` (0.52.4) |
| **`docs/PALM.md`** | **Canonical high-level system map** (0.57+) — read first for layer purpose |
| **`docs/SYSTEM-LOW-LEVEL.md`** | Low-level system design (package, ports, moves) for 0.57 |
| **`docs/STUBS.md`** | Intention catalog — purpose without fake implementations |
| `docs/wiki/` | Human narrative — guides & concepts |
| `docs/adr/` | Decisions — index [adr/README.md](adr/README.md); **ADR or explicit waive** (AGENTS §5) |
| `docs/migrations/`, `docs/releases/` | Point-in-time notes |
| `docs/VERSIONING.md` | Version scheme + **theme discipline** (floor · growth · exit; **José** decides) |
| **`docs/blueprint/`** | **Intended architecture** (C4 / SE vault) — [index](blueprint/README.md) · not theme PM |
| **`docs/vision/`** | Theme plans — [index](vision/README.md) · **current:** [ASSEMBLY](vision/VISION-ASSEMBLY.md) · [0.56 workload](vision/VISION-0.56.md) · [SURFACE-DEFLATION](vision/VISION-SURFACE-DEFLATION.md) · [GROVE](vision/VISION-GROVE.md) · **closed:** [vision/closed/](vision/closed/) |
| **`TECH-DEBT.md` (root)** | Live open residual + master index · paid detail [audit/TECH-DEBT-PAID.md](audit/TECH-DEBT-PAID.md) · PD era [audit/TECH-DEBT-ERA-0.45.md](audit/TECH-DEBT-ERA-0.45.md) |
| `docs/llms.txt`, `docs/mcp.txt`, `docs/MCP.md`, `docs/skills/` | Agent progressive disclosure |
| **Landing (website)** | [`website/`](../website/) SOURCE · **`website/dist/`** BUILD (`just website-build`) · CF assets = `website/dist` · [website/README.md](../website/README.md) |

## BUILD (only the builder writes)

| Path | Role |
|------|------|
| `docs/_build/` | Living Library only (wiki/reference/inventory) — **gitignored**. `just docs-build`. Not palmengine.org. |
| `website/dist/` | Public site BUILD — `just website-build`. Cloudflare **assets = `website/dist`**. |

Do not hand-edit under `_build/`. Do not commit generated inventories (gitignore). Edge deploy is not coupled to “copy raw `docs/`” — adjust the host; the genome stays SOURCE.

## MIRRORS (derived; `docs-check` enforces)

| Source | Destinations |
|--------|----------------|
| `docs/llms.txt`, `docs/mcp.txt`, `docs/skills/palm/**` | `src/palm/runtimes/mcp/data/…`, `.grok/skills/palm/…` |

Sync: `just docs-sync-mirrors` or `just bump-version` ([PD-031](../TECH-DEBT.md) closed 0.52.1).

## SURFACES (consume artifacts / SOURCE, do not invent a second truth)

- **Cloudflare (palmengine.org)** — assets directory **`website/dist`** after `just website-build` (see `website/wrangler.jsonc`).
- **MCP / agents** — `palm://…` and skill mirrors over the same genome.
- **Hermetic rebuild (0.53+)** — NeonRoot + palm-docs / palm-ci ([VISION-0.53](vision/closed/VISION-0.53.md), [ci/README.md](../ci/README.md)).
- **Hermetic jobs / DAG (0.54)** — definition-driven work; tools only via neonroot ([VISION-0.54](vision/closed/VISION-0.54.md)).
- **Docs dogfood domain (0.55)** — optional Living Library business process + DocsService ([VISION-0.55](vision/closed/VISION-0.55.md)).
- **Horizon:** DB adapters in NeonRoot images (PD-022).

## Wiki map

Start at [wiki/index.md](wiki/index.md).
