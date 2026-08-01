"""
System runtime package — instance shell, schedulers, wiring, job hooks.

**Import law (0.59.3):** this package ``__init__`` must **not** eagerly import
``BaseRuntime``. Boot owns system start and may import hooks/wiring as
collaborators; if ``__init__`` pulls ``base``, boot → runtime → base → boot cycles.

Prefer explicit submodules:

- ``palm.system.runtime.base`` — system instance shell
- ``palm.system.runtime.hooks`` / ``job_hooks`` / ``wiring`` — start collaborators
- ``palm.system`` re-exports ``BaseRuntime`` for the public façade
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "BaseRuntime",
    "RuntimeHost",
    "SchedulerPolicy",
    "resolve_runner",
    "resolve_scheduler",
]

_LAZY: dict[str, tuple[str, str]] = {
    "BaseRuntime": ("palm.system.runtime.base", "BaseRuntime"),
    "RuntimeHost": ("palm.system.runtime.host", "RuntimeHost"),
    "SchedulerPolicy": ("palm.system.runtime.wiring", "SchedulerPolicy"),
    "resolve_runner": ("palm.system.runtime.wiring", "resolve_runner"),
    "resolve_scheduler": ("palm.system.runtime.wiring", "resolve_scheduler"),
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_path, attr = _LAZY[name]
    import importlib

    module = importlib.import_module(module_path)
    value = getattr(module, attr)
    globals()[name] = value
    return value
