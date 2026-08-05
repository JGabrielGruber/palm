#!/usr/bin/env python3
"""Living Library builder v0 (0.52.6) — thin SOURCE → docs/_build.

Stdlib only. No mkdocs/Sphinx. Palm-pipeline dogfood is 0.53.

Layout written under ``docs/_build/`` (gitignored)::

    meta.json                 # version + build stamp
    inventory/library.json    # ADR / wiki / service package inventory
    wiki/                     # copy of docs/wiki
    library/                  # LIBRARY.md + adr index
    reference/index.html      # minimal generated reference
    deploy/                   # edge-ready assemble (website + wiki + reference)
        index.html, styles/, images/, …   # from repo website/
        wiki/, library/, reference/, robots.txt, sitemap.xml

Cloudflare (or any static host) may point assets at ``docs/_build/deploy`` after
this script runs. Landing SOURCE is ``website/`` (not ``docs/index.html``).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from version_utils import ROOT, read_version  # noqa: E402

DOCS = ROOT / "docs"
BUILD = DOCS / "_build"
WEBSITE = ROOT / "website"
WIKI_SRC = DOCS / "wiki"
ADR_SRC = DOCS / "adr"
SERVICES_SRC = ROOT / "src" / "palm" / "services"


def _rm_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def _copytree(src: Path, dest: Path) -> None:
    if not src.is_dir():
        return
    shutil.copytree(src, dest, dirs_exist_ok=True)


def _copy_file(src: Path, dest: Path) -> None:
    if not src.is_file():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def _title_from_md(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return path.stem


def inventory_adrs() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not ADR_SRC.is_dir():
        return rows
    for path in sorted(ADR_SRC.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        m = re.match(r"^(\d+)-", path.name)
        rows.append(
            {
                "id": m.group(1) if m else path.stem,
                "file": path.name,
                "title": _title_from_md(path),
                "path": f"docs/adr/{path.name}",
            }
        )
    return rows


def inventory_wiki() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not WIKI_SRC.is_dir():
        return rows
    for path in sorted(WIKI_SRC.rglob("*.md")):
        rel = path.relative_to(WIKI_SRC).as_posix()
        rows.append(
            {
                "file": rel,
                "title": _title_from_md(path),
                "path": f"docs/wiki/{rel}",
            }
        )
    return rows


def inventory_services() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not SERVICES_SRC.is_dir():
        return rows
    for path in sorted(SERVICES_SRC.iterdir()):
        if not path.is_dir() or path.name.startswith("_") or path.name.startswith("."):
            continue
        if not (path / "__init__.py").is_file():
            continue
        rows.append(
            {
                "name": path.name,
                "package": f"palm.services.{path.name}",
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            }
        )
    return rows


def write_library_json(version: str, built_at: str) -> dict:
    payload = {
        "schema": "palm.living_library.inventory/v0",
        "version": version,
        "built_at": built_at,
        "adrs": inventory_adrs(),
        "wiki": inventory_wiki(),
        "services": inventory_services(),
    }
    out = BUILD / "inventory" / "library.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def write_reference_html(inv: dict) -> None:
    def _rows(items: list[dict], keys: tuple[str, ...]) -> str:
        lines = []
        for item in items:
            cells = "".join(f"<td>{item.get(k, '')}</td>" for k in keys)
            lines.append(f"<tr>{cells}</tr>")
        return "\n".join(lines) if lines else "<tr><td colspan='4'><em>empty</em></td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Palm Living Library — reference (generated)</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 52rem; line-height: 1.45; }}
    h1, h2 {{ font-weight: 600; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95rem; }}
    th, td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: left; }}
    th {{ background: #f4f4f4; }}
    code, .meta {{ color: #444; font-size: 0.9rem; }}
    a {{ color: #0b5; }}
  </style>
</head>
<body>
  <p class="meta">Generated by <code>scripts/docs_build.py</code> · Palm <strong>{inv["version"]}</strong>
     · {inv["built_at"]} · do not hand-edit</p>
  <h1>Living Library — reference</h1>
  <p>Thin inventory (0.52.6). SOURCE of truth remains the repo; this page is a BUILD artifact.</p>
  <p><a href="../wiki/index.md">Wiki</a> · <a href="../library/LIBRARY.md">LIBRARY contract</a>
     · <a href="../../index.html">Landing (deploy root)</a></p>

  <h2>Service packages</h2>
  <table>
    <thead><tr><th>name</th><th>package</th><th>path</th></tr></thead>
    <tbody>
{_rows(inv["services"], ("name", "package", "path"))}
    </tbody>
  </table>

  <h2>ADRs</h2>
  <table>
    <thead><tr><th>id</th><th>file</th><th>title</th></tr></thead>
    <tbody>
{_rows(inv["adrs"], ("id", "file", "title"))}
    </tbody>
  </table>

  <h2>Wiki pages</h2>
  <table>
    <thead><tr><th>file</th><th>title</th></tr></thead>
    <tbody>
{_rows(inv["wiki"], ("file", "title"))}
    </tbody>
  </table>

  <p class="meta">JSON: <code>inventory/library.json</code></p>
</body>
</html>
"""
    out = BUILD / "reference" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def write_build_readme() -> None:
    text = """# docs/_build — generated (do not edit)

Produced by `just docs-build` / `uv run python scripts/docs_build.py`.

- Hand genome lives in `docs/wiki`, `docs/adr`, landing assets, constitution at repo root.
- Point static hosts at **`deploy/`** (assembled canopy), not this README's parent alone.
- Palm-native pipeline build → theme 0.53.
"""
    (BUILD / "README.md").write_text(text, encoding="utf-8")


