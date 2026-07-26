# Living Library — on-disk contract (0.52)

Palm’s knowledge house under `docs/`. Layers are law ([ADR-021](adr/021-living-library.md), [VISION-0.52](VISION-0.52.md)).

## SOURCE (humans edit; generators never overwrite)

| Path | Role |
|------|------|
| Repo root constitution | `README`, `AGENTS`, `PHILOSOPHY`, `STATUS`, `TECH-DEBT`, `ARCHITECTURE`, `DEVELOPMENT`, `SCOPE`, `CHANGELOG` — header version stamps on ARCHITECTURE / DEVELOPMENT / SCOPE sync via `scripts/sync_version.py` (0.52.4) |
| `docs/wiki/` | Human narrative — guides & concepts |
| `docs/adr/` | Decisions — index [adr/README.md](adr/README.md); **ADR or explicit waive** (AGENTS §5) |
| `docs/migrations/`, `docs/releases/` | Point-in-time notes |
| `docs/VISION-*.md` | Theme plans (optional later move to `docs/vision/`) |
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

- **Cloudflare** — today deploys `docs/` assets (wrangler); later the assembled bundle from `_build/`.
- **SSR / DocsService** — late 0.52 stub or later; list/get over the same tree.
- **MCP / agents** — `palm://…` and skill mirrors over the same genome.

## Wiki map

Start at [wiki/index.md](wiki/index.md).
