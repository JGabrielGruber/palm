# Palm Engine — Project Status

**Current Version:** `0.54.10` · **Theme (plan):** **`0.57` Palm System** · **Scout:** **`0.56` Workload** (foundation) · **Prior:** **`0.55` Reactive Interests** · **`0.54` Hermetic Jobs**  
**Last Updated:** July 29, 2026  
**System map (read first):** [docs/PALM.md](docs/PALM.md) · [VISION-0.57](docs/VISION-0.57.md) · [ADR-026](docs/adr/026-palm-system-layer.md)  
**Library (0.52 tooling):** [docs/LIBRARY.md](docs/LIBRARY.md) · [docs/wiki/](docs/wiki/index.md)  
**Maturity:** Wizard · MCP · Assist · composition profiles · **0.52–0.55** law · continue plane · **WorkloadEngine** scout · **0.57** names the system layer · north star [Grove](docs/VISION-GROVE.md).

## Quick Overview

Palm is a lightweight, Python-first orchestration engine built on a clean **Behavior Tree** foundation. It excels at complex multi-step workflows, rich interactive wizards, compositional sub-flow orchestration, and transactional processes with durable state and human-in-the-loop participation.

**Distribution name:** `palmengine` (PyPI)  
**Import name:** `palm`  
**Recommended entrypoint:** `ApplicationHost` via `create_cli_host()` for CLI, or `ApplicationHost(profile=DeploymentProfile.all_in_one())` for library use

## Architecture Snapshot

**Canonical map:** [docs/PALM.md](docs/PALM.md) — whole organism (job path, engines, ports, planes, product). Dense detail: [ARCHITECTURE.md](ARCHITECTURE.md) · agent rules: [AGENTS.md](AGENTS.md).

Palm is layered and registry-driven. Core stays pure. The **job path** is the spine (definition → pattern → job → effects → events).

| Layer | Role (short) |
|-------|----------------|
| `palm/core/` | Pure engines. No external Palm imports. |
| **System** (0.57 target) | Running Palm: engines, ports, planes. Today split across `BaseRuntime` + parts of `common`. |
| `palm/common/` | Shared + undeclared system — split is the 0.57 work ([VISION-0.57](docs/VISION-0.57.md)). |
| `palm/services/` | Product (userland): definitions, execution, assist, design, … |
| `palm/app/` | Host + composition / deployment profiles. |
| `palm/patterns/`, `providers/`, `storages/`, `runners/` | Plugins by registry. |
| `palm/runtimes/` | Thin surfaces. |

## 0.57 — Palm System (**plan open**)

**Vision:** [docs/VISION-0.57.md](docs/VISION-0.57.md) · **ADR:** [docs/adr/026-palm-system-layer.md](docs/adr/026-palm-system-layer.md) · **Map:** [docs/PALM.md](docs/PALM.md)

**Theme:** Name the system layer. Shared vs system. One execution port for graphs and product. Archive old debt era. Docs in Simplified Technical English.

| Patch | Status |
|-------|--------|
| 0.57.0 Plan + map + ADR | 📋 plan open (this status) |
| 0.57.1+ Execute slices | pending |

**Docs rule:** New theme text uses **ASD-STE100** Simplified Technical English.

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

- **0.55** Reactive Interests — law closed; continue plane through deliver registry  
- **0.56** Workload plane — foundation green; runners + CQRS next ([VISION-0.56](docs/VISION-0.56.md) · [ADR-024](docs/adr/024-workload-engine.md))  
- **Session plane** (queued) — [VISION-SESSION-PLANE](docs/VISION-SESSION-PLANE.md)  
- Docs dogfood domain (post session + workload)  
- Adapter runners via workloads (PD-022)  
- Peer / org dogfood (Grove later seasons)  
- Payload/artifact registry for registered modules

See [TECH-DEBT.md](TECH-DEBT.md), [docs/VERSIONING.md](docs/VERSIONING.md), [docs/VISION-GROVE.md](docs/VISION-GROVE.md).
