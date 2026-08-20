"""Admission inventory — admitted paths vs dual-readiness residual (0.63.8).

Read this for admitted paths vs dual-readiness residual. Not product control.
Living admission is on the shell; this map is honest cartography.
"""

from __future__ import annotations

from typing import Any

# Paths that must fail closed under admission (law landed).
GATED_PATHS: tuple[dict[str, str], ...] = (
    {
        "id": "work_plane.tick",
        "slice": "0.63.3",
        "law": "able = started ∧ ready ∧ work_drain (0.67.2); wait stays ready",
    },
    {
        "id": "work_plane.tick_schedules",
        "slice": "0.67.5",
        "law": "tick_schedules uses the same able as tick (drain); host tick_work follows",
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
        "id": "definition.seed",
        "slice": "0.63.5",
        "law": "host mode/composition → structure-definition seed",
    },
    {
        "id": "definition.refuse",
        "slice": "0.63.6",
        "law": "refuse_violations block admission on dual membership",
    },
    {
        "id": "vitality.structure",
        "slice": "0.63.7",
        "law": "eyes sample admission + definition id",
    },
    {
        "id": "inventory.admission",
        "slice": "0.63.8",
        "law": "admission_inventory / packaging admission pointer",
    },
    {
        "id": "cli.seed_local_cli",
        "slice": "0.63.9",
        "law": "create_cli_host → BootMode.cli → local.cli definition",
    },
    {
        "id": "inspect.present_admission",
        "slice": "0.63.10",
        "law": "present_top / present_vitality nest admission snapshot",
    },
    {
        "id": "place_registry.in_process",
        "slice": "0.63.11",
        "law": "PlaceEffectPort ensure/release → PLACE_READY/GONE",
    },
    {
        "id": "run_host.deployment_seed",
        "slice": "0.63.12",
        "law": "deployment profile → definition + composition (server/worker/all_in_one)",
    },
    {
        "id": "env.structure_seed",
        "slice": "0.63.13",
        "law": "PALM_STRUCTURE_DEFINITION_ID seed · membership refuse always · drain listed on definition",
    },
    {
        "id": "place_registry.spawn_port",
        "slice": "0.63.14",
        "law": "PlaceSpawnPort · RegisteredPlaceSpawn · os: fail-closed until body",
    },
    {
        "id": "structure.effect_intents",
        "slice": "0.63.15",
        "law": "StructureEffectPort · OS process spawn · projection/policy/seed hands",
    },
    {
        "id": "place_registry.workload",
        "slice": "0.63.16",
        "law": "workload: places via WorkloadPlaceSpawn · fail closed unbound",
    },
    {
        "id": "host.structure_bind",
        "slice": "0.63.17",
        "law": (
            "default assemble binds shell WorkloadEngine into combined place spawn "
            "(structure_bind_workload opt-out)"
        ),
    },
    {
        "id": "structure.reassemble",
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
            "ExecutionPort.start_workload requires admission · structure "
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
        "id": "assist.published_admission",
        "slice": "0.63.22",
        "law": (
            "AssistService.admission_source inject · path gates use "
            "admission_gate() · coerce_admission_snapshot · no resolve_runtime dig "
            "for readiness (published admission / SD-016 boy-scout)"
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
        "id": "host.outbox_composition_seed",
        "slice": "0.65.2",
        "law": (
            "host system_spawn aligns enable_event_outbox from "
            "structure definition has_capability('outbox') unless explicit start override"
        ),
    },
    {
        "id": "assist.continue_session",
        "slice": "0.63.29",
        "law": (
            "AssistSession input / resume / backtrack require admission via "
            "admission_gate() (published admission) · cancel stays control residual"
        ),
    },
    {
        "id": "executor.resume_process",
        "slice": "0.63.29",
        "law": (
            "resume_process is product continue path · gated via "
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
        "id": "flows.published_admission",
        "slice": "0.63.30",
        "law": (
            "FlowExecutionService.admission_source inject · admission_gate() · "
            "same helper as assist (no product base)"
        ),
    },
    {
        "id": "execution.product_facade_admission",
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
        "id": "host.packaging_start_continue",
        "slice": "0.63.33",
        "law": (
            "ApplicationHost submit_flow / submit_process / provide_input / "
            "resume_process / invoke_resource + CQRS Submit*/Provide*/Resume* / "
            "PreparePlans / SubmitPlans require admission · cancel residual · "
            "kernel dig second wall via ports"
        ),
    },
    {
        "id": "surface.host_port",
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
            "(not submit_failed 500 / input_rejected 400) on business "
            "start/continue handlers"
        ),
    },
    {
        "id": "surface.mcp_ws_admission_voice",
        "slice": "0.63.36",
        "law": (
            "MCP in-process PalmRestError 503 admission_refused + "
            "WebSocket assist error code admission_refused (not internal/"
            "500/400) on business start/continue"
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
    {
        "id": "inventory.exit_residual",
        "slice": "0.63.38",
        "law": (
            "open_residual_edges / admission_inventory open_residual_* split "
            "named residuals from paid; doctor + packaging present for "
            "exit judgment (not dual readiness)"
        ),
    },
    {
        "id": "surface.capability_voice",
        "slice": "0.67.4",
        "law": (
            "REST 409 capability_refused + MCP/WS/CLI/SSR label the organ "
            "door (not 500 / admission_refused / generic RuntimeError)"
        ),
    },
)

# Known open edges — purge or kill-date; not permanent dual.
READINESS_EDGES: tuple[dict[str, str], ...] = (
    {
        "id": "assist.soft_catalog",
        "note": (
            "0.63.10 operate eyes; 0.63.21 scenario start + open flow create gated; "
            "0.63.22 admission_source inject (published admission); menu nests "
            "admission / start_allowed (no start CTA when closed)"
        ),
        "intent": "paid start + published-admission inject; residual only soft catalog browse packaging",
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
            "0.63.13 definition seed + drain seed; 0.63.19 full MEMBERSHIP_CAPABILITY_SEEDS "
            "catalog + bootstrap single source. work_drain install reads definition "
            "capabilities after load (not composition.has / BootMode)."
        ),
        "intent": "paid catalog SD-021 — residual only named packaging duals (bare enable_event_outbox)",
        "status": "paid_catalog_0_63_19",
    },
    {
        "id": "outbox.start_option_seed",
        "note": (
            "0.65.2: host system_spawn sets enable_event_outbox from "
            "definition has_capability('outbox') when not explicit. "
            "Bare BaseRuntime.start(enable_event_outbox=) remains packaging "
            "residual for non-host shells."
        ),
        "intent": "paid host path — DNA chooser; bare runtime seed named residual",
        "status": "paid_host_0_65_2",
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
        "id": "place_registry.os_spawn",
        "note": (
            "0.63.15–17: OS process + workload: place spawn + host auto-bind "
            "WorkloadEngine on assemble (structure_bind_workload=False opt-out)"
        ),
        "intent": "paid for host path; residual only if custom seats bypass bind",
        "status": "paid_0_63_17",
    },
    {
        "id": "work_plane.able_default_open",
        "note": (
            "0.63.23: able default / attach omit / set_able(None) / install missing "
            "able all fail closed (False). 0.67.2: work-plane able also needs work_drain."
        ),
        "intent": "paid",
        "status": "paid_0_63_23",
    },
    {
        "id": "host.soft_definitions_ready",
        "note": (
            "Audit 0.63.23: no host flag invents business readiness beside admission "
            "pointer (packaging_status.structure). Residual: packaging bags remain "
            "eyes residual (CS-002), not structure law."
        ),
        "intent": "named residual — packaging eyes only, not dual ready flag",
        "status": "named_0_63_23",
    },
    {
        "id": "execution.workload_engine_dig",
        "note": (
            "0.63.20 start_workload · 0.63.27 exec_workload gated on port. Direct "
            "WorkloadEngine.start/exec: structure place registry + unit free; product dig "
            "for business is dual readiness."
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
        "intent": "name residual — control path, not business start; revisit if product misuses",
        "status": "named_0_63_27",
    },

    {
        "id": "execution.resource_engine_dig",
        "note": (
            "0.63.24 gates ExecutionPort.invoke_resource. Direct ResourceEngine.invoke "
            "is unit/non-port free; product/surface dig for business effects is dual readiness."
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
        "intent": "name residual — control path, not business continue (SD-020)",
        "status": "named_0_63_29",
    },
    {
        "id": "assist.continue_edge",
        "note": (
            "0.63.29: AssistSession input / resume / backtrack gate on "
            "admission_gate() at product edge (published admission); deep "
            "provide_input / resume_job remain second wall."
        ),
        "intent": "paid product continue edge",
        "status": "paid_0_63_29",
    },
    {
        "id": "flows.continue_edge",
        "note": (
            "0.63.30: FlowSession input / resume / backtrack gate on "
            "flows.admission_gate(); host injects admission_source via "
            "admission_source_from_runtime_resolver (published-admission boy-scout)."
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
        "intent": "name residual — control path, not business start (SD-020)",
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
            "run_flow gate on admission_gate() at product edge (published admission); "
            "deep submit_flow / executor remain second wall. LIST/DESCRIBE catalog "
            "browse stays soft packaging eyes."
        ),
        "intent": "paid product start edge",
        "status": "paid_0_63_32",
    },
    {
        "id": "flows.soft_catalog",
        "note": (
            "FlowExecutionService LIST / DESCRIBE remain without business "
            "admission — packaging catalog browse, not business start."
        ),
        "intent": "named residual — soft catalog eyes (same spirit as assist.soft_catalog)",
        "status": "named_0_63_32",
    },
    {
        "id": "host.packaging_start_continue_edge",
        "note": (
            "0.63.33: ApplicationHost business start/continue doors + PalmCommandHandlers "
            "SubmitFlow/Process, ProvideInput, ResumeProcess, PreparePlans, "
            "SubmitPlans gate on admission; product façades remain preferred "
            "product path; ports remain second wall."
        ),
        "intent": "paid packaging host business start/continue edge",
        "status": "paid_0_63_33",
    },
    {
        "id": "kernel.direct_dig",
        "note": (
            "PalmKernel / BaseRuntime public submit/provide/invoke remain "
            "port-gated only. Digging host.app or bare runtime bypasses "
            "host packaging edge — dual readiness if product uses it for business. "
            "0.63.34: CLI + SSR explorer business start/continue digs boy-scouted to host."
        ),
        "intent": "name residual — port is law; packaging host is the door (SD-020)",
        "status": "named_0_63_33",
    },
    {
        "id": "surface.host_port_edge",
        "note": (
            "0.63.34: CLI resume_job/invoke and SSR explorer invoke/resume "
            "route through host packaging (or admit+port when host-less); "
            "wizard CQRS ProvideWizardInput / RequestWizardBacktrack gate "
            "admission at pattern handler; host.resume_job packaging door."
        ),
        "intent": "paid surface host/port boy-scout",
        "status": "paid_0_63_34",
    },
    {
        "id": "surface.rest_admission_voice_edge",
        "note": (
            "0.63.35: REST error helper admission_refused (503) + "
            "maybe_admission_refused on assist/flows/processes/providers/"
            "workloads/jobs/plans/instances business start/continue paths. "
            "Gate already raised under product/port; surface now speaks truth."
        ),
        "intent": "paid REST honest voice for closed gate",
        "status": "paid_0_63_35",
    },
    {
        "id": "surface.mcp_ws_admission_voice_edge",
        "note": (
            "0.63.36: MCP maybe_admission_refused_error → PalmRestError 503 "
            "admission_refused on in-process business start/continue; WebSocket "
            "assist maps AdmissionRefusedError to code admission_refused "
            "(not internal). HTTP MCP inherits REST voice via bridge."
        ),
        "intent": "paid MCP + WS honest voice for closed gate",
        "status": "paid_0_63_36",
    },
    {
        "id": "surface.cli_ssr_admission_voice_edge",
        "note": (
            "0.63.37: CLI business start/continue commands use print_cli_error "
            "(admission_refused brand); SSR explorer start/continue "
            "banners use operator_error_text; wizard backtrack catches "
            "RuntimeError so closed gate is not an unhandled 500."
        ),
        "intent": "paid CLI + SSR explorer honest voice for closed gate",
        "status": "paid_0_63_37",
    },
    {
        "id": "inventory.exit_residual_edge",
        "note": (
            "0.63.38: admission_inventory exposes open_residuals / open_residual_ids "
            "and paid_edge_count; doctor prints structure admission + open "
            "residuals; packaging bag nests open_residual_count. "
            "Does not invent dual readiness — cartography for José exit."
        ),
        "intent": "paid exit residual cartography",
        "status": "paid_0_63_38",
    },
    {
        "id": "surface.capability_voice_edge",
        "note": (
            "0.67.4: REST maybe_admission_refused maps CapabilityRefusedError "
            "to 409 capability_refused; MCP PalmRestError 409; CLI/SSR brand "
            "capability_refused; Assist WS structure_refuse_voice. Ready-false "
            "stays 503 admission_refused."
        ),
        "intent": "paid surface honest voice for missing organ",
        "status": "paid_0_67_4",
    },
    {
        "id": "work_plane.tick_schedules_edge",
        "note": (
            "0.67.5: tick_schedules fail-closed on work-plane able (ready then "
            "work_drain). Host tick_work follows. Background poll already skipped "
            "when not able. ScheduleRegistry.tick stays a store helper."
        ),
        "intent": "paid schedule fire as drain query, not ready-as-membership",
        "status": "paid_0_67_5",
    },
)


def _status_kind(status: str) -> str:
    """Classify dual-readiness residual row status for exit cartography."""
    if status.startswith("named_"):
        return "open"
    if status.startswith("paid"):
        return "paid"
    return "other"


def open_residual_edges() -> list[dict[str, str]]:
    """Named residuals still open — not architecture; exit judgment map."""
    return [dict(row) for row in READINESS_EDGES if _status_kind(row["status"]) == "open"]


def paid_readiness_edges() -> list[dict[str, str]]:
    """Edges paid or boy-scouted (status starts with ``paid``)."""
    return [dict(row) for row in READINESS_EDGES if _status_kind(row["status"]) == "paid"]


def admission_inventory() -> dict[str, Any]:
    """Static admission inventory — admitted paths vs dual-readiness residual · open residuals."""
    open_rows = open_residual_edges()
    paid_rows = paid_readiness_edges()
    return {
        "theme": "0.63",
        "role": "admission_inventory",
        "gated_paths": list(GATED_PATHS),
        "readiness_edges": list(READINESS_EDGES),
        "gated_count": len(GATED_PATHS),
        "readiness_edge_count": len(READINESS_EDGES),
        # 0.63.38 exit readiness — open named residuals first-class
        "open_residuals": open_rows,
        "open_residual_count": len(open_rows),
        "open_residual_ids": [row["id"] for row in open_rows],
        "paid_edge_count": len(paid_rows),
        "paid_edge_ids": [row["id"] for row in paid_rows],
    }


def admission_inventory_snapshot(runtime: Any | None = None) -> dict[str, Any]:
    """Static map plus live admission when *runtime* is given."""
    body = admission_inventory()
    body["live"] = None
    if runtime is None:
        return body
    admission = getattr(runtime, "admission", None)
    structure = getattr(runtime, "structure", None)
    live: dict[str, Any] = {
        "is_started": bool(getattr(runtime, "is_started", False)),
        "has_structure_seat": structure is not None,
    }
    from palm.system.structure.errors import admission_as_dict

    bag = admission_as_dict(admission) if admission is not None else None
    if bag is not None:
        live["admission"] = bag
    if structure is not None:
        definition = getattr(structure, "definition", None)
        live["definition_id"] = (
            getattr(definition, "id", None) if definition is not None else None
        )
        live["refuse"] = (
            sorted(getattr(definition, "refuse", ())) if definition is not None else []
        )
    body["live"] = live
    return body


__all__ = [
    "GATED_PATHS",
    "READINESS_EDGES",
    "open_residual_edges",
    "paid_readiness_edges",
    "admission_inventory",
    "admission_inventory_snapshot",
]
