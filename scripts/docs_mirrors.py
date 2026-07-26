"""Canonical docs → MCP package / Grok skill mirrors (Living Library SOURCE mirrors).

``docs/llms.txt``, ``docs/mcp.txt``, and ``docs/skills/palm/**`` are the hand genome.
Bundled MCP data and ``.grok/skills/palm`` are derived copies. ``docs_check`` fails when
they drift; ``sync_version`` (and ``just docs-sync-mirrors``) rewrite them from source.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from version_utils import ROOT

DOCS_LLMS = ROOT / "docs/llms.txt"
DOCS_MCP = ROOT / "docs/mcp.txt"
DOCS_PALM_SKILL = ROOT / "docs/skills/palm"

BUNDLED_LLMS = ROOT / "src/palm/runtimes/mcp/data/llms.txt"
BUNDLED_MCP = ROOT / "src/palm/runtimes/mcp/data/mcp.txt"
BUNDLED_PALM_SKILL = ROOT / "src/palm/runtimes/mcp/data/skills/palm"
GROK_PALM_SKILL = ROOT / ".grok/skills/palm"

PALM_SKILL_SYNC_FILES = (
    "SKILL.md",
    "references/agent-guide.md",
    "references/mcp-patterns.md",
    "references/session-management.md",
    "references/common-flows.md",
    "references/design-flows.md",
    "references/branching-flows.md",
)


def _copy_file(src: Path, dest: Path, *, dry_run: bool) -> bool:
    """Return True if dest would change (or did change)."""
    if not src.is_file():
        return False
    if dest.is_file() and src.read_bytes() == dest.read_bytes():
        return False
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return True


def iter_mirror_pairs() -> list[tuple[Path, Path]]:
    """(source, destination) pairs that must stay byte-identical."""
    pairs: list[tuple[Path, Path]] = [
        (DOCS_LLMS, BUNDLED_LLMS),
        (DOCS_MCP, BUNDLED_MCP),
    ]
    for rel in PALM_SKILL_SYNC_FILES:
        pairs.append((DOCS_PALM_SKILL / rel, BUNDLED_PALM_SKILL / rel))
        pairs.append((DOCS_PALM_SKILL / rel, GROK_PALM_SKILL / rel))
    return pairs


def sync_doc_mirrors(*, dry_run: bool = False) -> list[str]:
    """Copy canonical docs into MCP + Grok mirrors. Returns relative paths written (or dirty)."""
    changed: list[str] = []
    for src, dest in iter_mirror_pairs():
        if not src.is_file():
            continue
        if _copy_file(src, dest, dry_run=dry_run):
            changed.append(str(dest.relative_to(ROOT)))
    return changed
