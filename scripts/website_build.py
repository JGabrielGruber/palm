#!/usr/bin/env python3
"""Assemble palmengine.org static site → website/dist.

SOURCE: website/{index.html,styles,images,robots.txt,sitemap.xml}
BUILD:  website/dist/  (Cloudflare assets.directory)

Stdlib only. Does not touch docs/ Living Library.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from version_utils import ROOT  # noqa: E402

WEBSITE = ROOT / "website"
DIST = WEBSITE / "dist"

# Paths under website/ to publish (relative)
PUBLISH = (
    "index.html",
    "robots.txt",
    "llms.txt",
    "sitemap.xml",
    "styles",
    "images",
)


def _rm_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def build(*, clean: bool = True) -> Path:
    if not (WEBSITE / "index.html").is_file():
        raise SystemExit(f"missing {WEBSITE / 'index.html'}")

    if clean:
        _rm_tree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

    for name in PUBLISH:
        src = WEBSITE / name
        dest = DIST / name
        if not src.exists():
            print(f"warning: skip missing {src.relative_to(ROOT)}", file=sys.stderr)
            continue
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(
                src,
                dest,
                ignore=shutil.ignore_patterns("placeholders", "README.md"),
            )
        else:
            shutil.copy2(src, dest)

    # Do not ship internal placeholder notes as public paths
    placeholders = DIST / "images" / "placeholders"
    if placeholders.is_dir():
        shutil.rmtree(placeholders)

    return DIST


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not wipe website/dist before copy",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build then assert index.html + styles exist",
    )
    args = parser.parse_args()
    dist = build(clean=not args.no_clean)
    expected = [
        dist / "index.html",
        dist / "styles" / "output.css",
        dist / "images" / "logo.webp",
    ]
    missing = [str(p.relative_to(ROOT)) for p in expected if not p.is_file()]
    if missing:
        print("website_build incomplete; missing:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print(f"[OK] website → {dist.relative_to(ROOT)}/")
    print("     Cloudflare assets.directory: website/dist  (repo root as project root)")
    if args.check:
        print("[OK] --check artifacts present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
