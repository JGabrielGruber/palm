# NeonRoot tool images (Sovereign Runners)

Palm’s hermetic runners live as NeonRoot images. The **product** talks to them via
`palm.providers.neonroot` ([VISION-0.53](../docs/VISION-0.53.md)); **just** recipes
build and spawn them for day-to-day ops.

| Image | Containerfile | Purpose | Recipe |
|-------|---------------|---------|--------|
| **palm-ci** | [Containerfile](Containerfile) | ruff, pytest, guards (`just ci`) | `just ci-image` · `just ci-sandbox` |
| **palm-docs** | [Containerfile.docs](Containerfile.docs) | `docs_build` + Tailwind CLI (no host Node required) | `just docs-image` · `just docs-css-sandbox` · `just docs-build-sandbox` |

## Workspace profiles

| Profile | Host needs | Images |
|---------|------------|--------|
| Edit engine | `uv` + runtime deps | — |
| Checks | optional | palm-ci |
| Docs canopy | optional (committed `output.css` or sandbox) | palm-docs |
| Full weight | Node + all groups | optional |

Full-weight local `docs/node_modules` remains supported (`just docs-css`).

## Seed policy (be careful)

NeonRoot `--seed <dir>` **walks and copies** that directory. It is **not** “load Palm into the sandbox.”

| Seed | Used by | Notes |
|------|---------|--------|
| **`docs/` only** | `just docs-css-sandbox` | Enough for Tailwind; avoids host `data/`, `.venv`, secrets |
| **git-archive HEAD** | `just docs-build-sandbox`, `ci-sandbox` | Tracked files only — no gitignored `data/` |
| **Full `$PWD`** | **Avoid** for Palm checkouts | Host `data/palm/…` is often root-owned → `permission denied` mid-seed |

**Do we need a NeonRoot seed-ignore?** Useful for full-tree seeds (`.neonrootignore` / exclude `data/`, `.venv`, `.git`). That’s a **NeonRoot** feature if you want it later — Palm recipes should not rely on seeding the whole monorepo in the meantime.

**Write-back:** if seed is copy-in (not a bind mount), container writes may not update the host; treat sandbox CSS/build as hermetic verify unless your NeonRoot version binds the seed path. Host authoring fallback: `just docs-css` with optional `docs/node_modules`.

See ADR-022 and the neonroot provider `spawn` action (`seed: git-archive` | path).
