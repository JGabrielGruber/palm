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

## Seed policy

- **git-archive** — hermetic verification (no write-back to host).
- **workspace path** (`$PWD`) — used by `docs-css-sandbox` so CSS can land on the host when NeonRoot seeds allow; prefer for authoring.

See ADR-022 and the neonroot provider `spawn` action.
