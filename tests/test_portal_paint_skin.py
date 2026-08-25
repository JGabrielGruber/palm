"""Portal dogfood — paint-only language skin (not a 0.68 compost slice)."""

from __future__ import annotations

import re
from pathlib import Path

STATIC = (
    Path(__file__).resolve().parents[1]
    / "src/palm/runtimes/server/surfaces/websocket/static"
)
PORTAL_JS = STATIC / "portal.js"
SKINS_JS = STATIC / "skins.js"
INDEX_HTML = STATIC / "index.html"
SESSION_PY = (
    Path(__file__).resolve().parents[1]
    / "src/palm/runtimes/server/surfaces/websocket/session.py"
)


def test_landing_has_skin_links_outside_the_chat() -> None:
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert 'id="landing"' in html
    assert 'id="fab"' in html
    assert "?lang=en" in html
    assert "?lang=pt-BR" in html
    assert "/portal/skins.js" in html
    # Language picker lives on the empty page, not in the panel header.
    panel = html.split('id="panel"', 1)[1]
    assert "?lang=pt-BR" not in panel


def test_portal_js_paints_labels_not_values() -> None:
    source = PORTAL_JS.read_text(encoding="utf-8")
    assert "function paint(" in source
    assert "function applySynonym(" in source
    assert "resolvePortalLang" in source
    assert "paint(c.label" in source
    assert "chip.onclick = () => submitValue(String(value))" in source
    assert "frame.alias = action.alias" in source
    assert "PALM_PORTAL_SKINS" in source


def test_paint_map_is_exact_and_skips_wire_tokens() -> None:
    source = SKINS_JS.read_text(encoding="utf-8")
    assert "PALM_PORTAL_SKINS" in source
    assert '"pt-BR"' in source
    assert "Lista de tarefas" in source
    assert "sim: \"yes\"" in source or "sim: 'yes'" in source
    # Choice values / aliases stay English on the wire.
    assert "operator-entry/start" not in source
    assert '"todo-builder"' not in source
    assert '"coconut-npc"' not in source
    assert '"yes":' not in source


def test_session_plane_has_no_locale() -> None:
    source = SESSION_PY.read_text(encoding="utf-8")
    assert "locale" not in source.lower()
    assert "lang" not in source.lower()
    assert "pt-BR" not in source


def test_skins_js_parses_as_script() -> None:
    source = SKINS_JS.read_text(encoding="utf-8")
    assert source.strip().startswith("/**") or source.strip().startswith("(() =>")
    assert "window.PALM_PORTAL_SKINS" in source
    # Duplicate synonym keys would be a silent overwrite; sim/nao must exist once.
    assert len(re.findall(r"\bsim:", source)) == 1
    assert len(re.findall(r"\bnao:", source)) == 1
