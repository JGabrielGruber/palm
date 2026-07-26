"""NeonRoot doctor section (0.53.6)."""

from __future__ import annotations

from unittest.mock import patch

from palm.providers.neonroot.cli import NeonrootProbe
from palm.providers.neonroot.doctor import neonroot_doctor_issues, neonroot_doctor_section


def test_neonroot_doctor_section_available() -> None:
    import palm.providers  # noqa: F401

    present = NeonrootProbe(available=True, path="/bin/neonroot", version="NeonRoot 0.0.2")
    with patch("palm.providers.neonroot.doctor.probe_neonroot", return_value=present):
        section = neonroot_doctor_section(composition_has_neonroot=True)
    assert section["registered"] is True
    assert section["available"] is True
    assert section["issues"] == []


def test_neonroot_doctor_soft_issue_when_declared_but_missing() -> None:
    missing = NeonrootProbe(available=False, error="neonroot not found on PATH")
    with patch("palm.providers.neonroot.doctor.probe_neonroot", return_value=missing):
        section = neonroot_doctor_section(composition_has_neonroot=True)
    assert section["available"] is False
    issues = neonroot_doctor_issues(section)
    assert any("neonroot" in i for i in issues)


def test_build_doctor_report_includes_neonroot() -> None:
    import palm.providers  # noqa: F401
    from palm.common.runtimes.server.diagnostics import build_doctor_report

    class _RT:
        runtime_name = "test"
        storage = None
        orchestration = None
        repository = None
        auth_enforce = False

    report = build_doctor_report(_RT())
    assert "neonroot" in report
    assert "registered" in report["neonroot"]
