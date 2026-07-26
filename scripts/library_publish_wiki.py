#!/usr/bin/env python3
"""Publish docs/wiki SOURCE into Palm library storage (0.54.2).

Uses the host StorageEngine (filesystem by default via PalmSettings) so the
live pin is durable. Example::

    uv run python scripts/library_publish_wiki.py
    uv run python scripts/library_publish_wiki.py --wiki-root docs/wiki --memory
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wiki-root",
        type=Path,
        default=ROOT / "docs" / "wiki",
        help="SOURCE wiki directory (default: docs/wiki)",
    )
    parser.add_argument(
        "--memory",
        action="store_true",
        help="Use in-process memory storage (demo/tests; not durable)",
    )
    parser.add_argument(
        "--no-pin",
        action="store_true",
        help="Write blobs/manifest but do not flip meta/current",
    )
    args = parser.parse_args()

    import palm.storages  # noqa: F401
    from palm import __version__
    from palm.common.library.corpora.wiki import publish_wiki_corpus
    from palm.common.library.store import LibraryStore
    from palm.core.storage import StorageEngine

    engine = StorageEngine()
    engine.initialize()
    if args.memory:
        engine.select("memory")
    else:
        from palm.app.settings import PalmSettings
        from palm.common.storage import StorageFactory

        settings = PalmSettings()
        StorageFactory.initialize_engine(
            engine,
            storage_backend=settings.storage_backend,
            **StorageFactory.backend_options(settings=settings),
        )

    store = LibraryStore(engine)
    pin, count = publish_wiki_corpus(
        store,
        wiki_root=args.wiki_root,
        palm_version=__version__,
        pin=not args.no_pin,
    )
    print(f"[OK] published wiki corpus: {count} page(s)")
    print(f"     revision={pin.revision}")
    print(f"     pin_current={not args.no_pin}")
    print(f"     corpora={pin.corpora}")
    sample = store.list_paths("wiki")[:5]
    print(f"     paths_sample={sample}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
