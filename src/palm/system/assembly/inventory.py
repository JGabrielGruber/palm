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
    {
        "id": "place_book.in_process",
        "slice": "0.63.11",
        "law": "PlaceBookEffectPort ensure/release → PLACE_READY/GONE",
    },
    {
        "id": "run_host.deployment_seed",
        "slice": "0.63.12",
        "law": "deployment profile → DNA + composition (server/worker/all_in_one)",
    },
    {
        "id": "env.structure_seed",
        "slice": "0.63.13",
        "law": "PALM_ASSEMBLY_DNA_ID seed · membership refuse always · drain DNA king",
    },
    {
        "id": "place_book.spawn_port",
        "slice": "0.63.14",
        "law": "PlaceSpawnPort · RegisteredPlaceSpawn · os: fail-closed until body",
    },
    {
        "id": "household.structure_intents",
        "slice": "0.63.15",
        "law": "HouseholdEffectPort · OS process spawn · projection/policy/seed hands",
    },
    {
        "id": "place_book.workload",
        "slice": "0.63.16",
        "law": "workload: places via WorkloadPlaceSpawn · fail closed unbound",
    },
    {
        "id": "host.structure_bind",
        "slice": "0.63.17",
        "law": (
            "default assemble binds shell WorkloadEngine into combined place spawn "
            "(assembly_bind_workload opt-out)"
        ),
    },
    {
        "id": "assembly.reassemble",
        "slice": "0.63.18",
        "law": (
            "reassemble / force invalidate · membership refuse re-check · "
            "fail closed while invalidated"
        ),
    },
    {
        "id": "env.membership_seed_catalog",
        "slice": "0.63.19",
        "law": (
            "MEMBERSHIP_CAPABILITY_SEEDS single map · bootstrap derives caps · "
            "STRUCTURE_SEED_ENV full enable_* cartography (SD-021)"
        ),
    },
    {
        "id": "execution.start_workload",
        "slice": "0.63.20",
        "law": (
            "ExecutionPort.start_workload requires admission · household "
            "WorkloadEngine path remains ungated"
        ),
    },
    {
        "id": "assist.start_scenario",
        "slice": "0.63.21",
        "law": (
            "assist scenario start + menu open→flow create require admission · "
            "menu nests admission / start_allowed"
        ),
    },
    {
        "id": "assist.admission_oath",
        "slice": "0.63.22",
        "law": (
            "AssistService.admission_source inject · citizen gates use "
            "admission_gate() · coerce_admission_snapshot · no resolve_runtime dig "
            "for readiness (peasants' oath / SD-016 boy-scout)"
        ),
    },
    {
        "id": "work_plane.able_fail_closed",
        "slice": "0.63.23",
        "law": (
            "WorkPlane able default / set_able(None) / install missing able "
            "→ False (was soft-open True) · admission_source_from_runtime_resolver "
            "helper (shape without product base)"
        ),
    },
    {
        "id": "execution.invoke_resource",
        "slice": "0.63.24",
        "law": (
            "ExecutionPort.invoke_resource requires admission · direct "
            "ResourceEngine.invoke remains ungated (unit / non-port path)"
        ),
    },
    {
        "id": "execution.resume_job",
        "slice": "0.63.25",
        "law": (
            "ExecutionPort.resume_job requires admission · product re-drive "
            "fail closed"
        ),
    },
    {
        "id": "runtime.provide_input",
        "slice": "0.63.25",
        "law": (
            "BaseRuntime.provide_input requires admission · product interactive "
            "continue fail closed"
        ),
    },
    {
        "id": "wait_plane.able_resume",
        "slice": "0.63.26",
        "law": (
            "WaitPlane able gates match→resume · omit/None fail closed · install "
            "binds started∧admission · target fail still applies"
        ),
    },
    {
        "id": "execution.exec_workload",
        "slice": "0.63.27",
        "law": (
            "ExecutionPort.exec_workload requires admission · direct "
            "WorkloadEngine.exec remains ungated (unit / non-port)"
        ),
    },
    {
        "id": "host.outbox_composition_king",
        "slice": "0.63.28",
        "law": (
            "host system_spawn aligns enable_event_outbox from "
            "composition.has('outbox') unless explicit start override"
        ),
    },
    {
        "id": "assist.continue_session",
        "slice": "0.63.29",
        "law": (
            "AssistSession input / resume / backtrack require admission via "
            "admission_gate() (oath) · cancel stays control residual"
        ),
    },
    {
        "id": "executor.resume_process",
        "slice": "0.63.29",
        "law": (
            "resume_process is product continue citizen · gated via "
            "_require_runtime admission since 0.63.4 (cartography honesty)"
        ),
    },
    {
        "id": "flows.continue_session",
        "slice": "0.63.30",
        "law": (
            "FlowSession input / resume / backtrack require admission via "
            "flows.admission_gate() · host injects admission_source · "
            "cancel stays control residual"
        ),
    },
    {
        "id": "flows.admission_oath",
        "slice": "0.63.30",
        "law": (
            "FlowExecutionService.admission_source inject · admission_gate() · "
            "same helper as assist (no product base)"
        ),
    },
    {
        "id": "execution.product_facade_oath",
        "slice": "0.63.31",
        "law": (
            "Workload / Provider / Process execution services inject "
            "admission_source · edge gates on start/exec/invoke/prepare/"
            "submit/run · stop/cancel control residual"
        ),
    },
    {
        "id": "flows.start_session",
        "slice": "0.63.32",
        "law": (
            "FlowExecutionService submit_flow_body / run_wizard / run_flow "
            "require admission via admission_gate() · product start edge "
            "(port remains second wall) · list/describe stay soft catalog"
        ),
    },
    {
        "id": "host.packaging_market_day",
        "slice": "0.63.33",
        "law": (
            "ApplicationHost submit_flow / submit_process / provide_input / "
            "resume_process / invoke_resource + CQRS Submit*/Provide*/Resume* / "
            "PreparePlans / SubmitPlans require admission · cancel residual · "
            "kernel dig second wall via ports"
        ),
    },
    {
        "id": "surface.fealty",
        "slice": "0.63.34",
        "law": (
            "CLI resume_job / invoke → host packaging; SSR explorer invoke / "
            "resume_wizard → host or admit+port; wizard CQRS Provide/Backtrack "
            "edge admission; host.resume_job packaging door"
        ),
    },
    {
        "id": "surface.rest_admission_voice",
        "slice": "0.63.35",
        "law": (
            "REST maps AdmissionRefusedError → 503 admission_refused "
            "(not submit_failed 500 / input_rejected 400) on market-day "
            "and continue handlers"
        ),
    },
    {
        "id": "surface.mcp_ws_admission_voice",
        "slice": "0.63.36",
        "law": (
            "MCP in-process PalmRestError 503 admission_refused + "
            "WebSocket assist error code admission_refused (not internal/"
            "500/400) on market-day and continue"
        ),
    },
    {
        "id": "surface.cli_ssr_admission_voice",
        "slice": "0.63.37",
        "law": (
            "CLI print_cli_error labels admission_refused; SSR explorer "
            "operator_error_text + wizard backtrack catches RuntimeError "
            "(not bare red / generic form failure)"
        ),
    },
)

