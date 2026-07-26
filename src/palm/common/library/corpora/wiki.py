"""Publish the wiki corpus from SOURCE markdown into LibraryStore (0.54.2)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from palm.common.library.models import LibraryBlobRecord, LibraryPin
from palm.common.library.store import LibraryStore, new_revision_id

CORPUS_WIKI = "wiki"
_DEFAULT_REL = Path("docs") / "wiki"


def _title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or fallback
    return fallback


def collect_wiki_blobs(
    wiki_root: Path,
    *,
    revision: str,
) -> list[LibraryBlobRecord]:
    """Walk ``wiki_root`` for ``*.md`` and build blob records (does not write storage)."""
    root = wiki_root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"wiki SOURCE root not found: {root}")

    records: list[LibraryBlobRecord] = []
    for path in sorted(root.rglob("*.md")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        body = path.read_text(encoding="utf-8")
        title = _title_from_markdown(body, path.stem)
        records.append(
            LibraryBlobRecord(
                corpus=CORPUS_WIKI,
                revision=revision,
                path=rel,
                content_type="text/markdown; charset=utf-8",
                body=body,
                title=title,
                extras={"source": str(path)},
            )
        )
    if not records:
        raise ValueError(f"no markdown files under wiki root {root}")
    return records


def publish_wiki_corpus(
    store: LibraryStore,
    *,
    wiki_root: Path | str | None = None,
    revision: str | None = None,
    palm_version: str = "",
    pin: bool = True,
    merge_corpora: dict[str, str] | None = None,
) -> tuple[LibraryPin, int]:
    """Publish wiki SOURCE into a new (or given) revision and optionally pin.

    Parameters
    ----------
    store:
        Target :class:`LibraryStore`.
    wiki_root:
        Directory of markdown (default: ``docs/wiki`` under cwd).
    revision:
        Explicit revision id; default :func:`new_revision_id`.
    palm_version:
        Recorded on pin/manifest.
    pin:
        If True, set ``meta/current`` (merges existing pin corpora when
        ``merge_corpora`` is None — keeps other corpora pins).
    merge_corpora:
        If provided, used as the full corpora map for the pin; otherwise
        previous pin's corpora are merged with ``wiki → revision``.

    Returns
    -------
    (pin, blob_count)
    """
    root = Path(wiki_root) if wiki_root is not None else Path.cwd() / _DEFAULT_REL
    rev = revision or new_revision_id()
    blobs = collect_wiki_blobs(root, revision=rev)
    count = store.publish_corpus_blobs(corpus=CORPUS_WIKI, revision=rev, blobs=blobs)

    if merge_corpora is not None:
        corpora = dict(merge_corpora)
        corpora[CORPUS_WIKI] = rev
    else:
        previous = store.get_current_pin()
        corpora = dict(previous.corpora) if previous is not None else {}
        corpora[CORPUS_WIKI] = rev

    counts: dict[str, int] = {CORPUS_WIKI: count}
    # Preserve prior counts for other corpora when present on old manifest
    if previous_manifest_counts := _prior_blob_counts(store, corpora, skip=CORPUS_WIKI):
        counts.update(previous_manifest_counts)

    pin_obj = store.finalize_revision(
        revision=rev,
        corpora=corpora,
        blob_counts=counts,
        palm_version=palm_version,
        source=f"wiki:{root}",
        notes="wiki corpus publish (0.54.2)",
        pin=pin,
    )
    return pin_obj, count


def _prior_blob_counts(
    store: LibraryStore,
    corpora: dict[str, str],
    *,
    skip: str,
) -> dict[str, int]:
    out: dict[str, int] = {}
    for corpus, crev in corpora.items():
        if corpus == skip:
            continue
        man = store.get_manifest(crev)
        if man is not None and corpus in man.blob_counts:
            out[corpus] = man.blob_counts[corpus]
        else:
            out[corpus] = len(store.list_paths(corpus, revision=crev))
    return out


def publish_wiki_from_storage_engine(
    storage: Any,
    **kwargs: Any,
) -> tuple[LibraryPin, int]:
    """Convenience: wrap a StorageEngine as LibraryStore and publish wiki."""
    return publish_wiki_corpus(LibraryStore(storage), **kwargs)


__all__ = [
    "CORPUS_WIKI",
    "collect_wiki_blobs",
    "publish_wiki_corpus",
    "publish_wiki_from_storage_engine",
]
