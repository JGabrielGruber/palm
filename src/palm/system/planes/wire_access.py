"""Resolve the system wire seat for bind helpers — no bag scrape for ports."""

from __future__ import annotations

from typing import Any

from palm.system.ports.wire import WirePort


def require_system_wire(runtime: Any) -> WirePort:
    """
    Return the instance's wire seat.

    Prefer :meth:`bind_system_wire` so the board is current. Then read
    ``runtime.wire``. Never rebuild orchestration/storage via ``getattr`` soup.
    """
    bind = getattr(runtime, "bind_system_wire", None)
    if callable(bind):
        wire = bind()
        if wire is not None:
            return wire  # type: ignore[return-value]

    try:
        wire = runtime.wire
    except AttributeError as exc:
        raise RuntimeError(
            "system instance has no wire; implement wire + bind_system_wire "
            "(see BaseRuntime)"
        ) from exc

    if wire is None:
        raise RuntimeError(
            "system instance wire is None; call bind_system_wire first"
        )
    return wire  # type: ignore[return-value]


__all__ = ["require_system_wire"]
