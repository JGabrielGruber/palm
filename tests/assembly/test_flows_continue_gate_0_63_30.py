"""0.63.30 — flow product continue doors are citizens; cancel_job named residual."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from palm.app.host.application_host import ApplicationHost
from palm.app.settings import PalmSettings
from palm.common.cqrs.bus import CommandBus, QueryBus
from palm.core.assembly import AdmissionSnapshot, AssemblyPhase
from palm.services.execution.flows.service import FlowExecutionService
from palm.services.execution.flows.session import FlowSession
from palm.system.assembly.errors import AdmissionRefusedError
from palm.system.assembly.inventory import GATED_CITIZENS, PRETENDER_EDGES, kingdom_map
from palm.system.log import reset_system_log_for_tests
from palm.system.runtime.base import BaseRuntime


def _settings() -> PalmSettings:
    return PalmSettings(
        load_example_definitions=True,
        storage_backend="memory",
        rebuild_projections_on_startup=False,
        reconcile_instances_on_startup=False,
        enable_compensation=False,
        enable_outbox_service=False,
        enable_event_outbox=False,
        enable_work_drain_service=False,
    )


def _flows_with_closed_inject() -> FlowExecutionService:
    closed = AdmissionSnapshot(
        may_run_business=False,
        phase=AssemblyPhase.BLOCKED,
        reasons=("test_closed",),
    )
    inspect = MagicMock()
    flows = FlowExecutionService(
        commands=CommandBus(),
        queries=QueryBus(),
        schemas=MagicMock(),
        inspect=inspect,
        admission_source=lambda: closed,
    )
    flows.resolve_runtime = MagicMock(  # type: ignore[method-assign]
        side_effect=AssertionError("oath broken: resolve_runtime used for admission")
    )
    return flows


def test_flow_session_input_refused_on_oath_without_runtime_dig() -> None:
    flows = _flows_with_closed_inject()
    session = FlowSession(flows, flow_id="f", session_id="inst-1")
    with pytest.raises(AdmissionRefusedError, match="test_closed"):
        session.input("x")
    flows.resolve_runtime.assert_not_called()


def test_flow_session_resume_refused_on_oath() -> None:
    flows = _flows_with_closed_inject()
    session = FlowSession(flows, flow_id="f", session_id="inst-1")
    with pytest.raises(AdmissionRefusedError, match="test_closed"):
        session.resume()


def test_flow_session_backtrack_refused_on_oath() -> None:
    flows = _flows_with_closed_inject()
    session = FlowSession(flows, flow_id="f", session_id="inst-1")
    with pytest.raises(AdmissionRefusedError, match="test_closed"):
        session.backtrack()


def test_flow_session_cancel_not_admission_citizen() -> None:
    """Cancel stays control path when admission is closed (named residual)."""
    closed = AdmissionSnapshot(
        may_run_business=False,
        phase=AssemblyPhase.BLOCKED,
        reasons=("test_closed",),
    )
    inspect = MagicMock()
    inspect.inspect_instance.return_value = {"job_id": "job-1"}
    flows = FlowExecutionService(
        commands=CommandBus(),
        queries=QueryBus(),
        schemas=MagicMock(),
        inspect=inspect,
        admission_source=lambda: closed,
    )
    flows.dispatch_command = MagicMock(return_value={"cancelled": True})  # type: ignore[method-assign]
    flows.wait_until_idle = MagicMock(return_value=True)  # type: ignore[method-assign]
    session = FlowSession(flows, flow_id="f", session_id="inst-1")
    assert session.cancel() == {"cancelled": True}
    flows.dispatch_command.assert_called_once()


def test_flows_admission_gate_prefers_inject() -> None:
    ready = AdmissionSnapshot(
        may_run_business=True,
        phase=AssemblyPhase.READY,
        definition_id="test",
    )
    flows = FlowExecutionService(
        commands=CommandBus(),
        queries=QueryBus(),
        schemas=MagicMock(),
        inspect=MagicMock(),
        admission_source=lambda: ready,
    )
    flows.resolve_runtime = MagicMock(  # type: ignore[method-assign]
        side_effect=AssertionError("must not dig for gate when inject set")
    )
    gate = flows.admission_gate()
    assert gate is not None
    assert callable(gate)
    assert gate().may_run_business is True
    flows.resolve_runtime.assert_not_called()


def test_host_flows_continue_refused_when_assembly_skipped() -> None:
    reset_system_log_for_tests()
    host = ApplicationHost.for_mode("all_in_one", settings=_settings())
    host.start(assembly_skip=True)
    try:
        assert host.admission.may_run_business is False
        flows = host.execution.flows
        session = FlowSession(flows, flow_id="f", session_id="inst-x")
        with pytest.raises(AdmissionRefusedError):
            session.resume()
        with pytest.raises(AdmissionRefusedError):
            session.input("x")
        with pytest.raises(AdmissionRefusedError):
            session.backtrack()
    finally:
        host.shutdown()


def test_cancel_job_not_admission_citizen() -> None:
    """Shell cancel remains control path when admission closed."""
    reset_system_log_for_tests()
    rt = BaseRuntime()
    rt.start(
        storage_backend="memory",
        enable_event_outbox=False,
        assembly_skip=True,
    )
    try:
        assert rt.admission.may_run_business is False
        # Missing job → False / no AdmissionRefusedError
        try:
            result = rt.cancel_job("job-missing")
        except Exception as exc:
            assert not isinstance(exc, AdmissionRefusedError)
            return
        assert result is False or result is True
    finally:
        rt.stop()


def test_inventory_flows_continue_and_cancel_residuals() -> None:
    gated = {row["id"] for row in GATED_CITIZENS}
    assert "flows.continue_session" in gated
    assert "flows.admission_oath" in gated
    pretenders = {row["id"]: row["status"] for row in PRETENDER_EDGES}
    assert pretenders["flows.continue_edge"] == "paid_0_63_30"
    assert pretenders["flows.session_cancel_ungated"] == "named_0_63_30"
    assert pretenders["runtime.cancel_job_ungated"] == "named_0_63_30"
    assert kingdom_map()["gated_count"] >= 1
