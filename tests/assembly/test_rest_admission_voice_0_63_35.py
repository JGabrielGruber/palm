"""0.63.35 — REST honest voice for AdmissionRefusedError (not submit_failed 500)."""

from __future__ import annotations

from palm.core.assembly import AdmissionSnapshot, AssemblyPhase
from palm.runtimes.server.surfaces.rest import errors
from palm.system.assembly.errors import AdmissionRefusedError
from palm.system.assembly.inventory import GATED_CITIZENS, PRETENDER_EDGES, kingdom_map


def test_admission_refused_helper_is_503_not_500() -> None:
    resp = errors.admission_refused("admission refused: test_closed")
    assert resp.status == 503
    assert isinstance(resp.body, dict)
    assert resp.body["error"] == "admission_refused"
    assert "test_closed" in resp.body["detail"]


def test_maybe_admission_refused_maps_error() -> None:
    snap = AdmissionSnapshot(
        may_run_business=False,
        phase=AssemblyPhase.BLOCKED,
        reasons=("rest_closed",),
    )
    exc = AdmissionRefusedError(snap)
    resp = errors.maybe_admission_refused(exc)
    assert resp is not None
    assert resp.status == 503
    assert resp.body["error"] == "admission_refused"
    assert "rest_closed" in resp.body["detail"]


def test_maybe_admission_refused_ignores_other() -> None:
    assert errors.maybe_admission_refused(ValueError("nope")) is None
    assert errors.maybe_admission_refused(RuntimeError("other")) is None


def test_submit_failed_still_500() -> None:
    resp = errors.submit_failed("boom")
    assert resp.status == 500
    assert resp.body["error"] == "submit_failed"


def test_inventory_rest_admission_voice() -> None:
    gated = {row["id"] for row in GATED_CITIZENS}
    assert "surface.rest_admission_voice" in gated
    pretenders = {row["id"]: row["status"] for row in PRETENDER_EDGES}
    assert pretenders["surface.rest_admission_voice_edge"] == "paid_0_63_35"
    assert kingdom_map()["gated_count"] >= 1
