# Site — landing soul

**SOURCE (edit these):** still at the **`docs/` root** until a later move into this folder:

- `docs/index.html`, `docs/styles/`, `docs/images/`, `docs/robots.txt`, `docs/sitemap.xml`

**BUILD (0.52.6+):** `just docs-build` copies those assets into **`docs/_build/deploy/`** together with wiki + generated reference. That deploy tree is the **edge canopy** — not a limit of Cloudflare; Workers/Pages can point `assets.directory` at `_build/deploy` and run the builder on each push (see `docs/wrangler.jsonc`).

**Hermetic:** `just docs-build-sandbox` runs the same builder in NeonRoot (git-seeded), same spirit as `just ci-sandbox`.

Do **not** hand-edit anything under `docs/_build/`.
