"""NeonRoot doctor section (WorkloadRuntime, not provider)."""

from __future__ import annotations

from unittest.mock import patch

from palm.runners.neonroot.cli import NeonrootProbe
from palm.runners.neonroot.doctor import neonroot_doctor_issues, neonroot_doctor_section


def test_neonroot_doctor_section_available() -> None:
    import palm.runners  # noqa: F401

    present = NeonrootProbe(available=True, path="/bin/neonroot", version="NeonRoot 0.0.2")
    with patch("palm.runners.neonroot.doctor.probe_neonroot", return_value=present):
        section = neonroot_doctor_section()
    assert section["registered"] is True
    assert section["available"] is True
    assert section["role"] == "workload_runtime"
    assert section["issues"] == []
    assert "composition_declares" not in section


def test_neonroot_doctor_missing_cli_is_unavailable_not_declared() -> None:
    missing = NeonrootProbe(available=False, error="neonroot not found on PATH")
    with patch("palm.runners.neonroot.doctor.probe_neonroot", return_value=missing):
        section = neonroot_doctor_section()
    assert section["registered"] is True
    assert section["available"] is False
    assert "composition_declares" not in section
    assert neonroot_doctor_issues(section) == []


def test_build_doctor_report_includes_neonroot() -> None:
    import palm.runners  # noqa: F401
    from palm.kits.server.diagnostics import build_doctor_report

    class _RT:
        runtime_name = "test"
        storage = None
        orchestration = None
        repository = None
        auth_enforce = False

    report = build_doctor_report(_RT())
    assert "neonroot" in report
    assert "registered" in report["neonroot"]
