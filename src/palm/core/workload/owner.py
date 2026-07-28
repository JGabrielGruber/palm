"""Ownership binding — who started a workload and when it must stop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class WorkloadOwner:
    """Mandatory ownership record (VISION §5.1). At least one id should be set."""

    job_id: str | None = None
    instance_id: str | None = None
    lease_id: str | None = None
    session_id: str | None = None
    created_by_palm: bool = True

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"created_by_palm": self.created_by_palm}
        if self.job_id is not None:
            data["job_id"] = self.job_id
        if self.instance_id is not None:
            data["instance_id"] = self.instance_id
        if self.lease_id is not None:
            data["lease_id"] = self.lease_id
        if self.session_id is not None:
            data["session_id"] = self.session_id
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> WorkloadOwner:
        if not data:
            return cls()
        return cls(
            job_id=_opt(data.get("job_id")),
            instance_id=_opt(data.get("instance_id")),
            lease_id=_opt(data.get("lease_id")),
            session_id=_opt(data.get("session_id")),
            created_by_palm=bool(data.get("created_by_palm", True)),
        )

    def matches(
        self,
        *,
        job_id: str | None = None,
        instance_id: str | None = None,
        lease_id: str | None = None,
        session_id: str | None = None,
    ) -> bool:
        """True if any provided filter matches the corresponding owner field."""
        checks: list[bool] = []
        if job_id is not None:
            checks.append(self.job_id == job_id)
        if instance_id is not None:
            checks.append(self.instance_id == instance_id)
        if lease_id is not None:
            checks.append(self.lease_id == lease_id)
        if session_id is not None:
            checks.append(self.session_id == session_id)
        return any(checks) if checks else True


def _opt(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None
