"""NeonRoot resource provider — hermetic isolation as a Palm resource (0.53)."""

from __future__ import annotations

from typing import Any

from palm.core.resource import BaseProvider
from palm.core.resource.result import (
    ProviderActionDescriptor,
    ProviderDescriptor,
    ProviderHealth,
    ProviderResult,
)
from palm.providers.neonroot.cli import probe_neonroot


class NeonrootProvider(BaseProvider):
    """Invoke NeonRoot from the resource engine (optional host binary)."""

    def connect(self) -> None:
        """No persistent connection — each probe is independent."""

    def disconnect(self) -> None:
        pass

    def fetch(self, resource_id: str, **params: Any) -> Any:
        """NeonRoot has no fetch-by-id; use ``invoke('health')`` / ``spawn``."""
        raise RuntimeError(
            "neonroot provider does not support fetch; use invoke(action='health'|'spawn'|…)"
        )

    def invoke(
        self,
        action: str,
        *,
        params: dict[str, Any] | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> ProviderResult:
        merged = dict(params or {})
        merged.update(kwargs)
        if resource_id is not None:
            merged.setdefault("resource_id", resource_id)

        if action == "health":
            probe = probe_neonroot()
            data = probe.as_dict()
            if probe.available:
                return ProviderResult.ok(data, action=action, provider=self.name)
            # Do not pass data["error"] as kwargs — fail() already takes error=
            meta = {k: v for k, v in data.items() if k != "error" and v is not None}
            return ProviderResult.fail(
                probe.error or "neonroot unavailable",
                action=action,
                provider=self.name,
                **meta,
            )

        if action in ("spawn", "list_images", "image.ensure", "image.build"):
            return ProviderResult.fail(
                f"action {action!r} not implemented until a later 0.53 slice "
                f"(scaffold 0.53.1 provides health only)",
                action=action,
                provider=self.name,
            )

        return ProviderResult.fail(
            f"Unsupported action {action!r}",
            action=action,
            provider=self.name,
        )

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            description=(
                "NeonRoot hermetic runners — sandbox spawn and tool images "
                "(optional host CLI; health is honest when missing)"
            ),
            actions=(
                ProviderActionDescriptor("health", "Probe neonroot CLI availability/version"),
                ProviderActionDescriptor(
                    "spawn",
                    "Run a command in a NeonRoot sandbox (0.53.2+)",
                ),
                ProviderActionDescriptor(
                    "list_images",
                    "List images in a vault (later 0.53)",
                ),
            ),
        )

    def health(self) -> ProviderHealth:
        probe = probe_neonroot()
        if probe.available:
            msg = f"neonroot ready ({probe.version or probe.path})"
            return ProviderHealth(healthy=True, message=msg)
        return ProviderHealth(
            healthy=False,
            message=probe.error or "neonroot not available",
        )


__all__ = ["NeonrootProvider"]
