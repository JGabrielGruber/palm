"""Fake WorkloadRuntime for pure core tests (no host/neonroot)."""

from __future__ import annotations

from typing import Any

from palm.core.workload.handle import WorkloadHandle
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


class FakeWorkloadRuntime(WorkloadRuntime):
    """
    Controllable in-memory runtime.

    * kind=run with command ending in ``fail`` → FAILED
    * kind=run otherwise → completes synchronously as STOPPED exit 0
    * kind=workspace/service → READY with a handle
    * ``async_run=True`` → start returns RUNNING; complete via ``finish_run``
    """

    __test__ = False

    def __init__(
        self,
        *,
        name: str = "fake",
        isolation_modes: frozenset[IsolationPolicy] | None = None,
        async_run: bool = False,
        default_enabled: bool = True,
    ) -> None:
        super().__init__(name=name)
        self._isolation_modes = isolation_modes or frozenset(
            {
                IsolationPolicy.HOST,
                IsolationPolicy.HERMETIC,
                IsolationPolicy.BEST_EFFORT,
            }
        )
        self.async_run = async_run
        self.default_enabled = default_enabled
        self._live: dict[str, dict[str, Any]] = {}
        self.starts: list[str] = []
        self.stops: list[str] = []
        self.execs: list[tuple[str, tuple[str, ...]]] = []

    def capabilities(self) -> RuntimeCapabilities:
        return RuntimeCapabilities(
            name=self.name,
            isolation_modes=self._isolation_modes,
            kinds=frozenset({"run", "service", "workspace"}),
            description="test fake runtime",
            default_enabled=self.default_enabled,
        )

    def start(
        self,
        workload_id: str,
        spec: WorkloadSpec,
        *,
        owner: WorkloadOwner | None = None,
    ) -> RuntimeStartOutcome:
        self.starts.append(workload_id)
        self._live[workload_id] = {"spec": spec, "owner": owner}

        if spec.kind is WorkloadKind.RUN:
            if self.async_run:
                return RuntimeStartOutcome(status=WorkloadStatus.RUNNING)
            if spec.command and spec.command[-1] == "fail":
                result = WorkloadResult.fail("fake command failed", exit_code=1)
                return RuntimeStartOutcome(
                    status=WorkloadStatus.FAILED,
                    result=result,
                    message="fake command failed",
                )
            result = WorkloadResult.ok(
                exit_code=0,
                stdout_tail="ok",
                duration_s=0.01,
            )
            return RuntimeStartOutcome(status=WorkloadStatus.STOPPED, result=result)

        handle = WorkloadHandle(
            workload_id=workload_id,
            base_url=f"fake://{workload_id}",
            connection_hints={"runtime": self.name},
        )
        return RuntimeStartOutcome(status=WorkloadStatus.READY, handle=handle)

    def poll(self, workload_id: str) -> RuntimePollOutcome:
        entry = self._live.get(workload_id)
        if entry is None:
            return RuntimePollOutcome(
                status=WorkloadStatus.FAILED,
                message="unknown workload",
            )
        if "terminal" in entry:
            return entry["terminal"]
        if entry["spec"].kind is WorkloadKind.RUN and self.async_run:
            return RuntimePollOutcome(status=WorkloadStatus.RUNNING)
        if entry["spec"].kind in (WorkloadKind.WORKSPACE, WorkloadKind.SERVICE):
            return RuntimePollOutcome(
                status=WorkloadStatus.READY,
                handle=WorkloadHandle(
                    workload_id=workload_id,
                    base_url=f"fake://{workload_id}",
                ),
            )
        return RuntimePollOutcome(status=WorkloadStatus.RUNNING)

    def finish_run(
        self,
        workload_id: str,
        *,
        exit_code: int = 0,
        error: str | None = None,
    ) -> None:
        """Mark an async run terminal for the next poll/status(refresh=True)."""
        if error or exit_code != 0:
            result = WorkloadResult.fail(error or "failed", exit_code=exit_code)
            outcome = RuntimePollOutcome(
                status=WorkloadStatus.FAILED,
                result=result,
                message=error or "failed",
            )
        else:
            result = WorkloadResult.ok(exit_code=0, stdout_tail="done")
            outcome = RuntimePollOutcome(
                status=WorkloadStatus.STOPPED,
                result=result,
            )
        self._live.setdefault(workload_id, {})["terminal"] = outcome

    def stop(self, workload_id: str) -> RuntimeStopOutcome:
        self.stops.append(workload_id)
        entry = self._live.pop(workload_id, None)
        if entry and "terminal" in entry:
            term: RuntimePollOutcome = entry["terminal"]
            return RuntimeStopOutcome(
                status=term.status,
                result=term.result,
                message=term.message,
            )
        return RuntimeStopOutcome(status=WorkloadStatus.STOPPED)

    def exec(
        self,
        workload_id: str,
        command: list[str] | tuple[str, ...],
        *,
        timeout_s: float | None = None,
        env: dict[str, str] | None = None,
    ) -> WorkloadResult:
        cmd = tuple(str(c) for c in command)
        self.execs.append((workload_id, cmd))
        if cmd and cmd[-1] == "fail":
            return WorkloadResult.fail("exec failed", exit_code=2)
        return WorkloadResult.ok(exit_code=0, stdout_tail=" ".join(cmd))


class HostLikeFakeRuntime(FakeWorkloadRuntime):
    """Fake that only supports host isolation (for hermetic policy tests)."""

    def __init__(self, *, name: str = "host") -> None:
        super().__init__(
            name=name,
            isolation_modes=frozenset({IsolationPolicy.HOST}),
            default_enabled=False,
        )
