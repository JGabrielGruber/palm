"""Wiki corpus publish SOURCE → LibraryStore (0.54.2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from palm.common.library.corpora.wiki import (
    CORPUS_WIKI,
    collect_wiki_blobs,
    publish_wiki_corpus,
)
from palm.common.library.store import LibraryStore, new_revision_id


class _DictBackend:
    def __init__(self) -> None:
        self.data: dict[str, object] = {}

    def get(self, key: str) -> object | None:
        return self.data.get(key)

    def set(self, key: str, value: object) -> None:
        self.data[key] = value


def test_collect_wiki_blobs_from_fixture(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    (wiki / "guides").mkdir(parents=True)
    (wiki / "index.md").write_text("# Home\n\nHello.\n", encoding="utf-8")
    (wiki / "guides" / "a.md").write_text("# Guide A\n", encoding="utf-8")
    rev = new_revision_id()
    blobs = collect_wiki_blobs(wiki, revision=rev)
    assert len(blobs) == 2
    paths = {b.path for b in blobs}
    assert paths == {"index.md", "guides/a.md"}
    home = next(b for b in blobs if b.path == "index.md")
    assert home.title == "Home"
    assert home.corpus == CORPUS_WIKI


def test_publish_wiki_corpus_pins(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "index.md").write_text("# Index\n", encoding="utf-8")
    store = LibraryStore(_DictBackend())
    pin, count = publish_wiki_corpus(
        store,
        wiki_root=wiki,
        palm_version="0.54.2",
        pin=True,
    )
    assert count == 1
    assert pin.corpora[CORPUS_WIKI] == pin.revision
    assert store.get_blob("wiki", "index.md") is not None
    assert store.get_blob("wiki", "index.md").body.startswith("# Index")


def test_publish_wiki_merges_other_corpora(tmp_path: Path) -> None:
    from palm.common.library.models import LibraryBlobRecord

    store = LibraryStore(_DictBackend())
    old_rev = new_revision_id()
    store.put_blob(
        LibraryBlobRecord(
            corpus="mcp",
            revision=old_rev,
            path="catalog.json",
            content_type="application/json",
            body={},
        )
    )
    store.finalize_revision(
        revision=old_rev,
        corpora={"mcp": old_rev},
        blob_counts={"mcp": 1},
        pin=True,
    )

    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "x.md").write_text("# X\n", encoding="utf-8")
    pin, _ = publish_wiki_corpus(store, wiki_root=wiki, pin=True)
    assert pin.corpora["mcp"] == old_rev
    assert pin.corpora["wiki"] == pin.revision


def test_collect_empty_raises(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(ValueError, match="no markdown"):
        collect_wiki_blobs(empty, revision="r1")
