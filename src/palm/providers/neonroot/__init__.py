"""NeonRoot provider — hermetic spawn / tool images (Sovereign Runners, 0.53).

Hermetic job contract (0.54): :mod:`palm.providers.neonroot.contract`.
"""

from palm.providers.neonroot import registry as registry
from palm.providers.neonroot.contract import validate_hermetic_job_params
from palm.providers.neonroot.provider import NeonrootProvider
from palm.providers.neonroot.run_dir import (
    HermeticRunDir,
    create_run_dir,
    remove_run_dir,
    write_payload_file,
)

__all__ = [
    "HermeticRunDir",
    "NeonrootProvider",
    "create_run_dir",
    "registry",
    "remove_run_dir",
    "validate_hermetic_job_params",
    "write_payload_file",
]
