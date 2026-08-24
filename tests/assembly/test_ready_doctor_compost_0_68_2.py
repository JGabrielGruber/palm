"""0.68.2 — runner ready() doctor register composted."""

from __future__ import annotations

import importlib.util

from palm.kits.server.diagnostics import build_doctor_report
from palm.runners.host.app import HostRunnerApp
from palm.runners.neonroot.app import NeonrootRunnerApp


def test_doctor_contributor_registry_is_gone() -> None:
    assert importlib.util.find_spec("palm.common.runtimes.doctor_contributors") is None
    assert importlib.util.find_spec("palm.runners.host.doctor") is None
    assert importlib.util.find_spec("palm.runners.neonroot.doctor") is None
    import palm.common.runtimes as cr

    assert not hasattr(cr, "register_doctor_contributor")
    assert not hasattr(cr, "collect_doctor_extensions")


def test_host_and_neonroot_ready_are_not_doctor_registers() -> None:
    assert not hasattr(HostRunnerApp, "ready")
    assert not hasattr(NeonrootRunnerApp, "ready")


def test_anatomy_doctor_has_no_contributor_bags() -> None:
    import palm.runners  # noqa: F401

    class _RT:
        runtime_name = "test"
        storage = None
        orchestration = None
        repository = None
        auth_enforce = False

    report = build_doctor_report(_RT())
    assert "neonroot" not in report
    assert "workload_host" not in report
    assert "neonroot" in report["workloads"]["registered_runtimes"]
    assert "host" in report["workloads"]["registered_runtimes"]
