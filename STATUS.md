# Palm Engine — Project Status

**Current Version:** `0.61.0` (stamp) · **Active theme:** **`0.61` Living-kernel vitality** · **Prior closed:** **`0.60` Supervisor + work plane** · **`0.59` System Boot** · **`0.58` Session** · **`0.57` System** · **`0.56` Workload** · **`0.55` Reactive**  
**Last Updated:** August 3, 2026 · **Theme open:** **0.61.0** ✅ · **0.61.1** walk landed · **0.61.2** projection landed (stamps later)  
**System map:** [docs/PALM.md](docs/PALM.md) · **Theme:** [VISION-0.61](docs/VISION-0.61.md) **open** · **ADR:** [030](docs/adr/030-system-vitality.md) **Proposed** · prior [VISION-0.60](docs/VISION-0.60.md) · [ADR-029](docs/adr/029-system-supervisor.md) Accepted  
**Migration / release:** prior [MIGRATION-0.60](docs/migrations/MIGRATION-0.60.md) · [RELEASE-0.60.9](docs/releases/RELEASE-0.60.9.md) · [MIGRATION-0.59](docs/migrations/MIGRATION-0.59.md) · [RELEASE-0.59.8](docs/releases/RELEASE-0.59.8.md)  
**Debt (live):** [TECH-DEBT.md](TECH-DEBT.md) — **SD-007** / **CS-002** / **OD-001** (vitality) · residual **BI-*** / **SI-*** / **SU-*** · surface seed [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md) · seed essay [VISION-VITALITY](docs/VISION-VITALITY.md) · archive [docs/audit/TECH-DEBT-ERA-0.45.md](docs/audit/TECH-DEBT-ERA-0.45.md)  
**Library:** [docs/LIBRARY.md](docs/LIBRARY.md) · [docs/wiki/](docs/wiki/index.md)  
**Maturity:** Wizard · MCP · Assist · composition · reactive law · workload scout · **system + kits** · **session plane** · **boot + modes** · **supervisor + work plane** · system log **live** · **vitality seat walk live** · [Grove](docs/VISION-GROVE.md).

### Agent resume (after compact)

Read in order: **this STATUS** → [PALM.md](docs/PALM.md) → open [VISION-0.61](docs/VISION-0.61.md) · [ADR-030](docs/adr/030-system-vitality.md) · residual [TECH-DEBT.md](TECH-DEBT.md) · seed essay [VISION-VITALITY](docs/VISION-VITALITY.md) · [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md).

| Spirit | Decision |
|--------|----------|
| **0.61 open** | Living-kernel **vitality** — system eyes (`top`); inspect present; doctor is debt |
| **Seat walk** | **`palm.system.vitality`** — `palm.seat_report/1` · `discover_seats` · probe catalog |
| **Projection** | `VitalityRegistry` + `VitalityProjection` · `palm.vitality_snapshot/1` · `project` / `project_top` |
| **Adapter law** | Residue only — forward work as if not foundation; interpret in product present |
| **0.60 closed** | Planes = start/continue traffic; **Supervisor** = continuous services; inbound on system |
| **Host** | Packaging — prefers system seats; product enrich residual; host status not living law |
| **Boot law** | Two schedules; composition = membership; modes via `for_mode` |
| **System log** | Observation tape live — [SYSTEM-LOG](docs/SYSTEM-LOG.md); catalog residual **BI-015** |
| **Closed** | **0.60.0–0.60.9 + exit** — BI-013 closed · ADR-029 Accepted · stamp `0.60.9` |
| **Next** | **0.61.3+** emission window · Inspect rename · growth (stamps when José exits) |
| **Later seeds** | [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md) · residual BI · user-plane · workload remainder · Grove |

## Quick Overview

Palm is a lightweight, Python-first orchestration engine built on a clean **Behavior Tree** foundation. It excels at complex multi-step workflows, rich interactive wizards, compositional sub-flow orchestration, and transactional processes with durable state and human-in-the-loop participation.

