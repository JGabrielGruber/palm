"""DocsService stub — list/get/status/rebuild over library pin (0.54.3)."""

from __future__ import annotations

from pathlib import Path

import pytest

from palm.common.cqrs.bus import CommandBus, QueryBus
from palm.common.cqrs.schemas import CqrsSchemaRegistry
from palm.core.storage import StorageEngine
from palm.services.docs import DocsService
from palm.services.docs.service import DocsNotFoundError


@pytest.fixture
def docs_service(tmp_path: Path) -> DocsService:
    import palm.storages  # noqa: F401

    engine = StorageEngine()
    engine.initialize()
    engine.select("memory")

    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "index.md").write_text("# Home\n\nHi.\n", encoding="utf-8")
    (wiki / "guides").mkdir()
    (wiki / "guides" / "a.md").write_text("# A\n", encoding="utf-8")

    return DocsService(
        commands=CommandBus(),
        queries=QueryBus(),
        schemas=CqrsSchemaRegistry(),
        storage_resolver=lambda: engine,
        palm_version="0.54.3-test",
        wiki_root=wiki,
    )


def test_status_empty_before_publish(docs_service: DocsService) -> None:
    st = docs_service.status()
    assert st["published"] is False
    assert docs_service.list_corpora() == []


def test_rebuild_wiki_then_get(docs_service: DocsService) -> None:
    result = docs_service.rebuild("wiki")
    assert result["ok"] is True
    assert result["blob_count"] == 2
    st = docs_service.status()
    assert st["published"] is True
    assert "wiki" in st["corpora"]
    assert st["corpora"]["wiki"]["path_count"] == 2

    paths = docs_service.list_paths("wiki")
    assert "index.md" in paths
    page = docs_service.get("wiki", "index.md")
    assert page["title"] == "Home"
    assert "Hi" in str(page["body"])


def test_get_missing_raises(docs_service: DocsService) -> None:
    docs_service.rebuild("wiki")
    with pytest.raises(DocsNotFoundError):
        docs_service.get("wiki", "nope.md")


def test_rebuild_unknown_corpus(docs_service: DocsService) -> None:
    with pytest.raises(DocsNotFoundError, match="not implemented"):
        docs_service.rebuild("api")


def test_host_wires_docs_service() -> None:
    from palm.app import ApplicationHost
    from palm.app.settings import PalmSettings

    host = ApplicationHost(settings=PalmSettings.for_tests(load_examples=False))
    host.start()
    try:
        assert host.docs is not None
        assert "docs" in host.composition.services
        st = host.docs.status()
        assert "published" in st
    finally:
        host.shutdown()
