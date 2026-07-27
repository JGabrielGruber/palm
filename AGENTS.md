# AGENTS.md

**Palm Engine Constitution**  
For AI coding agents and human developers  

*“Palm grows where the sun meets the sea.”*  
Orchestration should feel alive, truthful, and humane. Structure must serve clarity and longevity, never become a cage.

**Last updated:** July 2026 (0.54 closed; **0.55 Reactive Interests** executing — [VISION-0.55](docs/VISION-0.55.md) · [ADR-025](docs/adr/025-reactive-interests.md); law in [EVENT-PLANE](docs/EVENT-PLANE.md) · [WORK-DRAIN](docs/WORK-DRAIN.md); north star [VISION-GROVE](docs/VISION-GROVE.md); session plane → [VISION-SESSION-PLANE](docs/VISION-SESSION-PLANE.md))

---

## 1. Enduring Principles

These principles are non-negotiable. They exist so that Palm can evolve for a decade without descending into complexity debt.

| Principle | Meaning | Why it enables longevity |
|---------|--------|--------------------------|
| **Single Responsibility** | One reason to change per module, class, or function | Prevents god objects and tangled growth |
| **Explicit Boundaries** | Clear contracts between layers. Prefer composition and registries over inheritance and implicit magic | Makes the system understandable at any scale |
| **Core Purity** | `palm/core/` must never import from any other Palm package | The foundation stays stable and testable forever |
| **Registry-Based Extension** | New capabilities are added by registering at the edges, never by modifying core contracts | Evolutionary architecture without core erosion |
| **Documentation as Code** | Documentation, ADRs, and architectural summaries are maintained with the same rigor as source code | Prevents knowledge rot as the project grows |
| **Testability First** | Core logic and critical paths must be unit-testable in isolation | Enables confident refactoring and long-term maintenance |
| **Human-First + Truth-Seeking** | Interactive flows, backtracking, compensation, and observability are first-class concerns | The engine serves people, not the other way around |
| **Minimal Magic** | Prefer readable, explicit code over clever dynamic behavior | Reduces cognitive load and surprises over time |

---

## 2. Current Architecture Snapshot (0.10+)

Palm follows a **layered, registry-driven** architecture with a pure core.

```
User / CLI / REST / MCP
        ↓
palm/runtimes/             ← Thin adapters per service domain (map transport → services)
        ↓
palm/app/                  ← ApplicationHost (primary orchestrator)
        ↓
palm/services/             ← User-facing API (definitions, execution, system, assist)
        ↓
palm/common/               ← CQRS buses, schemas, hooks, persistence, service primitives
        ↓
palm/core/                 ← PURE foundational engines (Behavior Tree, Orchestration,
                            Context, Storage, Resource, Event, Auth, Transform)
```

> **0.16** domain API lives in `palm/services/`; `palm/common/services/` retains `BaseService`, `errors`, `views` only. Vision: [docs/VISION-0.16.md](docs/VISION-0.16.md).

**Key layers and their roles:**

- **`palm/core/`** — Pure engines and primitives. Behavior Trees are the universal control-flow model. No external Palm imports allowed.
- **`palm/services/`** — User-facing business API (`DefinitionService`, `ExecutionService`, `SystemService`) composing schema-validated CQRS. Domain modules own `registry.py`. Runtimes call services; services do not import runtimes. Shared `BaseService` / views remain in `palm/common/services/`.
- **`palm/common/`** — The “middle layer” where most coordination lives. Execution plans, hooks, CQRS + `CqrsSchemaRegistry`, reliable events (outbox), compensation, transforms, and shared runtime infrastructure.
- **`palm/app/`** — Application-level orchestration. `ApplicationHost` (with composable `DeploymentProfile` roles) is the recommended entry point for most use cases. `PalmKernel` is infrastructure.
- **`palm/patterns/`, `palm/providers/`, `palm/storages/`** — Extensible “Django-style apps”. Each capability lives in its own subpackage with `registry.py`.
- **`palm/runtimes/`** — Thin surfaces (CLI, embedded, daemon, server). Heavy lifting lives in `palm.common.runtimes`.
- **`palm/definitions/` + `palm/instances/`** — Stable contracts and durable state.

