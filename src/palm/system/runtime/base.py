"""
BaseRuntime — concrete **system instance** for a running Palm.

Holds engines, planes, and the :class:`~palm.system.ports.execution.ExecutionPort`
surface for graphs and product. Canonical home: :mod:`palm.system.runtime`.


Concrete surfaces (:class:`~palm.runtimes.embedded.runtime.EmbeddedRuntime`,
:class:`~palm.runtimes.daemon.runtime.DaemonRuntime`) differ only in default scheduling
policy and optional runtime-specific conveniences.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from palm import __version__
from palm.common import DefinitionRepository, InstanceRepository
from palm.common.events import OutboxProcessor, OutboxStore
from palm.system.executions import DefinitionExecutor
from palm.common.managers import InstanceManager
from palm.common.providers._registry import get_runtime_unbinding
from palm.core import (
    AuthEngine,
    BehaviorTreeEngine,
    ContextEngine,
    EventEngine,
    Job,
    OrchestrationEngine,
    ResourceEngine,
    StorageEngine,
)
from palm.core.workload import WorkloadEngine
from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.spec import WorkloadSpec
from palm.definitions.flow import FlowDefinition
from palm.definitions.process import ProcessDefinition
from palm.instances import ProcessInstance
from palm.states import BlackboardState
from palm.system.boot import (
    SYSTEM_PHASES,
    BootContext,
    build_system_handlers,
    walk_schedule,
)
from palm.system.log import get_system_log
from palm.system.planes.hub import SystemPlanes
from palm.system.planes.session.plane import SessionPlaneService
from palm.system.planes.wait.plane import WaitPlaneService
from palm.system.ports.wire import SystemWire
from palm.system.runtime.schedulers import QueuedScheduler
from palm.system.runtime.wiring import SchedulerPolicy

if TYPE_CHECKING:
    from palm.system.ports.execution import ExecutionPort


class BaseRuntime:
    """
    System instance shell: engines, planes, effect ports.

    **Start law lives in** ``palm.system.boot`` (0.59.3+). This class holds the
    machine; ``start()`` walks the system phase table. Do not grow private boot
    order here — add or migrate a phase handler under boot.

    Satisfies :class:`~palm.system.instance.SystemInstance` and
    :class:`~palm.system.ports.execution.ExecutionPort` structurally.
    Also satisfies the thin legacy :class:`~palm.system.runtime.host.RuntimeHost`.

    Subclasses set :attr:`default_scheduler_policy` to choose inline vs queued driving.
    Prefer ``runtime.execution`` for resource/workload effects (0.57+), not edge
    field access to engines.
    """

    runtime_name: ClassVar[str] = "Runtime"
    default_scheduler_policy: ClassVar[SchedulerPolicy] = "inline"

    def __init__(
        self,
        *,
        storage: StorageEngine | None = None,
        instance_manager: InstanceManager | None = None,
    ) -> None:
        self.context = ContextEngine()
        self.event = EventEngine()
        self.behavior_tree = BehaviorTreeEngine()
        self.resource = ResourceEngine()
        self.workload = WorkloadEngine()
        self.auth = AuthEngine()
        self.orchestration = OrchestrationEngine()
        self._owns_storage = storage is None
        self.storage = storage if storage is not None else StorageEngine()
        self.repository = DefinitionRepository(self.storage)
        if instance_manager is not None:
            self.instance_manager = instance_manager
            self.instances = instance_manager.repository
        else:
            self.instances = InstanceRepository(self.storage)
            self.instance_manager = InstanceManager(self.instances)
        self._owns_instance_manager = instance_manager is None
        self.executor = DefinitionExecutor(self, self.repository, self.instance_manager)
        self._started = False
        self._auth_enforce = False
        self._outbox_store: OutboxStore | None = None
        self._outbox_processor: OutboxProcessor | None = None
        self._planes: SystemPlanes | None = None
        self._supervisor: Any | None = None
        self._wire = SystemWire()
        self._last_boot_walk: list[Any] | None = None

    @property
    def is_started(self) -> bool:
        return self._started

    @property
    def execution(self) -> ExecutionPort:
        """Effect port shared by graphs and product (resource + workload)."""
        return self

    @property
    def wire(self) -> SystemWire:
        """
        Collaborator wire port (peer of :attr:`execution`).

        Boot binds named ports via :meth:`bind_system_wire`. Plane and
        supervisor install read this seat — they do not dig the bag.
        """
        return self._wire

    @property
    def version(self) -> str:
        return __version__

    @property
    def auth_enforce(self) -> bool:
        """Whether drive authorization is required for job execution."""
        return self._auth_enforce

    @property
    def outbox_store(self) -> OutboxStore | None:
        """Durable outbox store when ``enable_event_outbox`` is active."""
        return self._outbox_store

    @property
    def outbox_processor(self) -> OutboxProcessor | None:
        """Outbox drain helper wired at runtime start."""
        return self._outbox_processor

    @property
    def planes(self) -> SystemPlanes | None:
        """Planes hub — consumes wait/session/work (0.61). ``None`` before attach."""
        return self._planes

    @property
    def wait_plane(self) -> WaitPlaneService | None:
        """Continue plane — from :attr:`planes` hub, or ``None``."""
        hub = self._planes
        return None if hub is None else hub.get("wait")  # type: ignore[return-value]

    @property
    def wait_matcher(self) -> Any:
        """Matcher inside the continue plane (0.55.4+), or ``None``."""
        plane = self.wait_plane
        return None if plane is None else plane.matcher

    @property
    def session_plane(self) -> SessionPlaneService | None:
        """Session plane — from :attr:`planes` hub, or ``None``."""
        hub = self._planes
        return None if hub is None else hub.get("session")  # type: ignore[return-value]

    @property
    def work_plane(self) -> Any | None:
        """Start plane — from :attr:`planes` hub, or ``None``."""
        hub = self._planes
        return None if hub is None else hub.get("work")

    def plane(self, name: str) -> Any | None:
        """Plane by hub name (``wait``) or alias (``wait_plane``)."""
        hub = self._planes
        return None if hub is None else hub.get(name)

    @property
    def supervisor(self) -> Any | None:
        """Continuous system services supervisor (0.60), or ``None`` before wire."""
        return self._supervisor

    def bind_system_wire(self) -> SystemWire:
        """
        Explicitly bind engine collaborators onto :attr:`wire`.

        Call after engines/storage/orchestration exist (boot phase
        ``system.wire.bind``). Re-call after planes attach to publish
        ``work_plane`` for the supervisor.
        """

        def _get_job(job_id: str) -> Any:
            return self.get_job(str(job_id))

        def _submit(
            flow_id: str,
            metadata: dict[str, Any] | None = None,
            state: Any = None,
        ) -> Any:
            return self.submit_flow(flow_id, metadata=metadata, state=state)

        def _able() -> bool:
            return bool(self._started)

        self._wire.bind(
            orchestration=self.orchestration,
            event=self.event,
            storage=self.storage,
            instance_manager=self.instance_manager,
            get_job=_get_job,
            submit=_submit,
            able=_able,
            outbox_store=self._outbox_store,
            outbox_processor=self._outbox_processor,
            work_plane=self.work_plane,
        )
        return self._wire

    @property
    def last_boot_walk(self) -> list[Any] | None:
        """Last system boot walk results (0.59+), or ``None`` before start.

        Vitality / membership observation reads this seat. Prefer this property
        over the private ``_last_boot_walk`` field.
        """
        return self._last_boot_walk

    def start(self, **options: Any) -> None:
        """Hand control to the system boot schedule (``SYSTEM_PHASES``).

        0.59.3 — no private soup here. Rules live in
        ``palm.system.boot.system_schedule``. Observation via SystemLog.
        """
        if self._started:
            return

        slog = get_system_log()
        runtime = getattr(self, "name", None) or self.runtime_name
        ctx = BootContext(schedule="system", runtime=str(runtime))
        slog.info(
            "boot.start",
            "system schedule start",
            schedule="system",
            runtime=str(runtime),
        )
        try:
            # Boot owns order + handlers; this shell is the assembly target.
            self._last_boot_walk = walk_schedule(
                SYSTEM_PHASES,
                build_system_handlers(self, options),
                ctx=ctx,
                log=slog,
                require_handlers=True,
            )
        except Exception as exc:
            slog.emit(
                1,
                "boot.fail",
                f"system boot fail: {type(exc).__name__}: {exc}",
                schedule="system",
                runtime=str(runtime),
                reason=f"{type(exc).__name__}: {exc}",
            )
            raise

    def stop(self) -> None:
        """Stop orchestration and shut down all engines."""
        if not self._started:
            return

        slog = get_system_log()
        runtime = getattr(self, "name", None) or self.runtime_name
        slog.info(
            "shutdown.start",
            "system shutdown start",
            schedule="system",
            runtime=str(runtime),
        )

        unbind_runtime = get_runtime_unbinding()
        if unbind_runtime is not None:
            unbind_runtime()

        if self._supervisor is not None:
            try:
                self._supervisor.stop()
            except Exception:
                pass
            self._supervisor = None

        if self._planes is not None:
            try:
                self._planes.detach()
            except Exception:
                pass
            self._planes = None

        self.orchestration.stop()
        if self._owns_instance_manager:
            self.instance_manager.shutdown()
        if self._owns_storage:
            self.storage.shutdown()
        self.orchestration.shutdown()
        self.behavior_tree.shutdown()
        if self.workload.is_initialized:
            self.workload.shutdown()
        self.resource.shutdown()
        self.auth.shutdown()
        self.context.shutdown()
        self.event.shutdown()
        self._started = False
        slog.info(
            "shutdown.end",
            "system shutdown end",
            schedule="system",
            runtime=str(runtime),
        )

    def submit_flow(
        self,
        flow: FlowDefinition | str,
        *,
        by_id: bool = False,
        job_id: str | None = None,
        state: BlackboardState | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Job:
        """Submit a flow definition or repository name/id as an orchestration job."""
        if isinstance(flow, FlowDefinition):
            return self.executor.submit_flow(
                flow,
                job_id=job_id,
                state=state,
                metadata=metadata,
            )
        return self.executor.submit_flow(
            flow,
            by_id=by_id,
            job_id=job_id,
            state=state,
            metadata=metadata,
        )

    def submit_process(
        self,
        process: ProcessDefinition | str,
        *,
        by_id: bool = False,
        job_id: str | None = None,
        state: BlackboardState | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Job | list[Job]:
        """Submit a process definition or repository reference."""
        if isinstance(process, ProcessDefinition):
            jobs = self.executor.submit_process(
                process,
                job_id=job_id,
                state=state,
                metadata=metadata,
            )
        else:
            jobs = self.executor.submit_process(
                process,
                by_id=by_id,
                job_id=job_id,
                state=state,
                metadata=metadata,
            )
        return jobs[0] if len(jobs) == 1 else jobs

    def submit_wizard(
        self,
        *,
        name: str = "wizard",
        config: object | None = None,
        steps: int | None = None,
        job_id: str | None = None,
        state: BlackboardState | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Job:
        """Submit an interactive wizard via the executions builder."""
        options: dict[str, Any] = {}
        if config is not None:
            options["config"] = config
        if steps is not None:
            options["steps"] = steps
        flow = FlowDefinition(name=name, pattern="wizard", options=options)
        meta = dict(metadata or {})
        meta.setdefault("pattern", "wizard")
        return self.submit_flow(flow, job_id=job_id, state=state, metadata=meta)

    def provide_input(self, job_id: str, value: Any) -> str | None:
        """Provide input for a waiting interactive job and resume execution."""
        self._require_started()
        return self.orchestration.deliver_input(job_id, value)

    def resume_process(self, instance_id: str) -> Job:
        """Resume a persisted process instance."""
        self._require_started()
        return self.executor.resume_process(instance_id)

    def get_instance(self, instance_id: str) -> ProcessInstance:
        """Load a persisted process instance record."""
        self._require_started()
        return self.instance_manager.get(instance_id)

    def get_job(self, job_id: str) -> Job:
        """Return a registered orchestration job."""
        self._require_started()
        return self.orchestration.get_job(job_id)

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a non-terminal job."""
        self._require_started()
        return self.orchestration.cancel_job(job_id)

    def current_wizard_step(self, job_id: str) -> str | None:
        """Return the active step slug when the job executable supports inspection."""
        self._require_started()
        return self.orchestration.inspect_step(job_id)

    def wizard_answers(self, job_id: str) -> dict[str, Any]:
        """Return collected answers when the job executable supports inspection."""
        self._require_started()
        return self.orchestration.inspect_answers(job_id)

    def wait_until_idle(self, *, timeout: float = 5.0) -> bool:
        """
        Block until a queued scheduler has processed pending work.

        No-op for inline schedulers. Useful for tests and coordinated shutdown
        of background runtimes (:class:`~palm.runtimes.daemon.runtime.DaemonRuntime`,
        :class:`~palm.runtimes.server.runtime.ServerRuntime`).
        """
        self._require_started()
        scheduler = self.orchestration.scheduler
        if isinstance(scheduler, QueuedScheduler):
            return scheduler.wait_until_idle(timeout=timeout)
        return True

    # --- ExecutionPort (system effect surface) --------------------------------

    def invoke_resource(
        self,
        resource_ref: str | None = None,
        *,
        provider: str | None = None,
        action: str | None = None,
        params: dict[str, Any] | None = None,
        state: Any = None,
        resource_id: str | None = None,
        correlation: dict[str, Any] | None = None,
    ) -> Any:
        """Invoke a resource via the resource engine (ExecutionPort)."""
        engine = self.resource
        if not engine.is_initialized:
            engine.initialize()
        return engine.invoke(
            resource_ref,
            provider=provider,
            action=action,
            params=params,
            state=state,
            resource_id=resource_id,
            correlation=correlation,
        )

    def start_workload(
        self,
        spec: Any,
        *,
        owner: Any = None,
        workload_id: str | None = None,
        idempotency_key: str | None = None,
        host_id: str | None = None,
    ) -> Any:
        """Start a workload via the workload engine (ExecutionPort)."""
        engine = self._require_workload_engine()
        parsed = (
            spec if isinstance(spec, WorkloadSpec) else WorkloadSpec.from_dict(dict(spec))
        )
        bound_owner = _coerce_workload_owner(owner)
        # 0.58.8 — fill session/job/instance from event context when job path has them
        bound_owner = _enrich_workload_owner_from_event_context(self, bound_owner)
        return engine.start(
            parsed,
            owner=bound_owner,
            workload_id=workload_id,
            idempotency_key=idempotency_key,
            host_id=host_id,
        )

    def exec_workload(
        self,
        workload_id: str,
        command: list[str] | tuple[str, ...],
        *,
        timeout_s: float | None = None,
        env: dict[str, str] | None = None,
    ) -> Any:
        """Exec argv on a READY workload (ExecutionPort)."""
        return self._require_workload_engine().exec(
            str(workload_id),
            command,
            timeout_s=timeout_s,
            env=env,
        )

    def stop_workload(self, workload_id: str, **kwargs: Any) -> Any:
        """Idempotent stop of a workload (ExecutionPort)."""
        del kwargs  # reserved for future flags
        return self._require_workload_engine().stop(str(workload_id))

    def workload_status(self, workload_id: str, *, refresh: bool = False) -> Any:
        """Workload snapshot; optional runtime refresh (ExecutionPort)."""
        engine = self._require_workload_engine()
        if refresh:
            return engine.status(str(workload_id), refresh=True)
        return engine.get(str(workload_id))

    def resume_job(self, job_id: str) -> Any:
        """Re-drive a registered orchestration job (ExecutionPort)."""
        self._require_started()
        return self.orchestration.resume_job(str(job_id))

    def list_jobs(self, status: Any = None) -> list[Any]:
        """List orchestration jobs (ExecutionPort inspect)."""
        self._require_started()
        return self.orchestration.list_jobs(status=status)

    def list_workloads(
        self,
        *,
        job_id: str | None = None,
        instance_id: str | None = None,
        session_id: str | None = None,
        status: Any = None,
        runtime: str | None = None,
    ) -> list[Any]:
        """List tracked workloads (ExecutionPort catalog)."""
        return self._require_workload_engine().list(
            job_id=job_id,
            instance_id=instance_id,
            session_id=session_id,
            status=status,
            runtime=runtime,
        )

    def list_workload_runtimes(self) -> list[Any]:
        """Workload runtime catalog with health (ExecutionPort)."""
        return self._require_workload_engine().runtimes()

    def doctor_workloads(self) -> dict[str, Any]:
        """Workload-plane doctor snapshot (ExecutionPort)."""
        return self._require_workload_engine().doctor()

    def stop_owned_workloads(
        self,
        *,
        job_id: str | None = None,
        instance_id: str | None = None,
        session_id: str | None = None,
    ) -> list[Any]:
        """Stop owned workloads (ExecutionPort cancel path)."""
        return self._require_workload_engine().stop_owned(
            job_id=job_id,
            instance_id=instance_id,
            session_id=session_id,
        )

    def _require_workload_engine(self) -> WorkloadEngine:
        engine = self.workload
        if not engine.is_initialized:
            engine.initialize()
        return engine

    def _require_started(self) -> None:
        if not self._started:
            raise RuntimeError(f"{self.runtime_name} is not started; call start() first")


def _coerce_workload_owner(owner: Any) -> WorkloadOwner | None:
    if owner is None:
        return None
    if isinstance(owner, WorkloadOwner):
        return owner
    if isinstance(owner, dict):
        return WorkloadOwner.from_dict(owner)
    raise TypeError(f"owner must be WorkloadOwner or dict, got {type(owner)!r}")


def _enrich_workload_owner_from_event_context(
    runtime: Any, owner: WorkloadOwner | None
) -> WorkloadOwner:
    """Copy system session / job / instance from active EventContext when missing."""
    base = owner or WorkloadOwner()
    if base.session_id and base.job_id and base.instance_id:
        return base
    event = getattr(runtime, "event", None)
    if event is None or not hasattr(event, "current_context"):
        return base
    try:
        ctx = event.current_context()
    except Exception:
        return base
    if ctx is None:
        return base
    return WorkloadOwner(
        job_id=base.job_id or getattr(ctx, "job_id", None),
        instance_id=base.instance_id or getattr(ctx, "instance_id", None),
        lease_id=base.lease_id,
        session_id=base.session_id or getattr(ctx, "session_id", None),
        created_by_palm=base.created_by_palm,
    )
