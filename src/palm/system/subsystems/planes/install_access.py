"""
Resolve InstallInterface for shell-side helpers.

Prefer seat-first APIs that already hold :class:`InstallInterface` and
:class:`SystemPlanes`. This module is only for the thin shell bridge
(``bind_*_to_runtime`` / tests that still start from a system instance).
"""

from __future__ import annotations

from typing import Any

from palm.system.interfaces.install import InstallInterface


def require_system_install(shell: Any) -> InstallInterface:
    """
    Return the instance's install interface seat.

    Prefer :meth:`bind_system_install` so the board is current. Then read
    ``shell.install``. Never rebuild orchestration/storage via ``getattr`` soup.
    """
    bind = getattr(shell, "bind_system_install", None)
    if bind is None:
        bind = getattr(shell, "bind_system_wire", None)  # temporary alias
    if callable(bind):
        board = bind()
        if board is not None:
            return board  # type: ignore[return-value]

    board = None
    try:
        board = shell.install
    except AttributeError:
        try:
            board = shell.wire  # temporary alias
        except AttributeError as exc:
            raise RuntimeError(
                "system instance has no install interface; implement install + "
                "bind_system_install (see BaseRuntime)"
            ) from exc

    if board is None:
        raise RuntimeError(
            "system instance install is None; call bind_system_install first"
        )
    return board  # type: ignore[return-value]


# temporary alias
require_system_wire = require_system_install

__all__ = ["require_system_install", "require_system_wire"]
