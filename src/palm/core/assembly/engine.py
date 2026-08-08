"""AssemblyEngine — pure desired-structure reconciler.

No sockets. No OS spawn. No business jobs. System applies effect intents;
clients read admission. Floor: embedded DNA with empty places becomes READY
after tick when not blocked.
"""

from __future__ import annotations

import threading
from typing import Any

from palm.core.assembly.definition import AssemblyDefinition
from palm.core.assembly.exceptions import AssemblyEngineError
from palm.core.assembly.intent import EffectIntent, EffectIntentKind
from palm.core.assembly.observation import Observation, ObservationKind
from palm.core.assembly.result import AssembleResult
from palm.core.assembly.status import (
    AdmissionSnapshot,
    AssemblyPhase,
    AssemblyStatus,
)
from palm.core.base import BasePalmEngine


class AssemblyEngine(BasePalmEngine):
    """In-memory assembly reconciler (durable projection later in system)."""

    def __init__(self) -> None:
        super().__init__(name="assembly")
        self._lock = threading.RLock()
        self._definition: AssemblyDefinition | None = None
        self._phase: AssemblyPhase = AssemblyPhase.EMPTY
        self._places_ready: set[str] = set()
        self._block_reasons: list[str] = []
        self._truth_home_up: bool = True
        self._pending_ensure: set[str] = set()

    def _do_initialize(self, **options: Any) -> None:
        return

    def _do_shutdown(self) -> None:
        with self._lock:
            self._definition = None
            self._phase = AssemblyPhase.EMPTY
            self._places_ready.clear()
            self._block_reasons.clear()
            self._truth_home_up = True
            self._pending_ensure.clear()

    # --- public API ---------------------------------------------------------

    def receive_definition(
        self,
        definition: AssemblyDefinition,
        *,
        force: bool = False,
    ) -> AdmissionSnapshot:
        """Load (or replace) desired structure. Resets readiness under new law.

        When the same id/version is already READY, returns without reset unless
        *force* is True (0.63.18 reassemble edge — external structure change).
        """
        if not definition.id:
            raise AssemblyEngineError("assembly definition id must be non-empty")
        with self._lock:
            same = (
                not force
                and self._definition is not None
                and self._definition.id == definition.id
                and self._definition.version == definition.version
                and self._phase is AssemblyPhase.READY
            )
            if same:
                return self._status_unlocked().admission()

            had_ready = self._phase is AssemblyPhase.READY
            self._definition = definition
            self._places_ready.clear()
            self._block_reasons.clear()
            self._truth_home_up = True
            self._pending_ensure.clear()
            self._phase = (
                AssemblyPhase.INVALIDATED if had_ready else AssemblyPhase.RECEIVED
            )
            return self._status_unlocked().admission()

    def invalidate(self, *, reason: str = "invalidated") -> AdmissionSnapshot:
        """Void current readiness; keep definition. Requires reassemble to recover."""
        with self._lock:
            if self._definition is None:
                self._phase = AssemblyPhase.EMPTY
                return self._status_unlocked().admission()
            if self._phase is not AssemblyPhase.EMPTY:
                self._phase = AssemblyPhase.INVALIDATED
                # reason is visible via phase; optional note for callers
                _ = reason
            return self._status_unlocked().admission()

    def observe(self, observation: Observation) -> AdmissionSnapshot:
        """Fold one structure fact. Does not apply effects (call tick)."""
        with self._lock:
            self._apply_observation_unlocked(observation)
            return self._status_unlocked().admission()

    def tick(self) -> AssembleResult:
        """Reconcile once: emit intents, advance phase when facts allow."""
        with self._lock:
            before = self._status_unlocked()
            intents: list[EffectIntent] = []
            notes: list[str] = []

            if self._definition is None:
                status = self._status_unlocked()
                admission = status.admission()
                return AssembleResult(
                    status=status,
                    admission=admission,
                    intents=(),
                    changed=False,
                    notes=("no_definition",),
                )

            # Truth home down blocks business even if places look ready.
            if not self._truth_home_up:
                self._phase = AssemblyPhase.BLOCKED
                if "truth_home_down" not in self._block_reasons:
                    self._block_reasons.append("truth_home_down")
                status = self._status_unlocked()
                admission = status.admission()
                return AssembleResult(
                    status=status,
                    admission=admission,
                    intents=(),
                    changed=before.phase != status.phase
                    or before.admission().may_run_business != admission.may_run_business,
                    notes=("blocked_truth_home",),
                )

            # Clear truth_home block if up again
            self._block_reasons = [r for r in self._block_reasons if r != "truth_home_down"]

            if self._phase in (
                AssemblyPhase.RECEIVED,
                AssemblyPhase.INVALIDATED,
                AssemblyPhase.BLOCKED,
            ):
                # Leave BLOCKED only when block_reasons empty after filter above
                if self._phase is AssemblyPhase.BLOCKED and self._block_reasons:
                    status = self._status_unlocked()
                    admission = status.admission()
                    return AssembleResult(
                        status=status,
                        admission=admission,
                        intents=(),
                        changed=False,
                        notes=("still_blocked",),
                    )
                self._phase = AssemblyPhase.ASSEMBLING
                notes.append("enter_assembling")

            missing = self._missing_places_unlocked()
            for place in missing:
                if place not in self._pending_ensure:
                    intents.append(
                        EffectIntent(
                            kind=EffectIntentKind.ENSURE_PLACE,
                            target=place,
                        )
                    )
                    self._pending_ensure.add(place)
                    notes.append(f"ensure_place:{place}")

            if missing:
                self._phase = AssemblyPhase.ASSEMBLING
            else:
                # No places (embedded floor) or all places ready → definition-ready
                self._phase = AssemblyPhase.READY
                self._pending_ensure.clear()
                notes.append("definition_ready")

            status = self._status_unlocked()
            admission = status.admission()
            changed = (
                before.phase != status.phase
                or before.admission().may_run_business != admission.may_run_business
                or bool(intents)
            )
            return AssembleResult(
                status=status,
                admission=admission,
                intents=tuple(intents),
                changed=changed,
                notes=tuple(notes),
            )

    def status(self) -> AssemblyStatus:
        with self._lock:
            return self._status_unlocked()

    def admission(self) -> AdmissionSnapshot:
        with self._lock:
            return self._status_unlocked().admission()

    def definition(self) -> AssemblyDefinition | None:
        with self._lock:
            return self._definition

    # --- internals ----------------------------------------------------------

    def _missing_places_unlocked(self) -> tuple[str, ...]:
        if self._definition is None:
            return ()
        required = self._definition.places_required
        return tuple(p for p in required if p not in self._places_ready)

    def _status_unlocked(self) -> AssemblyStatus:
        definition = self._definition
        missing = self._missing_places_unlocked()
        return AssemblyStatus(
            phase=self._phase,
            definition_id=definition.id if definition else None,
            definition_version=definition.version if definition else None,
            places_ready=frozenset(self._places_ready),
            places_missing=missing,
            block_reasons=tuple(self._block_reasons),
            truth_home_up=self._truth_home_up,
        )

    def _apply_observation_unlocked(self, observation: Observation) -> None:
        kind = observation.kind
        target = observation.target

        if kind is ObservationKind.PLACE_READY:
            if target:
                self._places_ready.add(target)
                self._pending_ensure.discard(target)
            # Drop place_failed for this target
            self._block_reasons = [
                r
                for r in self._block_reasons
                if r != f"place_failed:{target}"
            ]
        elif kind is ObservationKind.PLACE_FAILED:
            if target:
                self._places_ready.discard(target)
                reason = f"place_failed:{target}"
                if reason not in self._block_reasons:
                    self._block_reasons.append(reason)
                self._phase = AssemblyPhase.BLOCKED
        elif kind is ObservationKind.PLACE_GONE:
            if target:
                self._places_ready.discard(target)
                if self._phase is AssemblyPhase.READY:
                    self._phase = AssemblyPhase.INVALIDATED
        elif kind is ObservationKind.TRUTH_HOME_UP:
            self._truth_home_up = True
            self._block_reasons = [
                r for r in self._block_reasons if r != "truth_home_down"
            ]
        elif kind is ObservationKind.TRUTH_HOME_DOWN:
            self._truth_home_up = False
            if "truth_home_down" not in self._block_reasons:
                self._block_reasons.append("truth_home_down")
            if self._phase is AssemblyPhase.READY:
                self._phase = AssemblyPhase.BLOCKED
        elif kind is ObservationKind.PROJECTION_FAILED:
            reason = f"projection_failed:{target or 'default'}"
            if reason not in self._block_reasons:
                self._block_reasons.append(reason)
            if self._phase is AssemblyPhase.READY:
                self._phase = AssemblyPhase.BLOCKED
        elif kind is ObservationKind.PROJECTION_LOADED:
            # Floor: no projection required; clear matching fail reason
            reason = f"projection_failed:{target or 'default'}"
            self._block_reasons = [r for r in self._block_reasons if r != reason]
        elif kind is ObservationKind.STRUCTURE_SEED_FAILED:
            reason = "structure_seed_failed"
            if reason not in self._block_reasons:
                self._block_reasons.append(reason)
            self._phase = AssemblyPhase.BLOCKED
        elif kind is ObservationKind.STRUCTURE_SEED_FINISHED:
            self._block_reasons = [
                r for r in self._block_reasons if r != "structure_seed_failed"
            ]
        elif kind is ObservationKind.STRUCTURE_POLICY_VIOLATION:
            reason = target or "refuse:policy"
            if reason not in self._block_reasons:
                self._block_reasons.append(reason)
            self._phase = AssemblyPhase.BLOCKED
        elif kind is ObservationKind.STRUCTURE_POLICY_CLEARED:
            if target:
                self._block_reasons = [
                    r for r in self._block_reasons if r != target
                ]
            else:
                self._block_reasons = [
                    r for r in self._block_reasons if not r.startswith("refuse:")
                ]
        elif kind is ObservationKind.SEAT_BOUND:
            pass  # optional floor; no phase change yet
        else:
            # Exhaustiveness for future kinds — ignore unknown safely
            pass


__all__ = ["AssemblyEngine"]
