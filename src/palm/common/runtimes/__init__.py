"""Shared runtime *helpers* that are not system and not kits.

- :mod:`palm.common.runtimes.doctor_contributors` — doctor section registry

System instance: :mod:`palm.system.runtime`.  
Server transport kit: :mod:`palm.kits.server`.
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
