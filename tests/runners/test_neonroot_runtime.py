"""Neonroot WorkloadRuntime — Spec→spawn mapping (CLI optional)."""

from __future__ import annotations

from unittest.mock import patch

from palm.core.workload import (
    IsolationPolicy,
    LifecyclePolicy,
    WorkloadEngine,
    WorkloadKind,
    WorkloadPlacement,
    WorkloadSpec,
    WorkloadStatus,
)
from palm.providers.neonroot.cli import NeonrootProbe
from palm.runners.neonroot.runtime import NeonrootWorkloadRuntime, _spec_to_spawn_params


def _hermetic_run(*, image: str = "palm-ci") -> WorkloadSpec:
    return WorkloadSpec(
        kind=WorkloadKind.RUN,
        isolation=IsolationPolicy.HERMETIC,
        lifecycle=LifecyclePolicy.JOB,
        image=image,
        command=("true",),
        placement=WorkloadPlacement(runtime="neonroot"),
        seed={"type": "none"},
    )


def test_spec_to_spawn_params_seed_none() -> None:
    spec = _hermetic_run()
    params = _spec_to_spawn_params(spec)
    assert params["image"] == "palm-ci"
    assert params["command"] == ["true"]
    assert params["seed"] == "none"
    assert params["isolated"] is True


def test_neonroot_missing_cli_fails_closed() -> None:
    rt = NeonrootWorkloadRuntime()
    engine = WorkloadEngine()
    engine.initialize(runtimes={"neonroot": rt})
    missing = NeonrootProbe(available=False, error="neonroot not found on PATH")
    with patch("palm.providers.neonroot.cli.probe_neonroot", return_value=missing):
        # runtime imports probe inside start via providers path
        with patch(
            "palm.runners.neonroot.runtime.probe_neonroot",
            return_value=missing,
            create=True,
        ):
            # Patch where runtime imports from
            with patch(
                "palm.providers.neonroot.cli.probe_neonroot",
                return_value=missing,
            ):
                wl = engine.start(_hermetic_run())
    assert wl.status is WorkloadStatus.FAILED
    assert wl.result is not None
    assert "neonroot" in (wl.result.error or "").lower() or "not" in (wl.result.error or "").lower()
    engine.shutdown()


def test_neonroot_spawn_success_mapped() -> None:
    rt = NeonrootWorkloadRuntime()
    engine = WorkloadEngine()
    engine.initialize(runtimes={"neonroot": rt})
    present = NeonrootProbe(available=True, path="/bin/neonroot", version="0.2")
    payload = {
        "exit_code": 0,
        "stdout_tail": "ok",
        "stderr_tail": "",
        "duration_s": 0.1,
        "image": "palm-ci",
        "neonroot": present.as_dict(),
    }
    with (
        patch("palm.providers.neonroot.cli.probe_neonroot", return_value=present),
        patch("palm.providers.neonroot.spawn.run_spawn", return_value=payload),
        patch("palm.providers.neonroot.spawn.resolve_repo_root", return_value=None),
    ):
        wl = engine.start(_hermetic_run())
    assert wl.status is WorkloadStatus.STOPPED
    assert wl.result is not None and wl.result.success
    engine.shutdown()


def test_neonroot_rejects_workspace_kind() -> None:
    rt = NeonrootWorkloadRuntime()
    engine = WorkloadEngine()
    engine.initialize(runtimes={"neonroot": rt})
    wl = engine.start(
        WorkloadSpec(
            kind=WorkloadKind.WORKSPACE,
            isolation=IsolationPolicy.HERMETIC,
            lifecycle=LifecyclePolicy.SESSION,
            image="palm-ci",
            placement=WorkloadPlacement(runtime="neonroot"),
        )
    )
    assert wl.status is WorkloadStatus.FAILED
    text = f"{wl.message or ''} {(wl.result.error if wl.result else '')}".lower()
    assert "workspace" in text or "kind=run" in text
    engine.shutdown()


def test_registry_registers_neonroot_and_host() -> None:
    import palm.runners  # noqa: F401
    from palm.core.workload.registry import workload_runtime_registry

    names = set(workload_runtime_registry.names())
    assert "host" in names
    assert "neonroot" in names
