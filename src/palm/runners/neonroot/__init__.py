"""NeonRoot WorkloadRuntime package — sole NeonRoot integration surface."""

from palm.runners.neonroot.cli import NeonrootProbe, find_neonroot_binary, probe_neonroot
from palm.runners.neonroot.contract import validate_hermetic_job_params
from palm.runners.neonroot.registry import *  # noqa: F403
from palm.runners.neonroot.runtime import NeonrootWorkloadRuntime
from palm.runners.neonroot.spawn import resolve_repo_root, run_spawn

__all__ = [
    "NeonrootProbe",
    "NeonrootWorkloadRuntime",
    "find_neonroot_binary",
    "probe_neonroot",
    "resolve_repo_root",
    "run_spawn",
    "validate_hermetic_job_params",
]
