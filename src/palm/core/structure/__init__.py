"""Structure — pure organism-structure reconciler (0.63).

Core purity: no imports outside ``palm.core``.
System applies effect intents; clients use :class:`AdmissionSnapshot`.
"""

from palm.core.structure.definition import (
    CAPABILITY_JOURNAL,
    CAPABILITY_OUTBOX,
    CAPABILITY_WORK_DRAIN,
    LOCAL_ALL_IN_ONE_ID,
    LOCAL_CLI_ID,
    LOCAL_EMBEDDED_ID,
    LOCAL_MCP_ID,
    LOCAL_SERVER_ID,
    LOCAL_WORKER_ID,
    StructureDefinition,
    local_all_in_one,
    local_cli,
    local_embedded,
    local_mcp,
    local_server,
    local_worker,
    resolve_builtin_definition,
)
from palm.core.structure.engine import StructureEngine
from palm.core.structure.exceptions import (
    NoDefinitionError,
    StructureEngineError,
    StructureError,
)
from palm.core.structure.intent import EffectIntent, EffectIntentKind
from palm.core.structure.observation import Observation, ObservationKind
from palm.core.structure.policy import (
    REFUSE_HTTP_SERVER_SURFACES,
    REFUSE_PRODUCT_CATALOG_HOME,
    REFUSE_SERVER_SURFACES,
    refuse_violations,
)
from palm.core.structure.result import AssembleResult
from palm.core.structure.status import (
    AdmissionSnapshot,
    StructurePhase,
    StructureStatus,
)

__all__ = [
    "CAPABILITY_JOURNAL",
    "CAPABILITY_OUTBOX",
    "CAPABILITY_WORK_DRAIN",
    "LOCAL_ALL_IN_ONE_ID",
    "LOCAL_CLI_ID",
    "LOCAL_EMBEDDED_ID",
    "LOCAL_MCP_ID",
    "LOCAL_SERVER_ID",
    "LOCAL_WORKER_ID",
    "AdmissionSnapshot",
    "AssembleResult",
    "StructureDefinition",
    "StructureEngine",
    "StructureEngineError",
    "StructureError",
    "StructurePhase",
    "StructureStatus",
    "EffectIntent",
    "EffectIntentKind",
    "NoDefinitionError",
    "Observation",
    "ObservationKind",
    "REFUSE_HTTP_SERVER_SURFACES",
    "REFUSE_PRODUCT_CATALOG_HOME",
    "REFUSE_SERVER_SURFACES",
    "local_all_in_one",
    "local_cli",
    "local_embedded",
    "local_mcp",
    "local_server",
    "local_worker",
    "refuse_violations",
    "resolve_builtin_definition",
]
