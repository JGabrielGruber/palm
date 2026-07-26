"""DocsService — list/get/status over library storage pin; rebuild wiki corpus (0.54.3).

Live docs are **storage-backed** (:class:`~palm.common.library.store.LibraryStore`),
not host ``docs/_build``. Rebuild publishes SOURCE wiki into a new pin.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from palm.common.library import LibraryStore
from palm.common.library.corpora.wiki import CORPUS_WIKI, publish_wiki_corpus
from palm.common.services.base import BaseService


class DocsNotConfiguredError(RuntimeError):
    """Storage is not available for the library store."""


class DocsNotFoundError(LookupError):
    """Requested corpus path or pin is missing."""


class DocsService(BaseService):
    """Living Library product API (read pin + publish wiki for v0)."""

    def __init__(
        self,
        *,
        commands: Any,
        queries: Any,
        schemas: Any,
        storage_resolver: Callable[[], Any],
        palm_version: str = "",
        wiki_root: Any | None = None,
    ) -> None:
        super().__init__(commands=commands, queries=queries, schemas=schemas)
        self._storage_resolver = storage_resolver
        self._palm_version = palm_version
        self._wiki_root = wiki_root

    def _store(self) -> LibraryStore:
        storage = self._storage_resolver()
        if storage is None:
            raise DocsNotConfiguredError("storage_resolver returned None")
        if hasattr(storage, "is_initialized") and not storage.is_initialized:
            raise DocsNotConfiguredError("StorageEngine is not initialized")
        if hasattr(storage, "backend") and (
            storage.backend is None or not getattr(storage.backend, "is_open", False)
        ):
            raise DocsNotConfiguredError("StorageEngine backend is not open")
        return LibraryStore(storage)

    def status(self) -> dict[str, Any]:
        """Current pin + corpora summary (empty library if never published)."""
        store = self._store()
        pin = store.get_current_pin()
        if pin is None:
            return {
                "published": False,
                "revision": None,
                "corpora": {},
                "built_at": None,
                "palm_version": self._palm_version,
                "note": "no library pin yet — publish wiki via rebuild('wiki') or just library-publish-wiki",
            }
        corpus_stats: dict[str, Any] = {}
        for corpus, crev in pin.corpora.items():
            paths = store.list_paths(corpus, revision=crev)
            corpus_stats[corpus] = {
                "revision": crev,
                "path_count": len(paths),
            }
        return {
            "published": True,
            "revision": pin.revision,
            "corpora": corpus_stats,
            "built_at": pin.built_at,
            "palm_version": pin.palm_version or self._palm_version,
            "generator": pin.generator,
            "notes": pin.notes,
        }

    def list_corpora(self) -> list[dict[str, Any]]:
        """Corpora on the current pin."""
        status = self.status()
        if not status.get("published"):
            return []
        rows = []
        for name, info in (status.get("corpora") or {}).items():
            rows.append({"corpus": name, **info})
        return sorted(rows, key=lambda r: str(r.get("corpus") or ""))

    def list_paths(self, corpus: str, *, revision: str | None = None) -> list[str]:
        store = self._store()
        pin = store.get_current_pin()
        if pin is None and revision is None:
            return []
        return store.list_paths(corpus, revision=revision)

    def get(
        self,
        corpus: str,
        path: str,
        *,
        revision: str | None = None,
    ) -> dict[str, Any]:
        store = self._store()
        blob = store.get_blob(corpus, path, revision=revision)
        if blob is None:
            raise DocsNotFoundError(f"library blob not found: {corpus}/{path}")
        return {
            "corpus": blob.corpus,
            "revision": blob.revision,
            "path": blob.path,
            "content_type": blob.content_type,
            "title": blob.title,
            "body": blob.body,
            "extras": dict(blob.extras),
        }

    def rebuild(self, corpus: str = CORPUS_WIKI) -> dict[str, Any]:
        """Publish a corpus into a new pin.

        v0 supports ``wiki`` only (SOURCE → storage). Other corpora later.
        """
        name = str(corpus or CORPUS_WIKI).strip().lower()
        if name != CORPUS_WIKI:
            raise DocsNotFoundError(
                f"rebuild corpus {corpus!r} not implemented yet (v0: wiki only)"
            )
        store = self._store()
        kwargs: dict[str, Any] = {
            "palm_version": self._palm_version,
            "pin": True,
        }
        if self._wiki_root is not None:
            kwargs["wiki_root"] = self._wiki_root
        pin, count = publish_wiki_corpus(store, **kwargs)
        return {
            "ok": True,
            "corpus": CORPUS_WIKI,
            "revision": pin.revision,
            "blob_count": count,
            "corpora": dict(pin.corpora),
            "built_at": pin.built_at,
        }


__all__ = [
    "DocsNotConfiguredError",
    "DocsNotFoundError",
    "DocsService",
]
