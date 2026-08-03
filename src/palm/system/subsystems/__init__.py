"""
System subsystems — membership + lifecycle regions (planes, supervisor).

Target layout:

* ``palm.system.subsystems.planes`` — reactive planes
* ``palm.system.subsystems.supervisor`` — continuous services

Compatibility shims: ``palm.system.subsystems.planes``, ``palm.system.subsystems.supervisor``.
"""

from __future__ import annotations

from palm.system.subsystems.protocol import Subsystem

__all__ = ["Subsystem"]
