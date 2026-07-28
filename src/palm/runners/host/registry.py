"""Register host WorkloadRuntime class + app."""

from palm.core.workload.registry import workload_runtime_registry
from palm.runners.host.app import host_runner_app
from palm.runners.host.runtime import HostWorkloadRuntime

workload_runtime_registry.register("host", HostWorkloadRuntime)
host_runner_app.register()
