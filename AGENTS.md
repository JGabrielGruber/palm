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
| How to write docs | [docs/WRITING.md](docs/WRITING.md) (ASD-STE100 · VISION floor/growth) |
| Version + **theme discipline** | [docs/VERSIONING.md](docs/VERSIONING.md) — floor · growth · exit; **José** decides; ambition over empty process |
| Project status / themes | [STATUS.md](STATUS.md) · [docs/VISION-0.61.md](docs/VISION-0.61.md) (**open** vitality) · [docs/VISION-0.60.md](docs/VISION-0.60.md) (**closed** supervisor + work plane) · [docs/VISION-0.59.md](docs/VISION-0.59.md) (**closed** boot) · [docs/VISION-0.58.md](docs/VISION-0.58.md) (**closed** session) · [docs/VISION-SURFACE-DEFLATION.md](docs/VISION-SURFACE-DEFLATION.md) (queue) · [docs/VISION-VITALITY.md](docs/VISION-VITALITY.md) (seed essay) · [docs/VISION-0.57.md](docs/VISION-0.57.md) (**closed** system) |
| Multi-Palm horizon | [docs/VISION-GROVE.md](docs/VISION-GROVE.md) |
| MCP operate | [docs/MCP.md](docs/MCP.md) · skill [docs/skills/palm/SKILL.md](docs/skills/palm/SKILL.md) |

**Rule:** [PALM.md](docs/PALM.md) is the system map.  
**Do not** paste a second full architecture into this file.  
When structure changes, update **PALM.md** (and ADR if needed). Keep this file as **rules for agents**.

**Last updated:** August 2026 · map [PALM.md](docs/PALM.md) · theme [VISION-0.61](docs/VISION-0.61.md) **open** · [ADR-030](docs/adr/030-system-vitality.md) Proposed · stamp `0.61.0` · **registry extension / OCP** §1.1 · **seat DI** §1.2 · theme law [VERSIONING.md](docs/VERSIONING.md) · residual **BI-*** / **OD-001** / **SD-016** · queue [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md)

---

## 1. Enduring principles

| Principle | Meaning |
|-----------|---------|
| **Single responsibility** | One reason to change per module |
| **Explicit boundaries** | Clear contracts; composition and registries over magic |
| **Core purity** | `palm/core/` never imports other Palm packages |
| **Registry extension** | Add capability at the edge; do not edit core contracts (see §1.1) |
| **Documentation as code** | Docs and ADRs match the same rigor as source |
| **Testability first** | Critical paths unit-testable in isolation |
| **Human-first + truth-seeking** | Wait, resume, inspect, honest failure |
| **Minimal magic** | Prefer readable, explicit code |
| **Proper over workaround** | Break ugly dual truth; pay debt or name it — do not ship permanent lies as architecture |
| **Ambition over empty process** | Themes grow until intent is proper; exit is **José’s** judgment, not checklist theater |

Full layer laws: [PALM.md §9](docs/PALM.md).  
Theme discipline: [docs/VERSIONING.md](docs/VERSIONING.md) (floor · growth · exit · **who decides**).

### 1.1 Registry extension (OCP / DIP) — aim and boy scout

**Classic names:** Open/Closed Principle · Dependency Inversion · Inversion of Control.  
**Palm shape:** **definition at the edge; consumer only holds and runs.**

| Prefer | Avoid |
|--------|--------|
| Participation **law** next to the subject (plane, plugin, capability, seat) | Teaching the bag a **private menu** of subjects |
| One loop over registered definitions / members | Open-coded `if` / `install_*` branches per concrete type in core or hub |
| New member = new definition + register | Edit hub, schedule, vitality, or product to name the new concrete |
| Consumer depends on a small protocol | Consumer imports and wires every concrete’s prose |

**When it is suitable:** new families of members; install/wire/observe of peer capabilities; anything that today would grow a switch inside a seat, schedule, or walk.  
**When it is not forced:** pure algorithms, one-off glue with a single owner, micro-helpers that are not extension points.

