"""
External event consumers — webhook dispatcher organ.

**Add a webhook consumer**

1. Configure targets via :class:`WebhookTarget` (URL + optional event filter).
2. Structure DNA lists ``webhook`` (``has_capability("webhook")``). Recover
   refines the install dispatcher from ``PALM_WEBHOOK_URLS``.
   ``PALM_ENABLE_WEBHOOK_DISPATCHER`` is unread packaging.
3. For tests, inject :class:`RecordingWebhookDeliverer` to capture deliveries
   without network I/O.

``dispatch`` POSTs JSON with ``type``, ``payload``, ``context``, and
``timestamp``. Production outbox drain does not call it.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from palm.core.event import Event


class WebhookDeliverer(Protocol):
    """Transport for a single webhook delivery attempt."""

    def deliver(self, url: str, body: bytes, *, headers: dict[str, str]) -> None:
        """Raise on delivery failure."""


@dataclass(frozen=True)
class WebhookTarget:
    """Destination for outbox-driven webhook dispatch."""

    url: str
    name: str = ""
    event_types: frozenset[str] | None = None

    def matches(self, event_type: str) -> bool:
        if self.event_types is None:
            return True
        return event_type in self.event_types


@dataclass
class WebhookDelivery:
    """Record of a single delivery attempt."""

    target: str
    url: str
    event_type: str
    event_id: str
    ok: bool
    error: str | None = None
    delivered_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class HttpWebhookDeliverer:
    """POST JSON payloads via stdlib ``urllib`` (no extra dependencies)."""

    def __init__(self, *, timeout: float = 5.0) -> None:
        self._timeout = timeout

    def deliver(self, url: str, body: bytes, *, headers: dict[str, str]) -> None:
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            if response.status >= 400:
                raise urllib.error.HTTPError(
                    url, response.status, response.reason, response.headers, None
                )


class RecordingWebhookDeliverer:
    """In-memory deliverer for tests — records bodies without network I/O."""

    def __init__(self) -> None:
        self.deliveries: list[dict[str, Any]] = []

    def deliver(self, url: str, body: bytes, *, headers: dict[str, str]) -> None:
        self.deliveries.append(
            {
                "url": url,
                "body": json.loads(body.decode("utf-8")),
                "headers": dict(headers),
            }
        )


class WebhookDispatcher:
    """Delivers events to configured webhook targets.

    Membership is DNA ``has_capability("webhook")``. Recover refines this
    object in place. Production outbox drain does not call ``dispatch``.
    """

    def __init__(
        self,
        targets: list[WebhookTarget],
        *,
        deliverer: WebhookDeliverer | None = None,
    ) -> None:
        self._targets = list(targets)
        self._deliverer = deliverer or HttpWebhookDeliverer()
        self._history: list[WebhookDelivery] = []

    @property
    def targets(self) -> tuple[WebhookTarget, ...]:
        return tuple(self._targets)

    def replace_targets(self, targets: list[WebhookTarget]) -> None:
        """Replace destinations on this dispatcher. Does not construct a twin."""
        self._targets = list(targets)

    @property
    def deliveries(self) -> tuple[WebhookDelivery, ...]:
        return tuple(self._history)

    def dispatch(self, event: Event) -> list[WebhookDelivery]:
        """Deliver ``event`` to all matching targets. Raises if any delivery fails."""
        if not self._targets:
            return []

        body = json.dumps(_event_payload(event)).encode("utf-8")
        headers = {"Content-Type": "application/json", "User-Agent": "Palm-Webhook/0.10"}
        results: list[WebhookDelivery] = []

        for target in self._targets:
            if not target.matches(event.type):
                continue
            label = target.name or target.url
            try:
                self._deliverer.deliver(target.url, body, headers=headers)
                record = WebhookDelivery(
                    target=label,
                    url=target.url,
                    event_type=event.type,
                    event_id=event.id,
                    ok=True,
                )
            except Exception as exc:
                record = WebhookDelivery(
                    target=label,
                    url=target.url,
                    event_type=event.type,
                    event_id=event.id,
                    ok=False,
                    error=str(exc),
                )
                self._history.append(record)
                raise
            self._history.append(record)
            results.append(record)
        return results


def webhook_targets_from_urls(
    urls: list[str],
    *,
    event_types: list[str] | None = None,
) -> list[WebhookTarget]:
    """Build :class:`WebhookTarget` list from plain URL strings."""
    types = frozenset(event_types) if event_types else None
    return [WebhookTarget(url=url, event_types=types) for url in urls if url]


def _event_payload(event: Event) -> dict[str, Any]:
    return {
        "id": event.id,
        "type": event.type,
        "payload": dict(event.payload),
        "context": event.context.to_dict() if event.context is not None else None,
        "timestamp": event.timestamp.isoformat(),
    }
