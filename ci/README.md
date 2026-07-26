# NeonRoot tool images (Sovereign Runners)

Palm’s hermetic runners live as NeonRoot images. The **product** talks to them via
`palm.providers.neonroot` ([VISION-0.53](../docs/VISION-0.53.md)); **just** recipes
build and spawn them for day-to-day ops.

| Image | Containerfile | Purpose | Recipe |
|-------|---------------|---------|--------|
| **palm-ci** | [Containerfile](Containerfile) | ruff, pytest, guards (`just ci`) | `just ci-image` · `just ci-sandbox` |
| **palm-docs** | [Containerfile.docs](Containerfile.docs) | `docs_build` + Tailwind CLI (no host Node required) | `just docs-image` · `just docs-css-sandbox` · `just docs-build-sandbox` |

## Project vault: `.neonroot/` (gitignored — on purpose)

Palm uses a **local NeonRoot vault** at the repo root:

```text
.neonroot/           # gitignored — local cold store (like data/)
  index.toml         # vault registry metadata
  images/            # built palm-ci / palm-docs layers
  workspaces/        # durable NeonRoot workspaces (commit-back target)
```

| In git (SOURCE) | On disk only (vault) |
|-----------------|----------------------|
| `ci/Containerfile*` | Built images |
| `ci/README.md` (this file) | Workspace clones / pending commit state |
| `just ci-image` / `docs-image` recipes | Large binary layers |

**Decision: keep ignoring `.neonroot/`.**  
Same class of artifact as `data/` and `.venv` — machine-local, rebuildable, not the genome.  
**Maintain with the project** the *recipe* (Containerfiles + just + provider), not the *vault contents*.

Rebuild after clone:

```bash
just ci-image      # palm-ci → .neonroot/images/…
just docs-image    # palm-docs
```

### NeonRoot primitives (how Palm should use them)

| Primitive | Copy? | Persist changes? | Palm use |
|-----------|-------|------------------|----------|
| **`spawn --seed` + `--seed-mode copy`** (default) | Into vault bare → tmpfs | Hermetic; use `--output` for host artifacts | CI, dogfood purity |
| **`spawn --seed-mode bind`** (NeonRoot 0.2) | Host dir live-mounted | Writes hit host; not hermetic; no exclude/commit | Trusted local whole-tree (e.g. `docs-css-bind`) |
| **`spawn --output host:container`** | — | Explicit files/dirs **after success** | Safe write-back with copy mode |
| **`spawn --seed-exclude` / `.neonrootignore`** | Skips paths (copy mode) | — | Full-tree seed hygiene |
| **workspace** (`load` / `run` / `commit`) | tmpfs; optional vault commit | Durable tool tree | Inspect / long tool work — not product pin |

**Seed is not whole-tree write-back.** For host artifacts use **`--output`**. For vault durability use **workspaces**. Repo root may use [`.neonrootignore`](../.neonrootignore) when seeding `$PWD`.

## Workspace profiles (developer desk)

| Profile | Host needs | Images |
|---------|------------|--------|
| Edit engine | `uv` + runtime deps | — |
| Checks | optional | palm-ci |
| Docs canopy | optional (committed `output.css` or sandbox) | palm-docs |
| Full weight | Node + all groups | optional |

Full-weight local `docs/node_modules` remains supported (`just docs-css`).

## Seed policy (be careful)

NeonRoot `--seed <dir>` **walks and copies** that directory. It is **not** “mount the live Palm checkout” and **not** “boot Palm inside the sandbox.”

| Seed | Used by | Notes |
|------|---------|--------|
| **`docs/` only** | `just docs-css-sandbox` | + `--output …/output.css:styles/output.css` |
| **git-archive HEAD** | `just docs-build-sandbox`, `ci-sandbox` | + optional `--output docs/_build:docs/_build` |
| **Full `$PWD`** | Only with `.neonrootignore` / `--seed-exclude` | Skips `data/`, `.venv`, … |

See ADR-022; provider `spawn` params: `seed`, `seed_exclude`, `outputs`.
