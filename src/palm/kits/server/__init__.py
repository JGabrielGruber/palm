"""Server kit — HTTP protocol, routing, transport, CQRS bridge, SSR helpers.

**Kit home:** :mod:`palm.kits.server` (0.57.13). Surfaces under
``palm.runtimes.server`` compose this kit; they do not re-own the protocol.

Composition roots (``ServerApp`` / ``ServerContext``) stay in
``palm.runtimes.server``. ``ServerWebhookBridge`` is exported lazily.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from palm.kits.registry import register_kit
from palm.kits.server.middleware import (
    PALM_SUBJECT_HEADER,
    authenticate_request,
    current_principal_id,
)
from palm.kits.server.protocol import (
    HttpMethod,
    ServerRequest,
    ServerResponse,
    ServerSurface,
)
from palm.kits.server.registry import RouteRegistry, RouteSpec, SurfaceRegistry
from palm.kits.server.responses import error_response
from palm.kits.server.surface import BaseSurface
from palm.kits.server.transport import (
    BaseTransport,
    TransportRegistry,
    transport_registry,
)

register_kit(
    "server",
    description="HTTP protocol, routes, transport, CQRS bridge, SSR helpers",
    module="palm.kits.server",
)

if TYPE_CHECKING:
    from palm.kits.server.webhooks import ServerWebhookBridge

_LAZY_EXPORTS = {
    "ServerWebhookBridge": "palm.kits.server.webhooks",
}


def __getattr__(name: str) -> object:
    target = _LAZY_EXPORTS.get(name)
    if target is not None:
        import importlib

        return getattr(importlib.import_module(target), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BaseSurface",
    "BaseTransport",
    "HttpMethod",
    "PALM_SUBJECT_HEADER",
    "RouteRegistry",
    "RouteSpec",
    "ServerRequest",
    "ServerResponse",
    "ServerSurface",
    "ServerWebhookBridge",
    "SurfaceRegistry",
    "TransportRegistry",
    "authenticate_request",
    "current_principal_id",
    "error_response",
    "transport_registry",
]
