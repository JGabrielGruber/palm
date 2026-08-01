# AGENTS.md

**Palm Engine — agent constitution**  
For AI coding agents and human developers who change code.

*“Palm grows where the sun meets the sea.”*

---

## 0. Read first (do not skip)

| Need | Open |
|------|------|
| **What Palm is** (layers, job path, ports, planes, laws) | **[docs/PALM.md](docs/PALM.md)** |
| **System low-level** (package, port, moves) | [docs/SYSTEM-LOW-LEVEL.md](docs/SYSTEM-LOW-LEVEL.md) |
| **Live debt** | [TECH-DEBT.md](TECH-DEBT.md) (SD/SU/ST/CS) · [docs/STUBS.md](docs/STUBS.md) intentions · archive [docs/audit/TECH-DEBT-ERA-0.45.md](docs/audit/TECH-DEBT-ERA-0.45.md) |
| How to write docs | [docs/WRITING.md](docs/WRITING.md) (ASD-STE100) |
| Project status / themes | [STATUS.md](STATUS.md) · [docs/VISION-0.59.md](docs/VISION-0.59.md) (**open** boot) · [docs/VISION-0.58.md](docs/VISION-0.58.md) (**closed** session) · [docs/VISION-SURFACE-DEFLATION.md](docs/VISION-SURFACE-DEFLATION.md) (queue) · [docs/VISION-0.57.md](docs/VISION-0.57.md) (**closed** system) |
| Multi-Palm horizon | [docs/VISION-GROVE.md](docs/VISION-GROVE.md) |
| MCP operate | [docs/MCP.md](docs/MCP.md) · skill [docs/skills/palm/SKILL.md](docs/skills/palm/SKILL.md) |

**Rule:** [PALM.md](docs/PALM.md) is the system map.  
**Do not** paste a second full architecture into this file.  
When structure changes, update **PALM.md** (and ADR if needed). Keep this file as **rules for agents**.

**Last updated:** August 2026 · map [PALM.md](docs/PALM.md) · boot theme [VISION-0.59](docs/VISION-0.59.md) **open** · [ADR-028](docs/adr/028-system-boot.md) Proposed · session [VISION-0.58](docs/VISION-0.58.md) **closed** · surface seed [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md)

---

## 1. Enduring principles

| Principle | Meaning |
|-----------|---------|
| **Single responsibility** | One reason to change per module |
| **Explicit boundaries** | Clear contracts; composition and registries over magic |
| **Core purity** | `palm/core/` never imports other Palm packages |
| **Registry extension** | Add capability at the edge; do not edit core contracts |
| **Documentation as code** | Docs and ADRs match the same rigor as source |
| **Testability first** | Critical paths unit-testable in isolation |
| **Human-first + truth-seeking** | Wait, resume, inspect, honest failure |
| **Minimal magic** | Prefer readable, explicit code |

Full layer laws: [PALM.md §9](docs/PALM.md).

---

## 2. Structure (pointer only)

Palm is layered: **core → system / shared / kits → plugins → product → surfaces**, with **app host** for boot.

- **Job path** is the spine (definition → pattern → job → effects → events).  
- **Ports** are the shared effect contract (graphs + product): ``palm.system.ExecutionPort``.  
- **`palm.system`** is the system home (BaseRuntime, planes, ports, executions, job hooks).  
- **`palm.kits`** is exposed surface infrastructure (``INSTALLED_KITS``; server kit first).  
- **Product** `services.system` ≠ **system layer** (kernel shape).  
- **Capability catalog is truthful:** default ``INSTALLED_*`` only; intentions use ``INTENTION_*`` / [STUBS.md](docs/STUBS.md).

Detail, engines, planes, growth table: **[docs/PALM.md](docs/PALM.md)** only.

**Hard invariants (code):**

- `palm/core/` imports nothing outside itself.  
- Extension via registries; registries use `threading.RLock`; populate at bootstrap.  
- Job transitions only through `RunResult` + `OrchestrationEngine.apply_result()`.  
- Persistence and resume are first-class.  
- No imports from `archive/`.  
- **No new engine shortcuts** for effects: use ``runtime.execution`` (or product that does).  
  Do not add edge/product calls to ``runtime.resource`` / ``runtime.orchestration`` for
  invoke/resume/workload effects without an SD-005 residual row.

---

## 3. Reactive interests (do not invent a second path)

Law: completers emit **self-events**; Palm **starts** or **continues**.  
Map: [PALM.md §5.4](docs/PALM.md) · [VISION-GROVE](docs/VISION-GROVE.md) §4 · [ADR-025](docs/adr/025-reactive-interests.md)

| Verb | Interest | Action |
|------|----------|--------|
| **Start** | Trigger | WorkIntent → drain → new job |
| **Continue** | Wait on owner | resume / fail owner |

**Agent rules:**

- State key: `palm.wait.interests`.  
- Continue path: **`WaitPlaneService`** on `runtime.event` only.  
- Do **not** invent private resume or completer→parent hooks.  
- Nested parent unpark: drive the **child**; do not poke the parent.  
- Detail: [EVENT-PLANE](docs/EVENT-PLANE.md) · [WORK-DRAIN](docs/WORK-DRAIN.md).

---

## 4. Operate Palm via MCP (assist-first)

Prefer **`palm_assist`**, not curl or many domain tools.

| Goal | Call |
|------|------|
| Menu | `palm_assist()` |
| Discover | `palm_assist(alias="assist/discover", params={query: "…"})` |
| Run flow | `palm_assist(params={flow_id: "…"})` |
| Continue | `palm_assist(params={instance_id, flow_id, value})` (legacy `session_id` ok if not `sess-…`) |
| Publish flow | `palm_assist(params={body: {…}})` or `alias=design/publish` |
| Doctor / list / waiting | `assist/doctor` · `assist/catalog/flows` · `assist/catalog/waiting` |

