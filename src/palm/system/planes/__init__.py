"""
Compatibility shim — prefer :mod:`palm.system.subsystems.planes`.

``__path__`` is extended so nested imports (``palm.system.planes.wait…``) resolve
to the real subsystem package for one theme.
"""

from __future__ import annotations

import palm.system.subsystems.planes as _real

__path__ = list(_real.__path__)  # type: ignore[name-defined]

from palm.system.subsystems.planes import *  # noqa: F403, E402
from palm.system.subsystems.planes import __all__ as __all__  # noqa: E402
