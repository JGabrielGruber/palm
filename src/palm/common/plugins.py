"""Plugin package side-effect registration (shared bootstrap helper).

System code must not import ``palm.patterns`` / product surfaces
(``scripts/guard_system.py``). Call :func:`ensure_core_plugins` from
system-instance start so registries populate without the system layer
depending on plugin packages at import time.
"""

from __future__ import annotations

_loaded = False


def ensure_core_plugins() -> None:
    """Import extensible plugin packages so registries are populated.

    Safe to call multiple times. Used by system runtime start and app bootstrap.
    """
    global _loaded
    if _loaded:
        return
    import palm.common.transforms  # noqa: F401 — common transform rules
    import palm.kits  # noqa: F401 — surface kits (server, …); autoload on import
    import palm.patterns  # noqa: F401 — pattern apps
    import palm.providers  # noqa: F401 — provider apps
    import palm.runners  # noqa: F401 — WorkloadRuntime adapters
    import palm.storages  # noqa: F401 — storage backends

    _loaded = True
