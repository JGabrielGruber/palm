# Palm website (palmengine.org)

**SOURCE** for the public landing. Not the Living Library wiki.

| Path | Role |
|------|------|
| `index.html` | Showcase landing (edit here) |
| `styles/` | Tailwind `input.css` + built `output.css` |
| `images/` | Logo, OG, screenshots |
| `themes/alacritty-palm.toml` | Terminal theme (zinc night + teal) |
| `wrangler.jsonc` | Cloudflare static assets config |
| **`dist/`** | **BUILD output** — what Cloudflare serves |

## Cloudflare

Point the project at the **repository root**.

| Setting | Value |
|---------|--------|
| **Assets / output directory** | **`website/dist`** |
| **Wrangler config** | `website/wrangler.jsonc` (if using Workers static assets; `assets.directory` is `dist` relative to `website/`) |
| **Build command** (optional) | `just website-build` or `uv run python scripts/website_build.py` |
| **CSS before build** | `just website-css` then `just website-build` · or `just website-build-all` |

If you **commit `website/dist`**, you may leave the build command empty and still set assets to `website/dist`.

## Local recipes

```bash
just website-css          # rebuild styles/output.css
just website-build        # → website/dist/
just website-build-all    # css + dist

# preview
python -m http.server 8765 --directory website/dist
```

Living Library (wiki/reference only, no site):

```bash
just docs-build           # → docs/_build/  (gitignored)
```

## Placeholders

See `images/placeholders/README.md` for screenshot requests.
