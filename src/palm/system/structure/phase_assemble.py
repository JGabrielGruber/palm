"""System start phase: structure assemble (system.structure.assemble).

After the machine is ready (``system.ready``), load the structure definition and reconcile until
steady. Publishes admission on the shell. Does **not** start business.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from palm.core.structure import StructureDefinition, resolve_builtin_definition
from palm.system.boot.context import BootContext
from palm.system.boot.definition import PhaseDefinition
from palm.system.boot.shell import resolve_shell
from palm.system.boot.skip import PhaseSkip
from palm.system.log import get_system_log
from palm.system.structure.hands import CapabilitySeats
from palm.system.structure.host_bind import (
    bind_host_structure_to_seat,
    default_structure_effects,
    resolve_workload_engine,
)
from palm.system.structure.seat import StructureSeat


def _resolve_definition(options: Mapping[str, Any]) -> StructureDefinition:
    raw = options.get("structure_definition")
    if isinstance(raw, StructureDefinition):
        return raw
    if isinstance(raw, dict):
        return StructureDefinition.from_dict(raw)
    definition_id = str(options.get("structure_definition_id") or "local.embedded")
    version = str(options.get("structure_definition_version") or "1")
    return resolve_builtin_definition(definition_id, version=version)


def _bind_workload_flag(options: Mapping[str, Any]) -> bool:
    """Opt-in engine bind (default True). False keeps workload: fail-closed."""
    if "structure_bind_workload" in options:
        return bool(options.get("structure_bind_workload"))
    return True


def run(ctx: BootContext, options: Mapping[str, Any]) -> None:
    if options.get("structure_skip"):
        raise PhaseSkip("structure_skip")

    shell = resolve_shell(ctx)
    bind_workload = _bind_workload_flag(options)
    seat: StructureSeat | None = shell.structure
    if seat is None:
        # 0.63.17 — place-effect hands + combined structure spawn; bind engine when ready.
        engine = resolve_workload_engine(shell) if bind_workload else None
        seat = StructureSeat(effects=default_structure_effects(engine=engine))
        shell.structure = seat
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
        bind_report = bind_host_structure_to_seat(seat, shell, bind_workload=bind_workload)

    definition = _resolve_definition(options)
    max_ticks = int(options.get("structure_max_ticks") or 32)
    surfaces = options.get("structure_surfaces") or ()
    if isinstance(surfaces, str):
        surfaces = (surfaces,)
    loop = seat.assemble(
        definition,
        max_ticks=max_ticks,
        surfaces=surfaces,
    )
    board = ctx.install if ctx.install is not None else shell.install
    supervisor = ctx.supervisor if ctx.supervisor is not None else shell.supervisor
    plane = board.work_plane if board is not None else None
    outbox_store = board.outbox_store if board is not None else None
    outbox_processor = board.outbox_processor if board is not None else None
    event = board.event if board is not None else None
    if event is None:
        event = ctx.event
    storage = board.storage if board is not None else None
    if storage is None:
        storage = ctx.storage
    seat.materialize(
        CapabilitySeats(
            supervisor=supervisor,
            work_plane=plane,
            outbox_store=outbox_store,
            outbox_processor=outbox_processor,
            event=event,
            storage=storage,
        )
    )

    admission = seat.admission()

    ctx.publish(
        structure=seat,
        structure_admission=admission,
        structure_definition=definition,
    )
    ctx.set("structure_bind", bind_report)
    get_system_log().info(
        "structure.assemble",
        "structure assemble complete",
        schedule="system",
        runtime=ctx.runtime,
        definition_id=definition.id,
        definition_version=definition.version,
        phase=str(admission.phase),
        may_run_business=admission.may_run_business,
        ticks=loop.ticks,
        steady=loop.steady,
        reasons=",".join(admission.reasons) or "(none)",
        structure_bind=bind_report.get("spawn"),
        structure_engine=bind_report.get("engine"),
    )


DEFINITION = PhaseDefinition(
    id="system.structure.assemble",
    run=run,
    description="Structure assemble — load definition, reconcile, publish admission",
)

__all__ = ["DEFINITION", "run"]