**Distribution name:** `palmengine` (PyPI)  
**Import name:** `palm`  
**Recommended entrypoint:** `ApplicationHost` via `create_cli_host()` for CLI, or `ApplicationHost(profile=DeploymentProfile.all_in_one())` for library use

## 0.61 — Living-kernel vitality (**open** · plan `0.61.0` · walk landed)

**Vision:** [docs/VISION-0.61.md](docs/VISION-0.61.md) · **ADR:** [docs/adr/030-system-vitality.md](docs/adr/030-system-vitality.md) **Proposed**  
**Seed essay:** [docs/VISION-VITALITY.md](docs/VISION-VITALITY.md)  
**Package:** `palm.system.vitality` · schema **`palm.seat_report/1`**  
**Debt:** [TECH-DEBT.md](TECH-DEBT.md) **SD-007** · **CS-002** · **OD-001** · **BI-015** neighbor  
**Map:** [docs/PALM.md](docs/PALM.md) · prior supervisor [VISION-0.60](docs/VISION-0.60.md)

**Theme purpose:** System-intrinsic **vitality** (living `top`) — dynamic seat discovery, seat reports, projection + registry, inspect present. Doctor is legacy debt, not the kernel home. Not surface compost. Not Grove mesh.

| Patch | Status |
|-------|--------|
| **0.61.0** | ✅ plan + ADR-030 Proposed |
| **0.61.1** | ✅ seat report + dynamic walk — stamp when José exits |
| **0.61.2** | ✅ projection + registry (`seat_walk`) — stamp when José exits |
| **0.61.3+** | 📋 emission · Inspect rename · growth |

**Floor (eyes open):** dynamic walk · seat report · projection + registry · inspect top from projection · emission identity · SD-007 path · doctor debt named.  
**Exit:** **José’s** judgment when eyes are proper — not empty checklist death.  
**Theme law (all minors):** [docs/VERSIONING.md](docs/VERSIONING.md) (*Who decides*) · [AGENTS.md](AGENTS.md) §6b.

---

## Architecture Snapshot

**Canonical map:** [docs/PALM.md](docs/PALM.md) — whole organism (job path, engines, ports, planes, product). Dense detail: [ARCHITECTURE.md](ARCHITECTURE.md) · agent rules: [AGENTS.md](AGENTS.md).

Palm is layered and registry-driven. Core stays pure. The **job path** is the spine (definition → pattern → job → effects → events).

| Layer | Role (short) |
|-------|----------------|
| `palm/core/` | Pure engines. No external Palm imports. |
| **`palm/system/`** | Running Palm: `BaseRuntime`, ports, wait/work/workload planes; **session (0.58)**; **vitality (0.61)** (`palm.system.vitality`) ([PALM.md](docs/PALM.md)). |
| `palm/common/` | Shared libraries (plans, CQRS, transforms, persistence). No system shims. |
| `palm/kits/` | Surface infrastructure kits (`server`, …) — install-list truth. |
| `palm/services/` | Product (userland): definitions, execution, assist, design, … |
| `palm/app/` | Host + composition / deployment profiles. |
| `palm/patterns/`, `providers/`, `storages/`, `runners/` | Plugins by registry (`INSTALLED_*` truthful; intentions gated). |
| `palm/runtimes/` | Thin surfaces. |

## 0.60 — System Supervisor + Work Plane (**closed** · theme exit `0.60.9`)

**Vision:** [docs/VISION-0.60.md](docs/VISION-0.60.md) · **ADR:** [docs/adr/029-system-supervisor.md](docs/adr/029-system-supervisor.md) **Accepted**  
**Migration:** [MIGRATION-0.60](docs/migrations/MIGRATION-0.60.md) · **Release:** [RELEASE-0.60.9](docs/releases/RELEASE-0.60.9.md)  
**Debt:** [TECH-DEBT.md](TECH-DEBT.md) **BI-013** ✅ closed  
**Map:** [docs/PALM.md](docs/PALM.md) · prior boot [VISION-0.59](docs/VISION-0.59.md) · reactive [VISION-0.55](docs/VISION-0.55.md)  

**Theme purpose:** **Work plane** (start) on system · **Supervisor** for continuous services (work drain, outbox, inbound) · **inbound** system contract · host packaging. Not surface compost. Not Grove mesh.

