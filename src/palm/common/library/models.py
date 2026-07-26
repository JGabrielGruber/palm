"""Library pin / manifest / blob records (JSON-friendly)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class LibraryCorpusPin:
    """Per-corpus revision pointer (usually matches global pin in v0)."""

    corpus: str
    revision: str
    blob_count: int = 0


@dataclass
class LibraryPin:
    """Current live library pin (``meta/current``)."""

    revision: str
    built_at: str
    palm_version: str = ""
    corpora: dict[str, str] = field(default_factory=dict)  # corpus → rev
    generator: str = "library-store/v0"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LibraryPin:
        corpora_raw = data.get("corpora") or {}
        corpora = {str(k): str(v) for k, v in dict(corpora_raw).items()}
        return cls(
            revision=str(data["revision"]),
            built_at=str(data.get("built_at") or ""),
            palm_version=str(data.get("palm_version") or ""),
            corpora=corpora,
            generator=str(data.get("generator") or "library-store/v0"),
            notes=str(data.get("notes") or ""),
        )


@dataclass
class LibraryManifest:
    """Full record of a library revision build."""

    revision: str
    built_at: str
    palm_version: str = ""
    corpora: list[str] = field(default_factory=list)
    blob_counts: dict[str, int] = field(default_factory=dict)
    source: str = ""  # e.g. git-archive, local
    generator: str = "library-store/v0"
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LibraryManifest:
        return cls(
            revision=str(data["revision"]),
            built_at=str(data.get("built_at") or ""),
            palm_version=str(data.get("palm_version") or ""),
            corpora=[str(c) for c in (data.get("corpora") or [])],
            blob_counts={str(k): int(v) for k, v in dict(data.get("blob_counts") or {}).items()},
            source=str(data.get("source") or ""),
            generator=str(data.get("generator") or "library-store/v0"),
            extras=dict(data.get("extras") or {}),
        )


@dataclass
class LibraryBlobRecord:
    """One stored page / inventory document."""

    corpus: str
    revision: str
    path: str
    content_type: str
    body: str | bytes | dict[str, Any] | list[Any]
    title: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "corpus": self.corpus,
            "revision": self.revision,
            "path": self.path,
            "content_type": self.content_type,
            "body": self.body,
            "title": self.title,
            "extras": dict(self.extras),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LibraryBlobRecord:
        return cls(
            corpus=str(data["corpus"]),
            revision=str(data["revision"]),
            path=str(data["path"]),
            content_type=str(data.get("content_type") or "application/octet-stream"),
            body=data.get("body"),
            title=str(data.get("title") or ""),
            extras=dict(data.get("extras") or {}),
        )


__all__ = [
    "LibraryBlobRecord",
    "LibraryCorpusPin",
    "LibraryManifest",
    "LibraryPin",
]
