"""Host runner app manifest."""

from __future__ import annotations

from typing import Any

from palm.common.runtimes.doctor_contributors import register_doctor_contributor
from palm.runners.app import RunnerApp


def _host_doctor_contributor(runtime: Any) -> dict[str, Any]:
    from palm.runners.host.doctor import (
        host_workload_doctor_issues,
        host_workload_doctor_section,
    )

    try:
        section = host_workload_doctor_section(runtime=runtime)
        return {
            "section": {"workload_host": section},
            "issues": host_workload_doctor_issues(section),
        }
    except Exception as exc:
        return {
            "section": {
                "workload_host": {
                    "registered": False,
                    "error": f"host workload doctor failed: {exc}",
                }
            },
            "issues": [],
        }


class HostRunnerApp(RunnerApp):
    name = "host"
    label = "Host subprocess WorkloadRuntime (default OFF)"
    default_enabled = False

    def ready(self) -> None:
        register_doctor_contributor(_host_doctor_contributor)


host_runner_app = HostRunnerApp()

__all__ = ["HostRunnerApp", "host_runner_app"]
