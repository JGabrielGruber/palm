"""Host WorkloadRuntime — local subprocess isolation (default OFF).

Unsupported as multi-tenant isolation. Dogfood / slim Compose only.
See ADR-024 D6 · VISION-0.56 §7.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
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

_DEFAULT_TAIL = 8000


class HostWorkloadRuntime(WorkloadRuntime):
    """Run argv on the Palm host process machine via subprocess."""

    def __init__(
        self,
        *,
        name: str = "host",
        enabled: bool = False,
        work_root: Path | str | None = None,
    ) -> None:
        super().__init__(name=name)
        self._enabled = bool(enabled)
        self._work_root = Path(work_root).resolve() if work_root else None
        self._live: dict[str, dict[str, Any]] = {}

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)

    def is_enabled(self) -> bool:
        return self._enabled

    def capabilities(self) -> RuntimeCapabilities:
        return RuntimeCapabilities(
            name=self.name,
            isolation_modes=frozenset({IsolationPolicy.HOST, IsolationPolicy.BEST_EFFORT}),
            kinds=frozenset({"run"}),
            description="Local subprocess (default OFF; not multi-tenant safe)",
            default_enabled=False,
        )

    def start(
        self,
        workload_id: str,
        spec: WorkloadSpec,
        *,
        owner: WorkloadOwner | None = None,
    ) -> RuntimeStartOutcome:
        if not self._enabled:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(
                    "host runtime is disabled "
                    "(set PALM_WORKLOAD_HOST_ENABLED=1 / workload_host_enabled)",
                    runtime=self.name,
                ),
                message="host runtime disabled",
            )
        if spec.kind is not WorkloadKind.RUN:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(
                    f"host runtime supports kind=run only (got {spec.kind})",
                    runtime=self.name,
                ),
                message="unsupported kind",
            )
        if not spec.command:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail("empty command", runtime=self.name),
            )

        workdir = self._resolve_workdir(spec)
        env = os.environ.copy()
        env.update(spec.env)
        timeout = float(spec.timeout_s) if spec.timeout_s is not None else 3600.0
        argv = list(spec.command)
        started = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                cwd=str(workdir) if workdir is not None else None,
                env=env,
            )
        except subprocess.TimeoutExpired as exc:
            duration = time.monotonic() - started
            stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
            stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
            result = WorkloadResult(
                exit_code=124,
                stdout_tail=_tail(stdout),
                stderr_tail=_tail(stderr or f"timeout after {timeout}s"),
                duration_s=round(duration, 3),
                error=f"host run timed out after {timeout}s",
                runtime_meta={"runtime": self.name, "argv": argv},
            )
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=result,
                message=result.error,
            )
        except OSError as exc:
            return RuntimeStartOutcome(
                status=WorkloadStatus.FAILED,
                result=WorkloadResult.fail(str(exc), runtime=self.name),
                message=str(exc),
            )

        duration = time.monotonic() - started
        result = WorkloadResult(
            exit_code=int(proc.returncode),
            stdout_tail=_tail(proc.stdout or ""),
            stderr_tail=_tail(proc.stderr or ""),
            duration_s=round(duration, 3),
            error=None if proc.returncode == 0 else f"exit {proc.returncode}",
            runtime_meta={
                "runtime": self.name,
                "argv": argv,
                "cwd": str(workdir) if workdir else None,
            },
        )
        status = (
            WorkloadStatus.STOPPED if result.success else WorkloadStatus.FAILED
        )
        self._live[workload_id] = {
            "result": result,
            "status": status,
            "owner": owner,
        }
        return RuntimeStartOutcome(status=status, result=result)

    def poll(self, workload_id: str) -> RuntimePollOutcome:
        entry = self._live.get(workload_id)
        if entry is None:
            return RuntimePollOutcome(
                status=WorkloadStatus.FAILED,
                message="unknown host workload",
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

    def _resolve_workdir(self, spec: WorkloadSpec) -> Path | None:
        if spec.workdir:
            path = Path(spec.workdir)
            if not path.is_absolute() and self._work_root is not None:
                path = self._work_root / path
            return path.resolve()
        if self._work_root is not None:
            return self._work_root
        return None


def _tail(text: str, limit: int = _DEFAULT_TAIL) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


__all__ = ["HostWorkloadRuntime"]
