"""Optional neonroot provider → WorkloadEngine bridge (0.56.4b).

When an in-process runtime is bound and its WorkloadEngine is live, hermetic
``spawn`` params are mapped to a WorkloadSpec and allocated via the neonroot
WorkloadRuntime — one isolation truth. Falls back to None so the classic
provider path can run (CLI-only / no host).
"""

from __future__ import annotations

from typing import Any

from palm.core.resource.result import ProviderResult
from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.spec import (
    IsolationPolicy,
    LifecyclePolicy,
    WorkloadKind,
    WorkloadPlacement,
    WorkloadSpec,
)
from palm.core.workload.status import WorkloadStatus


def try_spawn_via_workload(
    params: dict[str, Any],
    *,
    owner: WorkloadOwner | None = None,
) -> ProviderResult | None:
    """
    Run spawn through WorkloadEngine when possible.

    Returns ``None`` when the façade cannot apply (caller uses legacy spawn).
    """
    from palm.common.providers._registry import get_bound_runtime

    runtime = get_bound_runtime()
    if runtime is None:
        return None
    engine = getattr(runtime, "workload", None)
    if engine is None or not getattr(engine, "is_initialized", False):
        return None

    try:
        spec = spawn_params_to_spec(params)
    except (ValueError, TypeError) as exc:
        return ProviderResult.fail(str(exc), action="spawn", provider="neonroot")

    try:
        wl = engine.start(spec, owner=owner or WorkloadOwner(created_by_palm=True))
    except Exception as exc:
        return ProviderResult.fail(
            str(exc),
            action="spawn",
            provider="neonroot",
            via="workload_engine",
        )

    payload = _workload_payload(wl)
    if wl.status is WorkloadStatus.STOPPED and (wl.result is None or wl.result.success):
        return ProviderResult.ok(
            payload,
            action="spawn",
            provider="neonroot",
            via="workload_engine",
        )
    err = (
        (wl.result.error if wl.result else None)
        or wl.message
        or f"workload status={wl.status}"
    )
    return ProviderResult.fail(
        str(err),
        action="spawn",
        provider="neonroot",
        via="workload_engine",
        **{k: v for k, v in payload.items() if k != "error" and v is not None},
    )


def spawn_params_to_spec(params: dict[str, Any]) -> WorkloadSpec:
    """Map neonroot spawn invoke params onto a portable WorkloadSpec."""
    image = params.get("image")
    if not image or not str(image).strip():
        raise ValueError("spawn requires params.image")
    command = params.get("command")
    if isinstance(command, str):
        raise ValueError("command must be an argv list, not a shell string")
    if not isinstance(command, list | tuple) or not command:
        raise ValueError("spawn requires params.command (non-empty argv list)")
    cmd = tuple(str(c) for c in command)

    isolated = bool(params.get("isolated", False))
    isolation = IsolationPolicy.HERMETIC if isolated else IsolationPolicy.BEST_EFFORT

    seed_raw = params.get("seed", "git-archive")
    seed: dict[str, Any] | None
    if seed_raw in (None, "", "none", "false", "no"):
        seed = {"type": "none"}
    elif seed_raw == "git-archive":
        seed = {"type": "git_archive"}
    else:
        seed_mode = str(params.get("seed_mode") or "copy").strip().lower()
        seed = {
            "type": "bind" if seed_mode == "bind" else "path",
            "path": str(seed_raw),
        }
        if params.get("seed_exclude") or params.get("seed_excludes"):
            excl = params.get("seed_exclude") or params.get("seed_excludes")
            if isinstance(excl, list | tuple):
                seed["exclude"] = [str(x) for x in excl]

    timeout = params.get("timeout")
    timeout_s = float(timeout) if timeout is not None else None

    return WorkloadSpec(
        kind=WorkloadKind.RUN,
        isolation=isolation,
        lifecycle=LifecyclePolicy.JOB,
        image=str(image).strip(),
        command=cmd,
        seed=seed,
        timeout_s=timeout_s,
        placement=WorkloadPlacement(runtime="neonroot"),
        labels={"via": "neonroot_provider_facade"},
    )


def _workload_payload(wl: Any) -> dict[str, Any]:
    result = wl.result
    data: dict[str, Any] = {
        "workload_id": wl.workload_id,
        "status": str(wl.status),
        "runtime": wl.runtime,
        "via": "workload_engine",
    }
    if result is not None:
        data["exit_code"] = result.exit_code
        data["stdout_tail"] = result.stdout_tail
        data["stderr_tail"] = result.stderr_tail
        data["duration_s"] = result.duration_s
        if result.error:
            data["error"] = result.error
        data["runtime_meta"] = dict(result.runtime_meta)
    return data


__all__ = ["spawn_params_to_spec", "try_spawn_via_workload"]
