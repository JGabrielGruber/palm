# Palm website (palmengine.org)

**SOURCE** for the public landing page. Not the Living Library wiki — the **brand canopy**.

| Path | Role |
|------|------|
| `index.html` | Showcase landing |
| `styles/` | Tailwind input + built `output.css` |
| `images/` | Logo, OG, screenshots, placeholders |
| `robots.txt` · `sitemap.xml` | Crawlers |

## Build into deploy canopy

From repo root:

```bash
just docs-build
# → docs/_build/deploy/  (website + wiki + reference)
```

Cloudflare (wrangler under `docs/`) expects:

- **Build command:** from repo root, `uv run python scripts/docs_build.py` (or `just docs-build`)
- **Root directory:** `docs` (where `wrangler.jsonc` lives)
- **Assets directory:** `_build/deploy` (created by the build)

If the build step is skipped, deploy fails with “directory does not exist” — that is expected.

## Local preview

```bash
# After docs-build:
python -m http.server 8765 --directory docs/_build/deploy
# open http://127.0.0.1:8765/

# Or website only (no wiki):
python -m http.server 8765 --directory website
```

## CSS

Prefer hermetic: `just docs-css-sandbox` (updates `docs/styles` historically).  
For website-first: copy or rebuild Tailwind with `website/styles/input.css` → `output.css` (same pins as `docs/package.json` / palm-docs image).

## Placeholders (José)

See `images/placeholders/README.md` — screenshots to drop in when ready.
