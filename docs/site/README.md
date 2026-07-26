# Site — landing soul

**Today (0.52.3):** the public landing page and static assets still live at the **`docs/` root** so Cloudflare Pages (`wrangler.jsonc` → `"assets": { "directory": "." }`) keeps working without an assemble step:

- `docs/index.html`
- `docs/styles/`
- `docs/images/`
- `docs/robots.txt`, `docs/sitemap.xml`

**Intended home (after 0.52.7 assemble):** `docs/site/` as SOURCE for the brand page, with `just docs-build` copying them into `docs/_build/site/` (or a deploy root) alongside wiki + reference.

Do **not** hand-move `index.html` here until the builder owns the deploy tree — that would break the edge phenotype mid-theme.
