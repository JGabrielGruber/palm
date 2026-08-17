"""Assembly DNA seed map — packaging chooses the decree (0.63.5+).

Profiles, boot modes, composition, and structure-shaped env are **seeds**, not
parallel structure kings. After load, assembly status under the DNA is truth.

**0.63.13 — env pretenders (SD-021 growth):**
- ``PALM_ASSEMBLY_DNA_ID`` / ``settings.assembly_dna_id`` is the explicit DNA seed.
- Membership-shaped flags feed composition at resolve for organs that still
  live there. ``work_drain`` is not one of them.

**0.63.19 — full membership seed cartography (SD-021 residual):**
- Every ``enable_*`` / analytics flag that feeds composition is catalogued here.
- Bootstrap derives capabilities from this map — one truth for seed resolve.
- ``work_drain`` install reads DNA ``capabilities``. Other capabilities still
  seed composition at resolve.
"""

from __future__ import annotations

from typing import Any

from palm.core.assembly import (
    LOCAL_ALL_IN_ONE_ID,
    LOCAL_CLI_ID,
    LOCAL_EMBEDDED_ID,
    LOCAL_MCP_ID,
    LOCAL_SERVER_ID,
    LOCAL_WORKER_ID,
    AssemblyDefinition,
    resolve_builtin_dna,
)

# BootMode.name → builtin DNA id (VISION-0.63 §6)
_MODE_TO_DNA: dict[str, str] = {
    "safe": LOCAL_EMBEDDED_ID,
    "test": LOCAL_EMBEDDED_ID,
    "cli": LOCAL_CLI_ID,
    "server": LOCAL_SERVER_ID,
    "prod": LOCAL_SERVER_ID,
    "mcp": LOCAL_MCP_ID,
    "worker": LOCAL_WORKER_ID,
    "all_in_one": LOCAL_ALL_IN_ONE_ID,
    "dev": LOCAL_ALL_IN_ONE_ID,
}

# 0.63.19 — settings field → composition capability at resolve only.
# Single source for bootstrap ``_capabilities_from_settings`` and cartography.
# Always-on membership (journal / projections / workloads) has no flag — not listed.
MEMBERSHIP_CAPABILITY_SEEDS: tuple[dict[str, str], ...] = (
    {
        "env": "PALM_ENABLE_COMPENSATION",
        "settings": "enable_compensation",
        "capability": "compensation",
        "role": "membership_seed",
        "note": "Feeds composition.compensation at resolve; host wires via composition.has",
    },
    {
        "env": "PALM_ENABLE_EVENT_OUTBOX",
        "settings": "enable_event_outbox",
        "capability": "outbox",
        "role": "membership_seed",
        "note": (
            "Feeds composition.outbox at resolve; host spawn aligns "
            "enable_event_outbox from composition.has (0.63.28); bare runtime "
            "start option remains packaging for non-host shells"
        ),
    },
    {
        "env": "PALM_ENABLE_WEBHOOK_DISPATCHER",
        "settings": "enable_webhook_dispatcher",
        "capability": "webhook",
        "role": "membership_seed",
        "note": "Feeds composition.webhook at resolve; URLs refine targets within capability",
    },
    {
        "env": "PALM_ANALYTICS_ENABLED",
        "settings": "analytics_enabled",
        "capability": "analytics",
        "role": "membership_seed",
        "note": "Feeds composition.analytics at resolve",
    },
    {
        "env": "PALM_ENABLE_NEONROOT_RUNNERS",
        "settings": "enable_neonroot_runners",
        "capability": "neonroot",
        "role": "membership_seed",
        "note": "Feeds composition.neonroot availability; does not install CLI binary",
    },
)

# Capabilities always present on settings-composed hosts (no enable_* seed).
ALWAYS_ON_MEMBERSHIP_CAPABILITIES: frozenset[str] = frozenset(
    {"journal", "projections", "workloads"}
)

# 0.63.13 / 0.63.19 — cartography: env / settings that *seed* structure (not packaging).
# Packaging stays free (storage, ports, log, pool widths, secrets).
STRUCTURE_SEED_ENV: tuple[dict[str, str], ...] = (
    {
        "env": "PALM_ASSEMBLY_DNA_ID",
        "settings": "assembly_dna_id",
        "role": "explicit_dna_seed",
        "note": "Chooses which DNA loads; wins over mode/composition inference",
    },
    *MEMBERSHIP_CAPABILITY_SEEDS,
    {
        "env": "PALM_HOST_PROFILE",
        "settings": "host_profile",
        "role": "deployment_seed",
        "note": "Deployment preset seed when no BootMode",
    },
    {
        "env": "PALM_HOST_ROLES",
        "settings": "host_roles",
        "role": "deployment_seed",
        "note": "Deployment roles seed when no preset / BootMode",
    },
)

# Packaging knobs (not structure kings) — non-exhaustive; spirit not inventory.
PACKAGING_ENV_SPIRIT: tuple[str, ...] = (
    "PALM_STORAGE_BACKEND",
    "PALM_DATA_DIR",
    "PALM_SERVER_HOST",
    "PALM_SERVER_PORT",
    "PALM_WORK_DRAIN_WORKERS",
    "PALM_WORK_DRAIN_LEASE_SECONDS",
    "PALM_QUEUED_WORKERS",
    "PALM_ENABLE_OUTBOX_SERVICE",  # deployment/node role refine, not capability seed
    "PALM_ENABLE_STATE_SNAPSHOT",  # product packaging, not composition membership
)


