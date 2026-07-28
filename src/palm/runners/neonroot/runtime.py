"""NeonRoot WorkloadRuntime — hermetic isolation via NeonRoot CLI.

Sole NeonRoot integration path (provider removed 0.56). kind=run; warm later.
"""

from __future__ import annotations

from typing import Any

from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.protocol import (
    RuntimeCapabilities,
    RuntimePollOutcome,
    RuntimeStartOutcome,
    RuntimeStopOutcome,
    WorkloadRuntime,
)
from palm.core.workload.result import WorkloadResult
from palm.core.workload.spec import IsolationPolicy, WorkloadKind, WorkloadSpec
from palm.core.workload.status import WorkloadStatus


class NeonrootWorkloadRuntime(WorkloadRuntime):
    """Hermetic one-shot runs through ``neonroot spawn``."""

    def __init__(self, *, name: str = "neonroot") -> None:
        super().__init__(name=name)
        self._live: dict[str, dict[str, Any]] = {}

    def capabilities(self) -> RuntimeCapabilities:
        return RuntimeCapabilities(
            name=self.name,
            isolation_modes=frozenset(
                {
                    IsolationPolicy.HERMETIC,
                    IsolationPolicy.BEST_EFFORT,
                }
            ),
            kinds=frozenset({"run"}),
            description="NeonRoot CLI hermetic spawn (image + argv)",
            default_enabled=True,
        )

    def is_enabled(self) -> bool:
        # Soft: available when CLI present; start fails clearly if missing.
        return True

    def start(
        self,
        workload_id: str,
        spec: WorkloadSpec,
        *,
        owner: WorkloadOwner | None = None,
    ) -> RuntimeStartOutcome:
        if spec.kind is not WorkloadKind.RUN:
            msg = (
                f"neonroot runtime supports kind=run only (got kind={spec.kind}); "
                "warm workspace lands in a later 0.56 slice"
            )
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(msg, runtime=self.name),
                message=msg,
            )
        image = spec.image_or_ref
        if not image:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(
                    "neonroot run requires image or image_ref",
                    runtime=self.name,
                ),
            )
        if not spec.command:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail("empty command", runtime=self.name),
            )

        from palm.runners.neonroot.cli import probe_neonroot
        from palm.runners.neonroot.spawn import resolve_repo_root, run_spawn

        probe = probe_neonroot()
        if not probe.available:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(
                    probe.error or "neonroot CLI not available",
                    runtime=self.name,
                ),
                message=probe.error or "neonroot unavailable",
            )

        params = _spec_to_spawn_params(spec)
        try:
            payload = run_spawn(params, repo_root=resolve_repo_root())
        except (ValueError, RuntimeError) as exc:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(str(exc), runtime=self.name),
                message=str(exc),
            )
        except Exception as exc:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(
                    f"neonroot spawn failed: {exc}",
                    runtime=self.name,
                ),
                message=str(exc),
            )

        result = _payload_to_result(payload, runtime=self.name)
        if payload.get("timed_out") or payload.get("exit_code") is None:
            status = WorkloadStatus.FAILED
        elif int(payload.get("exit_code", 1)) != 0:
            status = WorkloadStatus.FAILED
        else:
            status = WorkloadStatus.STOPPED

        self._live[workload_id] = {
            "result": result,
            "status": status,
            "owner": owner,
            "payload": payload,
        }
        return RuntimeStartOutcome(
            status=status,
            result=result,
            runtime_meta={"neonroot": payload.get("neonroot"), "image": image},
        )

    def poll(self, workload_id: str) -> RuntimePollOutcome:
        entry = self._live.get(workload_id)
        if entry is None:
            return RuntimePollOutcome(
                status=WorkloadStatus.FAILED,
                message="unknown neonroot workload",
            )
        return RuntimePollOutcome(
            status=entry["status"],
            result=entry.get("result"),
        )

    def stop(self, workload_id: str) -> RuntimeStopOutcome:
        entry = self._live.pop(workload_id, None)
        if entry is None:
            return RuntimeStopOutcome(status=WorkloadStatus.STOPPED)
        return RuntimeStopOutcome(
            status=entry.get("status", WorkloadStatus.STOPPED),
            result=entry.get("result"),
        )


def _spec_to_spawn_params(spec: WorkloadSpec) -> dict[str, Any]:
    """Map WorkloadSpec fields onto neonroot spawn params."""
    seed = "git-archive"
    seed_mode = "copy"
    seed_exclude: list[str] = []
    if isinstance(spec.seed, dict):
        stype = str(spec.seed.get("type") or spec.seed.get("mode") or "").strip()
        if stype in ("none", "omit"):
            seed = "none"
        elif stype in ("uri", "path", "bind"):
            seed = str(spec.seed.get("path") or spec.seed.get("uri") or "none")
            if stype == "bind":
                seed_mode = "bind"
        elif stype == "git_archive" or stype == "git-archive":
            seed = "git-archive"
        if spec.seed.get("exclude"):
            seed_exclude = [str(x) for x in spec.seed["exclude"]]
        if spec.seed.get("seed_mode"):
            seed_mode = str(spec.seed["seed_mode"])
    elif spec.seed is None:
        seed = "git-archive"

    params: dict[str, Any] = {
        "image": spec.image_or_ref,
        "command": list(spec.command),
        "seed": seed,
        "seed_mode": seed_mode,
        "sandbox": True,
        "isolated": spec.isolation is IsolationPolicy.HERMETIC,
    }
    if seed_exclude:
        params["seed_exclude"] = seed_exclude
    if spec.timeout_s is not None:
        params["timeout"] = float(spec.timeout_s)
    if spec.workdir:
        params["cwd"] = spec.workdir
    # Pass-through labels as name hint when present
    if spec.labels.get("name"):
        params["name"] = spec.labels["name"]
    return params


def _payload_to_result(payload: dict[str, Any], *, runtime: str) -> WorkloadResult:
    exit_code = payload.get("exit_code")
    if exit_code is None:
        return WorkloadResult.fail(
            str(payload.get("error") or "spawn produced no exit code"),
            exit_code=1,
            stdout_tail=str(payload.get("stdout_tail") or ""),
            stderr_tail=str(payload.get("stderr_tail") or ""),
            runtime=runtime,
            duration_s=payload.get("duration_s"),
        )
    code = int(exit_code)
    if code != 0:
        return WorkloadResult(
            exit_code=code,
            stdout_tail=str(payload.get("stdout_tail") or ""),
            stderr_tail=str(payload.get("stderr_tail") or ""),
            duration_s=(
                float(payload["duration_s"])
                if payload.get("duration_s") is not None
                else None
            ),
            error=str(payload.get("error") or f"exit {code}"),
            runtime_meta={"runtime": runtime, "image": payload.get("image")},
        )
    return WorkloadResult.ok(
        exit_code=0,
        stdout_tail=str(payload.get("stdout_tail") or ""),
        stderr_tail=str(payload.get("stderr_tail") or ""),
        duration_s=(
            float(payload["duration_s"]) if payload.get("duration_s") is not None else None
        ),
        runtime=runtime,
        image=payload.get("image"),
    )


__all__ = ["NeonrootWorkloadRuntime"]
