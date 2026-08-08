"""0.63.37 — CLI + SSR explorer honest admission_refused voice."""

from __future__ import annotations

from palm.core.assembly import AdmissionSnapshot, AssemblyPhase
from palm.runtimes.cli.shared.admission_voice import format_cli_error
from palm.runtimes.server.surfaces.ssr.explorer.admission_voice import operator_error_text
from palm.system.assembly.errors import AdmissionRefusedError
from palm.system.assembly.inventory import GATED_CITIZENS, PRETENDER_EDGES, kingdom_map


def _closed() -> AdmissionRefusedError:
    return AdmissionRefusedError(
        AdmissionSnapshot(
            may_run_business=False,
            phase=AssemblyPhase.BLOCKED,
            reasons=("cli_ssr_closed",),
        )
    )


def test_cli_format_labels_admission_refused() -> None:
    text = format_cli_error(_closed())
    assert "admission_refused" in text
    assert "cli_ssr_closed" in text


def test_cli_format_leaves_other_errors_plain() -> None:
    text = format_cli_error(ValueError("nope"))
    assert "admission_refused" not in text
    assert "nope" in text


def test_ssr_operator_error_labels_admission_refused() -> None:
    text = operator_error_text(_closed())
    assert text.startswith("admission_refused:")
    assert "cli_ssr_closed" in text


def test_ssr_operator_error_leaves_other_plain() -> None:
    assert operator_error_text(RuntimeError("other")) == "other"


def test_inventory_cli_ssr_admission_voice() -> None:
    gated = {row["id"] for row in GATED_CITIZENS}
    assert "surface.cli_ssr_admission_voice" in gated
    pretenders = {row["id"]: row["status"] for row in PRETENDER_EDGES}
    assert pretenders["surface.cli_ssr_admission_voice_edge"] == "paid_0_63_37"
    assert kingdom_map()["gated_count"] >= 1
