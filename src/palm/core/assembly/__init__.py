"""Assembly — pure organism-structure reconciler (0.63).

Core purity: no imports outside ``palm.core``.
System applies effect intents; clients use :class:`AdmissionSnapshot`.
"""

from palm.core.assembly.definition import (
    LOCAL_EMBEDDED_ID,
    AssemblyDefinition,
    local_embedded,
)
from palm.core.assembly.engine import AssemblyEngine
from palm.core.assembly.exceptions import (
    AssemblyEngineError,
    AssemblyError,
    NoDefinitionError,
)
from palm.core.assembly.intent import EffectIntent, EffectIntentKind
from palm.core.assembly.observation import Observation, ObservationKind
from palm.core.assembly.result import AssembleResult
from palm.core.assembly.status import (
    AdmissionSnapshot,
    AssemblyPhase,
    AssemblyStatus,
)

__all__ = [
    "LOCAL_EMBEDDED_ID",
    "AdmissionSnapshot",
    "AssembleResult",
    "AssemblyDefinition",
    "AssemblyEngine",
    "AssemblyEngineError",
    "AssemblyError",
    "AssemblyPhase",
    "AssemblyStatus",
    "EffectIntent",
    "EffectIntentKind",
    "NoDefinitionError",
    "Observation",
    "ObservationKind",
    "local_embedded",
]
