"""Shared runtime *infrastructure* that is not the system instance.

System instance, ports, and schedulers live under :mod:`palm.system.runtime`.
This package holds:

- :mod:`palm.common.runtimes.server` — transport kit (SD-011 residual)
- :mod:`palm.common.runtimes.doctor_contributors` — doctor section registry

Import ``BaseRuntime`` from :mod:`palm.system` or :mod:`palm.system.runtime.base`.
"""

from palm.common.runtimes.doctor_contributors import (
    DoctorContributor,
    clear_doctor_contributors,
    collect_doctor_extensions,
    register_doctor_contributor,
)

__all__ = [
    "DoctorContributor",
    "clear_doctor_contributors",
    "collect_doctor_extensions",
    "register_doctor_contributor",
]