| Patch | Status |
|-------|--------|
| **0.60.0** | ✅ plan + ADR-029 Proposed |
| **0.60.1** | ✅ Supervisor seat |
| **0.60.2** | ✅ WorkPlaneService |
| **0.60.3** | ✅ System job start default |
| **0.60.4** | ✅ System-path session attr |
| **0.60.5** | ✅ Supervised work_drain |
| **0.60.6** | ✅ OutboxLoopService |
| **0.60.7** | ✅ Catalog reload_from_repository |
| **0.60.8** | ✅ Inbound on system |
| **0.60.9** | ✅ Lean seats without host |
| **exit** | ✅ ADR-029 Accepted · BI-013 closed · stamp `0.60.9` |

**Residual after 0.60:** host product enrich/catalog wire · WorkDrainService fallback · BI-003 product assembly · surface deflation.

---

## 0.59 — System Boot + Composition Truth (**closed** · theme exit `0.59.8`)

**Vision:** [docs/VISION-0.59.md](docs/VISION-0.59.md) · **ADR:** [docs/adr/028-system-boot.md](docs/adr/028-system-boot.md) **Accepted**  
**Migration:** [MIGRATION-0.59](docs/migrations/MIGRATION-0.59.md) · **Release:** [RELEASE-0.59.8](docs/releases/RELEASE-0.59.8.md)  
**Debt residual:** [TECH-DEBT.md](TECH-DEBT.md) **BI-*** · [SD-014](TECH-DEBT.md#sd-014) ✅ closed  
**Map:** [docs/PALM.md](docs/PALM.md) §5.8 boot · **System log:** [SYSTEM-LOG](docs/SYSTEM-LOG.md)  

**Theme purpose:** Named **host + system boot schedules**, **composition membership truth**, and **boot modes**. System log as observation. Not surface compost. Not a second plugin framework.

| Patch | Status |
|-------|--------|
| **0.59.0**–**0.59.4** | ✅ plan → inventory → log → stubs → system + host schedules walked |
| **0.59.5** | ✅ composition membership truth |
| **0.59.6**–**0.59.7** | ✅ mode + shape dogfood |
| **0.59.8** | ✅ residual cleanup (fixture + dead spine) |
| **exit** | ✅ ADR-028 Accepted · SD-014 closed · residual BI named · stamp `0.59.8` |

**Not paid in 0.59:** dual root fold (BI-003), full suite mode force (BI-007), work start → system (BI-013 → **0.60**), surface chrome (BI-010 / deflation), richer system-log catalog (BI-015).

---

## 0.58 — Session plane (**closed** · theme exit `0.58.20`)

**Vision:** [docs/VISION-0.58.md](docs/VISION-0.58.md) · **ADR:** [docs/adr/027-session-plane.md](docs/adr/027-session-plane.md) **Accepted**  
**Map:** [docs/PALM.md](docs/PALM.md) · **Migration:** [MIGRATION-0.58](docs/migrations/MIGRATION-0.58.md) · **Release:** [RELEASE-0.58.20](docs/releases/RELEASE-0.58.20.md)  
**Debt residual:** [TECH-DEBT.md](TECH-DEBT.md) **SI-*** / **SU-*** · surface seed [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md) · boot residual **BI-*** (SD-014 closed at 0.59.8)  

**Theme purpose:** Session as **system plane** and growth glue. Every external interaction has a session. One session may own **many instances**. **Session owns surface context** (BoundSurface). Product **SessionService** is the surface door. Not the user plane. Not a second wait/resume path.

| Patch | Status |
|-------|--------|
| 0.58.0–0.58.13 | ✅ plane through service/origin sessions |
| 0.58.14–0.58.18 | ✅ BoundSurface → strict → inherit → kit door → operate |
| 0.58.19 | ✅ product vocabulary rename (`instance`) |
| 0.58.20 | ✅ docs/skill + residual honesty |
| **exit** | ✅ ADR-027 Accepted · SD-008 closed · stamp `0.58.20` · surface deflation **named** (not paid) |

**Not paid in 0.58:** full surface purge, FlowWalk rewrite (SI-002), explorer bare bind (SI-010). Wisdom kept in [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md).

---

## 0.57 — Palm System (**closed** · theme exit `0.57.14`)

**Vision:** [docs/VISION-0.57.md](docs/VISION-0.57.md) · **ADR:** [docs/adr/026-palm-system-layer.md](docs/adr/026-palm-system-layer.md) **Accepted**  
**Map:** [docs/PALM.md](docs/PALM.md) · **Low-level:** [docs/SYSTEM-LOW-LEVEL.md](docs/SYSTEM-LOW-LEVEL.md)  
**Migration:** [docs/migrations/MIGRATION-0.57.md](docs/migrations/MIGRATION-0.57.md) · **Release:** [docs/releases/RELEASE-0.57.14.md](docs/releases/RELEASE-0.57.14.md)  
**Debt residual:** [TECH-DEBT.md](TECH-DEBT.md) **SU-*** (optional) · **SD-008** → **0.58** · [STUBS.md](docs/STUBS.md) · [era archive](docs/audit/TECH-DEBT-ERA-0.45.md)

**Theme:** Name the system layer. Shared vs system. One execution port. Kits exposed. Document debt; pay structure in order.

| Patch | Status |
|-------|--------|
| 0.57.0 Plan + map + ADR | ✅ |
| 0.57.1 Debt archive + low-level design | ✅ |
| 0.57.2 System boundary in code (`palm.system`) | ✅ |
| 0.57.3 Execution port v1 + product effect rebind | ✅ |
| 0.57.4 Rebind graphs (P2 invoker/driver + builders) | ✅ |
| 0.57.5 Rebind product | ✅ |
| 0.57.6 Deflate common | ✅ BaseRuntime + planes under `palm.system` |
| 0.57.7 Edge policy | ✅ `resume_job` on port |
| 0.57.8 SD-012 import sweep | ✅ |
| 0.57.9 Capability catalog truth | ✅ ST-001…005 gated |
| 0.57.10 Docs/notes coherence | ✅ |
| 0.57.11 Wave F + job list on port | ✅ |
| 0.57.12 Shim delete + port catalog | ✅ |
| 0.57.13 Kits package | ✅ `palm.kits` + `palm.kits.server` |
| **0.57.14** Theme exit + version dump | ✅ ADR-026 Accepted · MIGRATION-0.57 · stamp `0.57.14` |
| **0.57 structure** | ✅ closed — SU-* optional; session opened as **0.58** |

**Docs rule:** ASD-STE100 for new/revised theme text ([docs/WRITING.md](docs/WRITING.md)).

## 0.52 — The Living Library (tooling)

**Vision:** [docs/VISION-0.52.md](docs/VISION-0.52.md) · **ADR:** [docs/adr/021-living-library.md](docs/adr/021-living-library.md)  
SOURCE/BUILD/SURFACE, root declutter, wiki shelves, thin `just docs-build`, Cloudflare assemble. T6 PD-019–021, PD-031 closed.

| Notes |
|-------|
| Static docs tooling remains. **DocsService / storage corpora product → after session + workload.** |

## 0.53 — Sovereign Runners (landed)

**Vision:** [docs/VISION-0.53.md](docs/VISION-0.53.md) · **ADR:** [docs/adr/022-neonroot-provider.md](docs/adr/022-neonroot-provider.md)  

NeonRoot provider (`health`/`spawn`, exclude/output), palm-ci / palm-docs images, doctor, Assist discover, composition capability `neonroot`. Workspaces are **tmpfs-disposable** by default.

| Patch | Status |
|-------|--------|
| 0.53.0–0.53.8 | ✅ closed |

## 0.54 — Hermetic Jobs (**closed**)

**Vision:** [docs/VISION-0.54.md](docs/VISION-0.54.md) · **ADR:** [docs/adr/023-hermetic-jobs.md](docs/adr/023-hermetic-jobs.md)  

**Theme:** Purpose test — definition-driven multi-step work; foreign code only via **neonroot**; grow real **dag** pattern.  

**Discarded from interim 0.54:** `common.library`, `providers/library`, `services/docs`, wiki-pin product path.

| Patch | Status |
|-------|--------|
| 0.54.0 Replan + discard product stack | ✅ |
| 0.54.1 Hermetic job contract + [HERMETIC-JOBS.md](docs/HERMETIC-JOBS.md) | ✅ |
| 0.54.2 Dogfood flow `hermetic-job-smoke` (neonroot only) | ✅ |
| 0.54.3 DAG pattern v0 (resource nodes + deps) | ✅ |
| 0.54.4 DAG fan-out `hermetic-job-fanout` | ✅ |
| 0.54.5 seed_mode bind/copy + run-dir docs | ✅ |
| 0.54.6 Second dogfood `hermetic-ci-slice` | ✅ |
| 0.54.7 Purpose-test notes (DEVELOPMENT/AGENTS) | ✅ |
| 0.54.8 Polish: drain_ready, run_dir helper, Assist discover | ✅ |
| 0.54.9 Assist run-code wizard (`hermetic-run-code`) | ✅ |
| 0.54.10 Run-code dogfood complete (Portal + resource auto-advance) | ✅ |
| **0.54 theme** | ✅ closed — dogfood proven |

## 0.55 — Reactive Interests (**closed** · theme exit `0.55.9`)

**Vision:** [docs/VISION-0.55.md](docs/VISION-0.55.md) · **ADR:** [docs/adr/025-reactive-interests.md](docs/adr/025-reactive-interests.md)  
**Migration:** [docs/migrations/MIGRATION-0.55.md](docs/migrations/MIGRATION-0.55.md)  
**North star:** [docs/VISION-GROVE.md](docs/VISION-GROVE.md) §4  

**Theme:** Two verbs on `runtime.event` — **start** (trigger → WorkIntent) and **continue** (wait interest → resume). Completers emit self-events; Palm matches. Nested flow cutover; second wait kind stub; inspect/doctor.

| Patch | Status |
|-------|--------|
| **0.55.0** Plan + ADR-025 + replan session → [VISION-SESSION-PLANE](docs/VISION-SESSION-PLANE.md) | ✅ |
| **0.55.1** Wait interest contract + helpers (`palm.core.wait`) | ✅ |
| **0.55.2** Matcher + resume/fail policy (`palm.common.wait`) | ✅ |
| **0.55.3** Nested flow opens wait (dual-path OK) | ✅ |
| **0.55.4** Matcher normative unpark; cutover | ✅ |
| **0.55.5** Inspect / Assist / list-waiting / doctor (`waiting_on`) | ✅ |
| **0.55.6** Restart + idempotency (rehydrate + matcher guards) | ✅ |
| **0.55.7** Second kind stub (`workload` + emit ready/fail) | ✅ |
| **0.55.8** Docs constitution (EVENT-PLANE, WORK-DRAIN, AGENTS, ARCHITECTURE) | ✅ |
| **0.55.9** Compat time-box + MIGRATION-0.55 + theme exit | ✅ |
| **0.55 law** | ✅ closed — base reactiveness unlocked; dual-path hook removed |
| **0.55.10** Continue plane — [VISION-0.55.10](docs/VISION-0.55.10.md) (`WaitPlaneService`) | ✅ |
| **0.55.11** Index discipline / single open path (`access` + rebuild) | ✅ |
| **0.55.12** Dual nested-state collapse (interest authority) | ✅ |
| **0.55.13** Slash `set_child_wait` façade → `nested_park` | ✅ |
| **0.55.14** Plane delivers nested completion; no pattern_park keep-open | ✅ |
| **0.55.15** Slim public API door — [VISION-0.55.15](docs/VISION-0.55.15.md) | ✅ |
| **0.55.16** Kind-generic deliver registry — [VISION-0.55.16](docs/VISION-0.55.16.md) | ✅ |
| **0.55.17** Nested success via deliver (poll fallback); host `wait_plane`; tests/wait/ | ✅ |
| **0.55.18** Remove `resume_child_wait` operator verb (plane owns unpark) | ✅ |
| **0.55.19** Drop ChildWaitHooks + poll completion; park waits for plane only | ✅ |
| **0.55.20** Operator surfaces use `waiting_on` only (drop dual waiting_for_child UX) | ✅ |
| **0.55.21** Drop `WAITING_FOR_CHILD` status; park signal `nested_park` | ✅ |

**Replan:** former Session plane content → [docs/VISION-SESSION-PLANE.md](docs/VISION-SESSION-PLANE.md) (queued after 0.55).

## 0.56 — Workload plane (**in progress**)

**Vision:** [docs/VISION-0.56.md](docs/VISION-0.56.md) · **ADR:** [docs/adr/024-workload-engine.md](docs/adr/024-workload-engine.md) (**Accepted**)

**Theme:** First-class **place** — pure `WorkloadEngine`, pluggable `WorkloadRuntime` adapters (`palm/runners/`), execution CQRS, WorkloadLeaf, events on the reactive plane. NeonRoot becomes a runtime, not “just another provider.”

| Slice | Status |
|-------|--------|
| **0.56.0–0.56.2** ADR-024 + core engine + Spec/Result/status/registry + WorkloadLeaf contract tests | ✅ foundation landed |
| **0.56.3–0.56.4** `palm/runners/` host (default **OFF**) + neonroot WorkloadRuntime; BaseRuntime wires engine; doctor `workloads` / host warning; settings `workload_host_enabled` | ✅ runners cut landed |
| **0.56.5–0.56.6** host warm **workspace** + exec; **`ExecutionService.workloads`** + CQRS (`workload.start|exec|stop|…`); host registry v0 | ✅ product path landed |
| **0.56.dogfood** wizard **`step_kind: workload`** + **run-python** flow (host \| neonroot \| auto); hermetic-run-code alias | ✅ simple contract dogfood |
| **0.56.9** **`on_workload`** trigger + work-drain on `workload.*`; **workload-followup** dogfood | ✅ reactive start path |
| **0.56 dual-path cut** **Removed neonroot ResourceEngine provider** — isolation is **only** `palm.runners.neonroot`; hermetic dogfood → workload/DAG workload nodes | ✅ cleaner plane |
| **0.56 trust** **`local` WorkloadRuntime** always on; runner **`health()`** + **`engine.doctor()`**; host remains opt-in; neonroot CLI probe via health | ✅ plane is real by default |
| **0.56 neonroot polish** Spec→`SpawnRequest` (`spec_map`); seed vocabulary; `run_spawn_request`; doctor via `RuntimeHealth`; stable `error_class` | ✅ runner cleaned |
| **0.56 edge surface (small)** REST `/v1/api/workloads/*` + assist aliases `workloads/*` (patterns still bind engines) | ✅ product edges for workload |
| **0.56.7+** full placement, production leaf→port, session cancel hooks, blueprints, warm workspace, peer mesh | 📋 queued |

**Package law:** `palm/core/workload/` (pure) · `palm/common/workload/` (wire/doctor helpers) · `palm/runners/*` · `services/execution/workloads/` · wait kind socket already from 0.55.

## Horizon

**North star:** [**The Grove**](docs/VISION-GROVE.md) — Palm Organization; deepen **start / continue / place / speak / trust**.

- **0.59** System boot + composition truth — **closed** at `0.59.8` ([VISION-0.59](docs/VISION-0.59.md) · [ADR-028](docs/adr/028-system-boot.md) Accepted · [SD-014](TECH-DEBT.md#sd-014) closed)  
- **0.58** Session plane — **closed**  
- **0.55** Reactive Interests — law closed  
- **0.56** Workload plane — scout; cancel/ownership consume session  
- **0.57** System layer — closed  
- Surface deflation seed ([VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md))  
- Docs dogfood domain (post boot + workload)  
- Adapter runners via workloads (PD-022)  
- Peer / org dogfood (Grove later seasons)  
- Shared plane-store framework — **ponder later**

See [TECH-DEBT.md](TECH-DEBT.md), [docs/VERSIONING.md](docs/VERSIONING.md), [docs/VISION-GROVE.md](docs/VISION-GROVE.md).