**Boy scout (old code):** when you **touch** a path that still open-codes a closed menu (schedule, hub, walk, doctor, wire phase), **move it toward registry extension** in that same work if the touch is natural — do not only relocate the menu.  
**Smell name:** *menu relocation* — moving the same closed list from A to B without definitions at the edge is **not** done.

**Agency bar:** extension is **registration of a definition**; the core / hub / walk **only walks the registry** (or live membership that was installed from definitions).

### 1.2 Seat DI — inject interfaces and subsystems

**Law:** inject **interfaces** and **subsystems**. Do **not** inject the system instance as ambient DI when a call only needs a seat.

| Term | Meaning | Examples |
|------|---------|----------|
| **Shell** | System instance that **owns** seats | `BaseRuntime` / `SystemInstance` |
| **Interface** | Named contract others call | `execution`, **`install`** (`InstallInterface`) |
| **Subsystem** | Membership + lifecycle region | planes (`SystemPlanes`), supervisor |
| **Member** | One registered thing | wait plane, work_drain |

| Prefer | Avoid |
|--------|--------|
| `planes.install(install_iface, options)` | `fn(runtime)` then dig engines |
| `bind_wait_plane(install, planes)` | Open-coded bag scrape in helpers |
| Depend on `InstallInterface` / `ExecutionPort` | `source: Any` + `getattr` soup |
| Shell only for **owning** / seating | Passing shell into every definition |

**Classic names:** DIP · ISP · (no ambient service locator).  
**Smell:** *ambient system-instance DI* — everything takes `runtime` and digs.  
**Boy scout:** when you touch a `*_to_runtime` dig, prefer seat args; keep shell bridges thin.

