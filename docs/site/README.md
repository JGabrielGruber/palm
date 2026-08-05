# Site — landing soul

**SOURCE (2026-08+):** repo root **[`website/`](../../website/)** — dedicated canopy for palmengine.org.

| Was | Now |
|-----|-----|
| `docs/index.html`, `docs/styles/`, `docs/images/` | `website/index.html`, `website/styles/`, `website/images/` |
| Raw `docs/` deploy | **Build required:** `just docs-build` → `docs/_build/deploy` |

**BUILD:** `scripts/docs_build.py` copies `website/` into the deploy canopy together with wiki + reference.

**Wrangler:** `docs/wrangler.jsonc` → `assets.directory: _build/deploy`.  
Cloudflare **must** run the build from the monorepo (see `website/README.md`).

Do **not** hand-edit `docs/_build/`.