# Known open edges — purge or kill-date; not permanent dual.
PRETENDER_EDGES: tuple[dict[str, str], ...] = (
    {
        "id": "assist.soft_catalog",
        "note": (
            "0.63.10 operate eyes; 0.63.21 scenario start + open flow create gated; "
            "0.63.22 admission_source inject (oath); menu nests admission / "
            "start_allowed (no start CTA when closed)"
        ),
        "intent": "paid start + oath inject; residual only soft catalog browse packaging",
        "status": "paid_oath_0_63_22",
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
        "note": (
            "0.63.13 DNA seed + drain king; 0.63.19 full MEMBERSHIP_CAPABILITY_SEEDS "
            "catalog + bootstrap single source. Flags remain honest resolve seeds; "
            "gates after load use composition.has + DNA refuse."
        ),
        "intent": "paid catalog SD-021 — residual only named packaging duals (outbox start option)",
        "status": "paid_catalog_0_63_19",
    },
    {
        "id": "outbox.start_option_seed",
        "note": (
            "0.63.28: host system_spawn sets enable_event_outbox from "
            "composition.has('outbox') when not explicit; recovery already "
            "composition.has. Bare BaseRuntime.start(enable_event_outbox=) remains "
            "packaging residual for non-host shells."
        ),
        "intent": "paid host path — composition king; bare runtime seed named residual",
        "status": "paid_host_0_63_28",
    },
    {
        "id": "runtime.enable_event_outbox_bare",
        "note": (
            "BaseRuntime / runtime_start_options still accept enable_event_outbox "
            "for non-host and test shells without a CompositionProfile."
        ),
        "intent": "name residual — packaging seed for bare start, not dual on host path",
        "status": "named_0_63_28",
    },

    {
        "id": "place_book.os_spawn",
        "note": (
            "0.63.15–17: OS process + workload: place spawn + host auto-bind "
            "WorkloadEngine on assemble (assembly_bind_workload=False opt-out)"
        ),
        "intent": "paid for host path; residual only if custom seats bypass bind",
        "status": "paid_0_63_17",
    },
    {
        "id": "work_plane.able_default_open",
        "note": (
            "0.63.23: able default / attach omit / set_able(None) / install missing "
            "able all fail closed (False). Runtime still binds started∧admission."
        ),
        "intent": "paid",
        "status": "paid_0_63_23",
    },
    {
        "id": "host.soft_definitions_ready",
        "note": (
            "Audit 0.63.23: no host flag invents business readiness beside admission "
            "pointer (packaging_status.assembly). Residual: packaging bags remain "
            "eyes residual (CS-002), not structure law."
        ),
        "intent": "named residual — packaging eyes only, not dual ready flag",
        "status": "named_0_63_23",
    },
    {
        "id": "execution.workload_engine_dig",
        "note": (
            "0.63.20 start_workload · 0.63.27 exec_workload gated on port. Direct "
            "WorkloadEngine.start/exec: household place book + unit free; product dig "
            "for business is pretender."
        ),
        "intent": "name residual — port is law; dig ≠ free pass (SD-020)",
        "status": "named_0_63_27",
    },
    {
        "id": "execution.stop_workload_ungated",
        "note": (
            "stop_workload / stop_owned remain without business admission so "
            "shutdown and cleanup work when admission is closed."
        ),
        "intent": "name residual — control path, not market-day start; revisit if product misuses",
        "status": "named_0_63_27",
    },

    {
        "id": "execution.resource_engine_dig",
        "note": (
            "0.63.24 gates ExecutionPort.invoke_resource. Direct ResourceEngine.invoke "
            "is unit/non-port free; product/surface dig for business effects is pretender."
        ),
        "intent": "name residual — port is law; dig ≠ free pass (SD-020)",
        "status": "named_0_63_25",
    },
    {
        "id": "wait_plane.orch_resume_dig",
        "note": (
            "0.63.25 product resume_job / provide_input gated; 0.63.26 wait plane "
            "able gates match→resume (fail closed when admission down). "
            "resume_owner still calls orch.resume_job after able — dig paid as able."
        ),
        "intent": "paid — continue spine under same able as work plane",
        "status": "paid_0_63_26",
    },
    {
        "id": "assist.session_cancel_ungated",
        "note": (
            "AssistSession.cancel / session verb cancel remain without business "
            "admission so operators can stop work when the organism is closed."
        ),
        "intent": "name residual — control path, not market-day continue (SD-020)",
        "status": "named_0_63_29",
    },
    {
        "id": "assist.continue_edge",
        "note": (
            "0.63.29: AssistSession input / resume / backtrack gate on "
            "admission_gate() at product edge (oath); deep provide_input / "
            "resume_job remain second wall."
        ),
        "intent": "paid product continue edge",
        "status": "paid_0_63_29",
    },
    {
        "id": "flows.continue_edge",
        "note": (
            "0.63.30: FlowSession input / resume / backtrack gate on "
            "flows.admission_gate(); host injects admission_source via "
            "admission_source_from_runtime_resolver (oath boy-scout)."
        ),
        "intent": "paid product continue edge + inject",
        "status": "paid_0_63_30",
    },
    {
        "id": "flows.session_cancel_ungated",
        "note": (
            "FlowSession.cancel remains without business admission so product "
            "can stop work when the organism is closed."
        ),
        "intent": "name residual — control path (SD-020)",
        "status": "named_0_63_30",
    },
    {
        "id": "runtime.cancel_job_ungated",
        "note": (
            "BaseRuntime.cancel_job / CQRS CancelJobCommand remain without "
            "business admission for operator stop and shutdown."
        ),
        "intent": "name residual — control path, not market-day start (SD-020)",
        "status": "named_0_63_30",
    },
    {
        "id": "execution.product_facade_edge",
        "note": (
            "0.63.31: WorkloadExecutionService start/exec, "
            "ProviderExecutionService.invoke, ProcessExecutionService "
            "prepare/submit/run gate on admission_gate(); host injects "
            "shared admission_source for all execution façades."
        ),
        "intent": "paid product façade edge + inject",
        "status": "paid_0_63_31",
    },
    {
        "id": "workloads.product_stop_ungated",
        "note": (
            "WorkloadExecutionService.stop / cancel remain without business "
            "admission (control path when organism closed)."
        ),
        "intent": "name residual — control path (SD-020)",
        "status": "named_0_63_31",
    },
    {
        "id": "flows.start_edge",
        "note": (
            "0.63.32: FlowExecutionService submit_flow_body / run_wizard / "
            "run_flow gate on admission_gate() at product edge (oath); deep "
            "submit_flow / executor remain second wall. LIST/DESCRIBE catalog "
            "browse stays soft packaging eyes."
        ),
        "intent": "paid product start edge",
        "status": "paid_0_63_32",
    },
    {
        "id": "flows.soft_catalog",
        "note": (
            "FlowExecutionService LIST / DESCRIBE remain without business "
            "admission — packaging catalog browse, not market-day start."
        ),
        "intent": "named residual — soft catalog eyes (same spirit as assist.soft_catalog)",
        "status": "named_0_63_32",
    },
    {
        "id": "host.packaging_market_day_edge",
        "note": (
            "0.63.33: ApplicationHost market-day doors + PalmCommandHandlers "
            "SubmitFlow/Process, ProvideInput, ResumeProcess, PreparePlans, "
            "SubmitPlans gate on admission; product façades remain preferred "
            "peasant path; ports remain second wall."
        ),
        "intent": "paid packaging crown market-day edge",
        "status": "paid_0_63_33",
    },
    {
        "id": "kernel.direct_dig",
        "note": (
            "PalmKernel / BaseRuntime public submit/provide/invoke remain "
            "port-gated only. Digging host.app or bare runtime bypasses "
            "host packaging edge — pretender if product uses it for business. "
            "0.63.34: CLI + SSR explorer market-day digs boy-scouted to host."
        ),
        "intent": "name residual — port is law; packaging crown is host (SD-020)",
        "status": "named_0_63_33",
    },
    {
        "id": "surface.fealty_edge",
        "note": (
            "0.63.34: CLI resume_job/invoke and SSR explorer invoke/resume "
            "route through host packaging (or admit+port when host-less); "
            "wizard CQRS ProvideWizardInput / RequestWizardBacktrack gate "
            "admission at pattern handler; host.resume_job packaging door."
        ),
        "intent": "paid surface fealty boy-scout",
        "status": "paid_0_63_34",
    },
    {
        "id": "surface.rest_admission_voice_edge",
        "note": (
            "0.63.35: REST error helper admission_refused (503) + "
            "maybe_admission_refused on assist/flows/processes/providers/"
            "workloads/jobs/plans/instances market-day and continue paths. "
            "Gate already raised under product/port; surface now speaks truth."
        ),
        "intent": "paid REST honest voice for closed gate",
        "status": "paid_0_63_35",
    },
    {
        "id": "surface.mcp_ws_admission_voice_edge",
        "note": (
            "0.63.36: MCP maybe_admission_refused_error → PalmRestError 503 "
            "admission_refused on in-process market-day/continue; WebSocket "
            "assist maps AdmissionRefusedError to code admission_refused "
            "(not internal). HTTP MCP inherits REST voice via bridge."
        ),
        "intent": "paid MCP + WS honest voice for closed gate",
        "status": "paid_0_63_36",
    },
    {
        "id": "surface.cli_ssr_admission_voice_edge",
        "note": (
            "0.63.37: CLI market-day/continue commands use print_cli_error "
            "(admission_refused brand); SSR explorer market-day + continue "
            "banners use operator_error_text; wizard backtrack catches "
            "RuntimeError so closed gate is not an unhandled 500."
        ),
        "intent": "paid CLI + SSR explorer honest voice for closed gate",
        "status": "paid_0_63_37",
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
