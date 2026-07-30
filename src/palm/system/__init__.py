"""
Palm system layer — running machine: ports, planes, executions, system instance.

Holds :class:`~palm.system.runtime.base.BaseRuntime`, continue/start/session
planes, effect ports, definition executor, and job hooks. Prefer imports from
this package.

Rules (enforced by ``scripts/guard_system.py``):

- May import ``palm.core``, ``palm.definitions``, ``palm.instances``, and shared libraries.
- Must not import product (``palm.services``), surfaces (``palm.runtimes``), or patterns.
"""

from __future__ import annotations

from palm.system.effects import (
    PortResourceInvoker,
    PortWorkloadDriver,
    resource_invoker_from_port,
    workload_driver_from_port,
)
from palm.system.instance import SystemInstance
from palm.system.ports.execution import ExecutionPort
from palm.system.runtime.base import BaseRuntime

__all__ = [
    "BaseRuntime",
    "ExecutionPort",
    "PortResourceInvoker",
    "PortWorkloadDriver",
    "SystemInstance",
    "resource_invoker_from_port",
    "workload_driver_from_port",
]
