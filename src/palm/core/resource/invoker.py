"""
ResourceInvoker — narrow effect protocol for graphs (0.57.4 / P2).

Leaves and patterns call this instead of requiring concrete ResourceEngine.
ResourceEngine implements it. System adapters map ExecutionPort onto it.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from palm.core.resource.result import ProviderResult


@runtime_checkable
class ResourceInvoker(Protocol):
    """Minimal resource effect surface for ResourceLeaf and pattern ticks."""

    @property
    def is_initialized(self) -> bool:
        """Whether the invoker is ready for invoke."""
        ...

    def initialize(self, **options: Any) -> None:
        """Initialize if needed (may be a no-op for adapters)."""
        ...

    def invoke(
        self,
        resource_ref: str | None = None,
        *,
        provider: str | None = None,
        action: str | None = None,
        params: dict[str, Any] | None = None,
        state: Any = None,
        resource_id: str | None = None,
        correlation: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ProviderResult:
        """Invoke a resource definition or direct provider action."""
        ...
