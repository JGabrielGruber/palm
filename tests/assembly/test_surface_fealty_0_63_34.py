"""0.63.34 — surface fealty: CLI/SSR dig host packaging; wizard CQRS continue gate."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from palm.app.host.application_host import ApplicationHost
from palm.app.settings import PalmSettings
from palm.patterns.wizard.bindings.cqrs.commands import (
    ProvideWizardInputCommand,
    RequestWizardBacktrackCommand,
)
from palm.patterns.wizard.bindings.cqrs.handlers import handle_wizard_command
from palm.system.assembly.errors import AdmissionRefusedError
from palm.system.assembly.inventory import GATED_CITIZENS, PRETENDER_EDGES, kingdom_map
from palm.system.log import reset_system_log_for_tests


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


def test_host_resume_job_refused_when_assembly_skipped() -> None:
    reset_system_log_for_tests()
    host = ApplicationHost.for_mode("all_in_one", settings=_settings())
    host.start(assembly_skip=True)
    try:
        assert host.admission.may_run_business is False
        with pytest.raises(AdmissionRefusedError):
            host.resume_job("job-missing")
    finally:
        host.shutdown()


def _closed_wizard_ctx() -> MagicMock:
    from palm.core.assembly import AdmissionSnapshot, AssemblyPhase

    rt = MagicMock()
    rt.admission = AdmissionSnapshot(
        may_run_business=False,
        phase=AssemblyPhase.BLOCKED,
        reasons=("wizard_closed",),
    )
    ctx = MagicMock()
    ctx._router = None
    ctx._app = None
    ctx._runtime = rt
    return ctx


def test_wizard_provide_input_refused_when_runtime_closed() -> None:
    with pytest.raises(AdmissionRefusedError, match="wizard_closed"):
        handle_wizard_command(
            ProvideWizardInputCommand(instance_id="inst-1", value="x"),
            _closed_wizard_ctx(),
        )


def test_wizard_backtrack_refused_when_runtime_closed() -> None:
    with pytest.raises(AdmissionRefusedError, match="wizard_closed"):
        handle_wizard_command(
            RequestWizardBacktrackCommand(instance_id="inst-1"),
            _closed_wizard_ctx(),
        )


def test_inventory_surface_fealty() -> None:
    gated = {row["id"] for row in GATED_CITIZENS}
    assert "surface.fealty" in gated
    pretenders = {row["id"]: row["status"] for row in PRETENDER_EDGES}
    assert pretenders["surface.fealty_edge"] == "paid_0_63_34"
    assert kingdom_map()["gated_count"] >= 1
