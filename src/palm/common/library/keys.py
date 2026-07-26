"""Key layout for the Living Library namespace in StorageEngine."""

from __future__ import annotations

LIBRARY_PREFIX = "palm:library"


def normalize_blob_path(path: str) -> str:
    """Normalize a corpus-relative path for storage keys (no traversal)."""
    raw = str(path or "").strip().replace("\\", "/")
    if not raw or raw.startswith("/") or ".." in raw.split("/"):
        raise ValueError(f"invalid library blob path {path!r}")
    parts = [p for p in raw.split("/") if p and p != "."]
    if not parts:
        raise ValueError(f"invalid library blob path {path!r}")
    return "/".join(parts)


def _norm_seg(segment: str, *, what: str) -> str:
    s = str(segment or "").strip()
    if not s or "/" in s or ":" in s or s in (".", ".."):
        raise ValueError(f"invalid library {what} {segment!r}")
    return s


def key_current_pin() -> str:
    """Global pin: which revision is live."""
    return f"{LIBRARY_PREFIX}:meta:current"


def key_manifest(revision: str) -> str:
    rev = _norm_seg(revision, what="revision")
    return f"{LIBRARY_PREFIX}:revisions:{rev}:manifest"


def key_corpus_index(corpus: str, revision: str) -> str:
    """Optional per-corpus file list for a revision."""
    c = _norm_seg(corpus, what="corpus")
    rev = _norm_seg(revision, what="revision")
    return f"{LIBRARY_PREFIX}:{c}:{rev}:__index__"


def key_blob(corpus: str, revision: str, path: str) -> str:
    c = _norm_seg(corpus, what="corpus")
    rev = _norm_seg(revision, what="revision")
    p = normalize_blob_path(path)
    # Path segments joined with / inside the key value payload; key uses :
    key_path = p.replace("/", ":")
    return f"{LIBRARY_PREFIX}:{c}:{rev}:blob:{key_path}"


__all__ = [
    "LIBRARY_PREFIX",
    "key_blob",
    "key_corpus_index",
    "key_current_pin",
    "key_manifest",
    "normalize_blob_path",
]
