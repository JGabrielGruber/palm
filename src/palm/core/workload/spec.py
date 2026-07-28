"""Universal, versioned WorkloadSpec — portable intent (JSON-serializable).

Commands are argv lists only (no shell strings in v1). Secrets are refs, not
inline material. See docs/VISION-0.56.md §4 and ADR-024 D2/D3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from palm.core.workload.exceptions import WorkloadSpecError

SPEC_VERSION = 1


class WorkloadKind(StrEnum):
    """Allocation kind."""

    RUN = "run"
    SERVICE = "service"
    WORKSPACE = "workspace"  # warm exec box; may alias service at runtime


class IsolationPolicy(StrEnum):
    """Where foreign work may run — not synonymous with NeonRoot."""

    HOST = "host"
    HERMETIC = "hermetic"
    BEST_EFFORT = "best_effort"


class LifecyclePolicy(StrEnum):
    """Who owns stop/reap of the allocation."""

    JOB = "job"
    SESSION = "session"
    LEASE = "lease"


@dataclass(frozen=True, slots=True)
class WorkloadPlacement:
    """Soft placement constraints on a Spec."""

    host_id: str | None = None
    runtime: str | None = None
    reject_runtimes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.host_id is not None:
            out["host_id"] = self.host_id
        if self.runtime is not None:
            out["runtime"] = self.runtime
        if self.reject_runtimes:
            out["reject_runtimes"] = list(self.reject_runtimes)
        return out

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> WorkloadPlacement:
        if not data:
            return cls()
        reject = data.get("reject_runtimes") or ()
        return cls(
            host_id=_opt_str(data.get("host_id")),
            runtime=_opt_str(data.get("runtime")),
            reject_runtimes=tuple(str(x) for x in reject),
        )


@dataclass(frozen=True, slots=True)
class WorkloadSpec:
    """Portable workload intent. Runtimes adapt; they do not redefine this language."""

    kind: WorkloadKind
    isolation: IsolationPolicy
    lifecycle: LifecyclePolicy
    command: tuple[str, ...] = ()
    image: str | None = None
    image_ref: str | None = None
    workdir: str | None = None
    seed: dict[str, Any] | None = None
    env: dict[str, str] = field(default_factory=dict)
    secrets_ref: str | None = None
    ports: tuple[dict[str, Any], ...] = ()
    health: dict[str, Any] | None = None
    timeout_s: float | None = None
    resources: dict[str, Any] = field(default_factory=dict)
    labels: dict[str, str] = field(default_factory=dict)
    placement: WorkloadPlacement = field(default_factory=WorkloadPlacement)
    mesh: dict[str, Any] | None = None
    spec_version: int = SPEC_VERSION

    def __post_init__(self) -> None:
        if self.spec_version != SPEC_VERSION:
            raise WorkloadSpecError(
                f"Unsupported spec_version {self.spec_version}; expected {SPEC_VERSION}"
            )
        if self.kind is WorkloadKind.RUN and not self.command:
            raise WorkloadSpecError("kind=run requires a non-empty command (argv list)")
        if any(not isinstance(c, str) or not c for c in self.command):
            raise WorkloadSpecError("command must be a non-empty argv list of non-empty strings")
        # Reject shell-string smell: single element containing shell metacharacters is still
        # argv, but multi-word single strings are a common mistake — leave to runtime if needed.

    @property
    def image_or_ref(self) -> str | None:
        return self.image or self.image_ref

    def to_dict(self) -> dict[str, Any]:
        """JSON-serializable dict (append-friendly schema)."""
        data: dict[str, Any] = {
            "spec_version": self.spec_version,
            "kind": str(self.kind),
            "isolation": str(self.isolation),
            "lifecycle": str(self.lifecycle),
        }
        if self.command:
            data["command"] = list(self.command)
        if self.image is not None:
            data["image"] = self.image
        if self.image_ref is not None:
            data["image_ref"] = self.image_ref
        if self.workdir is not None:
            data["workdir"] = self.workdir
        if self.seed is not None:
            data["seed"] = dict(self.seed)
        if self.env:
            data["env"] = dict(self.env)
        if self.secrets_ref is not None:
            data["secrets_ref"] = self.secrets_ref
        if self.ports:
            data["ports"] = [dict(p) for p in self.ports]
        if self.health is not None:
            data["health"] = dict(self.health)
        if self.timeout_s is not None:
            data["timeout_s"] = self.timeout_s
        if self.resources:
            data["resources"] = dict(self.resources)
        if self.labels:
            data["labels"] = dict(self.labels)
        placement = self.placement.to_dict()
        if placement:
            data["placement"] = placement
        if self.mesh is not None:
            data["mesh"] = dict(self.mesh)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkloadSpec:
        """Parse and validate a Spec from a mapping."""
        if not isinstance(data, dict):
            raise WorkloadSpecError("WorkloadSpec must be a mapping")
        unknown = set(data) - _KNOWN_FIELDS
        if unknown:
            raise WorkloadSpecError(
                f"Unknown WorkloadSpec fields (strict): {sorted(unknown)}"
            )
        try:
            kind = WorkloadKind(str(data["kind"]))
            isolation = IsolationPolicy(str(data["isolation"]))
            lifecycle = LifecyclePolicy(str(data["lifecycle"]))
        except KeyError as exc:
            raise WorkloadSpecError(f"WorkloadSpec missing required field: {exc}") from exc
        except ValueError as exc:
            raise WorkloadSpecError(str(exc)) from exc

        command_raw = data.get("command") or ()
        if isinstance(command_raw, str):
            raise WorkloadSpecError(
                "command must be an argv list, not a shell string"
            )
        command = tuple(str(c) for c in command_raw)

        ports_raw = data.get("ports") or data.get("expose") or ()
        ports = tuple(dict(p) for p in ports_raw)

        env_raw = data.get("env") or {}
        env = {str(k): str(v) for k, v in dict(env_raw).items()}

        labels_raw = data.get("labels") or {}
        labels = {str(k): str(v) for k, v in dict(labels_raw).items()}

        version = int(data.get("spec_version", SPEC_VERSION))
        timeout = data.get("timeout_s")
        return cls(
            kind=kind,
            isolation=isolation,
            lifecycle=lifecycle,
            command=command,
            image=_opt_str(data.get("image")),
            image_ref=_opt_str(data.get("image_ref")),
            workdir=_opt_str(data.get("workdir")),
            seed=dict(data["seed"]) if data.get("seed") is not None else None,
            env=env,
            secrets_ref=_opt_str(data.get("secrets_ref")),
            ports=ports,
            health=dict(data["health"]) if data.get("health") is not None else None,
            timeout_s=float(timeout) if timeout is not None else None,
            resources=dict(data.get("resources") or {}),
            labels=labels,
            placement=WorkloadPlacement.from_dict(data.get("placement")),
            mesh=dict(data["mesh"]) if data.get("mesh") is not None else None,
            spec_version=version,
        )


_KNOWN_FIELDS = frozenset(
    {
        "spec_version",
        "kind",
        "isolation",
        "lifecycle",
        "command",
        "image",
        "image_ref",
        "workdir",
        "seed",
        "env",
        "secrets_ref",
        "ports",
        "expose",
        "health",
        "timeout_s",
        "resources",
        "labels",
        "placement",
        "mesh",
    }
)


def _opt_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None
