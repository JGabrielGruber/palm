"""Living Library storage schema + pin (0.54.1)."""

from __future__ import annotations

import pytest

from palm.common.library import (
    LIBRARY_PREFIX,
    LibraryBlobRecord,
    LibraryStore,
    key_blob,
    key_current_pin,
    new_revision_id,
    normalize_blob_path,
)
from palm.common.library.keys import key_manifest
from palm.core.storage import StorageEngine


class _DictBackend:
    def __init__(self) -> None:
        self.data: dict[str, object] = {}

    def get(self, key: str) -> object | None:
        return self.data.get(key)

    def set(self, key: str, value: object) -> None:
        self.data[key] = value


def test_normalize_blob_path_rejects_traversal() -> None:
    with pytest.raises(ValueError):
        normalize_blob_path("../etc/passwd")
    with pytest.raises(ValueError):
        normalize_blob_path("/abs")
    assert normalize_blob_path("guides/x.md") == "guides/x.md"


def test_key_layout() -> None:
    assert key_current_pin().startswith(LIBRARY_PREFIX)
    assert "meta:current" in key_current_pin()
    assert "blob:" in key_blob("wiki", "abc", "index.md")
    assert "manifest" in key_manifest("abc")


def test_publish_and_pin_round_trip() -> None:
    store = LibraryStore(_DictBackend())
    rev = new_revision_id()
    store.put_blob(
        LibraryBlobRecord(
            corpus="wiki",
            revision=rev,
            path="index.md",
            content_type="text/markdown",
            body="# Hello",
            title="Home",
        )
    )
    store.put_blob(
        LibraryBlobRecord(
            corpus="wiki",
            revision=rev,
            path="guides/a.md",
            content_type="text/markdown",
            body="guide",
        )
    )
    pin = store.finalize_revision(
        revision=rev,
        corpora={"wiki": rev},
        blob_counts={"wiki": 2},
        palm_version="0.51.6",
        source="test",
        pin=True,
    )
    assert pin.revision == rev
    assert store.get_current_pin() is not None
    assert store.get_current_pin().corpora["wiki"] == rev

    paths = store.list_paths("wiki")
    assert paths == ["guides/a.md", "index.md"]

    blob = store.get_blob("wiki", "index.md")
    assert blob is not None
    assert blob.body == "# Hello"
    assert blob.title == "Home"

    man = store.get_manifest(rev)
    assert man is not None
    assert man.blob_counts["wiki"] == 2


def test_get_blob_without_pin_returns_none() -> None:
    store = LibraryStore(_DictBackend())
    assert store.get_blob("wiki", "x.md") is None


def test_library_store_with_memory_storage_engine() -> None:
    import palm.storages  # noqa: F401 — register memory backend

    engine = StorageEngine()
    engine.initialize()
    engine.select("memory")
    store = LibraryStore(engine)
    rev = new_revision_id()
    store.publish_corpus_blobs(
        corpus="mcp",
        revision=rev,
        blobs=[
            LibraryBlobRecord(
                corpus="mcp",
                revision=rev,
                path="catalog.json",
                content_type="application/json",
                body={"tools": []},
            )
        ],
    )
    store.finalize_revision(
        revision=rev,
        corpora={"mcp": rev},
        blob_counts={"mcp": 1},
        pin=True,
    )
    got = store.get_blob("mcp", "catalog.json")
    assert got is not None
    assert got.body == {"tools": []}
