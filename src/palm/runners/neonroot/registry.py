"""Register neonroot WorkloadRuntime class + app."""

from palm.core.workload.registry import workload_runtime_registry
from palm.runners.neonroot.app import neonroot_runner_app
from palm.runners.neonroot.runtime import NeonrootWorkloadRuntime

workload_runtime_registry.register("neonroot", NeonrootWorkloadRuntime)
neonroot_runner_app.register()
