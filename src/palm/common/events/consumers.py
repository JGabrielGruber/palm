"""
Named journal consumers (0.40.3).

Standard names for lag observability:

- ``work_drain`` — deferred WorkIntent path (offsets for ops; drain still uses store)

Consumers advance **their own** offsets via :meth:`EventJournal.consume`.
"""

from __future__ import annotations

from typing import Any

from palm.common.events.journal import EventJournal

# Canonical names used in host.control_plane_status / doctor
JOURNAL_CONSUMER_WORK_DRAIN = "work_drain"

DEFAULT_JOURNAL_CONSUMERS: tuple[str, ...] = (JOURNAL_CONSUMER_WORK_DRAIN,)


def journal_consumer_status(
    journal: EventJournal,
    *,
    consumers: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Lag snapshot for doctor / control_plane."""
    names = list(consumers) if consumers is not None else list(DEFAULT_JOURNAL_CONSUMERS)
    return journal.status(consumers=names)


def mark_work_drain_caught_up(journal: EventJournal) -> int:
    """
    Advance ``work_drain`` consumer to latest journal offset.

    Work drain uses WorkIntentStore for execution; this offset is **observability**
    (and optional redrive coordination), not the claim queue.
    """
    latest = journal.latest_offset()
    journal.commit_consumer_offset(JOURNAL_CONSUMER_WORK_DRAIN, latest)
    return latest


__all__ = [
    "DEFAULT_JOURNAL_CONSUMERS",
    "JOURNAL_CONSUMER_WORK_DRAIN",
    "journal_consumer_status",
    "mark_work_drain_caught_up",
]
