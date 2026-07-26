# Site — landing soul

**SOURCE (edit these):** still at the **`docs/` root** until a later move into this folder:

- `docs/index.html`, `docs/styles/`, `docs/images/`, `docs/robots.txt`, `docs/sitemap.xml`

**BUILD (0.52.6+):** `just docs-build` copies those assets into **`docs/_build/deploy/`** together with wiki + generated reference. That deploy tree is the **edge canopy** — not a limit of Cloudflare; Workers/Pages can point `assets.directory` at `_build/deploy` and run the builder on each push (see `docs/wrangler.jsonc`).

**Hermetic / thin desk (0.53.4):**

| Recipe | Image | Role |
|--------|-------|------|
| `just docs-image` | palm-docs | Build image (uv + Tailwind CLI; see `ci/Containerfile.docs`) |
| `just docs-css-sandbox` | palm-docs | Rebuild CSS; seeds **`docs/` only** (never full repo / `data/`) |
| `just docs-build-sandbox` | palm-docs | Hermetic verify of Living Library builder (**git-archive** seed) |
| `just docs-css` | host | Optional full-weight path (`docs/package.json` + npx) |

Do **not** hand-edit anything under `docs/_build/`.
