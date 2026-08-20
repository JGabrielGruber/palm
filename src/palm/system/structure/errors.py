"""System structure errors — admission gate (0.63) and capability require (0.67)."""

from __future__ import annotations

from typing import Any

from palm.core.structure import AdmissionSnapshot, StructurePhase


class AdmissionRefusedError(RuntimeError):
    """Business that needs ground was refused — admission fail closed.

    Raised when a business path that needs admission (submit_flow, work-plane tick, …) runs while
    ``may_run_business`` is false.
    """

    def __init__(self, snapshot: AdmissionSnapshot | None = None) -> None:
        self.snapshot = snapshot
        if snapshot is None:
            msg = "admission refused: no snapshot"
        else:
            reasons = ",".join(snapshot.reasons) or "not_ready"
            msg = (
                f"admission refused: {reasons} "
                f"(phase={snapshot.phase}, definition={snapshot.definition_id!r})"
            )
        super().__init__(msg)


class CapabilityRefusedError(RuntimeError):
    """Organ required by this act is not installed — fail closed after ready.

    Raised when the organism is ready but ``has_capability(name)`` is false.
    Ready-false is :class:`AdmissionRefusedError`, not this error.
    """

    def __init__(self, snapshot: AdmissionSnapshot, name: str) -> None:
        self.snapshot = snapshot
        self.name = name
        msg = (
            f"capability refused: {name!r} not installed "
            f"(phase={snapshot.phase}, definition={snapshot.definition_id!r})"
        )
        super().__init__(msg)


def _capabilities_of(obj: Any) -> frozenset[str]:
    raw = getattr(obj, "capabilities", None)
    if raw is None:
        return frozenset()
    if isinstance(raw, str):
        return frozenset((raw,))
    try:
        return frozenset(str(x) for x in raw)
    except TypeError:
        return frozenset()


def _from_duck(obj: Any) -> AdmissionSnapshot | None:
    """Structural admission-like object → snapshot (test doubles)."""
    if obj is None:
        return None
    may = bool(getattr(obj, "may_run_business", False))
    phase = getattr(obj, "phase", None)
    if not isinstance(phase, StructurePhase):
        phase = StructurePhase.READY if may else StructurePhase.EMPTY
    caps = _capabilities_of(obj)
    if may:
        return AdmissionSnapshot(
            may_run_business=True,
            phase=phase,
            definition_id=getattr(obj, "definition_id", None),
            definition_version=getattr(obj, "definition_version", None),
            capabilities=caps,
        )
    reasons = getattr(obj, "reasons", ()) or ()
    if isinstance(reasons, str):
        reason_t = (reasons,)
    else:
        reason_t = tuple(str(r) for r in reasons) or ("not_ready",)
    return AdmissionSnapshot(
        may_run_business=False,
        phase=phase,
        definition_id=getattr(obj, "definition_id", None),
        definition_version=getattr(obj, "definition_version", None),
        reasons=reason_t,
        capabilities=caps,
    )


def coerce_admission_snapshot(source: object) -> AdmissionSnapshot | None:
    """Normalize a published admission *source* into a snapshot.

    Accepts (published admission shapes — not host dig):

    - :class:`AdmissionSnapshot`
    - zero-arg callable returning any of the below
    - object with ``admission`` attribute (snapshot, method, or duck)
    - structural duck with ``may_run_business``
    """
    if source is None:
        return None
    if isinstance(source, AdmissionSnapshot):
        return source

    # Zero-arg factory (callable that is not a class type with admission).
    if callable(source) and not isinstance(source, type):
        # Prefer objects that *are* gates (have .admission) over factories.
        if not hasattr(source, "admission"):
            try:
                return coerce_admission_snapshot(source())
            except TypeError:
                pass

    adm = getattr(source, "admission", None)
    if adm is not None:
        if isinstance(adm, AdmissionSnapshot):
            return adm
        if callable(adm) and not isinstance(adm, type):
            try:
                adm = adm()
            except TypeError:
                adm = None
            if isinstance(adm, AdmissionSnapshot):
                return adm
            if adm is not None and hasattr(adm, "may_run_business"):
                return _from_duck(adm)
        elif hasattr(adm, "may_run_business"):
            return _from_duck(adm)

    if hasattr(source, "may_run_business"):
        return _from_duck(source)
    return None


def admission_as_dict(source: object) -> dict[str, Any] | None:
    """Published snapshot as dict. Always includes ``capabilities`` (default empty)."""
    snap = coerce_admission_snapshot(source)
    if snap is None:
        return None
    return snap.to_dict()


def require_business_admission(source: object) -> AdmissionSnapshot:
    """Fail closed unless *source* publishes ready admission.

    *source* is a published gate shape (runtime shell, seat, host admission
    property, snapshot, or zero-arg factory) — product should inject one of
    these rather than dig the composition root for readiness (VISION-ASSEMBLY §3).
    Hosts without an ``admission`` attribute (test doubles) must expose one
    that reflects readiness — there is no silent bypass.

    Ready only. An act that needs an organ uses :func:`require_capability`.
    """
    snap = coerce_admission_snapshot(source)
    if snap is None:
        raise AdmissionRefusedError(None)
    if not snap.may_run_business:
        raise AdmissionRefusedError(snap)
    return snap


def require_capability(source: object, name: str) -> AdmissionSnapshot:
    """Fail closed unless *source* is ready and *name* is installed.

    Same published *source* as :func:`require_business_admission`. Coerce once
    via the ready door. Not ready → :class:`AdmissionRefusedError`. Ready but
    ``has_capability(name)`` is false → :class:`CapabilityRefusedError`.
    """
    snap = require_business_admission(source)
    if not snap.has_capability(name):
        raise CapabilityRefusedError(snap, name)
    return snap


__all__ = [
    "AdmissionRefusedError",
    "CapabilityRefusedError",
    "admission_as_dict",
    "coerce_admission_snapshot",
    "require_business_admission",
    "require_capability",
]
