"""0.63.38 — exit residual ledger: open named pretenders first-class cartography."""

from __future__ import annotations

from palm.system.assembly.inventory import (
    GATED_CITIZENS,
    PRETENDER_EDGES,
    kingdom_map,
    open_pretender_edges,
    paid_pretender_edges,
)


def test_open_residuals_are_named_status_only() -> None:
    open_rows = open_pretender_edges()
    assert open_rows
    for row in open_rows:
        assert row["status"].startswith("named_"), row
    open_ids = {row["id"] for row in open_rows}
    # Control / dig / soft catalog residuals still open by design
    assert "kernel.direct_dig" in open_ids
    assert "runtime.cancel_job_ungated" in open_ids
    assert "flows.soft_catalog" in open_ids


def test_paid_edges_not_in_open_ledger() -> None:
    open_ids = {row["id"] for row in open_pretender_edges()}
    paid_ids = {row["id"] for row in paid_pretender_edges()}
    assert open_ids.isdisjoint(paid_ids)
    assert "surface.cli_ssr_admission_voice_edge" in paid_ids
    assert "kingdom.exit_residual_ledger_edge" in paid_ids


def test_kingdom_map_exposes_open_residual_ledger() -> None:
    m = kingdom_map()
    assert m["open_residual_count"] == len(m["open_residuals"])
    assert m["open_residual_count"] == len(m["open_residual_ids"])
    assert m["paid_edge_count"] == len(m["paid_edge_ids"])
    assert m["open_residual_count"] + m["paid_edge_count"] <= m["pretender_count"]
    assert set(m["open_residual_ids"]) == {r["id"] for r in m["open_residuals"]}


def test_inventory_exit_residual_ledger_citizen() -> None:
    gated = {row["id"] for row in GATED_CITIZENS}
    assert "kingdom.exit_residual_ledger" in gated
    pretenders = {row["id"]: row["status"] for row in PRETENDER_EDGES}
    assert pretenders["kingdom.exit_residual_ledger_edge"] == "paid_0_63_38"