**Core invariants that must never be broken:**
- `palm/core/` imports nothing from outside itself.
- All extension happens through registries (never by editing core files).
- Registries use `threading.RLock` and are populated at bootstrap time.
- Job state transitions happen only through `RunResult` + `OrchestrationEngine.apply_result()`.
- Persistence and resume are first-class (via `InstancePersistenceHook` and state snapshots).

### Reactive Interests (0.55 — two verbs on `runtime.event`)

Law ([VISION-GROVE](docs/VISION-GROVE.md) §4, [ADR-025](docs/adr/025-reactive-interests.md)): **completers emit self-events; Palm starts or continues.**

| Verb | Interest | Action | Modules |
|------|----------|--------|---------|
| **Start** | Trigger / inbound / schedule | WorkIntent → drain → new job | [WORK-DRAIN](docs/WORK-DRAIN.md), `palm.core.work`, `WorkDrainService` |
| **Continue** | Wait interest on parked owner | resume / fail owner | `palm.core.wait`, `palm.common.wait.WaitMatcher` |

- State key: **`palm.wait.interests`** (list). Nested wizards open `kind=job` when parking; workload stub uses `kind=workload` ([VISION-0.56](docs/VISION-0.56.md) socket).
- Wire: `BaseRuntime` attaches matcher on `runtime.event` (`enable_wait_matcher`). `ChildCompletionHook` is dual-path compat only.
- Surfaces: inspect / list-waiting / doctor expose **`waiting_on`**; doctor `reactive_interests`.
- Catalog: [EVENT-PLANE](docs/EVENT-PLANE.md) trigger ↔ wait table. Do **not** invent private resume paths for new async steps.

### Operating Palm via MCP (0.31 — meta-surface + assist-first)

Coding agents should operate Palm through MCP — **prefer a single meta-tool `palm_assist`**, not curl or sprawling per-domain tools.

| Step | Action |
|------|--------|
| **Docs (progressive)** | **L1 first:** `palm://agent/card` · L2 only if stuck: `palm://agent/guide` · skill/references · [docs/MCP.md](docs/MCP.md) · [docs/llms.txt](docs/llms.txt) |
| Setup (local) | `uv sync --extra mcp` · `PALM_MCP_IN_PROCESS=1` · optional **`PALM_MCP_SURFACE=assist`** (one tool) |
| Grok (this repo) | [`.grok/config.toml`](.grok/config.toml); skill [docs/skills/palm/SKILL.md](docs/skills/palm/SKILL.md) |
| Catalog size | `just mcp-inventory` / `just mcp-inventory surface=assist` |
| Operator loop | `palm_assist` → question/actions → input → complete |

**Default calls (assist-only safe):**

| Goal | Call |
|------|------|
| Menu | `palm_assist()` |
| Discover | `palm_assist(alias="assist/discover", params={query: "…"})` |
| Run flow | `palm_assist(params={flow_id: "coconut-npc"})` |
| Continue | `palm_assist(params={session_id, flow_id, value})` |
| Publish flow | `palm_assist(params={body: {name, pattern, options.steps}})` or `alias=design/publish` |
| Doctor / list / waiting | `assist/doctor` · `assist/catalog/flows` · `assist/catalog/waiting` (rows may include **`waiting_on`**) |
| Resume resource | `alias=flows/session-resume` + `session_id`, `flow_id` |

**Conventions:** session-first (`session_id`); plain `value`/`input` strings; follow returned **`question` / `choices` / `actions` / `mutation`** / **`waiting_on`**; do **not** guess state; design writes via **publish** (or propose→impact→commit only when inspecting impact); never `palm_processes_submit` for interactive wizard entry; `resume-child-wait` only when `waiting_for_child` (matcher is normative unpark when interest is open).

**Token efficiency (0.31):**

