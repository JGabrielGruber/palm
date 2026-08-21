"""Install-board webhook bind — dispatcher object, not a loop."""

from __future__ import annotations

from palm.common.events.external import WebhookDispatcher


def wire_install_webhook() -> WebhookDispatcher:
    """Construct the webhook dispatcher. Recover refines targets on this object."""
    return WebhookDispatcher([])


__all__ = ["wire_install_webhook"]
