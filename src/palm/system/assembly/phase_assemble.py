"""System start phase: household assemble (system.assembly.assemble).

After the machine is ready (``system.ready``), load DNA and reconcile until
steady. Publishes admission on the shell. Does **not** start business.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.core.assembly import AssemblyDefinition, resolve_builtin_dna
from palm.system.assembly.hands import CapabilitySeats
from palm.system.assembly.host_bind import (
    bind_host_structure_to_seat,
    default_household_effects,
    resolve_workload_engine,
)
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
    return resolve_builtin_dna(dna_id, version=version)


def _bind_workload_flag(options: Mapping[str, Any]) -> bool:
    """Opt-in engine bind (default True). False keeps workload: fail-closed."""
    if "assembly_bind_workload" in options:
        return bool(options.get("assembly_bind_workload"))
    if "bind_assembly_workload" in options:
        return bool(options.get("bind_assembly_workload"))
    return True


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    if options.get("assembly_skip") or options.get("skip_assembly"):
        raise PhaseSkip("assembly_skip")

    shell = resolve_shell(ctx)
    bind_workload = _bind_workload_flag(options)
    seat: AssemblySeat | None = getattr(shell, "assembly", None)
    if seat is None:
        # 0.63.17 — household hands + combined structure spawn; bind engine when ready.
        engine = resolve_workload_engine(shell) if bind_workload else None
        seat = AssemblySeat(effects=default_household_effects(engine=engine))
        shell.assembly = seat  # type: ignore[attr-defined]
        bind_report = {
            "bound": True,
            "engine": engine is not None,
            "spawn": "combined",
            "skipped": None
            if engine is not None
            else ("bind_disabled" if not bind_workload else "engine_not_ready"),
        }
    else:
        # Pre-installed seat: upgrade default place hands / attach engine.
        bind_report = bind_host_structure_to_seat(
            seat, shell, bind_workload=bind_workload
        )

    dna = _resolve_definition(options)
    max_ticks = int(options.get("assembly_max_ticks") or 32)
    surfaces = options.get("assembly_surfaces") or ()
    capabilities = options.get("assembly_capabilities") or ()
    if isinstance(surfaces, str):
        surfaces = (surfaces,)
    if isinstance(capabilities, str):
        capabilities = (capabilities,)
    loop = seat.assemble(
        dna,
        max_ticks=max_ticks,
        surfaces=surfaces,
        capabilities=capabilities,
    )
    board = ctx.install if ctx.install is not None else shell.install
    supervisor = ctx.supervisor if ctx.supervisor is not None else shell.supervisor
    plane = board.work_plane if board is not None else None
    seat.materialize(CapabilitySeats(supervisor=supervisor, work_plane=plane))
    admission = seat.admission()

    ctx.publish(
        assembly=seat,
        assembly_admission=admission,
        assembly_definition=dna,
    )
    ctx.set("assembly_structure_bind", bind_report)
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
        structure_bind=bind_report.get("spawn"),
        structure_engine=bind_report.get("engine"),
    )


DEFINITION = PhaseDefinition(
    id="system.assembly.assemble",
    run=run,
    description="Household assemble — load DNA, reconcile, publish admission",
)

__all__ = ["DEFINITION", "run"]