- Prefer **`PALM_MCP_SURFACE=assist`** for weak LLMs (≈1 tool vs ≈39).
- Prefer **L1 card** over loading full skill + all references.
- Prefer **one-shot publish** over multi-step design tools when validating impact is not required.
- When **adding MCP capability**, prefer **assist aliases/paths** over new top-level tools so slim surface stays complete ([VISION-0.31](docs/VISION-0.31.md)).

**Extending MCP:** pattern `register_mcp_contributor()` / app `register_app_mcp_contributor()`; logic in `palm/common/operator/` or services — not thick runtime code. New happy paths should work via **`palm_assist` alone**.

---

## 3. Core Purity Rules (Strict)

Nothing inside `src/palm/core/` may import from:
- `palm.app`, `palm.common`, `palm.patterns`, `palm.providers`, `palm.storages`, `palm.runtimes`, `palm.definitions`, `palm.instances`, or `palm.utils`

Violation of this rule is considered a serious architectural defect.

---

## 4. How to Add or Extend Palm

Follow these patterns. They exist so growth remains orderly.

| What you want to add | Where it goes | How |
|----------------------|---------------|-----|
| New pattern (wizard, parallel, dag, etc.) | `palm/patterns/<name>/` | `pattern.py` + `app.py` (PatternApp) + `registry.py` + `bindings/definitions/builder.py`. Add to `INSTALLED_PATTERNS` in `patterns/_apps.py`. See [docs/PATTERN-APPS.md](docs/PATTERN-APPS.md) |
| New provider (REST, GraphQL, Postgres, `kv`, etc.) | `palm/providers/<name>/` | `provider.py` + `app.py` (ProviderApp) + `registry.py` + `bindings/` + `flow/` as needed. Optional `bindings/design.py` + `design_contributor` hook for `propose_resource`. Add to `INSTALLED_PROVIDERS`. See [docs/PROVIDER-APPS.md](docs/PROVIDER-APPS.md) · [ADR-011](docs/adr/011-local-document-resources.md) |
| New storage backend | `palm/storages/<name>/` | Same structure. Add to `INSTALLED_STORAGES` (use optional extras when drivers are needed) |
| New transform rule | `palm/common/transforms/rules/` | Implement `BaseTransformRule`, register with `register_transform()` or `@transform_rule` |
| CQRS command or query | Pattern-owned: `palm/patterns/<name>/bindings/cqrs/` | Register via `register_cqrs_contributor()` in `PatternApp.ready()`. Generic buses live in `palm/common/cqrs/` |
| Service CQRS transport | `palm/services/<domain>/bindings/cqrs/` | `ServiceCqrsContributor` in `palm/services/_cqrs_registry.py`; wire via `wire_all_service_cqrs()` on host/context — see [ADR-009](docs/adr/009-service-cqrs-contributors.md) |
| CQRS schemas | `palm/patterns/<name>/bindings/cqrs/schemas.py` | Add `command_schemas` / `query_schemas` on `CqrsContributor`; optional `instance_status_query` for inspect |
| Service method | `palm/services/<domain>/` | Compose CQRS in domain `service.py`; register REST/MCP in domain `registry.py`; wire on host/context in `_wire_cqrs()` |
| MCP tool (0.16+) | `palm/runtimes/mcp/<domain>/` | Group tools by service domain (`flows`, `providers`, `definitions`, `system`); pattern contributors stay in pattern `bindings/mcp.py` |
| New host role / capability | `palm/app/host/` | Extend `DeploymentProfile` or add to `ApplicationHost` wiring |
| Compensation handler | During definition bootstrap | Register on `default_compensation_registry()` |
| New runtime surface | `palm/runtimes/<name>/` | Keep thin. Put logic in `palm.common.runtimes` |
| WebSocket / Portal transport (0.32+) | `palm/runtimes/server/surfaces/websocket/` | Frames → shared assist dispatch; **no** new service domain; see [VISION-0.32](docs/VISION-0.32.md) |
| MCP tool, resource, or prompt | `palm/runtimes/mcp/` + pattern or app `app.py` | Pattern: `register_mcp_contributor()`. App: `register_app_mcp_contributor()`. See [docs/MCP.md](docs/MCP.md) |
| Cross-cutting coordination | `palm/common/<area>/` | executions, plans, hooks, persistence, etc. |
| Wait interest (pure) | `palm/core/wait/` | `WaitInterest`, open/close on state — no I/O |
| Wait matcher / policy / workload stub | `palm/common/wait/` | Match `runtime.event` → resume/fail; stub emit for 0.56 |
| Definition revisioning (0.24+) | `palm/common/persistence/definition_repository.py`, `palm/definitions/`, `palm/instances/` | Append-only `publish_flow_revision`; instance `flow_revision` pin; see [VISION-0.24](docs/VISION-0.24.md) |
| Definition migration rules (0.24.2+) | `palm/common/persistence/definition_migration.py` | `register_migration_rule()` / `resolve_migration_rule()`; see [ADR-007](docs/adr/007-definition-revisioning.md) |
| Instance migration execution (0.24.3+) | `palm/common/persistence/instance_migration.py` | `migrate_instance()`; preserve `migration_*` in `instance_sync.py`; REST `POST …/instances/{id}/migrate` |
| Design Service (0.25+) | `palm/services/design/` | Propose/validate/impact/commit + auto-migrate atop revisions; layered with `DefinitionService` CRUD — see [VISION-0.25](docs/VISION-0.25.md), [ADR-008](docs/adr/008-design-service.md) |
| Assist design entry (0.30+) | `palm/services/assist/` + operator-entry / design-entry scenarios | Surface create/improve flow from Assist without reimplementing Design — [VISION-0.30](docs/VISION-0.30.md) |
| MCP meta-surface (0.31+) | `palm/runtimes/mcp/` surface profiles | Progressive disclosure: slim tool catalogs, assist-as-meta-execute, inventory measurement — [VISION-0.31](docs/VISION-0.31.md) |
| WebSocket Assist / Portal (0.32+) | `palm/runtimes/server/surfaces/websocket/` | Human real-time Assist channel (same dispatch as MCP); Portal PWA client later — [VISION-0.32](docs/VISION-0.32.md) |
| Application-level orchestration | `palm/app/` | Prefer `ApplicationHost` over direct `PalmKernel` usage |

