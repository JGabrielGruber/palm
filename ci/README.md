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
| **`spawn --seed`** | Yes — seed tree copied into a throwaway workspace | **No** (reaped unless `--keep`) | Hermetic *verify*: `ci-sandbox`, `docs-build-sandbox`, CSS smoke |
| **workspace** (`load` / `run` / `commit`) | Yes — into vault workspace | **Yes** — commit back to vault | Authoring that must survive (future CSS write-back, longer edits) |

So: **seed is not for “edit Palm and get files back.”** For durable edits, use a NeonRoot **workspace** and commit to the vault (or keep authoring on the host). Recipes today prefer **spawn + narrow seed** for honesty and simplicity; workspace-based write-back can land later if we want `output.css` produced only inside NeonRoot.

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
| **`docs/` only** | `just docs-css-sandbox` | Enough for Tailwind; avoids host `data/`, `.venv`, secrets |
| **git-archive HEAD** | `just docs-build-sandbox`, `ci-sandbox` | Tracked files only — no gitignored `data/` |
| **Full `$PWD`** | **Avoid** for Palm checkouts | Host `data/palm/…` is often root-owned → `permission denied` mid-seed |

**NeonRoot seed-ignore** (e.g. exclude `data/`, `.venv`) would help full-tree seeds — a NeonRoot enhancement if you want it; Palm recipes stay narrow either way.

See ADR-022 and the neonroot provider `spawn` action (`seed: git-archive` | path).
