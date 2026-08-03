"""
Compatibility shim — prefer :mod:`palm.system.subsystems.supervisor`.
"""

from __future__ import annotations

import palm.system.subsystems.supervisor as _real

__path__ = list(_real.__path__)  # type: ignore[name-defined]

from palm.system.subsystems.supervisor import *  # noqa: F403, E402
from palm.system.subsystems.supervisor import __all__ as __all__  # noqa: E402
