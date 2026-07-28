"""Register local WorkloadRuntime."""

from palm.core.workload.registry import workload_runtime_registry
from palm.runners.local.app import local_runner_app
from palm.runners.local.runtime import LocalWorkloadRuntime

workload_runtime_registry.register("local", LocalWorkloadRuntime)
local_runner_app.register()
