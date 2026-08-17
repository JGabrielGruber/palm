"""Product start ports — submit + able for the install board.

Takes seats, not the host bag. Session enrich is one path
(``enrich_reactive_start``). No hasattr forks.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def product_start_ports(
    *,
    execution: Any,
    session: Any | None,
    started: Callable[[], bool],
) -> tuple[Callable[..., Any], Callable[[], bool]]:
    """Build ``submit`` / ``able`` closures bound to product seats."""

    def submit(flow_id: str, payload: dict[str, Any]) -> Any:
        body = dict(payload or {})
        seed = body.pop("_seed_state", None)
        submit_body: dict[str, Any] = {"flow_name": flow_id, "metadata": body}
        if seed is not None:
            submit_body["state"] = seed
        if session is not None:
            origin = session.reactive_origin(flow_id, body)
            submit_body = session.enrich_reactive_start(
                submit_body,
                origin=origin,
                surface="work-drain",
            )
        if execution is None:
            raise RuntimeError("host execution not bound")
        return execution.flows.submit_flow_body(submit_body)

    def able() -> bool:
        return bool(started())

    return submit, able
