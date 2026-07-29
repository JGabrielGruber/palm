"""WorkloadLeaf — BT contract with WorkloadDriver (start / poll / stop).

Freezes how graphs wait, fail, and complete before patterns invent divergent
shapes. Concrete WorkloadEngine and system ExecutionPort adapters both satisfy
WorkloadDriver (0.57.4 P2). Tests may bind the pure engine + fake runtime.

See docs/VISION-0.56.md §11 and ADR-024 D8b.
"""

from __future__ import annotations

from typing import Any

from palm.core.behavior_tree.base_pattern import PatternStatus
from palm.core.behavior_tree.leaf import LeafNode
from palm.core.context import BaseState
from palm.core.workload.driver import WorkloadDriver
from palm.core.workload.exceptions import WorkloadError
from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.spec import WorkloadSpec
from palm.core.workload.status import WorkloadStatus, is_terminal


class WorkloadLeaf(LeafNode):
    """
    Start a workload from a Spec and yield until terminal (or READY if wait_ready).

    Tick model
    ----------
    * First tick: ``driver.start(spec)``.
    * If status is terminal SUCCESS (STOPPED + exit 0): ``SUCCESS``.
    * If FAILED or STOPPED with non-zero exit: ``FAILURE``.
    * If RUNNING / STARTING / READY (when waiting for stop): ``RUNNING`` and
      re-poll on subsequent ticks (no infinite spin — job runner budgets ticks).
    * Optional ``stop_on_success`` / cancel: call ``driver.stop``.

    State keys
    ----------
    * ``output_key`` — final Workload.to_dict() (or result payload)
    * ``trace_key`` — audit dict
    * ``error_key`` — human message on failure
    * internal ``__bt_workload__:<name>:id`` — workload_id across ticks
    """

    TRACE_KEY_PREFIX = "__bt_workload__"
    ID_KEY_SUFFIX = ":id"

    def __init__(
        self,
        name: str,
        *,
        workload_engine: WorkloadDriver | None = None,
        spec: WorkloadSpec | dict[str, Any] | None = None,
        owner: WorkloadOwner | dict[str, Any] | None = None,
        output_key: str | None = None,
        error_key: str | None = None,
        trace_key: str | None = None,
        wait_ready: bool = False,
        stop_when_done: bool = False,
        idempotency_key: str | None = None,
    ) -> None:
        super().__init__(name)
        if spec is None:
            raise ValueError(f"WorkloadLeaf {name!r} requires a WorkloadSpec")
        self._workload_engine = workload_engine
        self._spec = spec if isinstance(spec, WorkloadSpec) else WorkloadSpec.from_dict(spec)
        if owner is None:
            self._owner = WorkloadOwner()
        elif isinstance(owner, WorkloadOwner):
            self._owner = owner
        else:
            self._owner = WorkloadOwner.from_dict(owner)
        self._output_key = output_key or name
        self._error_key = error_key
        self._trace_key = (
            trace_key if trace_key is not None else self.default_trace_key(name)
        )
        self._wait_ready = wait_ready
        self._stop_when_done = stop_when_done
        self._idempotency_key = idempotency_key
        self._id_key = f"{self.TRACE_KEY_PREFIX}:{name}{self.ID_KEY_SUFFIX}"

    @staticmethod
    def default_trace_key(name: str) -> str:
        return f"{WorkloadLeaf.TRACE_KEY_PREFIX}:{name}"

    @property
    def output_key(self) -> str:
        return self._output_key

    @property
    def trace_key(self) -> str:
        return self._trace_key

    def _tick_impl(self, state: BaseState) -> PatternStatus:
        engine = self._workload_engine
        if engine is None:
            return self._fail(state, "WorkloadDriver is not configured")
        if not engine.is_initialized:
            engine.initialize()

        workload_id = state.get(self._id_key)
        try:
            if not workload_id:
                wl = engine.start(
                    self._spec,
                    owner=self._owner,
                    idempotency_key=self._idempotency_key,
                )
                state.set(self._id_key, wl.workload_id)
            else:
                wl = engine.status(str(workload_id), refresh=True)
        except WorkloadError as exc:
            return self._fail(state, str(exc))
        except Exception as exc:
            return self._fail(state, str(exc))

        return self._interpret(state, wl)

    def _interpret(self, state: BaseState, wl: Any) -> PatternStatus:
        status = wl.status if isinstance(wl.status, WorkloadStatus) else WorkloadStatus(str(wl.status))
        payload = wl.to_dict() if hasattr(wl, "to_dict") else dict(wl)
        trace: dict[str, Any] = {
            "workload_id": payload.get("workload_id"),
            "status": str(status),
            "runtime": payload.get("runtime"),
            "kind": (payload.get("spec") or {}).get("kind"),
            "success": None,
            "exit_code": None,
            "error": payload.get("message"),
        }
        result = payload.get("result") or {}
        if isinstance(result, dict) and result:
            trace["exit_code"] = result.get("exit_code")
            if result.get("error"):
                trace["error"] = result.get("error")

        if status is WorkloadStatus.READY and self._wait_ready:
            if self._stop_when_done:
                return self._stop_and_finish(state, wl, trace)
            trace["success"] = True
            state.set(self._trace_key, trace)
            state.set(self._output_key, payload)
            if self._error_key:
                state.delete(self._error_key)
            return PatternStatus.SUCCESS

        if status is WorkloadStatus.READY and not self._wait_ready:
            # Service/workspace left running — success without waiting for stop
            if self._stop_when_done:
                return self._stop_and_finish(state, wl, trace)
            # Default for run-like wait: keep RUNNING until terminal unless wait_ready
            # For workspace without wait_ready and without stop: treat READY as success
            if self._spec.kind.value in ("workspace", "service"):
                trace["success"] = True
                state.set(self._trace_key, trace)
                state.set(self._output_key, payload)
                return PatternStatus.SUCCESS

        if is_terminal(status):
            exit_code = result.get("exit_code") if isinstance(result, dict) else None
            ok = status is WorkloadStatus.STOPPED and (exit_code is None or exit_code == 0)
            if status is WorkloadStatus.FAILED:
                ok = False
            if status is WorkloadStatus.STOPPED and exit_code not in (None, 0):
                ok = False
            trace["success"] = ok
            state.set(self._trace_key, trace)
            state.set(self._output_key, payload)
            if ok:
                if self._error_key:
                    state.delete(self._error_key)
                return PatternStatus.SUCCESS
            return self._fail(
                state,
                trace.get("error") or f"Workload {status}",
                already_traced=True,
            )

        # STARTING / RUNNING / STOPPING / PENDING
        state.set(self._trace_key, {**trace, "success": None})
        return PatternStatus.RUNNING

    def _stop_and_finish(
        self, state: BaseState, wl: Any, trace: dict[str, Any]
    ) -> PatternStatus:
        engine = self._workload_engine
        assert engine is not None
        try:
            stopped = engine.stop(wl.workload_id)
        except WorkloadError as exc:
            return self._fail(state, str(exc))
        return self._interpret(state, stopped)

    def _fail(
        self,
        state: BaseState,
        message: str,
        *,
        already_traced: bool = False,
    ) -> PatternStatus:
        detail = f"Workload {self.name!r} failed: {message}"
        if self._error_key:
            state.set(self._error_key, detail)
        if not already_traced:
            state.set(
                self._trace_key,
                {
                    "success": False,
                    "error": message,
                    "workload_id": state.get(self._id_key),
                },
            )
        return PatternStatus.FAILURE
