"""WorkloadResult — outcome of a run or exec (not full log bodies on the bus)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class WorkloadResult:
    """Terminal outcome of a run/exec. Artifact bodies stay behind refs."""

    exit_code: int
    stdout_tail: str = ""
    stderr_tail: str = ""
    duration_s: float | None = None
    artifact_refs: tuple[str, ...] = ()
    runtime_meta: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.exit_code == 0 and self.error is None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "exit_code": self.exit_code,
            "stdout_tail": self.stdout_tail,
            "stderr_tail": self.stderr_tail,
            "artifact_refs": list(self.artifact_refs),
            "runtime_meta": dict(self.runtime_meta),
        }
        if self.duration_s is not None:
            data["duration_s"] = self.duration_s
        if self.error is not None:
            data["error"] = self.error
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkloadResult:
        refs = data.get("artifact_refs") or ()
        return cls(
            exit_code=int(data.get("exit_code", 1)),
            stdout_tail=str(data.get("stdout_tail") or ""),
            stderr_tail=str(data.get("stderr_tail") or ""),
            duration_s=(
                float(data["duration_s"]) if data.get("duration_s") is not None else None
            ),
            artifact_refs=tuple(str(r) for r in refs),
            runtime_meta=dict(data.get("runtime_meta") or {}),
            error=str(data["error"]) if data.get("error") is not None else None,
        )

    @classmethod
    def ok(
        cls,
        *,
        exit_code: int = 0,
        stdout_tail: str = "",
        stderr_tail: str = "",
        duration_s: float | None = None,
        artifact_refs: tuple[str, ...] = (),
        **runtime_meta: Any,
    ) -> WorkloadResult:
        return cls(
            exit_code=exit_code,
            stdout_tail=stdout_tail,
            stderr_tail=stderr_tail,
            duration_s=duration_s,
            artifact_refs=artifact_refs,
            runtime_meta=dict(runtime_meta),
        )

    @classmethod
    def fail(
        cls,
        error: str,
        *,
        exit_code: int = 1,
        stdout_tail: str = "",
        stderr_tail: str = "",
        **runtime_meta: Any,
    ) -> WorkloadResult:
        return cls(
            exit_code=exit_code,
            stdout_tail=stdout_tail,
            stderr_tail=stderr_tail,
            error=error,
            runtime_meta=dict(runtime_meta),
        )
