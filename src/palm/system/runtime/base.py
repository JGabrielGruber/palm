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
from palm.common.events import OutboxProcessor, OutboxStore, wire_reliable_events
from palm.system.executions import DefinitionExecutor
from palm.system.runtime.job_hooks import (
    InstancePersistenceHook,
    OutboxDrainHook,
    StateSnapshotHook,
)
from palm.common.managers import InstanceManager
from palm.common.plugins import ensure_core_plugins
from palm.common.providers._registry import get_runtime_binding, get_runtime_unbinding
from palm.common.resource import resource_definition_resolver
from palm.common.storage import StorageFactory
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
from palm.core.context import BaseState
from palm.core.workload import WorkloadEngine
from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.spec import WorkloadSpec
from palm.definitions.flow import FlowDefinition
from palm.definitions.process import ProcessDefinition
from palm.instances import ProcessInstance
from palm.states import BlackboardState
from palm.system.planes.session.plane import SessionPlaneService
from palm.system.planes.wait.plane import WaitPlaneService
from palm.system.planes.workload.bootstrap import initialize_workload_engine
from palm.system.runtime.hooks import (
    AuthMiddleware,
    DriveObservabilityHook,
    JobExecutionContextHook,
    authenticate_runtime,
)
from palm.system.runtime.schedulers import QueuedScheduler
from palm.system.runtime.wiring import SchedulerPolicy, resolve_scheduler

if TYPE_CHECKING:
    from palm.system.ports.execution import ExecutionPort


class BaseRuntime:
    """
    System instance: coordinates engines, planes, and effect ports.

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
        self._wait_plane: WaitPlaneService | None = None
        self._session_plane: SessionPlaneService | None = None

    @property
    def is_started(self) -> bool:
        return self._started

    @property
    def execution(self) -> ExecutionPort:
        """Effect port shared by graphs and product (resource + workload)."""
        return self

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
    def wait_plane(self) -> WaitPlaneService | None:
        """Continue plane (wait interest match on ``runtime.event``), or ``None``."""
        return self._wait_plane

    @property
    def wait_matcher(self) -> Any:
        """Matcher inside the continue plane (0.55.4+), or ``None``."""
        return None if self._wait_plane is None else self._wait_plane.matcher

    @property
    def session_plane(self) -> SessionPlaneService | None:
        """Session plane (outside subject lifecycle), or ``None`` before start."""
        return self._session_plane

    def start(self, **options: Any) -> None:
        """Initialize engines, wire orchestration, and begin accepting jobs."""
        if self._started:
            return

        # Plugin registries (patterns/providers/runners/storages) — via common,
        # not direct system imports (guard_system purity).
        ensure_core_plugins()

        self.context.initialize()
        self.event.initialize()
        cache_options = options.get("resource_cache")
        resource_options: dict[str, Any] = {
            "event_engine": self.event,
            "definition_resolver": resource_definition_resolver(self.repository),
        }
        if cache_options is not None:
            resource_options["resource_cache"] = cache_options
        self.resource.initialize(**resource_options)

        def _publish_workload(event_type: str, payload: dict[str, Any]) -> None:
            self.event.emit(event_type, **payload)

        initialize_workload_engine(
            self.workload,
            host_enabled=bool(options.get("workload_host_enabled", False)),
            work_root=options.get("workload_work_root") or options.get("data_dir"),
            default_runtime=options.get("workload_default_runtime"),
            publish_event=_publish_workload,
        )

        self.auth.initialize()
        authenticate_runtime(self.auth, options.get("credentials"))

        if not self.storage.is_initialized:
            StorageFactory.initialize_engine(
                self.storage,
                storage_backend=str(options.get("storage_backend", "memory")),
                **dict(options.get("backend_options") or {}),
            )

        enable_outbox = bool(options.get("enable_event_outbox", True))
        if enable_outbox:
            self._outbox_store = OutboxStore(self.storage)
            wire_reliable_events(self.event, self._outbox_store)
            self._outbox_processor = OutboxProcessor(self._outbox_store, self.event)

        scheduler = resolve_scheduler(
            options,
            default_policy=self.default_scheduler_policy,
        )
        hooks = list(options.get("hooks") or [])
        if options.get("observability"):
            hooks.append(DriveObservabilityHook())
        self._auth_enforce = bool(options.get("auth_enforce"))
        if self._auth_enforce:
            hooks.append(
                AuthMiddleware(
                    self.auth,
                    required_roles=tuple(options.get("auth_roles") or ("user",)),
                )
            )
        hooks.append(JobExecutionContextHook())
        # Continue verb: WaitMatcher on runtime.event (not job hooks).
        hooks.append(
            InstancePersistenceHook(
                self.instance_manager,
                outbox_store=self._outbox_store,
            )
        )
        if self._outbox_processor is not None:
            hooks.append(OutboxDrainHook(self._outbox_processor))
        if options.get("enable_state_snapshot"):
            hooks.append(
                StateSnapshotHook(
                    self.instance_manager,
                    snapshot_on_status=options.get("snapshot_on_status"),
                    max_snapshots_per_instance=int(options.get("max_snapshots_per_instance", 10)),
                )
            )

        orch_options: dict[str, Any] = {
            "scheduler": scheduler,
            "event_engine": self.event,
            "context_engine": self.context,
            "hooks": hooks,
        }
        max_jobs = options.get("max_concurrent_jobs")
        if isinstance(max_jobs, int) and max_jobs > 0:
            orch_options["max_concurrent_jobs"] = max_jobs
        self.orchestration.initialize(**orch_options)

        state = options.get("state")
        bt_state: BaseState = state if isinstance(state, BaseState) else BlackboardState()
        self.behavior_tree.initialize(state=bt_state)

        if not self.instance_manager.is_initialized:
            self.instance_manager.initialize(
                max_loaded_instances=options.get("max_loaded_instances"),
                max_concurrent_active=options.get("max_concurrent_active"),
                max_snapshots_per_instance=options.get("max_snapshots_per_instance"),
                reconcile_on_startup=options.get("reconcile_on_startup"),
            )

        self.orchestration.start()

        # Continue plane — peer of work-drain (start); always wired.
        self._wait_plane = WaitPlaneService()
        self._wait_plane.attach(self)

        # Session plane — outside subject seat (0.58.1); StorageEngine store.
        self._session_plane = SessionPlaneService(storage=self.storage)
        self._session_plane.attach(self)

        self._started = True

        bind_runtime = get_runtime_binding()
        if bind_runtime is not None:
            bind_runtime(self)

    def stop(self) -> None:
        """Stop orchestration and shut down all engines."""
        if not self._started:
            return

        unbind_runtime = get_runtime_unbinding()
        if unbind_runtime is not None:
            unbind_runtime()

        if self._session_plane is not None:
            self._session_plane.detach()
            self._session_plane = None

        if self._wait_plane is not None:
            self._wait_plane.detach()
            self._wait_plane = None

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
