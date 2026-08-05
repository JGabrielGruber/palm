# AGENTS.md

**Palm Engine — agent constitution**  
Rules for AI coding agents and humans who change code.  
Not the system map. Not the theme history. Not the debt ledger.

*“Palm grows where the sun meets the sea.”*

---

## 0. Read first

| Need | Open |
|------|------|
| **What Palm is** | **[docs/PALM.md](docs/PALM.md)** |
| **Where we are / what is next** | **[STATUS.md](STATUS.md)** |
| **Spirit** | [PHILOSOPHY.md](PHILOSOPHY.md) |
| **Theme discipline** | [docs/VERSIONING.md](docs/VERSIONING.md) — floor · growth · exit; **José** decides |
| **Live debt** | [TECH-DEBT.md](TECH-DEBT.md) · intentions [docs/STUBS.md](docs/STUBS.md) |
| **Near structure (organism · tree)** | [docs/VISION-ASSEMBLY.md](docs/VISION-ASSEMBLY.md) |
| **Multi-Palm horizon** | [docs/VISION-GROVE.md](docs/VISION-GROVE.md) |
| **Docs voice** | [docs/WRITING.md](docs/WRITING.md) |
| **Operate via MCP** | [docs/MCP.md](docs/MCP.md) · [docs/skills/palm/SKILL.md](docs/skills/palm/SKILL.md) |
| **Low-level system** | [docs/SYSTEM-LOW-LEVEL.md](docs/SYSTEM-LOW-LEVEL.md) when you touch seats/ports |

**Rule:** [PALM.md](docs/PALM.md) is the map. [STATUS.md](STATUS.md) is the present.  
**Do not** paste architecture or closed-theme chronicles into this file.  
When structure changes → update **PALM.md**. When seasons move → update **STATUS**. Keep **AGENTS.md** as **rules only**.

Palm is **pre-1.0** and **experimental** — no LTS. Break for truth. See [README.md](README.md).

---

## 1. Principles

| Principle | Meaning |
|-----------|---------|
| **Single responsibility** | One reason to change per module |
| **Explicit boundaries** | Contracts; composition and registries over magic |
| **Core purity** | `palm/core/` never imports other Palm packages |
| **Registry extension** | Capability at the edge; consumers walk registries (§1.1) |
| **Seat DI** | Inject interfaces and subsystems — not the shell as a bag (§1.2) |
| **Documentation as code** | Docs and ADRs match source rigor |
| **Testability first** | Critical paths unit-testable in isolation |
| **Human-first + truth-seeking** | Wait, resume, inspect, honest failure |
| **Minimal magic** | Readable, explicit code |
| **Proper over workaround** | Break dual truth; pay debt or **name** it |
| **Ambition over empty process** | Themes grow until intent is proper; **José** exits |

Layer laws: [PALM.md §9](docs/PALM.md).  
Theme law: [VERSIONING.md](docs/VERSIONING.md).  
Spirit: [PHILOSOPHY.md](PHILOSOPHY.md) (purpose over doom; dead maps are shackles).

### 1.1 Registry extension

**Shape:** definition at the edge; consumer only holds and runs.

| Prefer | Avoid |
|--------|--------|
| Law next to the subject; register; one loop | Private menu of concretes in hub/schedule/walk |
| New member = new definition + register | Edit core/hub to name every new type |

**Boy scout:** when you touch an open-coded menu, move toward registry extension — do not only relocate the list.

### 1.2 Seat DI

**Law:** inject **interfaces** and **subsystems**. Do not pass the system instance as ambient DI when the call only needs a seat.

| Prefer | Avoid |
|--------|--------|
| `InstallInterface`, `ExecutionPort`, plane/supervisor args | `fn(runtime)` + `getattr` soup |

