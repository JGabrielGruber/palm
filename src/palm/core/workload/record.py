"""Workload — live allocation record held by WorkloadEngine (in-memory v0)."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Any

from palm.core.workload.handle import WorkloadHandle
from palm.core.workload.owner import WorkloadOwner
from palm.core.workload.result import WorkloadResult
from palm.core.workload.spec import WorkloadSpec
from palm.core.workload.status import WorkloadStatus


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class Workload:
    """Mutable live allocation. Engine is the sole writer of status transitions."""

    workload_id: str
    spec: WorkloadSpec
    status: WorkloadStatus
    runtime: str
    owner: WorkloadOwner = field(default_factory=WorkloadOwner)
    handle: WorkloadHandle | None = None
    result: WorkloadResult | None = None
    host_id: str | None = None
    message: str | None = None
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)
    idempotency_key: str | None = None
    runtime_meta: dict[str, Any] = field(default_factory=dict)
    leak_recorded: bool = False

    def touch(self) -> None:
        self.updated_at = _utc_now_iso()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "workload_id": self.workload_id,
            "spec": self.spec.to_dict(),
            "status": str(self.status),
            "runtime": self.runtime,
            "owner": self.owner.to_dict(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.handle is not None:
            data["handle"] = self.handle.to_dict()
        if self.result is not None:
            data["result"] = self.result.to_dict()
        if self.host_id is not None:
            data["host_id"] = self.host_id
        if self.message is not None:
            data["message"] = self.message
        if self.idempotency_key is not None:
            data["idempotency_key"] = self.idempotency_key
        if self.runtime_meta:
            data["runtime_meta"] = dict(self.runtime_meta)
        if self.leak_recorded:
            data["leak_recorded"] = True
        return data

    def snapshot(self) -> Workload:
        """Return a shallow copy safe to hand to callers."""
        return replace(
            self,
            owner=self.owner,
            handle=self.handle,
            result=self.result,
            runtime_meta=dict(self.runtime_meta),
        )
