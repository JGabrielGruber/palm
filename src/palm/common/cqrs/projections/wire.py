"""Install-board projection attach — core read models, not a loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from palm.common.cqrs.projections.instance_index import InstanceIndexProjection
from palm.common.cqrs.projections.job_status_board import JobStatusBoardProjection
from palm.common.cqrs.projections.resource_invocation import ResourceInvocationProjection


@dataclass
class InstallProjections:
    """Core projections the structure hand binds onto the install board."""

    instance: InstanceIndexProjection
    resource: ResourceInvocationProjection
    job_board: JobStatusBoardProjection


def wire_install_projections(storage: Any, instance_manager: Any) -> InstallProjections:
    """Construct core projections over storage. Pattern extras stay a host leftover."""
    return InstallProjections(
        instance=InstanceIndexProjection(storage, instance_manager),
        resource=ResourceInvocationProjection(storage),
        job_board=JobStatusBoardProjection(storage),
    )


__all__ = [
    "InstallProjections",
    "wire_install_projections",
]
