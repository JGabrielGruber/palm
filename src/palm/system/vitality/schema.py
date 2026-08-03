"""
Vitality schema constants — versioned seat-report contract (0.61.1).

Stable names for kinds, states, lineage, and the schema id. Growth adds
fields behind a new schema version; do not silently reshape ``/1``.
"""

from __future__ import annotations

from typing import Final, Literal

# ── Schema ───────────────────────────────────────────────────────────────────

SEAT_REPORT_SCHEMA: Final[str] = "palm.seat_report/1"
"""Versioned seat-report document id. Bump only with intentional migration."""

# ── Kind ─────────────────────────────────────────────────────────────────────

SeatKindName = Literal[
    "plane",
    "supervisor",
    "supervisor_service",
    "port",
    "log",
    "boot",
    "engine",
    "other",
]

KIND_PLANE: Final[str] = "plane"
KIND_SUPERVISOR: Final[str] = "supervisor"
KIND_SUPERVISOR_SERVICE: Final[str] = "supervisor_service"
KIND_PORT: Final[str] = "port"
KIND_LOG: Final[str] = "log"
KIND_BOOT: Final[str] = "boot"
KIND_ENGINE: Final[str] = "engine"
KIND_OTHER: Final[str] = "other"

KNOWN_KINDS: Final[frozenset[str]] = frozenset(
    {
        KIND_PLANE,
        KIND_SUPERVISOR,
        KIND_SUPERVISOR_SERVICE,
        KIND_PORT,
        KIND_LOG,
        KIND_BOOT,
        KIND_ENGINE,
        KIND_OTHER,
    }
)

# ── State ────────────────────────────────────────────────────────────────────

SeatStateName = Literal["ok", "degraded", "absent", "error", "skipped"]

STATE_OK: Final[str] = "ok"
STATE_DEGRADED: Final[str] = "degraded"
STATE_ABSENT: Final[str] = "absent"
STATE_ERROR: Final[str] = "error"
STATE_SKIPPED: Final[str] = "skipped"

KNOWN_STATES: Final[frozenset[str]] = frozenset(
    {
        STATE_OK,
        STATE_DEGRADED,
        STATE_ABSENT,
        STATE_ERROR,
        STATE_SKIPPED,
    }
)

# ── Lineage ──────────────────────────────────────────────────────────────────

SeatLineageName = Literal["native", "adapter"]

LINEAGE_NATIVE: Final[str] = "native"
LINEAGE_ADAPTER: Final[str] = "adapter"

KNOWN_LINEAGES: Final[frozenset[str]] = frozenset(
    {LINEAGE_NATIVE, LINEAGE_ADAPTER}
)

# ── Well-known seat ids (discovery seeds — not a closed forever menu) ───────
# New seats appear by attachment + probe registration. These ids stay stable
# for the seeds Palm attaches after system start (0.57–0.60 living graph).

SEAT_WAIT_PLANE: Final[str] = "wait_plane"
SEAT_SESSION_PLANE: Final[str] = "session_plane"
SEAT_WORK_PLANE: Final[str] = "work_plane"
SEAT_SUPERVISOR: Final[str] = "supervisor"
SEAT_EXECUTION: Final[str] = "execution"
SEAT_SYSTEM_LOG: Final[str] = "system_log"
SEAT_BOOT_MEMBERSHIP: Final[str] = "boot_membership"

# Supervisor service seats use: supervisor.<service_name>
SUPERVISOR_SERVICE_PREFIX: Final[str] = "supervisor."

# ── Walk options / capability seed (registry body lands 0.61.2) ─────────────

CAPABILITY_SEAT_WALK: Final[str] = "seat_walk"
"""Capability id reserved for projection/registry (0.61.2+). Walk exists now."""


def supervisor_service_seat_id(service_name: str) -> str:
    """Stable seat id for one supervised continuous service."""
    name = str(service_name or "").strip()
    if not name:
        raise ValueError("supervisor service name required")
    if name.startswith(SUPERVISOR_SERVICE_PREFIX):
        return name
    return f"{SUPERVISOR_SERVICE_PREFIX}{name}"


__all__ = [
    "CAPABILITY_SEAT_WALK",
    "KIND_BOOT",
    "KIND_ENGINE",
    "KIND_LOG",
    "KIND_OTHER",
    "KIND_PLANE",
    "KIND_PORT",
    "KIND_SUPERVISOR",
    "KIND_SUPERVISOR_SERVICE",
    "KNOWN_KINDS",
    "KNOWN_LINEAGES",
    "KNOWN_STATES",
    "LINEAGE_ADAPTER",
    "LINEAGE_NATIVE",
    "SEAT_BOOT_MEMBERSHIP",
    "SEAT_EXECUTION",
    "SEAT_REPORT_SCHEMA",
    "SEAT_SESSION_PLANE",
    "SEAT_SUPERVISOR",
    "SEAT_SYSTEM_LOG",
    "SEAT_WAIT_PLANE",
    "SEAT_WORK_PLANE",
    "STATE_ABSENT",
    "STATE_DEGRADED",
    "STATE_ERROR",
    "STATE_OK",
    "STATE_SKIPPED",
    "SUPERVISOR_SERVICE_PREFIX",
    "SeatKindName",
    "SeatLineageName",
    "SeatStateName",
    "supervisor_service_seat_id",
]
