"""Library provider + rebuild-living-library definitions (0.54.4)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from palm.core.registry import provider_registry
from palm.core.storage import StorageEngine
from palm.providers.library.provider import LibraryProvider


@pytest.fixture
def library_provider_with_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import palm.providers
    import palm.storages  # noqa: F401

    engine = StorageEngine()
    engine.initialize()
    engine.select("memory")

    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "index.md").write_text("# Lib\n", encoding="utf-8")

    runtime = MagicMock()
    runtime.storage = engine
    monkeypatch.setattr(
        "palm.providers.library.provider.get_bound_runtime",
        lambda: runtime,
    )

    # publish_wiki uses cwd wiki by default — point at fixture
    from palm.common.library.corpora import wiki as wiki_mod

    orig = wiki_mod.publish_wiki_corpus

    def _pub(store, **kwargs):
        kwargs.setdefault("wiki_root", wiki)
        return orig(store, **kwargs)

    monkeypatch.setattr(wiki_mod, "publish_wiki_corpus", _pub)
    monkeypatch.setattr(
        "palm.providers.library.provider.publish_wiki_corpus",
        _pub,
    )

    cls = provider_registry.get("library")
    p = cls(name="library")
    p.connect()
    return p, engine, wiki


def test_library_provider_registered() -> None:
    import palm.providers  # noqa: F401

    assert provider_registry.get("library") is LibraryProvider


def test_publish_wiki_and_status(library_provider_with_storage) -> None:
    p, _engine, _wiki = library_provider_with_storage
    result = p.invoke("publish_wiki", params={"pin": True})
    assert result.success is True
    assert result.data["blob_count"] >= 1
    st = p.invoke("status")
    assert st.success is True
    assert st.data["published"] is True
    assert "wiki" in st.data["corpora"]


def test_example_definitions_register() -> None:
    from examples.definitions.rebuild_living_library import (
        DOCS_CORPUS_WIKI_PUBLISH,
        REBUILD_LIVING_LIBRARY_FLOW,
        register_definitions,
    )

    assert DOCS_CORPUS_WIKI_PUBLISH.provider == "library"
    assert REBUILD_LIVING_LIBRARY_FLOW.pattern == "wizard"
    steps = REBUILD_LIVING_LIBRARY_FLOW.options["steps"]
    refs = [s.get("resource_ref") for s in steps]
    assert "docs-corpus-wiki-publish" in refs
    assert "library-status" in refs

    class _Repo:
        def __init__(self) -> None:
            self.resources = []
            self.flows = []
            self.processes = []

        def save_resource(self, r):
            self.resources.append(r)
            return r

        def save_flow(self, f):
            self.flows.append(f)
            return f

        def save_process(self, p):
            self.processes.append(p)
            return p

    repo = _Repo()
    register_definitions(repo)
    assert len(repo.resources) == 2
    assert len(repo.flows) == 1
