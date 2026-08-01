"""Continuous outbox poll as a supervised system service (0.60.6)."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from palm.common.events import OutboxProcessor, OutboxStore


class OutboxLoopService:
    """Poll :class:`OutboxProcessor` on a background thread.

    Implements :class:`~palm.system.supervisor.service.SystemService` by
    convention (``name`` / ``start`` / ``stop`` / ``status``).
    """

    def __init__(
        self,
        processor: OutboxProcessor,
        store: OutboxStore,
        *,
        poll_interval: float = 0.5,
        batch_size: int = 50,
        recover_on_start: bool = True,
    ) -> None:
        self._processor = processor
        self._store = store
        self._poll_interval = max(0.05, float(poll_interval))
        self._batch_size = max(1, int(batch_size))
        self._recover_on_start = bool(recover_on_start)
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._running = False

    @property
    def name(self) -> str:
        return "outbox"

    @property
    def is_running(self) -> bool:
        return (
            self._running
            and self._thread is not None
            and self._thread.is_alive()
        )

    def start(self) -> None:
        if self._running:
            return
        if self._recover_on_start:
            try:
                self._processor.recover_pending(replay_handlers=False)
            except Exception:
                pass
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._poll_loop,
            name="palm-outbox-loop",
            daemon=True,
        )
        self._thread.start()
        self._running = True

    def stop(self) -> None:
        if not self._running:
            return
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        self._thread = None
        self._running = False

    def process_once(self) -> int:
        return int(
            self._processor.process_batch(limit=self._batch_size) or 0
        )

    def status(self) -> dict[str, Any]:
        pending = 0
        try:
            pending = int(self._store.pending_count())
        except Exception:
            pending = -1
        return {
            "name": self.name,
            "running": self.is_running,
            "pending": pending,
            "poll_interval": self._poll_interval,
            "batch_size": self._batch_size,
        }

    def _poll_loop(self) -> None:
        while not self._stop.wait(self._poll_interval):
            try:
                self._processor.process_batch(limit=self._batch_size)
            except Exception:
                continue


__all__ = ["OutboxLoopService"]
