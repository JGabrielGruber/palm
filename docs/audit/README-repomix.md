# Repomix packs for Palm analysis

## Prefer the structure + surfaces slice

Full-repo packs grow multi‑MB and drown structure signal.

**Working generate command** (`uvx repomix` 0.5.x; use empty `-c` if root `repomix.config.json` is schema-stale):

```bash
uvx repomix \
  -c repomix.system.config.json \
  -o docs/audit/repomix-system-slice.xml \
  --style xml --compress --remove-comments --remove-empty-lines \
  --no-security-check \
  --header-text "Palm structure+surfaces slice 0.57" \
  --include "docs/PALM.md,docs/SYSTEM-LOW-LEVEL.md,docs/STUBS.md,TECH-DEBT.md,AGENTS.md,src/palm/core/**/*.py,src/palm/common/runtimes/**/*.py,src/palm/common/wait/**/*.py,src/palm/common/work/**/*.py,src/palm/common/workload/**/*.py,src/palm/common/executions/**/*.py,src/palm/common/patterns/**/*.py,src/palm/app/kernel.py,src/palm/services/execution/**/*.py,src/palm/patterns/_apps.py,src/palm/patterns/etl/**/*.py,src/palm/providers/_apps.py,src/palm/providers/graphql/**/*.py,src/palm/providers/postgres/**/*.py,src/palm/storages/_apps.py,src/palm/storages/postgres/**/*.py,src/palm/storages/mongodb/**/*.py,src/palm/runtimes/mcp/in_process.py,src/palm/runtimes/mcp/tools.py,src/palm/runtimes/cli/commands/registry.py,src/palm/runtimes/server/surfaces/ssr/explorer/fetch.py,src/palm/runtimes/server/surfaces/ssr/explorer/actions.py,tests/test_modular_apps.py"
```

| Result (example) | Value |
|------------------|------:|
| Files | ~150 |
| Size | ~250 KB compressed |

**What it carries:** map, debt, stubs, core, system-shaped common, execution product, lying plugins, **surface bypass samples** (Explorer engine access, MCP in_process, CLI registry).

**What it drops on purpose:** full Explorer HTML/forms, OpenAPI prose, most of server SSR, most tests.

`repomix.system.config.json` is intentionally `{}` so CLI flags own the slice (root `repomix.config.json` may be invalid for repomix 0.5 schema).
