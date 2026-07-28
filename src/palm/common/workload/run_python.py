"""Build a WorkloadSpec for simple run-python dogfood (host | neonroot | auto).

Keeps the product language one Spec — only placement/isolation change per runner.
"""

from __future__ import annotations

import sys
from typing import Any

from palm.core.workload.spec import (
    IsolationPolicy,
    LifecyclePolicy,
    WorkloadKind,
    WorkloadPlacement,
    WorkloadSpec,
)


def resolve_runtime_choice(choice: str | None) -> str:
    """Normalize host | neonroot | auto → concrete runtime name."""
    text = str(choice or "auto").strip().lower()
    if text in ("host", "local"):
        return "host"
    if text in ("neonroot", "nr", "hermetic"):
        return "neonroot"
    if text in ("auto", "default", ""):
        return _auto_runtime()
    return text


def _auto_runtime() -> str:
    """Prefer neonroot when CLI present; otherwise host (caller must enable host)."""
    try:
        from palm.providers.neonroot.cli import probe_neonroot

        if probe_neonroot().available:
            return "neonroot"
    except Exception:
        pass
    return "host"


def build_run_python_spec(
    *,
    code: str,
    runtime: str | None = None,
    image: str = "palm-ci",
    python: str | None = None,
    timeout_s: float = 120.0,
) -> WorkloadSpec:
    """One-shot ``python -c <code>`` Spec for host or neonroot."""
    source = str(code or "")
    if not source.strip():
        raise ValueError("run-python requires non-empty code")

    runtime_name = resolve_runtime_choice(runtime)
    if runtime_name == "host":
        exe = python or sys.executable or "python3"
        return WorkloadSpec(
            kind=WorkloadKind.RUN,
            isolation=IsolationPolicy.BEST_EFFORT,
            lifecycle=LifecyclePolicy.JOB,
            command=(exe, "-c", source),
            timeout_s=timeout_s,
            placement=WorkloadPlacement(runtime="host"),
            labels={"dogfood": "run-python"},
        )

    # neonroot (and unknown hermetic-capable runtimes)
    exe = python or "python3"
    return WorkloadSpec(
        kind=WorkloadKind.RUN,
        isolation=IsolationPolicy.HERMETIC,
        lifecycle=LifecyclePolicy.JOB,
        image=str(image or "palm-ci"),
        command=(exe, "-c", source),
        seed={"type": "none"},
        timeout_s=timeout_s,
        placement=WorkloadPlacement(runtime=runtime_name),
        labels={"dogfood": "run-python"},
    )


def spec_from_bound_params(params: dict[str, Any]) -> WorkloadSpec:
    """
    Build Spec from wizard/step params after state binding.

    * Full Spec fields (``kind`` present) → ``WorkloadSpec.from_dict``
    * Sugar: ``code`` + optional ``runtime`` / ``image`` / ``python`` → run-python
    """
    if not params:
        raise ValueError("workload step requires params (Spec or run-python sugar)")

    if params.get("kind"):
        return WorkloadSpec.from_dict(params)

    if "code" in params:
        return build_run_python_spec(
            code=str(params.get("code") or ""),
            runtime=str(params.get("runtime") or params.get("placement", {}).get("runtime") or "auto")
            if not isinstance(params.get("placement"), dict)
            else str(
                params.get("runtime")
                or (params.get("placement") or {}).get("runtime")
                or "auto"
            ),
            image=str(params.get("image") or "palm-ci"),
            python=str(params["python"]) if params.get("python") else None,
            timeout_s=float(params.get("timeout_s") or params.get("timeout") or 120),
        )

    raise ValueError(
        "workload params must be a WorkloadSpec mapping (kind=…) "
        "or run-python sugar (code=…, runtime=host|neonroot|auto)"
    )


__all__ = [
    "build_run_python_spec",
    "resolve_runtime_choice",
    "spec_from_bound_params",
]
