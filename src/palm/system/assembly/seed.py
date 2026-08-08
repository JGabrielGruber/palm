"""Assembly DNA seed map — packaging chooses the decree (0.63.5).

Profiles, boot modes, and composition are **seeds**, not parallel structure
kings. After load, assembly status under the DNA is truth.
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

    if not surfs and not caps:
        return LOCAL_EMBEDDED_ID

    if not surfs and "work_drain" in caps:
        return LOCAL_CLI_ID

    return LOCAL_ALL_IN_ONE_ID


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


def seed_assembly_options_from_host(host: Any) -> dict[str, Any]:
    """Build runtime.start kwargs for assembly seed from ApplicationHost-like shell.

    Does not override if the caller already set ``assembly_definition`` or
    ``assembly_dna_id`` (or ``assembly_skip``).
    """
    mode = getattr(host, "boot_mode", None)
    mode_name = getattr(mode, "name", None) if mode is not None else None
    composition = getattr(host, "composition", None)
    services: tuple[str, ...] = ()
    surfaces: tuple[str, ...] = ()
    capabilities: frozenset[str] = frozenset()
    if composition is not None:
        services = tuple(getattr(composition, "services", ()) or ())
        surfaces = tuple(getattr(composition, "surfaces", ()) or ())
        capabilities = frozenset(getattr(composition, "capabilities", ()) or ())

    dna = resolve_seed_dna(
        mode_name=mode_name,
        services=services,
        surfaces=surfaces,
        capabilities=capabilities,
    )
    return {
        "assembly_dna_id": dna.id,
        "assembly_definition": dna,
    }


__all__ = [
    "dna_id_for_boot_mode",
    "dna_id_for_composition",
    "resolve_seed_dna",
    "seed_assembly_options_from_host",
]
