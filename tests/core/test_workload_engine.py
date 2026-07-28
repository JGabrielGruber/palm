"""WorkloadEngine pure core tests — fake runtime, no outer Palm imports."""

from __future__ import annotations

import pytest

from palm.core.workload import (
    IsolationPolicy,
    LifecyclePolicy,
    WorkloadEngine,
    WorkloadKind,
    WorkloadNotFoundError,
    WorkloadOwner,
    WorkloadPlacement,
    WorkloadPlacementError,
    WorkloadPolicyError,
    WorkloadSpec,
    WorkloadSpecError,
    WorkloadStatus,
    WORKLOAD_EVENT_FAILED,
    WORKLOAD_EVENT_READY,
    WORKLOAD_EVENT_STARTED,
    WORKLOAD_EVENT_STOPPED,
)
from tests.core.fakes.workload_runtime import FakeWorkloadRuntime, HostLikeFakeRuntime


def _run_spec(**kwargs: object) -> WorkloadSpec:
    placement = kwargs.pop("placement", WorkloadPlacement(runtime="fake"))
    return WorkloadSpec(
        kind=WorkloadKind.RUN,
        isolation=IsolationPolicy.BEST_EFFORT,
        lifecycle=LifecyclePolicy.JOB,
        command=kwargs.pop("command", ("echo", "hi")),  # type: ignore[arg-type]
        placement=placement,  # type: ignore[arg-type]
        **kwargs,  # type: ignore[arg-type]
    )


def _workspace_spec(**kwargs: object) -> WorkloadSpec:
    placement = kwargs.pop("placement", WorkloadPlacement(runtime="fake"))
    return WorkloadSpec(
        kind=WorkloadKind.WORKSPACE,
        isolation=IsolationPolicy.BEST_EFFORT,
        lifecycle=LifecyclePolicy.SESSION,
        placement=placement,  # type: ignore[arg-type]
        **kwargs,  # type: ignore[arg-type]
    )


def _engine(runtime: FakeWorkloadRuntime | None = None) -> tuple[WorkloadEngine, FakeWorkloadRuntime]:
    rt = runtime or FakeWorkloadRuntime()
    events: list[tuple[str, dict]] = []
    engine = WorkloadEngine()
    engine.initialize(
        runtimes={rt.name: rt},
        default_runtime=rt.name,
        publish_event=lambda t, p: events.append((t, p)),
    )
    engine._test_events = events  # type: ignore[attr-defined]
    return engine, rt


def test_spec_rejects_shell_string_command() -> None:
    with pytest.raises(WorkloadSpecError, match="argv list"):
        WorkloadSpec.from_dict(
            {
                "kind": "run",
                "isolation": "hermetic",
                "lifecycle": "job",
                "command": "echo hi",
            }
        )


def test_spec_run_requires_command() -> None:
    with pytest.raises(WorkloadSpecError, match="command"):
        WorkloadSpec(
            kind=WorkloadKind.RUN,
            isolation=IsolationPolicy.HERMETIC,
            lifecycle=LifecyclePolicy.JOB,
        )


def test_spec_roundtrip() -> None:
    spec = _run_spec(
        image="palm-ci",
        labels={"role": "test"},
        env={"A": "1"},
    )
    again = WorkloadSpec.from_dict(spec.to_dict())
    assert again.kind is WorkloadKind.RUN
    assert again.command == ("echo", "hi")
    assert again.image == "palm-ci"
    assert again.labels["role"] == "test"


def test_spec_unknown_field_strict() -> None:
    with pytest.raises(WorkloadSpecError, match="Unknown"):
        WorkloadSpec.from_dict(
            {
                "kind": "run",
                "isolation": "host",
                "lifecycle": "job",
                "command": ["true"],
                "docker_compose": True,
            }
        )


def test_start_run_completes_synchronously() -> None:
    engine, rt = _engine()
    wl = engine.start(_run_spec(), owner=WorkloadOwner(job_id="j1"))
    assert wl.status is WorkloadStatus.STOPPED
    assert wl.result is not None and wl.result.success
    assert rt.starts == [wl.workload_id]
    types = [t for t, _ in engine._test_events]  # type: ignore[attr-defined]
    assert WORKLOAD_EVENT_STARTED in types
    assert WORKLOAD_EVENT_STOPPED in types
    engine.shutdown()


def test_start_run_failure() -> None:
    engine, _ = _engine()
    wl = engine.start(_run_spec(command=("cmd", "fail")))
    assert wl.status is WorkloadStatus.FAILED
    types = [t for t, _ in engine._test_events]  # type: ignore[attr-defined]
    assert WORKLOAD_EVENT_FAILED in types
    engine.shutdown()


def test_start_workspace_ready() -> None:
    engine, _ = _engine()
    wl = engine.start(_workspace_spec(), owner=WorkloadOwner(session_id="s1"))
    assert wl.status is WorkloadStatus.READY
    assert wl.handle is not None
    assert wl.handle.base_url.startswith("fake://")
    types = [t for t, _ in engine._test_events]  # type: ignore[attr-defined]
    assert WORKLOAD_EVENT_READY in types
    engine.shutdown()


