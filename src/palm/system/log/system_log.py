"""
System log implementation — ring buffer + optional console (0.59.1a).

Levels (docs/SYSTEM-LOG.md):
  0 quiet · 1 lifecycle · 2 system · 3 operate · 4 detail · 5 trace
"""

from __future__ import annotations

import os
import sys
import threading
import time
from collections import deque
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

LEVEL_QUIET = 0
LEVEL_LIFECYCLE = 1
LEVEL_SYSTEM = 2
LEVEL_OPERATE = 3
LEVEL_DETAIL = 4
LEVEL_TRACE = 5

_LEVEL_NAMES: dict[str, int] = {
    "quiet": LEVEL_QUIET,
    "0": LEVEL_QUIET,
    "lifecycle": LEVEL_LIFECYCLE,
    "1": LEVEL_LIFECYCLE,
    "system": LEVEL_SYSTEM,
    "2": LEVEL_SYSTEM,
    "operate": LEVEL_OPERATE,
    "3": LEVEL_OPERATE,
    "detail": LEVEL_DETAIL,
    "4": LEVEL_DETAIL,
    "trace": LEVEL_TRACE,
    "5": LEVEL_TRACE,
}

_LEVEL_LABEL: dict[int, str] = {
    LEVEL_QUIET: "quiet",
    LEVEL_LIFECYCLE: "info",
    LEVEL_SYSTEM: "info",
    LEVEL_OPERATE: "info",
    LEVEL_DETAIL: "debug",
    LEVEL_TRACE: "trace",
}


def _parse_level(value: str | int | None, default: int = LEVEL_LIFECYCLE) -> int:
    if value is None:
        return default
    if isinstance(value, int):
        return max(0, min(5, value))
    key = str(value).strip().lower()
    if key in _LEVEL_NAMES:
        return _LEVEL_NAMES[key]
    try:
        return max(0, min(5, int(key)))
    except ValueError:
        return default


def _env_level() -> int:
    return _parse_level(os.environ.get("PALM_SYSTEM_LOG_LEVEL"), LEVEL_LIFECYCLE)


def _env_console_default() -> bool:
    """Console on for humans; off under pytest unless PALM_SYSTEM_LOG forces it."""
    flag = (os.environ.get("PALM_SYSTEM_LOG") or "").strip().lower()
    if flag in ("0", "false", "off", "no"):
        return False
    if flag in ("1", "true", "on", "yes"):
        return True
    if os.environ.get("PYTEST_CURRENT_TEST") or "pytest" in sys.modules:
        return False
    return True


def _env_capacity() -> int:
    raw = (os.environ.get("PALM_SYSTEM_LOG_CAPACITY") or "").strip()
    if not raw:
        return 200
    try:
        return max(10, int(raw))
    except ValueError:
        return 200


@dataclass(frozen=True)
class SystemLogRecord:
    """One system-log line (structured + human message)."""

    ts: str
    level: int
    event: str
    message: str
    fields: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        row = {
            "ts": self.ts,
            "level": self.level,
            "event": self.event,
            "message": self.message,
        }
        row.update(self.fields)
        return row

    def format_console(self) -> str:
        label = _LEVEL_LABEL.get(self.level, "info").upper()
        extra_parts: list[str] = []
        for key in ("schedule", "phase", "runtime", "mode", "reason", "duration_ms"):
            if key in self.fields and self.fields[key] is not None:
                extra_parts.append(f"{key}={self.fields[key]}")
        extra = (" " + " ".join(extra_parts)) if extra_parts else ""
        return f"{self.ts} {label} [palm] {self.event}{extra} — {self.message}"


