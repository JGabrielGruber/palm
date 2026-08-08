"""System assembly errors — admission gate (0.63)."""

from __future__ import annotations

from palm.core.assembly import AdmissionSnapshot, AssemblyPhase


class AdmissionRefusedError(RuntimeError):
    """Business that needs ground was refused — admission fail closed.

    Raised when a citizen path (submit_flow, work-plane tick, …) runs while
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


def require_business_admission(runtime: object) -> AdmissionSnapshot:
    """Fail closed unless *runtime* publishes ready admission.

    Hosts without an ``admission`` attribute (test doubles) must expose one
    that reflects readiness — there is no silent bypass.
    """
    snap = getattr(runtime, "admission", None)
    if snap is None:
        raise AdmissionRefusedError(None)
    if not isinstance(snap, AdmissionSnapshot):
        # Structural double with admission-like object
        may = bool(getattr(snap, "may_run_business", False))
        if not may:
            raise AdmissionRefusedError(AdmissionSnapshot.empty())
        phase = getattr(snap, "phase", None)
        if not isinstance(phase, AssemblyPhase):
            phase = AssemblyPhase.READY
        return AdmissionSnapshot(
            may_run_business=True,
            phase=phase,
            definition_id=getattr(snap, "definition_id", None),
            definition_version=getattr(snap, "definition_version", None),
        )
    if not snap.may_run_business:
        raise AdmissionRefusedError(snap)
    return snap


__all__ = [
    "AdmissionRefusedError",
    "require_business_admission",
]
