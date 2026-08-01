"""Shared flow definitions for host / integration tests (0.59.8 cleanup).

Legacy ``pattern=\"dag\", options={\"name\": \"quick\"}`` is dead — DAG requires
``nodes`` / ``steps`` (0.54+). Prefer a one-step wizard for spine assertions.
"""

from __future__ import annotations

from typing import Any

from palm.definitions.flow import FlowDefinition


def spine_wizard(name: str = "spine") -> FlowDefinition:
    """Minimal interactive flow: submit → WAITING_FOR_INPUT → continue → SUCCEEDED."""
    return FlowDefinition(name=name, pattern="wizard", options={"steps": 1})


def complete_spine_job(host: Any, job_id: str, *, flow_name: str = "spine") -> Any:
    """Submit :func:`spine_wizard` and provide one input so the job SUCCEEDS.

    Works on collapsed hosts (inline scheduler). Callers that route to queued
    workers should wait for WAITING_FOR_INPUT before providing input.
    """
    job = host.submit_flow(spine_wizard(flow_name), job_id=job_id)
    if getattr(job.status, "value", None) == "WAITING_FOR_INPUT":
        host.provide_input(job_id, "ok")
        runtime = host.runtime()
        refreshed = runtime.orchestration.get_job(job_id)
        if refreshed is not None:
            return refreshed
    return job
