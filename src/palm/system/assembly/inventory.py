"""Kingdom inventory — gates raised vs pretenders still open (0.63.8).

A **guard tower**: read this to know the surrounding wall. Not product control.
Living admission is on the shell; this map is honest cartography.
"""

from __future__ import annotations

from typing import Any

# Paths that must fail closed under admission (law landed).
GATED_CITIZENS: tuple[dict[str, str], ...] = (
    {
        "id": "work_plane.tick",
        "slice": "0.63.3",
        "law": "able = started ∧ admission.may_run_business",
    },
    {
        "id": "work_plane.drain",
        "slice": "0.63.3",
        "law": "continuous poll checks is_able()",
    },
    {
        "id": "executor.submit_flow",
        "slice": "0.63.4",
        "law": "require_business_admission before submit",
    },
    {
        "id": "executor.submit_process",
        "slice": "0.63.4",
        "law": "require_business_admission before submit",
    },
    {
        "id": "executor.submit_plan",
        "slice": "0.63.4",
        "law": "require_business_admission (same _require_runtime)",
    },
    {
        "id": "dna.seed",
        "slice": "0.63.5",
        "law": "host mode/composition → DNA decree",
    },
    {
        "id": "dna.refuse",
        "slice": "0.63.6",
        "law": "refuse_violations block admission on dual membership",
    },
    {
        "id": "vitality.assembly",
        "slice": "0.63.7",
        "law": "eyes sample admission + definition id",
    },
    {
        "id": "inventory.tower",
        "slice": "0.63.8",
        "law": "kingdom_map / packaging admission pointer",
    },
    {
        "id": "cli.seed_local_cli",
        "slice": "0.63.9",
        "law": "create_cli_host → BootMode.cli → local.cli DNA",
    },
    {
        "id": "inspect.present_admission",
        "slice": "0.63.10",
        "law": "present_top / present_vitality nest admission snapshot",
    },
)

# Known open edges — purge or kill-date; not permanent dual.
PRETENDER_EDGES: tuple[dict[str, str], ...] = (
    {
        "id": "assist.soft_catalog",
        "note": "assist top/vitality nest admission via inspect present (0.63.10)",
        "intent": "paid for operate eyes; catalog scenarios still product-owned",
        "status": "partial_0_63_10",
    },
    {
        "id": "host.packaging_without_admission",
        "note": "packaging_status nests admission pointer (0.63.8)",
        "intent": "paid",
        "status": "paid_0_63_8",
    },
    {
        "id": "cli.default_composition",
        "note": "create_cli_host now seeds BootMode.cli → local.cli (0.63.9)",
        "intent": "paid — residual only if callers bypass create_cli_host",
        "status": "paid_0_63_9",
    },
    {
        "id": "env.structure_toggles",
        "note": "structure-shaped PALM_* knobs may still peer-law membership",
        "intent": "map into seed or kill (SD-021)",
    },
    {
        "id": "place_book.handlers",
        "note": "ENSURE_PLACE auto-ack only; no real place book hands yet",
        "intent": "live handlers under growth",
    },
)


def kingdom_map() -> dict[str, Any]:
    """Static cartography of the wall — gated vs pretender."""
    return {
        "theme": "0.63",
        "role": "assembly_kingdom_inventory",
        "gated_citizens": list(GATED_CITIZENS),
        "pretender_edges": list(PRETENDER_EDGES),
        "gated_count": len(GATED_CITIZENS),
        "pretender_count": len(PRETENDER_EDGES),
    }


def kingdom_snapshot(runtime: Any | None = None) -> dict[str, Any]:
    """Static map plus live admission when *runtime* is given."""
    body = kingdom_map()
    body["live"] = None
    if runtime is None:
        return body
    admission = getattr(runtime, "admission", None)
    assembly = getattr(runtime, "assembly", None)
    live: dict[str, Any] = {
        "is_started": bool(getattr(runtime, "is_started", False)),
        "has_assembly_seat": assembly is not None,
    }
    if admission is not None and hasattr(admission, "to_dict"):
        live["admission"] = admission.to_dict()
    elif admission is not None:
        live["admission"] = {
            "may_run_business": bool(getattr(admission, "may_run_business", False)),
            "phase": str(getattr(admission, "phase", "")),
            "definition_id": getattr(admission, "definition_id", None),
        }
    if assembly is not None:
        dna = getattr(assembly, "definition", None)
        live["definition_id"] = getattr(dna, "id", None) if dna is not None else None
        live["refuse"] = (
            sorted(getattr(dna, "refuse", ())) if dna is not None else []
        )
    body["live"] = live
    return body


__all__ = [
    "GATED_CITIZENS",
    "PRETENDER_EDGES",
    "kingdom_map",
    "kingdom_snapshot",
]
