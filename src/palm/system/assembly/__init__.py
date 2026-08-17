"""System assembly — loop, effect port, seat, admission on the shell (0.63)."""

from palm.system.assembly.access import admission_source_from_runtime_resolver
from palm.system.assembly.effects import EffectPort, RecordingEffectPort
from palm.system.assembly.errors import (
    AdmissionRefusedError,
    coerce_admission_snapshot,
    require_business_admission,
)
from palm.system.assembly.hands import LOCAL_CAPABILITY_HANDS, CapabilitySeats
from palm.system.assembly.host_bind import (
    bind_host_structure_to_seat,
    default_structure_effects,
    place_effect_port,
    resolve_workload_engine,
    workload_spawn_hands,
)
from palm.system.assembly.inventory import (
    GATED_PATHS,
    READINESS_EDGES,
    admission_inventory,
    admission_inventory_snapshot,
    open_residual_edges,
    paid_readiness_edges,
)
from palm.system.assembly.loop import (
    DEFAULT_MAX_TICKS,
    AssembleLoopResult,
    assemble_until_steady,
    load_and_assemble,
)
from palm.system.assembly.materialize import (
    apply_local_capabilities,
    definition_lists_work_drain,
)
from palm.system.assembly.place_registry import InProcessPlaceRegistry, PlaceEffectPort
from palm.system.assembly.place_spawn import (
    InProcessPlaceSpawn,
    OsProcessRegistry,
    PlaceSpawnPort,
    PlaceSpawnResult,
    RegisteredPlaceSpawn,
    fail_closed_os_ensure,
    os_prefix_spawn_port,
)
from palm.system.assembly.seat import AssemblySeat
from palm.system.assembly.seed import (
    ALWAYS_ON_MEMBERSHIP_CAPABILITIES,
    MEMBERSHIP_CAPABILITY_SEEDS,
    PACKAGING_ENV_SPIRIT,
    STRUCTURE_SEED_ENV,
    boot_mode_name_for_deployment,
    definition_id_for_boot_mode,
    definition_id_for_composition,
    definition_id_from_settings,
    membership_capabilities_from_settings,
    resolve_seed_definition,
    seed_assembly_options_from_host,
)
from palm.system.assembly.structure_effects import StructureEffectPort
from palm.system.assembly.workload_place import (
    WorkloadPlaceSpawn,
    combined_structure_spawn_port,
    workload_prefix_spawn_port,
)

__all__ = [
    "ALWAYS_ON_MEMBERSHIP_CAPABILITIES",
    "DEFAULT_MAX_TICKS",
    "GATED_PATHS",
    "LOCAL_CAPABILITY_HANDS",
    "MEMBERSHIP_CAPABILITY_SEEDS",
    "PACKAGING_ENV_SPIRIT",
    "READINESS_EDGES",
    "STRUCTURE_SEED_ENV",
    "CapabilitySeats",
    "AdmissionRefusedError",
    "AssembleLoopResult",
    "EffectPort",
    "AssemblySeat",
    "StructureEffectPort",
    "InProcessPlaceRegistry",
    "InProcessPlaceSpawn",
    "OsProcessRegistry",
    "PlaceEffectPort",
    "PlaceSpawnPort",
    "PlaceSpawnResult",
    "RecordingEffectPort",
    "RegisteredPlaceSpawn",
    "WorkloadPlaceSpawn",
    "bind_host_structure_to_seat",
    "combined_structure_spawn_port",
    "default_structure_effects",
    "fail_closed_os_ensure",
    "os_prefix_spawn_port",
    "place_effect_port",
    "resolve_workload_engine",
    "workload_prefix_spawn_port",
    "workload_spawn_hands",
    "assemble_until_steady",
    "boot_mode_name_for_deployment",
    "definition_id_for_boot_mode",
    "definition_id_for_composition",
    "definition_id_from_settings",
    "definition_lists_work_drain",
    "apply_local_capabilities",
    "admission_inventory",
    "admission_inventory_snapshot",
    "open_residual_edges",
    "paid_readiness_edges",
    "load_and_assemble",
    "membership_capabilities_from_settings",
    "admission_source_from_runtime_resolver",
    "coerce_admission_snapshot",
    "require_business_admission",
    "resolve_seed_definition",
    "seed_assembly_options_from_host",
]
