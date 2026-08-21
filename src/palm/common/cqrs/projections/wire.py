"""Install-board projection attach — core read models, not a loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from palm.common.cqrs.projection import ProjectionManager
from palm.common.cqrs.projections.instance_index import InstanceIndexProjection
from palm.common.cqrs.projections.job_status_board import JobStatusBoardProjection
from palm.common.cqrs.projections.resource_invocation import ResourceInvocationProjection


@dataclass
class InstallProjections:
    """Core projections the structure hand binds onto the install board."""

    instance: InstanceIndexProjection
    resource: ResourceInvocationProjection
    job_board: JobStatusBoardProjection
    manager: ProjectionManager


def wire_install_projections(storage: Any, instance_manager: Any, event: Any) -> InstallProjections:
    """Construct core projections and attach them to the runtime bus.

    Pattern extras stay a host leftover registered onto this same manager.
    """
    instance = InstanceIndexProjection(storage, instance_manager)
    resource = ResourceInvocationProjection(storage)
    job_board = JobStatusBoardProjection(storage)
    manager = ProjectionManager()
    manager.register(instance)
    manager.register(resource)
    manager.register(job_board)
    manager.attach(event)
    return InstallProjections(
        instance=instance,
        resource=resource,
        job_board=job_board,
        manager=manager,
    )


__all__ = [
    "InstallProjections",
    "wire_install_projections",
]
