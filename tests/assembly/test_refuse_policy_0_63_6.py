"""0.63.6 — DNA refuse vs membership; dual shape fails closed."""

from __future__ import annotations

from dataclasses import replace

from palm.core.assembly import (
    AssemblyPhase,
    local_cli,
    local_embedded,
    local_mcp,
    refuse_violations,
)
from palm.system.assembly import AssemblySeat
from palm.system.log import reset_system_log_for_tests
from palm.system.runtime.base import BaseRuntime


def test_refuse_violations_pure() -> None:
    emb = local_embedded()
    assert refuse_violations(emb, surfaces=(), capabilities=()) == ()
    # Composition / option bag is not work_drain membership.
    assert (
        refuse_violations(emb, surfaces=(), capabilities=frozenset({"work_drain"}))
        == ()
    )
    # Drain refuse fires only when DNA lists the capability and refuses it.
    dual = replace(emb, capabilities=frozenset({"work_drain"}))
    assert refuse_violations(dual, surfaces=(), capabilities=()) == (
        "refuse:background_drain",
    )
    assert refuse_violations(
        emb, surfaces=("rest",), capabilities=()
    ) == ("refuse:server_surfaces",)

    cli = local_cli()
    assert refuse_violations(
        cli, surfaces=(), capabilities=frozenset({"work_drain"})
    ) == ()
    assert refuse_violations(cli, surfaces=("rest",), capabilities=()) == (
        "refuse:server_surfaces",
    )

    mcp = local_mcp()
    assert refuse_violations(mcp, surfaces=("mcp",), capabilities=()) == ()
    assert refuse_violations(mcp, surfaces=("rest",), capabilities=()) == (
        "refuse:http_server_surfaces",
    )


def test_seat_blocks_on_refuse_dual() -> None:
    seat = AssemblySeat()
    loop = seat.assemble(
        replace(local_embedded(), capabilities=frozenset({"work_drain"})),
    )
    assert loop.steady is True
    assert seat.admission().may_run_business is False
    assert seat.admission().phase is AssemblyPhase.BLOCKED
    assert any("refuse:" in r for r in seat.admission().reasons)


def test_seat_ready_when_membership_honors_refuse() -> None:
    seat = AssemblySeat()
    seat.assemble(local_cli(), capabilities=frozenset({"work_drain"}))
    assert seat.admission().may_run_business is True


def test_runtime_membership_from_options() -> None:
    """Direct runtime start with dual membership fails closed."""
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=False,
        assembly_dna_id="local.embedded",
        assembly_surfaces=["rest"],
    )
    try:
        assert rt.admission.may_run_business is False
        assert any("refuse:" in r for r in rt.admission.reasons)
    finally:
        rt.stop()