def assemble_deploy() -> None:
    """Edge-ready tree: landing soul + library artifacts."""
    deploy = BUILD / "deploy"
    _rm_tree(deploy)
    deploy.mkdir(parents=True)

    # Landing (website/ canopy — brand showcase)
    site = WEBSITE if (WEBSITE / "index.html").is_file() else DOCS
    for name in ("index.html", "robots.txt", "sitemap.xml"):
        _copy_file(site / name, deploy / name)
    _copytree(site / "styles", deploy / "styles")
    _copytree(site / "images", deploy / "images")

    # Built library slices
    _copytree(BUILD / "wiki", deploy / "wiki")
    _copytree(BUILD / "library", deploy / "library")
    _copytree(BUILD / "reference", deploy / "reference")
    _copytree(BUILD / "inventory", deploy / "inventory")

    # Lightweight nav stub so /library/ is discoverable from deploy root without rewriting index.html
    (deploy / "library.html").write_text(
        """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/><meta http-equiv="refresh" content="0;url=reference/index.html"/>
<title>Palm Library</title>
</head><body>
<p>Living Library reference → <a href="reference/index.html">reference/index.html</a>
 · <a href="wiki/index.md">wiki</a> · <a href="index.html">home</a></p>
</body></html>
""",
        encoding="utf-8",
    )


def build(*, clean: bool = True) -> Path:
    version = read_version()
    built_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if clean:
        _rm_tree(BUILD)
    BUILD.mkdir(parents=True, exist_ok=True)

    write_build_readme()
    (BUILD / "meta.json").write_text(
        json.dumps({"version": version, "built_at": built_at, "builder": "docs_build.py/v0"}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    _copytree(WIKI_SRC, BUILD / "wiki")
    lib = BUILD / "library"
    lib.mkdir(parents=True, exist_ok=True)
    _copy_file(DOCS / "LIBRARY.md", lib / "LIBRARY.md")
    _copy_file(ADR_SRC / "README.md", lib / "adr-index.md")

    inv = write_library_json(version, built_at)
    write_reference_html(inv)
    assemble_deploy()

    return BUILD


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not wipe docs/_build before writing (default: clean)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build then assert expected artifacts exist (exit 1 if missing)",
    )
    args = parser.parse_args()
    build_root = build(clean=not args.no_clean)
    expected = [
        build_root / "meta.json",
        build_root / "inventory" / "library.json",
        build_root / "wiki" / "index.md",
        build_root / "reference" / "index.html",
        build_root / "deploy" / "index.html",
        build_root / "deploy" / "reference" / "index.html",
    ]
    missing = [str(p.relative_to(ROOT)) for p in expected if not p.is_file()]
    if missing:
        print("docs_build incomplete; missing:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print(f"[OK] Living Library build → {build_root.relative_to(ROOT)}/")
    print(f"     deploy canopy: { (build_root / 'deploy').relative_to(ROOT) }/")
    print(f"     inventory:     adrs={len(json.loads((build_root / 'inventory' / 'library.json').read_text())['adrs'])}")
    if args.check:
        print("[OK] --check artifacts present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
