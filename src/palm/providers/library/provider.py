"""Library resource provider — produce corpora into LibraryStore."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from palm import __version__
from palm.common.library import LibraryStore
from palm.common.library.corpora.wiki import CORPUS_WIKI, publish_wiki_corpus
from palm.common.providers._registry import get_bound_runtime
from palm.core.resource import BaseProvider
from palm.core.resource.result import (
    ProviderActionDescriptor,
    ProviderDescriptor,
    ProviderHealth,
    ProviderResult,
)


class LibraryProvider(BaseProvider):
    """Publish and read Living Library products via host storage."""

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def fetch(self, resource_id: str, **params: Any) -> Any:
        result = self.invoke("get", resource_id=resource_id, params=params)
        if not result.success:
            raise RuntimeError(result.error or "library get failed")
        return result.data

    def _store(self) -> LibraryStore:
        runtime = get_bound_runtime()
        if runtime is None or getattr(runtime, "storage", None) is None:
            raise RuntimeError("library provider requires a bound runtime with storage")
        storage = runtime.storage
        if not storage.is_initialized:
            raise RuntimeError("library provider: StorageEngine is not initialized")
        if storage.backend is None or not storage.backend.is_open:
            raise RuntimeError("library provider: storage backend is not open")
        return LibraryStore(storage)

    def invoke(
        self,
        action: str,
        *,
        params: dict[str, Any] | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> ProviderResult:
        merged = dict(params or {})
        merged.update(kwargs)
        if resource_id is not None:
            merged.setdefault("path", resource_id)
            merged.setdefault("resource_id", resource_id)

        try:
            if action == "publish_wiki":
                return self._publish_wiki(merged)
            if action == "status":
                return self._status()
            if action == "list_paths":
                return self._list_paths(merged)
            if action == "get":
                return self._get(merged)
            return ProviderResult.fail(
                f"Unsupported action {action!r}",
                action=action,
                provider=self.name,
            )
        except Exception as exc:
            return ProviderResult.fail(str(exc), action=action, provider=self.name)

    def _publish_wiki(self, params: dict[str, Any]) -> ProviderResult:
        store = self._store()
        wiki_root = params.get("wiki_root")
        kwargs: dict[str, Any] = {
            "palm_version": str(params.get("palm_version") or __version__),
            "pin": bool(params.get("pin", True)),
        }
        if wiki_root:
            kwargs["wiki_root"] = Path(str(wiki_root))
        pin, count = publish_wiki_corpus(store, **kwargs)
        return ProviderResult.ok(
            {
                "corpus": CORPUS_WIKI,
                "revision": pin.revision,
                "blob_count": count,
                "corpora": dict(pin.corpora),
                "built_at": pin.built_at,
            },
            action="publish_wiki",
            provider=self.name,
        )

    def _status(self) -> ProviderResult:
        store = self._store()
        pin = store.get_current_pin()
        if pin is None:
            return ProviderResult.ok(
                {"published": False, "revision": None, "corpora": {}},
                action="status",
                provider=self.name,
            )
        corpora: dict[str, Any] = {}
        for corpus, crev in pin.corpora.items():
            corpora[corpus] = {
                "revision": crev,
                "path_count": len(store.list_paths(corpus, revision=crev)),
            }
        return ProviderResult.ok(
            {
                "published": True,
                "revision": pin.revision,
                "corpora": corpora,
                "built_at": pin.built_at,
                "palm_version": pin.palm_version,
            },
            action="status",
            provider=self.name,
        )

    def _list_paths(self, params: dict[str, Any]) -> ProviderResult:
        corpus = str(params.get("corpus") or CORPUS_WIKI)
        revision = params.get("revision")
        paths = self._store().list_paths(
            corpus,
            revision=str(revision) if revision else None,
        )
        return ProviderResult.ok(
            {"corpus": corpus, "paths": paths},
            action="list_paths",
            provider=self.name,
        )

    def _get(self, params: dict[str, Any]) -> ProviderResult:
        corpus = str(params.get("corpus") or CORPUS_WIKI)
        path = str(params.get("path") or params.get("resource_id") or "").strip()
        if not path:
            return ProviderResult.fail("get requires path", action="get", provider=self.name)
        revision = params.get("revision")
        blob = self._store().get_blob(
            corpus,
            path,
            revision=str(revision) if revision else None,
        )
        if blob is None:
            return ProviderResult.fail(
                f"not found: {corpus}/{path}",
                action="get",
                provider=self.name,
            )
        return ProviderResult.ok(blob.to_dict(), action="get", provider=self.name)

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            description=(
                "Living Library corpus publish into Palm storage "
                "(wiki publish + status/get; more corpora later)"
            ),
            actions=(
                ProviderActionDescriptor("publish_wiki", "Publish docs/wiki SOURCE → storage pin"),
                ProviderActionDescriptor("status", "Current library pin summary"),
                ProviderActionDescriptor("list_paths", "List paths in a corpus"),
                ProviderActionDescriptor("get", "Get a published blob by corpus/path"),
            ),
        )

    def health(self) -> ProviderHealth:
        try:
            self._store()
            return ProviderHealth(healthy=True, message="library provider (storage ready)")
        except Exception as exc:
            return ProviderHealth(healthy=False, message=str(exc))


__all__ = ["LibraryProvider"]
