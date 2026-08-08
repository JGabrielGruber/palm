"""Assembly — pure organism-structure reconciler (0.63).

Core purity: no imports outside ``palm.core``.
System applies effect intents; clients use :class:`AdmissionSnapshot`.
"""

from palm.core.assembly.definition import (
    LOCAL_ALL_IN_ONE_ID,
    LOCAL_CLI_ID,
    LOCAL_EMBEDDED_ID,
    LOCAL_MCP_ID,
    LOCAL_SERVER_ID,
    LOCAL_WORKER_ID,
    AssemblyDefinition,
    local_all_in_one,
    local_cli,
    local_embedded,
    local_mcp,
    local_server,
    local_worker,
    resolve_builtin_dna,
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
    "LOCAL_ALL_IN_ONE_ID",
    "LOCAL_CLI_ID",
    "LOCAL_EMBEDDED_ID",
    "LOCAL_MCP_ID",
    "LOCAL_SERVER_ID",
    "LOCAL_WORKER_ID",
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
    "local_all_in_one",
    "local_cli",
    "local_embedded",
    "local_mcp",
    "local_server",
    "local_worker",
    "resolve_builtin_dna",
]