**Never:**
- Add new logic directly into core engines
- Create new top-level packages without strong justification
- Put pattern-specific logic in `palm/common/`

---

## 5. Documentation & Knowledge Discipline (Critical for Longevity)

Documentation is not optional. It is part of the system.

- **ADR or explicit waive (0.52.5 / PD-020):** every significant architectural decision **must** either:
  1. ship an ADR under [`docs/adr/`](docs/adr/) (template: [`.github/ISSUE_TEMPLATE/adr.md`](.github/ISSUE_TEMPLATE/adr.md)), **and** be listed in [`docs/adr/README.md`](docs/adr/README.md); or
  2. record an **explicit waive** on the theme VISION / STATUS slice: `ADR: waived — <one-line reason>` (e.g. pure rename covered by an existing ADR, docs-only, trivial fix).
  Numbers are **append-only** (next free integer; never renumber). Vacant slots (e.g. 013) stay vacant — see [013-number-reserved](docs/adr/013-number-reserved.md).
- Major changes to public API, layer responsibilities, or reliability primitives **must** update:
  - `README.md`
  - `ARCHITECTURE.md`
  - `DEVELOPMENT.md`
  - `AGENTS.md` (this file)
  - `docs/migrations/MIGRATION-*.md` when breaking changes occur
- A living `STATUS.md` must exist and be kept reasonably current. It is the single source of truth for the current state of the project.
- Living Library: [`docs/LIBRARY.md`](docs/LIBRARY.md) · wiki [`docs/wiki/`](docs/wiki/index.md).
- `docs/mcp.txt` should be maintained as the MCP operator guide (served as `palm://agent/guide` via `PALM_LLMS_TXT`).
- `docs/llms.txt` should be maintained as broader project context for AI agents.
- `docs/MCP.md` is the canonical guide for agent development with Palm MCP (setup, workflows, tool inventory).
- When updating the website (`docs/index.html`), structured data (JSON-LD) and feature highlights must reflect current capabilities.
- **`TECH-DEBT.md`** (repo root) is the single source of truth for known technical debt — peer to `STATUS.md`. Add new items as `PD-NNN`; close them as fixed. Do not let it go stale.
- **`docs/VERSIONING.md`** defines the versioning & release convention: **one theme per minor**, `X.0` plans (a `VISION-0.X.md`), `X.N` executes one slice each. Read it before opening a new minor.
- **Docs-sync is gated:** `just docs-check` must pass. Version stamps (including `ARCHITECTURE` / `DEVELOPMENT` / `SCOPE`) and MCP/Grok mirrors update via `scripts/sync_version.py` / `just bump-version`.

