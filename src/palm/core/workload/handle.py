"""WorkloadHandle — live service/workspace connection hints for providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class WorkloadHandle:
    """Handle for a READY service/workspace. Consumption stays with providers."""

    workload_id: str
    base_url: str | None = None
    endpoints: dict[str, str] = field(default_factory=dict)
    connection_hints: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"workload_id": self.workload_id}
        if self.base_url is not None:
            data["base_url"] = self.base_url
        if self.endpoints:
            data["endpoints"] = dict(self.endpoints)
        if self.connection_hints:
            data["connection_hints"] = dict(self.connection_hints)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkloadHandle:
        return cls(
            workload_id=str(data["workload_id"]),
            base_url=str(data["base_url"]) if data.get("base_url") is not None else None,
            endpoints={str(k): str(v) for k, v in dict(data.get("endpoints") or {}).items()},
            connection_hints=dict(data.get("connection_hints") or {}),
        )