Layout: `system.interfaces` · `system.subsystems` (planes, supervisor) — **not** `system.common`.  
Compat shims: `system.ports`, `system.planes`, `system.supervisor`.  
Map: [PALM.md](docs/PALM.md) §2 / §9 · residual [SD-016](TECH-DEBT.md#sd-016).

---

## 2. Structure (pointer only)

Palm is layered: **core → system / shared / kits → plugins → product → surfaces**, with **app host** for boot.

- **Job path** is the spine (definition → pattern → job → effects → events).  
- **Interfaces (ports)** are shared contracts: ``ExecutionPort`` (effects), ``InstallInterface`` (install collaborators).  
- **Subsystems** hold membership: planes, supervisor.  
- **`palm.system`** is the system home (shell, interfaces, subsystems, boot, vitality).  
- **Surfaces** (`palm.runtimes`) **depend on system** — never the reverse.  
- **`palm.kits`** is exposed surface infrastructure (``INSTALLED_KITS``; server kit first).  
- **Product** `services.inspect` (`InspectService`) ≠ **system layer** (kernel shape); supervisor loop protocol still named `SystemService`.  
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
- **Seat DI:** new install/bind paths take interfaces/subsystems, not the shell as ambient bag.

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
- Grow a **private menu** of peers inside a consumer when registry extension fits (§1.1).

---

## 6. Documentation discipline

- **System map:** [docs/PALM.md](docs/PALM.md) — update when layers/ports/planes change.  
- **ADR or waive** for significant decisions ([docs/adr/](docs/adr/), index; or `ADR: waived — …` on VISION/STATUS). Numbers append-only.  
- **Theme plan:** `docs/VISION-0.X.md` · full discipline [docs/VERSIONING.md](docs/VERSIONING.md) (floor · growth · exit judgment).  
- **Status / debt:** [STATUS.md](STATUS.md) · live [TECH-DEBT.md](TECH-DEBT.md) · intentions [docs/STUBS.md](docs/STUBS.md); PD-era archive under `docs/audit/`.  
- **Surfaces:** stay thin; no new `runtime.resource` / `runtime.orchestration` access from surfaces (SU-001 / SD-005).  
- **Stubs:** do not add fake-success providers/storages; record purpose in STUBS.md (ST-001+).  
- **STE:** new/revised docs per [WRITING.md](docs/WRITING.md).  
- Major public API change: also README, ARCHITECTURE, DEVELOPMENT, migrations as needed.  
- `just docs-check` when docs/version surfaces change.  
- Living Library: [docs/LIBRARY.md](docs/LIBRARY.md).

**Rule:** Code and docs diverge → treat as a bug.

---

## 6b. Theme planning and growth (agents)

**Who decides:** **José Gabriel Gruber (José)** is the sole human technical lead for Palm.  
Theme open/close, floor vs growth, ambition vs process, and ADR accept at exit are **his** calls.  
Agents **propose and implement**; they **negotiate with José** — they do not close themes alone or invent a faceless “maintainer.”

When you open or plan a minor (`0.X.0` / VISION / ADR), or execute slices:

| Do | Do not |
|----|--------|
| State **floor** (intent is real) and **growth line** (theme may continue) | Treat slice tables as sealed kill contracts |
| Protect **layer law** (purity, ports, one start/continue path) | Invent process that shrinks ambition to close faster |
| **Break** dual truth that blocks the home; **pay** debt or **name** residual | Ship permanent workarounds so tests stay green without truth |
| Allow **big renames / deletes** when the home is wrong | Fear large correct moves because “theme should stay thin” |
| Leave theme **open** until **José** judges intent finished | Force theme exit for empty checklist theater |
| Write **non-goals** as “not this subject” when another seed owns them | Write forever-bans that kill Palm’s prospect without layer reason |
| Name **José** in docs when exit or ambition judgment is the point | Hide authority behind vague “maintainer” when negotiation needs a person |

**Exit** is José’s judgment when homes are proper — see [VERSIONING.md](docs/VERSIONING.md) · spirit [PHILOSOPHY.md](PHILOSOPHY.md).

---

## 7. Review checklist (before merge)

- [ ] Core purity  
- [ ] SRP; no new god-objects  
- [ ] Extension via registries; registry thread-safety  
- [ ] **Registry extension / OCP:** no new private menus in consumers when a definition+register fit; boy-scout old menus when touched (§1.1)  
- [ ] **Seat DI:** no new ambient `runtime` dig when install/bind only needs `InstallInterface` / subsystem (§1.2)  
 
- [ ] Aligns with [PALM.md](docs/PALM.md) (ports/planes/purpose)  
- [ ] Tests updated; doubles match contracts  
- [ ] Docs: PALM.md / ADR / STATUS as needed; STE for new text  
- [ ] ADR or waive when required  
- [ ] `just docs-check` if docs/version touched  
- [ ] No `archive/` imports  
- [ ] `just guard-core` / `just guard-common`  
- [ ] **`just check` green** (declared green bar for the slice)  
- [ ] No experimental features registered as installed without a flag  
- [ ] No new deferred imports only to hide cycles (comment if unavoidable)  
- [ ] Slice labeled per [VERSIONING.md](docs/VERSIONING.md) (`feat(0.X.N): …`); one purpose when possible  
- [ ] No permanent workaround architecture; debt named if not paid  
- [ ] Theme floor/growth not confused with “must close now”; exit only with **José’s** call

---

## 8. Archive

`archive/` is history only. **Never import it.**

---

## 9. Spirit

Simple at the core. Powerful at the edges.  
Human-first. Truth-seeking. Evolutionary.  
Long clarity over short cleverness.  
**Proper homes over thin lies. Ambition over empty process.**

Spirit essay: [PHILOSOPHY.md](PHILOSOPHY.md).  
Theme discipline: [docs/VERSIONING.md](docs/VERSIONING.md).

---

## 10. How to update this file

Update **AGENTS.md** when **agent rules** change (checklist, MCP loop, purity, registry extension, extend table, theme discipline).  
Update **PALM.md** when **what Palm is** changes (including growth laws).  
Update **VERSIONING.md** when version or theme-process law changes.  
Do not grow this file back into a second map.
