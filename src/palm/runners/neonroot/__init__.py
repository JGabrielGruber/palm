"""NeonRoot WorkloadRuntime package — sole NeonRoot integration surface."""

from palm.runners.neonroot.cli import NeonrootProbe, find_neonroot_binary, probe_neonroot
from palm.runners.neonroot.contract import validate_hermetic_job_params
from palm.runners.neonroot.registry import *  # noqa: F403
from palm.runners.neonroot.runtime import NeonrootWorkloadRuntime
from palm.runners.neonroot.spec_map import spawn_request_from_spec
from palm.runners.neonroot.spawn import resolve_repo_root, run_spawn, run_spawn_request

__all__ = [
    "NeonrootProbe",
    "NeonrootWorkloadRuntime",
    "find_neonroot_binary",
    "probe_neonroot",
    "resolve_repo_root",
    "run_spawn",
    "run_spawn_request",
    "spawn_request_from_spec",
    "validate_hermetic_job_params",
]