**Conventions:** instance-continue / system-session bind (`session_id` ≠ `instance_id`, 0.58); plain `value`/`input`; follow `question` / `choices` / `actions` / `waiting_on`; do not guess state.

**Setup:** `uv sync --extra mcp` · `PALM_MCP_IN_PROCESS=1` · optional `PALM_MCP_SURFACE=assist`.  
**Docs L1:** `palm://agent/card` before full skill.  
**Guide:** [docs/MCP.md](docs/MCP.md).

New MCP happy paths must work via **`palm_assist` alone** when possible (assist aliases over new top-level tools).

---

## 5. How to add or extend

Purpose of each home: [PALM.md §7](docs/PALM.md). Practical table:

| Add | Where | How |
|-----|--------|-----|
| Pattern | `palm/patterns/<name>/` | PatternApp + registry + builder; `INSTALLED_PATTERNS` · [PATTERN-APPS](docs/PATTERN-APPS.md) |
| Provider | `palm/providers/<name>/` | ProviderApp + registry · [PROVIDER-APPS](docs/PROVIDER-APPS.md) |
| Storage | `palm/storages/<name>/` | Same; `INSTALLED_STORAGES` |
| Workload runner | `palm/runners/<name>/` | `INSTALLED_RUNNERS` — not `palm.runtimes` surfaces |
| Transform rule | `palm/common/transforms/rules/` | `BaseTransformRule` + register |
| Pattern CQRS | `patterns/<name>/bindings/cqrs/` | `register_cqrs_contributor()` |
| Service CQRS | `services/<domain>/bindings/cqrs/` | [ADR-009](docs/adr/009-service-cqrs-contributors.md) |
| Product method | `palm/services/<domain>/` | service + registry; no engines as public truth |
| Session (product door) | `palm/services/session/` | `SessionService` over system plane; surfaces use `host.session` (0.58.12) |
| MCP | `runtimes/mcp/` + contributors | Prefer assist paths · [MCP.md](docs/MCP.md) |
| Surface | `palm/runtimes/<name>/` | Thin; no second semantics |
| Wait types (pure) | `palm/core/wait/` | No I/O |
| Continue plane | system / today `common/wait/` | WaitPlaneService only |
| Workload pure | `palm/core/workload/` | No runner SDKs |
| Workload product | `services/execution/workloads/` | Not a top-level domain |
| Design | `palm/services/design/` | [VISION-0.25](docs/VISION-0.25.md) |
| Host / profile | `palm/app/host/` | Prefer ApplicationHost |
| Boot phase / mode | system schedule + host schedule | [VISION-0.59](docs/VISION-0.59.md) · [ADR-028](docs/adr/028-system-boot.md) — not import-order side effects; planes ≠ plugins |

**Never:**

- Put new logic into core engines without a pure contract reason.  
- Put pattern-specific logic in shared/system dump (`common` pattern ban).  
- Create a top-level package without purpose in [PALM.md](docs/PALM.md).  
- Add dual-path policy (graphs on engines, edges only on CQRS) for one capability.

---

## 6. Documentation discipline

- **System map:** [docs/PALM.md](docs/PALM.md) — update when layers/ports/planes change.  
- **ADR or waive** for significant decisions ([docs/adr/](docs/adr/), index; or `ADR: waived — …` on VISION/STATUS). Numbers append-only.  
- **Theme plan:** `docs/VISION-0.X.md` · versioning [docs/VERSIONING.md](docs/VERSIONING.md).  
- **Status / debt:** [STATUS.md](STATUS.md) · live [TECH-DEBT.md](TECH-DEBT.md) · intentions [docs/STUBS.md](docs/STUBS.md); PD-era archive under `docs/audit/`.  
- **Surfaces:** stay thin; no new `runtime.resource` / `runtime.orchestration` access from surfaces (SU-001 / SD-005).  
- **Stubs:** do not add fake-success providers/storages; record purpose in STUBS.md (ST-001+).  
- **STE:** new/revised docs per [WRITING.md](docs/WRITING.md).  
- Major public API change: also README, ARCHITECTURE, DEVELOPMENT, migrations as needed.  
- `just docs-check` when docs/version surfaces change.  
- Living Library: [docs/LIBRARY.md](docs/LIBRARY.md).

**Rule:** Code and docs diverge → treat as a bug.

---

## 7. Review checklist (before merge)

- [ ] Core purity  
- [ ] SRP; no new god-objects  
- [ ] Extension via registries; registry thread-safety  
- [ ] Aligns with [PALM.md](docs/PALM.md) (ports/planes/purpose)  
- [ ] Tests updated; doubles match contracts  
- [ ] Docs: PALM.md / ADR / STATUS as needed; STE for new text  
- [ ] ADR or waive when required  
- [ ] `just docs-check` if docs/version touched  
- [ ] No `archive/` imports  
- [ ] `just guard-core` / `just guard-common`  
- [ ] **`just check` green**  
- [ ] No experimental features registered as installed without a flag  
- [ ] No new deferred imports only to hide cycles (comment if unavoidable)  
- [ ] One slice per `docs/VERSIONING.md` (`feat(0.X.N): …`)

---

## 8. Archive

`archive/` is history only. **Never import it.**

---

## 9. Spirit

Simple at the core. Powerful at the edges.  
Human-first. Truth-seeking. Evolutionary.  
Long clarity over short cleverness.

Spirit essay: [PHILOSOPHY.md](PHILOSOPHY.md).

---

## 10. How to update this file

Update **AGENTS.md** when **agent rules** change (checklist, MCP loop, purity, extend table).  
Update **PALM.md** when **what Palm is** changes.  
Do not grow this file back into a second map.