**Rule:** If the code and the documentation diverge, the documentation debt must be treated as seriously as a bug.

---

## 6. Review Checklist (Before Merge)

- [ ] Core purity preserved (`palm/core/` has no external Palm imports)
- [ ] SRP respected — no god classes or mixed responsibilities
- [ ] Extension done via registries (not by modifying core contracts)
- [ ] Thread-safety respected for all registries
- [ ] Tests added/updated (unit + integration where appropriate)
- [ ] Documentation updated (README, ARCHITECTURE, ADRs, STATUS.md, etc.)
- [ ] **ADR or waive** — significant decisions have a new/updated `docs/adr/*` (+ index) **or** an explicit `ADR: waived — …` on the theme VISION/STATUS *(PD-020)*
- [ ] `just docs-check` green when docs or version surfaces change
- [ ] No imports from `archive/`
- [ ] Public API surface is explicit (`__all__` where relevant)
- [ ] Backward compatibility or clear deprecation path considered
- [ ] `palm doctor` and example flows still work (when relevant)
- [ ] `just guard-common` passes (no pattern-specific logic in `palm.common`)
- [ ] **`just check` is green in CI**, not only locally — lint, typecheck, test-quick, guard-core, guard-common. A red gate blocks merge. *(the enforcement gap that let the 0.45 suite rot — see TECH-DEBT PD-001/002)*
- [ ] **No new god-objects** — a class/module that mixes lifecycle + wiring + domain + presentation is a defect; extract role/subsystem objects instead of accreting onto `ApplicationHost` & friends *(PD-009)*
- [ ] **Test doubles contract-match production** — fakes/stubs are validated against the real interface (a `Protocol`/ABC or a contract test), never hand-drifted. A fake lagging a prod signature is a bug *(PD-003)*
- [ ] **Experimental / placeholder capabilities are gated** behind an explicit flag, not silently registered as installed *(PD-023)*
- [ ] **No new function-local ("deferred") imports** added solely to dodge an import cycle without a comment justifying why — prefer fixing the layering *(PD-012)*
- [ ] Changes are scoped to a single patch per `docs/VERSIONING.md` (`feat(0.X.N): …`, one slice, cite the item)

---

## 7. Archive Policy

Everything under `archive/` is historical reference only.  
**New code must never import from `archive/`.**

When a component is truly deprecated and removed from active use, it may eventually move to `archive/`, but only after a proper migration path and deprecation period.

---

## 8. Spirit of the Project

Palm should remain:
- **Simple at the core**, powerful at the edges
- **Human-first** — wizards, backtracking, compensation, and observability are not afterthoughts
- **Truth-seeking** — explicit state, durable instances, and honest error handling
- **Evolutionary** — registries and hooks allow major new capabilities without rewriting the foundation
- **Reference-quality** — clean boundaries, excellent documentation, and high testability so others can learn from it

We optimize for **long-term clarity and maintainability** over short-term cleverness.

---

## 9. How to Update This Constitution

This document is living. When the architecture evolves significantly (new major layer, fundamental shift in extension model, new reliability primitive, etc.), update this file through a pull request accompanied by an ADR when appropriate.

The goal is not rigidity, but **intentional, documented evolution**.
