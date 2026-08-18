"""Neonroot runner app — WorkloadRuntime + doctor (no ResourceEngine provider)."""

from __future__ import annotations

from typing import Any

from palm.common.runtimes.doctor_contributors import register_doctor_contributor
from palm.runners.app import RunnerApp


def _neonroot_doctor_contributor(runtime: Any) -> dict[str, Any]:
    from palm.runners.neonroot.doctor import (
        neonroot_doctor_issues,
        neonroot_doctor_section,
    )

    try:
        section = neonroot_doctor_section(runtime=runtime)
        return {
            "section": {"neonroot": section},
            "issues": neonroot_doctor_issues(section),
        }
    except Exception as exc:
        return {
            "section": {
                "neonroot": {
                    "available": False,
                    "error": f"neonroot doctor probe failed: {exc}",
                }
            },
            "issues": [],
        }


class NeonrootRunnerApp(RunnerApp):
    name = "neonroot"
    label = "NeonRoot WorkloadRuntime (hermetic spawn)"
    default_enabled = True

    def ready(self) -> None:
        register_doctor_contributor(_neonroot_doctor_contributor)


neonroot_runner_app = NeonrootRunnerApp()

__all__ = ["NeonrootRunnerApp", "neonroot_runner_app"]
