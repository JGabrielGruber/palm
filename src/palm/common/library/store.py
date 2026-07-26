"""LibraryStore — publish blobs and pin the live library revision (0.54.1)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Protocol

from palm.common.library.keys import (
    key_blob,
    key_corpus_index,
    key_current_pin,
    key_manifest,
    normalize_blob_path,
)
from palm.common.library.models import LibraryBlobRecord, LibraryManifest, LibraryPin


class _KeyValueBackend(Protocol):
    def get(self, key: str) -> Any | None: ...
    def set(self, key: str, value: Any) -> None: ...


def new_revision_id() -> str:
    """Opaque revision id (time-sortable-ish uuid4 for v0)."""
    return uuid.uuid4().hex


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class LibraryStore:
    """Read/write Living Library products on a StorageEngine-compatible backend.

    Does not open storage; caller passes an initialized engine (or test double).
    """

    def __init__(self, backend: _KeyValueBackend) -> None:
        self._backend = backend

    # ── pin ──────────────────────────────────────────────────────────────────

    def get_current_pin(self) -> LibraryPin | None:
        raw = self._backend.get(key_current_pin())
        if raw is None:
            return None
        if not isinstance(raw, dict):
            raise TypeError(f"library pin must be a dict, got {type(raw).__name__}")
        return LibraryPin.from_dict(raw)

    def pin_current(self, pin: LibraryPin) -> LibraryPin:
        """Atomically flip the live pin (last-write-wins; single-writer convention)."""
        if not pin.revision.strip():
            raise ValueError("pin.revision must be non-empty")
        self._backend.set(key_current_pin(), pin.to_dict())
        return pin

    # ── manifest ─────────────────────────────────────────────────────────────

    def put_manifest(self, manifest: LibraryManifest) -> None:
        self._backend.set(key_manifest(manifest.revision), manifest.to_dict())

    def get_manifest(self, revision: str) -> LibraryManifest | None:
        raw = self._backend.get(key_manifest(revision))
        if raw is None:
            return None
        if not isinstance(raw, dict):
            raise TypeError(f"library manifest must be a dict, got {type(raw).__name__}")
        return LibraryManifest.from_dict(raw)

    # ── blobs ────────────────────────────────────────────────────────────────

    def put_blob(self, record: LibraryBlobRecord) -> str:
        """Store a blob; return storage key. Updates corpus index for the rev."""
        path = normalize_blob_path(record.path)
        record = LibraryBlobRecord(
            corpus=record.corpus,
            revision=record.revision,
            path=path,
            content_type=record.content_type,
            body=record.body,
            title=record.title,
            extras=dict(record.extras),
        )
        storage_key = key_blob(record.corpus, record.revision, path)
        self._backend.set(storage_key, record.to_dict())
        self._index_add(record.corpus, record.revision, path)
        return storage_key

    def get_blob(
        self,
        corpus: str,
        path: str,
        *,
        revision: str | None = None,
    ) -> LibraryBlobRecord | None:
        rev = revision
        if rev is None:
            pin = self.get_current_pin()
            if pin is None:
                return None
            rev = pin.corpora.get(corpus) or pin.revision
        path = normalize_blob_path(path)
        raw = self._backend.get(key_blob(corpus, rev, path))
        if raw is None:
            return None
        if not isinstance(raw, dict):
            raise TypeError(f"library blob must be a dict, got {type(raw).__name__}")
        return LibraryBlobRecord.from_dict(raw)

    def list_paths(self, corpus: str, *, revision: str | None = None) -> list[str]:
        rev = revision
        if rev is None:
            pin = self.get_current_pin()
            if pin is None:
                return []
            rev = pin.corpora.get(corpus) or pin.revision
        raw = self._backend.get(key_corpus_index(corpus, rev))
        if raw is None:
            return []
        if isinstance(raw, dict):
            paths = raw.get("paths") or []
            return sorted(str(p) for p in paths)
        if isinstance(raw, list):
            return sorted(str(p) for p in raw)
        return []

    def _index_add(self, corpus: str, revision: str, path: str) -> None:
        idx_key = key_corpus_index(corpus, revision)
        raw = self._backend.get(idx_key)
        paths: set[str] = set()
        if isinstance(raw, dict) and isinstance(raw.get("paths"), list):
            paths = {str(p) for p in raw["paths"]}
        elif isinstance(raw, list):
            paths = {str(p) for p in raw}
        paths.add(path)
        self._backend.set(idx_key, {"paths": sorted(paths)})

    # ── publish helpers ──────────────────────────────────────────────────────

    def publish_corpus_blobs(
        self,
        *,
        corpus: str,
        revision: str,
        blobs: list[LibraryBlobRecord],
    ) -> int:
        """Write many blobs for one corpus/revision; returns count."""
        n = 0
        for blob in blobs:
            if blob.corpus != corpus or blob.revision != revision:
                raise ValueError("blob corpus/revision must match publish_corpus_blobs args")
            self.put_blob(blob)
            n += 1
        return n

    def finalize_revision(
        self,
        *,
        revision: str,
        corpora: dict[str, str],
        blob_counts: dict[str, int],
        palm_version: str = "",
        source: str = "",
        notes: str = "",
        pin: bool = True,
    ) -> LibraryPin:
        """Write manifest and optionally pin current to this revision."""
        built_at = _utc_now()
        manifest = LibraryManifest(
            revision=revision,
            built_at=built_at,
            palm_version=palm_version,
            corpora=sorted(corpora.keys()),
            blob_counts=dict(blob_counts),
            source=source,
        )
        self.put_manifest(manifest)
        library_pin = LibraryPin(
            revision=revision,
            built_at=built_at,
            palm_version=palm_version,
            corpora=dict(corpora),
            notes=notes,
        )
        if pin:
            self.pin_current(library_pin)
        return library_pin


__all__ = ["LibraryStore", "new_revision_id"]
