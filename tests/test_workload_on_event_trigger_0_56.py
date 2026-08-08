"""0.56.9 — on_workload triggers: workload.stopped → WorkIntent → drain."""

from __future__ import annotations

from examples.definitions.workload_followup import WORKLOAD_FOLLOWUP_FLOW
from palm.common.triggers import parse_triggers
from palm.common.triggers.registry import TriggerRegistry
from palm.core.event import EventEngine
from palm.core.storage import StorageEngine
from palm.system.subsystems.planes.work.plane import WorkPlaneService


def test_parse_on_workload_trigger() -> None:
    specs = parse_triggers(WORKLOAD_FOLLOWUP_FLOW.options)
    assert len(specs) == 1
    spec = specs[0]
    assert spec.kind == "on_workload"
    assert spec.work_flow_id == "workload-followup"
    assert spec.workload_when == "stopped"
    assert spec.workload_labels.get("dogfood") == "run-python"


def test_trigger_registry_matches_workload_stopped() -> None:
    reg = TriggerRegistry()
    reg.reload_from_flow_rows(
        [
            {
                "name": "workload-followup",
                "metadata": WORKLOAD_FOLLOWUP_FLOW.options,
            }
        ]
    )
    intents = reg.on_event(
        "workload.stopped",
        {
            "workload_id": "w1",
            "status": "STOPPED",
            "runtime": "host",
            "exit_code": 0,
            "labels": {"dogfood": "run-python"},
        },
    )
    assert len(intents) == 1
    assert intents[0].target == "workload-followup"
    assert intents[0].payload.get("trigger") == "on_workload"


def test_trigger_registry_label_filter() -> None:
    reg = TriggerRegistry()
    reg.reload_from_flow_rows(
        [
            {
                "name": "workload-followup",
                "metadata": WORKLOAD_FOLLOWUP_FLOW.options,
            }
        ]
    )
    intents = reg.on_event(
        "workload.stopped",
        {
            "workload_id": "w2",
            "labels": {"dogfood": "other"},
        },
    )
    assert intents == []


def test_work_drain_enqueues_on_workload_stopped() -> None:
    storage = StorageEngine()
    storage.initialize()
    storage.select("memory")
    submitted: list[str] = []
    engine = EventEngine()
    engine.initialize()
    drain = WorkPlaneService()
    drain.attach(
        storage=storage,
        submit_flow=lambda f, _p: submitted.append(f),
        able=lambda: True,  # unit drain; host path wires admission (0.63.23)
        event=engine,
        attach_events=True,
    )
    drain.reload_triggers(
        [
            {
                "name": "workload-followup",
                "metadata": WORKLOAD_FOLLOWUP_FLOW.options,
            }
        ]
    )
    engine.emit(
        "workload.stopped",
        workload_id="w-dog",
        status="STOPPED",
        runtime="host",
        exit_code=0,
        labels={"dogfood": "run-python"},
    )
    assert drain.store.pending_count() == 1
    n = drain.tick()
    assert n == 1
    assert submitted == ["workload-followup"]
    engine.shutdown()


def test_hermetic_workload_spec_shape() -> None:
    from palm.core.workload import (
        IsolationPolicy,
        LifecyclePolicy,
        WorkloadKind,
        WorkloadPlacement,
        WorkloadSpec,
    )

    spec = WorkloadSpec(
        kind=WorkloadKind.RUN,
        isolation=IsolationPolicy.HERMETIC,
        lifecycle=LifecyclePolicy.JOB,
        image="palm-ci",
        command=("true",),
        seed={"type": "none"},
        placement=WorkloadPlacement(runtime="neonroot"),
        timeout_s=30,
    )
    assert spec.placement.runtime == "neonroot"
    assert spec.isolation is IsolationPolicy.HERMETIC
