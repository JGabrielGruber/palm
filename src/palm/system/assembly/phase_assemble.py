"""System start phase: household assemble (system.assembly.assemble).

After the machine is ready (``system.ready``), load DNA and reconcile until
steady. Publishes admission on the shell. Does **not** start business.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.core.assembly import AssemblyDefinition, local_embedded
from palm.system.assembly.effects import RecordingEffectPort
from palm.system.assembly.seat import AssemblySeat
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip
from palm.system.log import get_system_log


def _resolve_definition(options: Mapping[str, Any]) -> AssemblyDefinition:
    raw = options.get("assembly_definition")
    if isinstance(raw, AssemblyDefinition):
        return raw
    if isinstance(raw, dict):
        return AssemblyDefinition.from_dict(raw)
    dna_id = str(options.get("assembly_dna_id") or "local.embedded")
    version = str(options.get("assembly_dna_version") or "1")
    if dna_id in ("local.embedded", "embedded"):
        return local_embedded(version=version)
    # Unknown id — still build a thin DNA with that id (growth will expand)
    return AssemblyDefinition(
        id=dna_id,
        version=version,
        role_intent=str(options.get("assembly_role_intent") or "embedded"),
    )


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    if options.get("assembly_skip") or options.get("skip_assembly"):
        raise PhaseSkip("assembly_skip")

    shell = resolve_shell(ctx)
    seat: AssemblySeat | None = getattr(shell, "assembly", None)
    if seat is None:
        auto_ack = bool(options.get("assembly_auto_ack_places", False))
        seat = AssemblySeat(effects=RecordingEffectPort(auto_ack_places=auto_ack))
        shell.assembly = seat  # type: ignore[attr-defined]

    dna = _resolve_definition(options)
    max_ticks = int(options.get("assembly_max_ticks") or 32)
    loop = seat.assemble(dna, max_ticks=max_ticks)
    admission = seat.admission()

    ctx.publish(
        assembly=seat,
        assembly_admission=admission,
        assembly_definition=dna,
    )
    get_system_log().info(
        "assembly.assemble",
        "household assemble complete",
        schedule="system",
        runtime=ctx.runtime,
        definition_id=dna.id,
        definition_version=dna.version,
        phase=str(admission.phase),
        may_run_business=admission.may_run_business,
        ticks=loop.ticks,
        steady=loop.steady,
        reasons=",".join(admission.reasons) or "(none)",
    )


DEFINITION = PhaseDefinition(
    id="system.assembly.assemble",
    run=run,
    description="Household assemble — load DNA, reconcile, publish admission",
)

__all__ = ["DEFINITION", "run"]
