# Palm Engine — Project Status

**Current Version:** `0.51.6` · **Theme open:** **`0.54.0` Hermetic Jobs (replan)**  
**Last Updated:** July 26, 2026  
**Library (0.52 tooling):** [docs/LIBRARY.md](docs/LIBRARY.md) · [docs/wiki/](docs/wiki/index.md)  
**Maturity:** Wizard · MCP · Assist · composition profiles · **0.52 Living Library tooling** · **0.53 Sovereign Runners (landed)** · **0.54 Hermetic Jobs (replanned)** · **0.55 docs dogfood domain (queued)**.

## Quick Overview

Palm is a lightweight, Python-first orchestration engine built on a clean **Behavior Tree** foundation. It excels at complex multi-step workflows, rich interactive wizards, compositional sub-flow orchestration, and transactional processes with durable state and human-in-the-loop participation.

**Distribution name:** `palmengine` (PyPI)  
**Import name:** `palm`  
**Recommended entrypoint:** `ApplicationHost` via `create_cli_host()` for CLI, or `ApplicationHost(profile=DeploymentProfile.all_in_one())` for library use

## Architecture Snapshot

Palm follows a **layered, registry-driven** model with a strictly pure core:

- `palm/core/` — Pure foundational engines. **Zero external Palm imports.**
- `palm/services/` — User-facing domain API (definitions, execution, system, assist, design, analytics).
- `palm/common/` — Shared coordination (not product domains).
- `palm/app/` — ApplicationHost + composition/deployment profiles.
- `palm/patterns/`, `palm/providers/`, `palm/storages/` — Registry extension.
- `palm/runtimes/` — Thin surfaces.

See [ARCHITECTURE.md](ARCHITECTURE.md) and [AGENTS.md](AGENTS.md).

## 0.52 — The Living Library (tooling)

**Vision:** [docs/VISION-0.52.md](docs/VISION-0.52.md) · **ADR:** [docs/adr/021-living-library.md](docs/adr/021-living-library.md)  
SOURCE/BUILD/SURFACE, root declutter, wiki shelves, thin `just docs-build`, Cloudflare assemble. T6 PD-019–021, PD-031 closed.

| Notes |
|-------|
| Static docs tooling remains. **DocsService / storage corpora product → 0.55.** |

## 0.53 — Sovereign Runners (landed)

**Vision:** [docs/VISION-0.53.md](docs/VISION-0.53.md) · **ADR:** [docs/adr/022-neonroot-provider.md](docs/adr/022-neonroot-provider.md)  

NeonRoot provider (`health`/`spawn`, exclude/output), palm-ci / palm-docs images, doctor, Assist discover, composition capability `neonroot`. Workspaces are **tmpfs-disposable** by default.

| Patch | Status |
|-------|--------|
| 0.53.0–0.53.8 | ✅ closed |

## 0.54 — Hermetic Jobs (open · **replanned**)

**Vision:** [docs/VISION-0.54.md](docs/VISION-0.54.md) · **ADR:** [docs/adr/023-hermetic-jobs.md](docs/adr/023-hermetic-jobs.md)  

**Theme:** Purpose test — definition-driven multi-step work; foreign code only via **neonroot**; grow real **dag** pattern.  

**Discarded from interim 0.54:** `common.library`, `providers/library`, `services/docs`, wiki-pin product path.

| Patch | Status |
|-------|--------|
| 0.54.0 Replan + discard product stack | ✅ |
| 0.54.1 Hermetic job contract + [HERMETIC-JOBS.md](docs/HERMETIC-JOBS.md) | ✅ |
| 0.54.2 Dogfood flow `hermetic-job-smoke` (neonroot only) | ✅ |
| 0.54.3 DAG pattern v0 (resource nodes + deps) | ✅ |
| 0.54.4+ multi-node / second example / run-dir | pending |

## 0.55 — Docs dogfood domain (queued)

**Vision:** [docs/VISION-0.55.md](docs/VISION-0.55.md)  

Optional Living Library **business process** + thin DocsService — analytics-shaped, not core.

## Horizon

- Adapter runners (postgres/mongo) via neonroot (PD-022)  
- Payload/artifact registry for registered modules  
- NeonRoot bind-mode + Palm run-dir contract  

See [TECH-DEBT.md](TECH-DEBT.md), [docs/VERSIONING.md](docs/VERSIONING.md).