Residual ambient dig: [SD-016](TECH-DEBT.md#sd-016). Map: [PALM.md](docs/PALM.md).

---

## 2. Structure (pointer)

Layers: **core → system / shared / kits → plugins → product → surfaces** · **app host** packs boot.

- **Job path** is the business spine: definition → pattern → job → effects → events.  
- **System** owns shell, interfaces, subsystems (planes, supervisor), boot, vitality.  
- **Surfaces** depend on system — never reverse.  
- **Workload** = place book (runners under `palm/runners/`, not surfaces).  
- **Assembly** (seed) = organism truth between boot and business — [VISION-ASSEMBLY](docs/VISION-ASSEMBLY.md).  
- **Flows** = business rules. Do not encode cluster topology as a customer flow.

Full map: **[docs/PALM.md](docs/PALM.md)** only.

**Hard invariants:**

- `palm/core/` imports nothing outside itself.  
- Registries: `threading.RLock`; populate at bootstrap.  
- Job transitions: `RunResult` + `OrchestrationEngine.apply_result()` only.  
- No `archive/` imports.  
- Effects through `runtime.execution` (or product that does) — no new edge digs into `runtime.resource` / `runtime.orchestration` without a named debt row.  
- New install/bind: interfaces/subsystems, not ambient shell.

---

## 3. Start and continue (one path each)

Completers emit **self-events**. Palm **starts** or **continues**.

| Verb | Action |
|------|--------|
| **Start** | WorkIntent → work plane / drain → new job |
| **Continue** | Wait interest → wait plane → resume / fail owner |

- Continue: **WaitPlaneService** on `runtime.event` only.  
- No private resume hooks. Nested unpark: drive the **child**.  
- Detail: [PALM.md](docs/PALM.md) · [EVENT-PLANE](docs/EVENT-PLANE.md) · [WORK-DRAIN](docs/WORK-DRAIN.md).

---

## 4. MCP (assist-first)

Prefer **`palm_assist`**. Full guide: [docs/MCP.md](docs/MCP.md).

| Goal | Call |
|------|------|
| Menu | `palm_assist()` |
| Discover | `alias="assist/discover"` |
| Run / continue / publish | params with `flow_id` / `instance_id` / `value` or `body` |
| Doctor / catalog | assist aliases |

`session_id` (system bind) ≠ `instance_id` (product continue). Follow `question` / `choices` / `waiting_on`. Do not guess state.  
New happy paths: assist aliases over new top-level tools when possible.

---

## 5. How to add

Homes and purpose: [PALM.md §7](docs/PALM.md).

| Add | Where |
|-----|--------|
| Pattern / provider / storage | `palm/patterns|providers|storages/<name>/` + `INSTALLED_*` |
| Workload runner | `palm/runners/<name>/` + `INSTALLED_RUNNERS` |
| Product service | `palm/services/<domain>/` — not engines as public truth |
| CQRS | `bindings/cqrs/` on pattern or service |
| Surface | `palm/runtimes/<name>/` — thin |
| Wait pure types | `palm/core/wait/` |
| Workload pure | `palm/core/workload/` |
| Workload product | `services/execution/workloads/` |
| Host / profile | `palm/app/host/` — prefer `ApplicationHost` |

**Never:** core pollution without pure reason · pattern logic in shared dump · top-level package without PALM purpose · dual-path graphs vs edges · private peer menus when register fits.

---

## 6. Documentation

| Change | Update |
|--------|--------|
| Layers / ports / planes / growth law | [PALM.md](docs/PALM.md) |
| Theme open/close / present | [STATUS.md](STATUS.md) · `docs/VISION-0.X.md` |
| Significant decision | ADR in `docs/adr/` (or `ADR: waived — …`) |
| Debt / intention | [TECH-DEBT.md](TECH-DEBT.md) · [STUBS.md](docs/STUBS.md) |
| Version / theme process | [VERSIONING.md](docs/VERSIONING.md) |
| Agent **rules** only | **this file** |

STE for new/revised docs: [WRITING.md](docs/WRITING.md).  
`just docs-check` when docs/version surfaces change.  
Code and docs diverge → bug.

**Do not** grow AGENTS into a second map or a museum of closed minors.

---

## 7. Themes (agents)

**José Gabriel Gruber (José)** decides theme open/close, floor vs growth, exit, ADR accept.  
Agents **propose and implement**; they negotiate with José — they do not close themes alone.

| Do | Do not |
|----|--------|
| Floor + growth line | Slice table as sealed kill contract |
| Protect layer law | Shrink ambition for empty process |
| Break dual truth; pay or name debt | Permanent workaround as architecture |
| Leave theme open until José judges | Checklist theater exit |
| Non-goals = “not this subject” | Forever-bans without layer reason |

Path when building new homes: **engine → alternate path → validate → migrate → clean**. Prefer 80/20. Complete open intent. Plan debt into theme homes.

---

## 8. Review (before merge)

- [ ] Core purity · no `archive/` imports  
- [ ] SRP · registries · no new private menus (§1.1) · seat DI (§1.2)  
- [ ] Aligns with [PALM.md](docs/PALM.md)  
- [ ] One start path · one continue path  
- [ ] Tests · doubles match contracts  
- [ ] Docs/ADR/STATUS as needed · STE · `just docs-check` if docs/version touched  
- [ ] `just guard-core` / `just guard-common` · **`just check`** green for the slice  
- [ ] No fake-installed experimental without a flag  
- [ ] Debt named if not paid · no permanent lie  
- [ ] Theme exit only with **José’s** call  

---

## 9. Archive

`archive/` is history only. **Never import it.**  
Closed themes live in their VISION/STATUS pages — not re-listed here.

---

## 10. Spirit

Simple at the core. Powerful at the edges.  
Human-first. Truth-seeking. Evolutionary.  
Long clarity over short cleverness.  
**Proper homes over thin lies. Ambition over empty process.**  
**Present purpose over doomed past.**

[PHILOSOPHY.md](PHILOSOPHY.md) · [VERSIONING.md](docs/VERSIONING.md) · [VISION-ASSEMBLY.md](docs/VISION-ASSEMBLY.md)

---

## 11. How to update this file

Update **AGENTS.md** only when **agent rules** change.  
Update **PALM.md** when **what Palm is** changes.  
Update **STATUS.md** when **where we are** changes.  
Update **VERSIONING.md** when theme-process law changes.  

If a sentence is history, map detail, or debt narrative — **it dies here** and lives in the right home, or not at all.
