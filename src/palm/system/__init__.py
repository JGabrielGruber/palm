"""
Palm system layer — running machine: ports, planes, system instance.

This package is the named home for system contracts (0.57+).
Concrete runtime wiring still lives partly in ``palm.common`` until deflate
waves (SYSTEM-LOW-LEVEL move waves A-H). Import **ports** and
:class:`~palm.system.instance.SystemInstance` from here.

Rules (enforced by ``scripts/guard_system.py``):

- May import ``palm.core``, ``palm.definitions``, ``palm.instances``, and shared libraries.
- Must not import product (``palm.services``), surfaces (``palm.runtimes``), or patterns.
"""

from __future__ import annotations

from palm.system.instance import SystemInstance
from palm.system.ports.execution import ExecutionPort

__all__ = [
    "ExecutionPort",
    "SystemInstance",
]