def dna_id_for_boot_mode(mode_name: str | None) -> str | None:
    """Map a boot mode name to a builtin DNA id, or None if unknown."""
    if not mode_name:
        return None
    return _MODE_TO_DNA.get(str(mode_name).strip().lower())


def dna_id_for_composition(
    *,
    services: tuple[str, ...] | list[str] = (),
    surfaces: tuple[str, ...] | list[str] = (),
    capabilities: frozenset[str] | set[str] | list[str] = (),
) -> str:
    """Infer DNA id from composition membership (when no boot mode)."""
    caps = frozenset(str(c) for c in capabilities)
    surfs = tuple(str(s) for s in surfaces)
    svcs = tuple(str(s) for s in services)

    if surfs:
        if surfs == ("mcp",) or (len(surfs) == 1 and surfs[0] == "mcp"):
            return LOCAL_MCP_ID
        return LOCAL_SERVER_ID

    if svcs == ("execution",) or (len(svcs) == 1 and svcs[0] == "execution"):
        return LOCAL_WORKER_ID

    if not caps:
        return LOCAL_EMBEDDED_ID

    return LOCAL_CLI_ID


def dna_id_from_settings(settings: Any | None) -> str | None:
    """Explicit DNA seed from packaging settings / ``PALM_ASSEMBLY_DNA_ID``."""
    if settings is None:
        return None
    raw = getattr(settings, "assembly_dna_id", None)
    if raw is None:
        return None
    text = str(raw).strip()
    return text or None


def membership_capabilities_from_settings(
    settings: Any | None,
    *,
    deployment: Any | None = None,
) -> frozenset[str]:
    """Derive composition capabilities from membership *seeds* (0.63.19).

    Settings ``enable_*`` / analytics flags seed membership **at resolve only**.
    ``work_drain`` is not a composition seed — DNA ``capabilities`` list it.
    """
    capabilities: set[str] = set(ALWAYS_ON_MEMBERSHIP_CAPABILITIES)
    if settings is not None:
        for row in MEMBERSHIP_CAPABILITY_SEEDS:
            field = row["settings"]
            if bool(getattr(settings, field, False)):
                capabilities.add(row["capability"])
    return frozenset(capabilities)


def resolve_seed_dna(
    *,
    mode_name: str | None = None,
    services: tuple[str, ...] | list[str] = (),
    surfaces: tuple[str, ...] | list[str] = (),
    capabilities: frozenset[str] | set[str] | list[str] = (),
    version: str = "1",
    explicit_dna_id: str | None = None,
) -> AssemblyDefinition:
    """Choose DNA: explicit id → boot mode → composition inference."""
    if explicit_dna_id:
        return resolve_builtin_dna(explicit_dna_id, version=version)
    from_mode = dna_id_for_boot_mode(mode_name)
    if from_mode:
        return resolve_builtin_dna(from_mode, version=version)
    inferred = dna_id_for_composition(
        services=services,
        surfaces=surfaces,
        capabilities=capabilities,
    )
    return resolve_builtin_dna(inferred, version=version)


def boot_mode_name_for_deployment(profile: Any) -> str | None:
    """Map DeploymentProfile roles to a BootMode-like seed name (0.63.12)."""
    if profile is None:
        return None
    master = bool(getattr(profile, "master", False))
    worker = bool(getattr(profile, "worker", False))
    server = bool(getattr(profile, "server", False))
    if server:
        return "server"
    if worker and not master:
        return "worker"
    if master and worker and not server:
        return "all_in_one"
    if master and not worker:
        return "cli"  # command-only collapsed-ish
    return None


def seed_assembly_options_from_host(host: Any) -> dict[str, Any]:
    """Build runtime.start kwargs for assembly seed from ApplicationHost-like shell.

    Priority for DNA id: settings.assembly_dna_id → boot mode → deployment →
    composition inference. Membership surfaces/capabilities always come from the
    host composition (refuse checks dual membership — 0.63.6).
    """
    mode = getattr(host, "boot_mode", None)
    mode_name = getattr(mode, "name", None) if mode is not None else None
    if mode_name is None:
        mode_name = boot_mode_name_for_deployment(getattr(host, "profile", None))
    composition = getattr(host, "composition", None)
    services: tuple[str, ...] = ()
    surfaces: tuple[str, ...] = ()
    capabilities: frozenset[str] = frozenset()
    if composition is not None:
        services = tuple(getattr(composition, "services", ()) or ())
        surfaces = tuple(getattr(composition, "surfaces", ()) or ())
        capabilities = frozenset(getattr(composition, "capabilities", ()) or ())

    settings = getattr(host, "settings", None)
    explicit = dna_id_from_settings(settings)
    dna = resolve_seed_dna(
        mode_name=mode_name,
        services=services,
        surfaces=surfaces,
        capabilities=capabilities,
        explicit_dna_id=explicit,
    )
    return {
        "assembly_dna_id": dna.id,
        "assembly_definition": dna,
        # Membership facts for refuse check (0.63.6) — not a second structure king.
        "assembly_surfaces": list(surfaces),
        "assembly_capabilities": sorted(capabilities),
    }


__all__ = [
    "ALWAYS_ON_MEMBERSHIP_CAPABILITIES",
    "MEMBERSHIP_CAPABILITY_SEEDS",
    "PACKAGING_ENV_SPIRIT",
    "STRUCTURE_SEED_ENV",
    "boot_mode_name_for_deployment",
    "dna_id_for_boot_mode",
    "dna_id_for_composition",
    "dna_id_from_settings",
    "membership_capabilities_from_settings",
    "resolve_seed_dna",
    "seed_assembly_options_from_host",
]
