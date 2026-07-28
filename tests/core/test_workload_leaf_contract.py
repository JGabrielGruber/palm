"""Contract tests: WorkloadLeaf + fake runtime + real WorkloadEngine."""

from __future__ import annotations

import pytest

from palm.core.behavior_tree import PatternStatus, WorkloadLeaf
from palm.core.workload import (
    IsolationPolicy,
    LifecyclePolicy,
    WorkloadEngine,
    WorkloadKind,
    WorkloadOwner,
    WorkloadPlacement,
    WorkloadSpec,
    WorkloadStatus,
)
from tests.core.fakes.state import TestState
from tests.core.fakes.workload_runtime import FakeWorkloadRuntime


def _engine_with(rt: FakeWorkloadRuntime) -> WorkloadEngine:
    engine = WorkloadEngine()
    engine.initialize(runtimes={rt.name: rt}, default_runtime=rt.name)
    return engine


def test_leaf_sync_run_success() -> None:
    rt = FakeWorkloadRuntime()
    engine = _engine_with(rt)
    leaf = WorkloadLeaf(
        "step-run",
        workload_engine=engine,
        spec=WorkloadSpec(
            kind=WorkloadKind.RUN,
            isolation=IsolationPolicy.BEST_EFFORT,
            lifecycle=LifecyclePolicy.JOB,
            command=("echo", "ok"),
            placement=WorkloadPlacement(runtime="fake"),
        ),
        owner=WorkloadOwner(job_id="job-1"),
        output_key="wl_out",
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.SUCCESS
    out = state.get("wl_out")
    assert out["status"] == "STOPPED"
    assert out["result"]["exit_code"] == 0
    trace = state.get(leaf.trace_key)
    assert trace["success"] is True
    engine.shutdown()


def test_leaf_sync_run_failure() -> None:
    rt = FakeWorkloadRuntime()
    engine = _engine_with(rt)
    leaf = WorkloadLeaf(
        "step-fail",
        workload_engine=engine,
        spec={
            "kind": "run",
            "isolation": "best_effort",
            "lifecycle": "job",
            "command": ["cmd", "fail"],
            "placement": {"runtime": "fake"},
        },
        error_key="wl_err",
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.FAILURE
    assert state.get("wl_err")
    engine.shutdown()


def test_leaf_async_run_polls_until_terminal() -> None:
    rt = FakeWorkloadRuntime(async_run=True)
    engine = _engine_with(rt)
    leaf = WorkloadLeaf(
        "async-run",
        workload_engine=engine,
        spec=WorkloadSpec(
            kind=WorkloadKind.RUN,
            isolation=IsolationPolicy.BEST_EFFORT,
            lifecycle=LifecyclePolicy.JOB,
            command=("sleep", "1"),
            placement=WorkloadPlacement(runtime="fake"),
        ),
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.RUNNING
    wid = state.get(f"{WorkloadLeaf.TRACE_KEY_PREFIX}:async-run:id")
    assert wid
    rt.finish_run(str(wid), exit_code=0)
    assert leaf.tick(state) == PatternStatus.SUCCESS
    engine.shutdown()


def test_leaf_workspace_ready_success() -> None:
    rt = FakeWorkloadRuntime()
    engine = _engine_with(rt)
    leaf = WorkloadLeaf(
        "box",
        workload_engine=engine,
        spec=WorkloadSpec(
            kind=WorkloadKind.WORKSPACE,
            isolation=IsolationPolicy.BEST_EFFORT,
            lifecycle=LifecyclePolicy.SESSION,
            placement=WorkloadPlacement(runtime="fake"),
        ),
        owner=WorkloadOwner(session_id="sess-1"),
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.SUCCESS
    out = state.get("box")
    assert out["status"] == "READY"
    assert out["handle"]["base_url"].startswith("fake://")
    engine.shutdown()


def test_leaf_workspace_stop_when_done() -> None:
    rt = FakeWorkloadRuntime()
    engine = _engine_with(rt)
    leaf = WorkloadLeaf(
        "box-stop",
        workload_engine=engine,
        spec=WorkloadSpec(
            kind=WorkloadKind.WORKSPACE,
            isolation=IsolationPolicy.BEST_EFFORT,
            lifecycle=LifecyclePolicy.SESSION,
            placement=WorkloadPlacement(runtime="fake"),
        ),
        stop_when_done=True,
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.SUCCESS
    out = state.get("box-stop")
    assert out["status"] == "STOPPED"
    assert rt.stops
    engine.shutdown()


def test_leaf_requires_spec() -> None:
    with pytest.raises(ValueError, match="WorkloadSpec"):
        WorkloadLeaf("orphan")


def test_leaf_requires_engine() -> None:
    leaf = WorkloadLeaf(
        "no-engine",
        spec=WorkloadSpec(
            kind=WorkloadKind.RUN,
            isolation=IsolationPolicy.BEST_EFFORT,
            lifecycle=LifecyclePolicy.JOB,
            command=("true",),
            placement=WorkloadPlacement(runtime="fake"),
        ),
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.FAILURE


def test_leaf_policy_denied_surfaces_failure() -> None:
    """Hermetic + host-named runtime → leaf FAILURE (engine policy)."""
    from tests.core.fakes.workload_runtime import HostLikeFakeRuntime

    host = HostLikeFakeRuntime()
    engine = WorkloadEngine()
    engine.initialize(runtimes={"host": host})
    leaf = WorkloadLeaf(
        "hermetic-host",
        workload_engine=engine,
        spec=WorkloadSpec(
            kind=WorkloadKind.RUN,
            isolation=IsolationPolicy.HERMETIC,
            lifecycle=LifecyclePolicy.JOB,
            command=("true",),
            placement=WorkloadPlacement(runtime="host"),
        ),
        error_key="err",
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.FAILURE
    assert "host" in state.get("err").lower() or "Hermetic" in state.get("err")
    engine.shutdown()


def test_owner_cancel_stop_owned_while_leaf_running() -> None:
    """Cancel path: engine.stop_owned stops what a leaf started."""
    rt = FakeWorkloadRuntime(async_run=True)
    engine = _engine_with(rt)
    leaf = WorkloadLeaf(
        "long",
        workload_engine=engine,
        spec=WorkloadSpec(
            kind=WorkloadKind.RUN,
            isolation=IsolationPolicy.BEST_EFFORT,
            lifecycle=LifecyclePolicy.JOB,
            command=("sleep", "99"),
            placement=WorkloadPlacement(runtime="fake"),
        ),
        owner=WorkloadOwner(job_id="cancel-me"),
    )
    state = TestState()
    assert leaf.tick(state) == PatternStatus.RUNNING
    stopped = engine.stop_owned(job_id="cancel-me")
    assert len(stopped) == 1
    assert stopped[0].status is WorkloadStatus.STOPPED
    # Leaf re-tick sees terminal stopped without result → success path (exit None)
    status = leaf.tick(state)
    assert status in (PatternStatus.SUCCESS, PatternStatus.FAILURE)
    engine.shutdown()
