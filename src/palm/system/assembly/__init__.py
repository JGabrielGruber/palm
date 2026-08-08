"""System assembly — loop, effect port, seat, admission on the shell (0.63)."""

from palm.system.assembly.effects import AssemblyEffectPort, RecordingEffectPort
from palm.system.assembly.household import HouseholdEffectPort
from palm.system.assembly.place_book import InProcessPlaceBook, PlaceBookEffectPort
from palm.system.assembly.place_spawn import (
    InProcessPlaceSpawn,
    OsProcessRegistry,
    PlaceSpawnPort,
    PlaceSpawnResult,
    RegisteredPlaceSpawn,
    fail_closed_os_ensure,
    os_prefix_spawn_port,
)
from palm.system.assembly.workload_place import (
    WorkloadPlaceSpawn,
    combined_structure_spawn_port,
    workload_prefix_spawn_port,
)
from palm.system.assembly.host_bind import (
    bind_host_structure_to_seat,
    default_household_effects,
    place_book_port,
    resolve_workload_engine,
    workload_spawn_hands,
)
from palm.system.assembly.access import admission_source_from_runtime_resolver
from palm.system.assembly.errors import (
    AdmissionRefusedError,
    coerce_admission_snapshot,
    require_business_admission,
)
from palm.system.assembly.loop import (
    DEFAULT_MAX_TICKS,
    AssembleLoopResult,
    assemble_until_steady,
    load_and_assemble,
)
from palm.system.assembly.seat import AssemblySeat
from palm.system.assembly.inventory import (
    GATED_CITIZENS,
    PRETENDER_EDGES,
    kingdom_map,
    kingdom_snapshot,
)
from palm.system.assembly.seed import (
    ALWAYS_ON_MEMBERSHIP_CAPABILITIES,
    MEMBERSHIP_CAPABILITY_SEEDS,
    PACKAGING_ENV_SPIRIT,
    STRUCTURE_SEED_ENV,
    boot_mode_name_for_deployment,
    dna_id_for_boot_mode,
    dna_id_for_composition,
    dna_id_from_settings,
    dna_refuses_background_drain,
    membership_capabilities_from_settings,
    resolve_seed_dna,
    seed_assembly_options_from_host,
)

__all__ = [
    "ALWAYS_ON_MEMBERSHIP_CAPABILITIES",
    "DEFAULT_MAX_TICKS",
    "GATED_CITIZENS",
    "MEMBERSHIP_CAPABILITY_SEEDS",
    "PACKAGING_ENV_SPIRIT",
    "PRETENDER_EDGES",
    "STRUCTURE_SEED_ENV",
    "AdmissionRefusedError",
    "AssembleLoopResult",
    "AssemblyEffectPort",
    "AssemblySeat",
    "HouseholdEffectPort",
    "InProcessPlaceBook",
    "InProcessPlaceSpawn",
    "OsProcessRegistry",
    "PlaceBookEffectPort",
    "PlaceSpawnPort",
    "PlaceSpawnResult",
    "RecordingEffectPort",
    "RegisteredPlaceSpawn",
    "WorkloadPlaceSpawn",
    "bind_host_structure_to_seat",
    "combined_structure_spawn_port",
    "default_household_effects",
    "fail_closed_os_ensure",
    "os_prefix_spawn_port",
    "place_book_port",
    "resolve_workload_engine",
    "workload_prefix_spawn_port",
    "workload_spawn_hands",
    "assemble_until_steady",
    "boot_mode_name_for_deployment",
    "dna_id_for_boot_mode",
    "dna_id_for_composition",
    "dna_id_from_settings",
    "dna_refuses_background_drain",
    "kingdom_map",
    "kingdom_snapshot",
    "load_and_assemble",
    "membership_capabilities_from_settings",
    "admission_source_from_runtime_resolver",
    "coerce_admission_snapshot",
    "require_business_admission",
    "resolve_seed_dna",
    "seed_assembly_options_from_host",
]
