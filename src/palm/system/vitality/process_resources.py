"""
Process resources — host-process load sample (0.61.8).

**Law (ADR-030 / VISION-0.61):**
  - Observation only — no start/continue, no second metrics write path.
  - Stdlib first (``resource``, ``os``, ``threading``; Linux ``/proc`` when present).
  - Honest units and sources — do not invent cross-platform RSS without labeling.
  - Cheap: safe/test modes may keep this enabled; cost stays ``cheap``.

**Not law:** shame scores, health grades, or “is Palm healthy?” from RSS alone.
Product present may interpret; system only reports measured facts.
"""

from __future__ import annotations

import os
import platform
import sys
import threading
from datetime import UTC, datetime
from typing import Any

from palm.system.vitality.capability import CapabilityFragment, SampleContext
from palm.system.vitality.schema import CAPABILITY_PROCESS_RESOURCES

try:
    import resource as _resource
except ImportError:  # pragma: no cover — rare (non-Unix)
    _resource = None  # type: ignore[assignment]


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _maxrss_unit() -> str:
    """``resource.ru_maxrss`` unit differs by platform (POSIX historic mess).

    Linux/BSD: kilobytes. Darwin/macOS: bytes.
    """
    sysname = platform.system().lower()
    if sysname == "darwin":
        return "bytes"
    return "kilobytes"


def _sample_rusage() -> dict[str, Any] | None:
    if _resource is None:
        return None
    try:
        usage = _resource.getrusage(_resource.RUSAGE_SELF)
    except Exception:
        return None
    return {
        "source": "resource.getrusage",
        "cpu_user_s": float(usage.ru_utime),
        "cpu_system_s": float(usage.ru_stime),
        "max_rss": int(usage.ru_maxrss),
        "max_rss_unit": _maxrss_unit(),
        "page_faults_soft": int(getattr(usage, "ru_minflt", 0) or 0),
        "page_faults_hard": int(getattr(usage, "ru_majflt", 0) or 0),
        "voluntary_ctx": int(getattr(usage, "ru_nvcsw", 0) or 0),
        "involuntary_ctx": int(getattr(usage, "ru_nivcsw", 0) or 0),
    }


def _parse_proc_status_kb(raw: str) -> int | None:
    """Parse ``VmRSS:  1234 kB`` style lines → integer kilobytes."""
    parts = raw.split()
    if len(parts) < 2:
        return None
    try:
        value = int(parts[1])
    except (TypeError, ValueError):
        return None
    unit = parts[2].lower() if len(parts) > 2 else "kb"
    if unit in {"kb", "kib"}:
        return value
    if unit in {"mb", "mib"}:
        return value * 1024
    if unit in {"b", "bytes"}:
        return max(1, value // 1024) if value >= 1024 else (1 if value > 0 else 0)
    return value


def _sample_proc_self() -> dict[str, Any] | None:
    """Linux current RSS/VMS when ``/proc/self/status`` is readable."""
    path = "/proc/self/status"
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        return None

    wanted = {
        "VmRSS": "rss_kb",
        "VmSize": "vms_kb",
        "VmPeak": "peak_vms_kb",
        "VmHWM": "peak_rss_kb",
        "Threads": "threads",
    }
    out: dict[str, Any] = {"source": "proc_self_status"}
    for line in lines:
        key, _, rest = line.partition(":")
        key = key.strip()
        if key not in wanted:
            continue
        field = wanted[key]
        rest = rest.strip()
        if field == "threads":
            try:
                out[field] = int(rest.split()[0])
            except (ValueError, IndexError):
                continue
        else:
            parsed = _parse_proc_status_kb(rest)
            if parsed is not None:
                out[field] = parsed
    if len(out) <= 1:
        return None
    return out


def sample_process_resources(
    _instance: Any, ctx: SampleContext
) -> CapabilityFragment:
    """Optional observe: process RSS/CPU/threads (stdlib).

    *instance* is unused — process scope is the host OS process that holds
    the live system, not a seat attribute.
    """
    # Mode gate hook: bag can force-skip without unregistering.
    if ctx.bag.get("process_resources_skip"):
        return CapabilityFragment.skipped(
            CAPABILITY_PROCESS_RESOURCES,
            "bag:process_resources_skip",
            meta={"capability": CAPABILITY_PROCESS_RESOURCES},
        )

    sources: list[str] = []
    notes: list[str] = []
    rusage = _sample_rusage()
    proc = _sample_proc_self()

    if rusage is not None:
        sources.append("resource")
    if proc is not None:
        sources.append("proc_status")

    if rusage is None and proc is None:
        return CapabilityFragment.error(
            CAPABILITY_PROCESS_RESOURCES,
            "no_resource_sources",
            meta={
                "capability": CAPABILITY_PROCESS_RESOURCES,
                "platform": sys.platform,
            },
        )

    threads_active = threading.active_count()
    memory: dict[str, Any] = {}
    cpu: dict[str, Any] = {}

    if rusage is not None:
        cpu["user_s"] = rusage["cpu_user_s"]
        cpu["system_s"] = rusage["cpu_system_s"]
        memory["max_rss"] = rusage["max_rss"]
        memory["max_rss_unit"] = rusage["max_rss_unit"]
        # Peak from rusage when proc does not give HWM.
        if proc is None or "peak_rss_kb" not in proc:
            if rusage["max_rss_unit"] == "kilobytes":
                memory["peak_rss_kb"] = rusage["max_rss"]
            elif rusage["max_rss_unit"] == "bytes":
                memory["peak_rss_kb"] = max(1, int(rusage["max_rss"]) // 1024)

    if proc is not None:
        if "rss_kb" in proc:
            memory["rss_kb"] = proc["rss_kb"]
        if "vms_kb" in proc:
            memory["vms_kb"] = proc["vms_kb"]
        if "peak_rss_kb" in proc:
            memory["peak_rss_kb"] = proc["peak_rss_kb"]
        if "peak_vms_kb" in proc:
            memory["peak_vms_kb"] = proc["peak_vms_kb"]

    # Prefer current RSS when known; else peak labeled honestly.
    if "rss_kb" in memory:
        memory["primary_rss_kb"] = memory["rss_kb"]
        memory["primary_rss_kind"] = "current"
    elif "peak_rss_kb" in memory:
        memory["primary_rss_kb"] = memory["peak_rss_kb"]
        memory["primary_rss_kind"] = "peak"
        notes.append("rss_is_peak_not_current")
    else:
        notes.append("rss_unavailable")

    data: dict[str, Any] = {
        "pid": os.getpid(),
        "platform": sys.platform,
        "system": platform.system(),
        "threads": {
            "active_count": threads_active,
            "proc_threads": (proc or {}).get("threads"),
        },
        "cpu": cpu,
        "memory": memory,
        "sources": sources,
        "sample_ts": _now_iso(),
        "raw": {
            "rusage": rusage,
            "proc_status": proc,
        },
    }

    summary = {
        "pid": data["pid"],
        "threads_active": threads_active,
        "primary_rss_kb": memory.get("primary_rss_kb"),
        "primary_rss_kind": memory.get("primary_rss_kind"),
        "cpu_user_s": cpu.get("user_s"),
        "cpu_system_s": cpu.get("system_s"),
        "sources": list(sources),
    }
    data["summary"] = summary

    return CapabilityFragment.ok(
        CAPABILITY_PROCESS_RESOURCES,
        data,
        notes=notes,
        meta={
            "capability": CAPABILITY_PROCESS_RESOURCES,
            "sample_source": "+".join(sources) if sources else "none",
        },
    )


__all__ = [
    "sample_process_resources",
]