class SystemLog:
    """Append-only process narrative with ring buffer and optional console sink."""

    def __init__(
        self,
        *,
        level: int | None = None,
        capacity: int | None = None,
        console: bool | None = None,
        stream: Any | None = None,
    ) -> None:
        self._lock = threading.RLock()
        self.level = _env_level() if level is None else _parse_level(level)
        self._capacity = _env_capacity() if capacity is None else max(10, int(capacity))
        self.console = _env_console_default() if console is None else bool(console)
        self._stream = stream if stream is not None else sys.stderr
        self._records: deque[SystemLogRecord] = deque(maxlen=self._capacity)

    @property
    def capacity(self) -> int:
        """Ring buffer capacity (max retained records)."""
        return self._capacity

    @property
    def record_count(self) -> int:
        """Current number of retained records."""
        with self._lock:
            return len(self._records)

    def seat_report(self) -> dict[str, Any]:
        """Native vitality seat report (0.61+) — process log physiology.

        Returns a plain ``palm.seat_report/1`` mapping. This seat does **not**
        import ``palm.system.vitality`` (eyes observe seats; seats do not
        depend on eyes). String literals must stay aligned with vitality schema.
        """
        return {
            "schema": "palm.seat_report/1",
            "seat_id": "system_log",
            "kind": "log",
            "present": True,
            "state": "ok",
            "load": {
                "records": self.record_count,
                "capacity": self.capacity,
                "level": self.level,
                "console": self.console,
            },
            "notes": [],
            "lineage": "native",
        }

    def configure(
        self,
        *,
        level: int | str | None = None,
        capacity: int | None = None,
        console: bool | None = None,
        stream: Any | None = None,
    ) -> None:
        with self._lock:
            if level is not None:
                self.level = _parse_level(level)
            if capacity is not None:
                self._capacity = max(10, int(capacity))
                old = list(self._records)
                self._records = deque(old[-self._capacity :], maxlen=self._capacity)
            if console is not None:
                self.console = bool(console)
            if stream is not None:
                self._stream = stream

    def clear(self) -> None:
        with self._lock:
            self._records.clear()

    def emit(
        self,
        level: int,
        event: str,
        message: str,
        **fields: Any,
    ) -> SystemLogRecord | None:
        """Record one line if ``level`` is within the configured threshold."""
        if level > self.level or self.level <= LEVEL_QUIET:
            return None
        clean = {k: v for k, v in fields.items() if v is not None}
        record = SystemLogRecord(
            ts=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            level=int(level),
            event=str(event),
            message=str(message),
            fields=clean,
        )
        with self._lock:
            self._records.append(record)
            if self.console:
                try:
                    print(record.format_console(), file=self._stream, flush=True)
                except Exception:
                    pass
        return record

    def info(self, event: str, message: str, **fields: Any) -> SystemLogRecord | None:
        return self.emit(LEVEL_LIFECYCLE, event, message, **fields)

    def system(self, event: str, message: str, **fields: Any) -> SystemLogRecord | None:
        return self.emit(LEVEL_SYSTEM, event, message, **fields)

    def operate(self, event: str, message: str, **fields: Any) -> SystemLogRecord | None:
        return self.emit(LEVEL_OPERATE, event, message, **fields)

    def phase_start(
        self,
        schedule: str,
        phase: str,
        message: str | None = None,
        **fields: Any,
    ) -> SystemLogRecord | None:
        msg = message or f"{schedule} phase {phase} start"
        return self.emit(
            LEVEL_LIFECYCLE,
            "phase.start",
            msg,
            schedule=schedule,
            phase=phase,
            **fields,
        )

    def phase_end(
        self,
        schedule: str,
        phase: str,
        *,
        duration_ms: float | None = None,
        message: str | None = None,
        **fields: Any,
    ) -> SystemLogRecord | None:
        msg = message or f"{schedule} phase {phase} ok"
        return self.emit(
            LEVEL_LIFECYCLE,
            "phase.end",
            msg,
            schedule=schedule,
            phase=phase,
            duration_ms=None if duration_ms is None else round(duration_ms, 1),
            **fields,
        )

    def phase_skip(
        self,
        schedule: str,
        phase: str,
        *,
        reason: str,
        message: str | None = None,
        **fields: Any,
    ) -> SystemLogRecord | None:
        msg = message or f"{schedule} phase {phase} skip: {reason}"
        return self.emit(
            LEVEL_LIFECYCLE,
            "phase.skip",
            msg,
            schedule=schedule,
            phase=phase,
            reason=reason,
            **fields,
        )

    def phase_fail(
        self,
        schedule: str,
        phase: str,
        *,
        reason: str,
        message: str | None = None,
        **fields: Any,
    ) -> SystemLogRecord | None:
        msg = message or f"{schedule} phase {phase} fail: {reason}"
        return self.emit(
            LEVEL_LIFECYCLE,
            "phase.fail",
            msg,
            schedule=schedule,
            phase=phase,
            reason=reason,
            **fields,
        )

    @contextmanager
    def phase(
        self,
        schedule: str,
        phase: str,
        *,
        message: str | None = None,
        **fields: Any,
    ) -> Iterator[None]:
        """Time a phase; emit start/end or fail."""
        self.phase_start(schedule, phase, message=message, **fields)
        t0 = time.perf_counter()
        try:
            yield
        except Exception as exc:
            self.phase_fail(
                schedule,
                phase,
                reason=f"{type(exc).__name__}: {exc}",
                **fields,
            )
            raise
        else:
            self.phase_end(
                schedule,
                phase,
                duration_ms=(time.perf_counter() - t0) * 1000.0,
                **fields,
            )

    def recent(self, *, limit: int | None = None) -> list[SystemLogRecord]:
        with self._lock:
            rows = list(self._records)
        if limit is not None:
            return rows[-max(0, int(limit)) :]
        return rows

    def recent_messages(self, *, limit: int | None = None) -> list[str]:
        return [r.message for r in self.recent(limit=limit)]

    def events(self, *, limit: int | None = None) -> list[str]:
        return [r.event for r in self.recent(limit=limit)]


_default: SystemLog | None = None
_default_lock = threading.Lock()


def get_system_log() -> SystemLog:
    """Process-wide system log (lazy default from env)."""
    global _default
    if _default is not None:
        return _default
    with _default_lock:
        if _default is None:
            _default = SystemLog()
        return _default


def configure_system_log(**kwargs: Any) -> SystemLog:
    """Configure (or create) the process-wide system log."""
    log = get_system_log()
    log.configure(**kwargs)
    return log


def reset_system_log_for_tests() -> SystemLog:
    """Replace the process-wide log (tests only)."""
    global _default
    with _default_lock:
        _default = SystemLog(console=False, level=LEVEL_OPERATE, capacity=200)
        return _default
