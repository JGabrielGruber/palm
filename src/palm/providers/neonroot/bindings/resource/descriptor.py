"""Provider descriptor for NeonRoot (Sovereign Runners, 0.53)."""

from __future__ import annotations

from palm.core.resource.result import ProviderActionDescriptor, ProviderDescriptor


def describe(*, name: str) -> ProviderDescriptor:
    return ProviderDescriptor(
        name=name,
        description=(
            "NeonRoot hermetic runners — sandbox spawn and tool images "
            "(optional host CLI; health is honest when missing)"
        ),
        actions=(
            ProviderActionDescriptor(
                "health",
                "Probe neonroot CLI availability and version",
            ),
            ProviderActionDescriptor(
                "spawn",
                "Run a command in a NeonRoot sandbox "
                "(params: image, command[], seed=git-archive|path, "
                "seed_exclude[], outputs[{host,container}|host:container], vault?, sandbox?)",
            ),
            ProviderActionDescriptor(
                "list_images",
                "List images in a vault (later 0.53)",
            ),
        ),
    )


__all__ = ["describe"]