def test_exec_on_ready_workspace() -> None:
    engine, rt = _engine()
    wl = engine.start(_workspace_spec())
    result = engine.exec(wl.workload_id, ["python", "-c", "print(1)"])
    assert result.success
    assert rt.execs[0][1] == ("python", "-c", "print(1)")
    still = engine.get(wl.workload_id)
    assert still.status is WorkloadStatus.READY
    engine.shutdown()


def test_exec_rejected_when_not_ready() -> None:
    engine, _ = _engine(FakeWorkloadRuntime(async_run=True))
    wl = engine.start(_run_spec())
    assert wl.status is WorkloadStatus.RUNNING
    with pytest.raises(Exception, match="READY"):
        engine.exec(wl.workload_id, ["true"])
    engine.shutdown()


def test_async_run_poll_to_stopped() -> None:
    rt = FakeWorkloadRuntime(async_run=True)
    engine, _ = _engine(rt)
    wl = engine.start(_run_spec())
    assert wl.status is WorkloadStatus.RUNNING
    rt.finish_run(wl.workload_id, exit_code=0)
    done = engine.status(wl.workload_id, refresh=True)
    assert done.status is WorkloadStatus.STOPPED
    assert done.result is not None and done.result.success
    engine.shutdown()


def test_stop_idempotent() -> None:
    engine, rt = _engine()
    wl = engine.start(_workspace_spec())
    a = engine.stop(wl.workload_id)
    b = engine.stop(wl.workload_id)
    assert a.status is WorkloadStatus.STOPPED
    assert b.status is WorkloadStatus.STOPPED
    assert rt.stops == [wl.workload_id]  # second stop short-circuits before runtime
    engine.shutdown()


def test_hermetic_rejects_host_runtime() -> None:
    host = HostLikeFakeRuntime()
    engine = WorkloadEngine()
    engine.initialize(runtimes={"host": host})
    spec = WorkloadSpec(
        kind=WorkloadKind.RUN,
        isolation=IsolationPolicy.HERMETIC,
        lifecycle=LifecyclePolicy.JOB,
        command=("true",),
        placement=WorkloadPlacement(runtime="host"),
    )
    with pytest.raises(WorkloadPolicyError, match="[Hh]ermetic|host"):
        engine.start(spec)
    engine.shutdown()


def test_runtime_isolation_mismatch() -> None:
    host = HostLikeFakeRuntime()
    engine = WorkloadEngine()
    engine.initialize(runtimes={"host": host})
    # even best_effort on host-only is ok; hermetic already tested.
    # Use a fake that only supports hermetic against host isolation request:
    hermetic_only = FakeWorkloadRuntime(
        name="nr",
        isolation_modes=frozenset({IsolationPolicy.HERMETIC}),
    )
    engine.register_runtime(hermetic_only)
    spec = WorkloadSpec(
        kind=WorkloadKind.RUN,
        isolation=IsolationPolicy.HOST,
        lifecycle=LifecyclePolicy.JOB,
        command=("true",),
        placement=WorkloadPlacement(runtime="nr"),
    )
    with pytest.raises(WorkloadPolicyError, match="isolation"):
        engine.start(spec)
    engine.shutdown()


def test_placement_requires_runtime() -> None:
    engine = WorkloadEngine()
    engine.initialize()
    with pytest.raises(WorkloadPlacementError, match="runtime"):
        engine.start(
            WorkloadSpec(
                kind=WorkloadKind.RUN,
                isolation=IsolationPolicy.BEST_EFFORT,
                lifecycle=LifecyclePolicy.JOB,
                command=("true",),
            )
        )
    engine.shutdown()


def test_idempotency_key_returns_same_workload() -> None:
    engine, _ = _engine()
    owner = WorkloadOwner(job_id="j-idem")
    a = engine.start(_run_spec(), owner=owner, idempotency_key="k1")
    b = engine.start(_run_spec(), owner=owner, idempotency_key="k1")
    assert a.workload_id == b.workload_id
    engine.shutdown()


def test_stop_owned_by_job() -> None:
    engine, rt = _engine()
    a = engine.start(_workspace_spec(), owner=WorkloadOwner(job_id="jA"))
    b = engine.start(_workspace_spec(), owner=WorkloadOwner(job_id="jB"))
    stopped = engine.stop_owned(job_id="jA")
    assert len(stopped) == 1
    assert stopped[0].workload_id == a.workload_id
    assert engine.get(a.workload_id).status is WorkloadStatus.STOPPED
    assert engine.get(b.workload_id).status is WorkloadStatus.READY
    assert a.workload_id in rt.stops
    engine.shutdown()


def test_list_filters() -> None:
    engine, _ = _engine()
    engine.start(_workspace_spec(), owner=WorkloadOwner(session_id="s1"))
    engine.start(_run_spec(), owner=WorkloadOwner(session_id="s2"))
    rows = engine.list(session_id="s1")
    assert len(rows) == 1
    assert rows[0].owner.session_id == "s1"
    engine.shutdown()


def test_get_unknown() -> None:
    engine, _ = _engine()
    with pytest.raises(WorkloadNotFoundError):
        engine.get("missing")
    engine.shutdown()


def test_events_payload_small() -> None:
    engine, _ = _engine()
    engine.start(_run_spec(), owner=WorkloadOwner(job_id="j1"))
    for _type, payload in engine._test_events:  # type: ignore[attr-defined]
        assert "workload_id" in payload
        assert "stdout" not in payload
        assert "stderr" not in payload
        assert "command" not in payload
    engine.shutdown()
