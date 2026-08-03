"""Storage backend select — boot assembly leaf."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.common.storage import StorageFactory


def select_system_storage(
    shell: Any,
    options: Mapping[str, Any] | None = None,
) -> Any:
    """
    Initialize storage on *shell* when not already initialized.

    Returns the storage engine seat for BootContext publish.
    """
    opts = dict(options or {})
    if not shell.storage.is_initialized:
        StorageFactory.initialize_engine(
            shell.storage,
            storage_backend=str(opts.get("storage_backend", "memory")),
            **dict(opts.get("backend_options") or {}),
        )
    return shell.storage


__all__ = ["select_system_storage"]
