"""System assembly — loop, effect port, seat, admission on the shell (0.63)."""

from palm.system.assembly.effects import AssemblyEffectPort, RecordingEffectPort
from palm.system.assembly.errors import (
    AdmissionRefusedError,
    require_business_admission,
)
from palm.system.assembly.loop import (
    DEFAULT_MAX_TICKS,
    AssembleLoopResult,
    assemble_until_steady,
    load_and_assemble,
)
from palm.system.assembly.seat import AssemblySeat
from palm.system.assembly.seed import (
    dna_id_for_boot_mode,
    dna_id_for_composition,
    resolve_seed_dna,
    seed_assembly_options_from_host,
)

__all__ = [
    "DEFAULT_MAX_TICKS",
    "AdmissionRefusedError",
    "AssembleLoopResult",
    "AssemblyEffectPort",
    "AssemblySeat",
    "RecordingEffectPort",
    "assemble_until_steady",
    "dna_id_for_boot_mode",
    "dna_id_for_composition",
    "load_and_assemble",
    "require_business_admission",
    "resolve_seed_dna",
    "seed_assembly_options_from_host",
]
