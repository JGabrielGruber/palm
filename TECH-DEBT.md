# Palm — Technical debt (live)

**Status:** Live register from **0.57.1**.  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [docs/PALM.md](docs/PALM.md) · **Low-level plan:** [docs/SYSTEM-LOW-LEVEL.md](docs/SYSTEM-LOW-LEVEL.md)  
**Theme:** [docs/VISION-0.57.md](docs/VISION-0.57.md) · [ADR-026](docs/adr/026-palm-system-layer.md)

---

## 1. How to use this file

| Rule | Meaning |
|------|---------|
| **This file is live** | Open work and residual risk after 0.57.1 |
| **Archive is history** | [docs/audit/TECH-DEBT-ERA-0.45.md](docs/audit/TECH-DEBT-ERA-0.45.md) — PD-001… era |
| **IDs** | **SD-** system · **SU-** surface · **ST-** stub/intention lie · **CS-** code smell · **CF-** carry from PD era |
| **Carry** | Still-real items from the old era use **CF-NNN** and link the old PD |
| **Stubs catalog** | Purpose without fake implementation: [docs/STUBS.md](docs/STUBS.md) |
| **Close** | Mark `✅ done` with theme patch; do not delete rows |
| **Victory path** | Name debt before workaround; fix by [PALM.md](docs/PALM.md) purpose, not by more dual paths |

**Add a row when:** you leave a shim, find an edge→engine bypass, discover a purpose lie, or ship a surface that bypasses product/ports.  
**Do not add:** fixed bugs that are not structural.

---

## 2. Master table (system debt)

| ID | Title | Sev | Effort | Theme slice | Status |
|----|-------|:---:|:------:|-------------|--------|
| [SD-001](#sd-001) | No unified execution port | S1 | L | 0.57.3–5 | ✅ mostly (list/doctor residual) |
| [SD-002](#sd-002) | System mixed into `palm.common` | S1 | XL | 0.57.2, 0.57.6 | open (deflate bulk ✅; residual) |
| [SD-003](#sd-003) | `RuntimeHost` incomplete vs live runtime | S2 | M | 0.57.2–3 | open (SystemInstance ✅; host residual) |
| [SD-004](#sd-004) | `PatternBuildContext` is an engine bag | S1 | M | 0.57.4 | ✅ done (execution + resolve helpers) |
| [SD-005](#sd-005) | Edge and product call engines by field | S2 | L | 0.57.5, 0.57.7 | open (effects ✅; list residual) |
| [SD-006](#sd-006) | `PalmKernel` name vs system instance | S3 | S | 0.57.2 docs + code | ✅ done (0.57.2) |
| [SD-007](#sd-007) | Product `SystemService` vs system layer name | S3 | S | docs / rename later | open |
| [SD-008](#sd-008) | Session plane has no system home | S2 | M | after system boundary | open |
| [SD-009](#sd-009) | Workload dual bind (leaf engine + service) | S1 | M | 0.57.3–5 | open |
| [SD-010](#sd-010) | STE rewrite backlog (legacy dense docs) | S4 | L | ongoing | open |
| [SD-011](#sd-011) | Server transport stack under `common.runtimes` | S2 | L | 0.57.6+ | open |
| [SD-012](#sd-012) | Cutover shims (fill as 0.57 moves) | S3 | — | 0.57.6–8 | open (import sweep ✅; modules remain) |
| [SD-013](#sd-013) | Installed placeholders that lie (capability catalog) | S1 | M | gate + STUBS | open |

### Surface debt (SU)

| ID | Title | Sev | Effort | Status |
|----|-------|:---:|:------:|--------|
| [SU-001](#su-001) | Explorer SSR bypasses product (engine fields) | S2 | M | open |
| [SU-002](#su-002) | Explorer / forms god-files (size + mixed roles) | S2 | L | open |
| [SU-003](#su-003) | MCP dual stack (assist meta + domain tools + fat in_process) | S2 | L | open |
| [SU-004](#su-004) | MCP legacy module names still in tree | S3 | S | open |
| [SU-005](#su-005) | CLI legacy alias forest locks old phrases | S3 | M | open |
| [SU-006](#su-006) | Surface transport kit split (`common.runtimes.server` vs `runtimes.server`) | S2 | L | open |
| [SU-007](#su-007) | WebSocket / Portal maturity vs dual frame homes | S3 | M | open |
| [SU-008](#su-008) | Surface weight vs thin-adapter law (~14k server LOC) | S2 | XL | open |

### Stub / intention debt (ST)

| ID | Title | Sev | Effort | Status |
|----|-------|:---:|:------:|--------|
| [ST-001](#st-001) | Fake-success providers (graphql, postgres) | S1 | S | open |
| [ST-002](#st-002) | No-op storage backends listed as installed | S1 | S | open |
| [ST-003](#st-003) | ETL pattern is a phase ticker, still installed | S2 | S | open |
| [ST-004](#st-004) | Transform `parquet_load` registered, always errors | S3 | XS | open |
| [ST-005](#st-005) | Tests freeze lying install sets (`test_modular_apps`) | S1 | S | open |
| [ST-006](#st-006) | Phase-named tests become eternal contracts | S3 | M | open |

### Code smell (CS)

| ID | Title | Sev | Effort | Status |
|----|-------|:---:|:------:|--------|
| [CS-001](#cs-001) | Layer bulk: `runtimes` + `common` dominate LOC | S2 | — | open (metric) |
| [CS-002](#cs-002) | Triple observability names on host | S2 | M | open (= CF-001) |
| [CS-003](#cs-003) | Core leaves take concrete engines (not protocols) | S2 | M | open |
| [CS-004](#cs-004) | Definition `from_dict` forever-legacy shapes | S3 | M | open |
| [CS-005](#cs-005) | Broad swallow `except` / empty `pass` in hot paths | S3 | M | open (= CF-007) |

---

## 3. System debt detail

### SD-001 — No unified execution port

**Severity:** S1 · **Effort:** L · **Slices:** 0.57.2–3 (port type + BaseRuntime), 0.57.4–5 (rebind)

**Observation:** Graphs bind `ResourceEngine` / `WorkloadEngine` via `PatternBuildContext`.  
Product binds the same engines via `ExecutionService` after `resolve_runtime()`.  

**Progress (0.57.2–4):** `ExecutionPort` on BaseRuntime; product effect methods use it.  
Graphs: builders resolve `ResourceInvoker` / `WorkloadDriver` from the port first
(`palm.system.effects` + `palm.common.patterns.effects`). Leaves typed to core protocols (P2).

**Residual:** workload list/doctor catalog still touch `WorkloadEngine`;
orchestration `list_jobs` inspect paths (SD-005 residual).

**Why it hurt:** Every new effect picked a side or duplicated both.

**Target:** Graphs and product both call `execution` on the system instance — **met for primary effect paths**.

---

### SD-002 — System mixed into `palm.common`

**Severity:** S1 · **Effort:** XL · **Slices:** 0.57.2 (boundary ✅), 0.57.6 (deflate ✅ bulk)

**Progress (0.57.6):** Canonical homes under `palm.system`:

| Area | Canonical | Residual in common |
|------|-----------|--------------------|
| `BaseRuntime` + host/wiring/hooks/schedulers | `palm.system.runtime` | SD-012 re-export shims |
| Wait (continue) | `palm.system.planes.wait` | SD-012 shims |
| Work (start intents) | `palm.system.planes.work` | SD-012 shims |
| Workload glue | `palm.system.planes.workload` | SD-012 shims |
| `executions/` | still common | system-adjacent — later wave |
| job hooks (`common/hooks`) | still common | system-adjacent — later |
| `runtimes/server` | still common | SD-011 |
| transforms / cqrs / services base | shared (stay) | — |

**Why it still hurts residual:** executions, persistence-adjacent job hooks, and server transport remain in `common`.  
Session plane still has no dedicated system seat (SD-008).

**Target:** Residual system-shaped modules move or stay classified; shims drop before theme exit when safe.

---

### SD-003 — `RuntimeHost` incomplete

**Severity:** S2 · **Effort:** M

**Observation:** Protocol exposes `orchestration`, `event`, `resource`, `is_started`.  
Live `BaseRuntime` also has `workload`, `context`, `wait_plane`, auth, storage, executor.

**Progress (0.57.2):** `SystemInstance` + `ExecutionPort` are the forward contracts.  
`RuntimeHost` remains a thin legacy subset for the executions layer; docstring points at system.

**Why it hurts:** Callers that type only `RuntimeHost` miss ports and workload.

**Target:** New code types `SystemInstance` / ports. Remove or shrink `RuntimeHost` when executor rebinds.

**Evidence:** `palm/system/instance.py`; `common/runtimes/host.py` vs `base.py`.

---

### SD-004 — `PatternBuildContext` is an engine bag

**Severity:** S1 · **Effort:** M · **Slice:** 0.57.4 · **Status:** ✅ done

**Observation:** Build context fields were raw engines only.

**Resolution:** Context carries `execution` plus optional engines for unit tests.  
Builders call `resolve_resource_invoker` / `resolve_workload_driver` (port first).  
Core leaves accept `ResourceInvoker` / `WorkloadDriver`. Engine fields remain for engine-only tests.

---

### SD-005 — Edge and product call engines by field

**Severity:** S2 · **Effort:** L · **Slices:** 0.57.5, 0.57.7 (effects ✅)

**Progress (0.57.7):** Effect samples use `runtime.execution` (including
`resume_job` on the port). Inspection/list paths remain residual.

| Site | Access |
|------|--------|
| `services/execution/providers/service.py` | ✅ port |
| `services/execution/workloads/service.py` | ✅ effect methods on port; list/doctor still engine |
| `services/execution/flows/session.py` | ✅ `execution.resume_job` |
| `app/kernel.py` | ✅ invoke + resume on port |
| `runtimes/server/.../explorer/fetch.py` | ✅ `execution.invoke_resource` |
| `runtimes/server/.../explorer/actions.py` | ✅ `execution.resume_job` |
| `providers/palm/.../local.py` | ✅ `execution.invoke_resource` |
| `providers/palm/.../system_inspect.py` | residual — `orchestration.list_jobs` (inspect) |
| `common/interactive_runtime.py` | ✅ `execution.resume_job` |
| `common/runtimes/server/cqrs.py` | residual — `list_jobs` (inspect) |
| Wait plane internal | system-internal `orch.resume_job` — not an edge |
| Pattern leaves (wizard/dag/pipeline) | ✅ port→invoker/driver (0.57.4) |

**Policy:** Product → port. Surfaces → product or thin system entry.  
**No new** `runtime.resource` / `runtime.orchestration.*` effect shortcuts
without adding a residual row here.

---

### SD-006 — `PalmKernel` name vs system instance

**Severity:** S3 · **Effort:** S · **Status:** ✅ done (0.57.2)

**Observation:** `PalmKernel` is infra (storage, instance manager, runtime registry).  
Readers may think it is the effect kernel.

**Resolution:** Docstrings on `PalmKernel` and `create_runtime` state infra vs system instance.  
PALM.md and SYSTEM-LOW-LEVEL already draw the line. No rename required.

---

### SD-007 — Product `SystemService` vs system layer

**Severity:** S3 · **Effort:** S

**Observation:** `palm.services.system` is doctor/health product.  
**System layer** is the kernel shape. Same English word, two purposes.

**Target:** Speech and docs: “product SystemService” vs “system layer”.  
Rename product only if needed after system package lands.

---

### SD-008 — Session plane has no system home

**Severity:** S2 · **Effort:** M

**Observation:** [VISION-SESSION-PLANE](docs/VISION-SESSION-PLANE.md) is queued.  
Without a system layer, session tends to fall into product or common.

**Target:** Seat under system after 0.57.2 boundary. Full session theme later.

---

### SD-009 — Workload dual bind

**Severity:** S1 · **Effort:** M · **Slices:** 0.57.3–5

**Observation:** WorkloadLeaf / wizard workload phase take `WorkloadEngine`.  
`WorkloadExecutionService` takes runtime → engine.  
0.56 vision still describes both paths.

**Target:** Same execution port methods for start/exec/stop/status.  
Rewrite leaf and service together; do not “CQRS-only” the leaf.

---

### SD-010 — STE rewrite backlog

**Severity:** S4 · **Effort:** L

**Observation:** New map/theme text uses STE.  
ARCHITECTURE, README, many VISION files remain dense legacy.

**Target:** Rewrite when a file is touched for substance. No big-bang rewrite required for 0.57 exit.

---

### SD-011 — Server transport under `common.runtimes`

**Severity:** S2 · **Effort:** L

**Observation:** HTTP protocol helpers, route types, and related server glue live under `palm.common.runtimes.server`.  
Surfaces import them heavily (~many files). This is surface **infra**, not pure shared, and not the system port table.

**Target:** After system extract, classify: stay shared transport kit, or move next to `palm.runtimes.server`.  
Do not block execution port on this move.

---

### SD-012 — Cutover shims

**Severity:** S3 · **List:** active after 0.57.6 · **Import sweep:** ✅ 0.57.8

When a temporary compatibility import or façade exists during 0.57, **add a bullet here** with path and remove-by slice.

| Shim | Path | Status |
|------|------|--------|
| BaseRuntime | `palm.common.runtimes.base` → `palm.system.runtime.base` | modules remain; **src/tests import system** (0.57.8) |
| RuntimeHost | `palm.common.runtimes.host` → `palm.system.runtime.host` | same |
| wiring / hooks / schedulers | `palm.common.runtimes.{wiring,hooks,schedulers}` → `palm.system.runtime.*` | same |
| Wait package | `palm.common.wait.*` → `palm.system.planes.wait.*` | same |
| Work package | `palm.common.work.*` → `palm.system.planes.work.*` | same |
| Workload glue | `palm.common.workload.*` → `palm.system.planes.workload.*` | same |

**Policy:** One implementation (system). Common paths are re-export only — not dual wiring.  
**Next:** delete shim modules when no external callers need them (theme exit).

---

### SD-013 — Installed placeholders that lie

**Severity:** S1 · **Effort:** M · **Related:** ST-001…005, CF-006 (PD-023)

**Observation:** Several plugins **register as installed** and return **fake success** or **no-op persistence**.  
Doctor, modular-app tests, and agent discovery treat them as real capabilities.

**Policy (normative):**

1. Keep **intention** (name + purpose) in [docs/STUBS.md](docs/STUBS.md).  
2. Do **not** keep a fake implementation that looks healthy.  
3. Gate experimental apps: not in default `INSTALLED_*`, or mark maturity `stub` and fail loudly on use.  
4. Tests assert **intention sets**, not “fake providers return data.”

**Target:** Capability catalog is truthful. Stubs do not hold Palm to legacy contracts.

---

## 3b. Surface debt detail

Surfaces must stay **thin** ([PALM.md](docs/PALM.md)). Today `palm.runtimes` is the largest tree (~22k LOC Python). Most weight is **server** (~14k) then **MCP** (~4.7k) then **CLI** (~3.8k). Embedded/daemon stay small.

### SU-001 — Explorer SSR bypasses product

**Severity:** S2 · **Effort:** M · **Related:** SD-005

**Observation:** Explorer fetch/actions touch system fields:

| Path | Access |
|------|--------|
| `runtimes/server/surfaces/ssr/explorer/fetch.py` | `runtime.resource` invoke |
| `runtimes/server/surfaces/ssr/explorer/actions.py` | `orchestration.resume_job` |

**Why it hurts:** Surfaces invent a second execution path. Port work will miss this unless listed.

**Target:** Explorer → product services or execution port only.

---

### SU-002 — Explorer / forms god-files

**Severity:** S2 · **Effort:** L · **Related:** CF-004 (PD-016)

**Observation:**

| File | ~LOC |
|------|-----:|
| `ssr/explorer/components.py` | 988 |
| `ssr/explorer/forms.py` | 942 |
| `ssr/explorer/actions.py` | 382 |
| `rest/doc_examples.py` | 642 |

Mixed HTML, forms, and orchestration concerns.

**Target:** Split present vs drive; drive through product.

---

### SU-003 — MCP dual stack

**Severity:** S2 · **Effort:** L · **Related:** CF-003 (PD-014/015)

**Observation:**

- Assist-first meta-tool is the **law** for agents.  
- Full domain tool packs still exist (`flows/`, `design/`, …).  
- `mcp/in_process.py` ~816 LOC — bridge + catalog + surface glue.

**Why it hurts:** Two mental models for agents; fat process entry resists “thin surface.”

**Target:** Assist path complete; domain tools optional or generated from same dispatch; shrink in_process.

---

### SU-004 — MCP legacy module names

**Severity:** S3 · **Effort:** S

**Observation:** Tiny re-export stubs still named as if they were eras:

- `mcp/tools.py` — “legacy tool registration”  
- `mcp/debug_tools.py`  
- `mcp/phase5_tools.py`

**Target:** Delete or one `mcp/legacy.py` with explicit deprecation; stop phase numbers in module names.

---

### SU-005 — CLI legacy alias forest

**Severity:** S3 · **Effort:** M

**Observation:** CLI keeps primary commands **and** shorter legacy phrases (`registry.py`, `catalog.py`, help text).  
Pre-1.0 is free to cut aliases; keeping them freezes old product language.

**Target:** One phrase set; migration note if needed; drop aliases that only exist for comfort.

---

### SU-006 — Surface transport kit split

**Severity:** S2 · **Effort:** L · **Related:** SD-011

**Observation:** ~80 surface modules import `palm.common.runtimes.server` (protocol, routes, middleware).  
Concrete surfaces live under `palm.runtimes.server`. Two homes for one HTTP story.

**Target:** One home after system extract (kit next to surfaces **or** named shared transport package).

---

### SU-007 — WebSocket / Portal dual homes

**Severity:** S3 · **Effort:** M

**Observation:** WS frames re-export from `common.websocket`; session logic under `runtimes/server/surfaces/websocket/`.  
Portal client direction is still thin vs Assist law.

**Target:** One frame module path; Portal stays a client of Assist dispatch only.

---

### SU-008 — Surface weight vs thin-adapter law

**Severity:** S2 · **Effort:** XL

**Observation (approx. Python LOC under `src/palm/runtimes/`):**

| Surface | ~LOC | Note |
|---------|-----:|------|
| server | 14100 | REST + SSR + WS |
| mcp | 4700 | tools + in_process |
| cli | 3800 | commands + TUI |
| daemon | 50 | thin OK |
| embedded | 30 | thin OK |

**Why it hurts:** “Thin surface” is a law surfaces currently fail by bulk. Not all LOC is wrong (HTML/OpenAPI is heavy), but bypass and dual stacks are.

**Target:** Metric + policy: new surface code must call product/ports; no new engine field access (SD-005/SU-001).

---

## 3c. Stub / intention debt detail

Full intention table: [docs/STUBS.md](docs/STUBS.md).

### ST-001 — Fake-success providers

**Severity:** S1 · **Effort:** S

| Provider | Behavior today |
|----------|----------------|
| `graphql` | `fetch` returns `{"source": "graphql", ...}` — **not** GraphQL |
| `postgres` | same pattern — **not** SQL |

Both sit in `INSTALLED_PROVIDERS`.

**Target:** Intention only in STUBS.md; remove from default install **or** raise `NotImplemented` / doctor `maturity=stub`.

---

### ST-002 — No-op storage backends

**Severity:** S1 · **Effort:** S

| Backend | Behavior |
|---------|----------|
| `storages/postgres` | `get` → always `None`; `set` no-op |
| `storages/mongodb` | placeholder client |

Listed in `INSTALLED_STORAGES` / optional set; modular tests require the names.

**Target:** Same as ST-001. Do not claim durable storage.

---

### ST-003 — ETL pattern phase ticker

**Severity:** S2 · **Effort:** S

**Observation:** `EtlPattern.tick` only sets `etl_phase` extract/transform/load. No real ETL.  
Still in `INSTALLED_PATTERNS` next to wizard/dag.

**Target:** Intention “ETL pattern” reserved; demote install or label scaffold. DAG is real enough to keep.

---

### ST-004 — `parquet_load` always errors

**Severity:** S3 · **Effort:** XS

**Observation:** Registered transform; `apply` always raises. Honest error, but catalog still lists it as a rule.

**Target:** Optional extra or intention-only; doctor marks stub.

---

### ST-005 — Tests freeze lying install sets

**Severity:** S1 · **Effort:** S

**Observation:** `tests/test_modular_apps.py` asserts exact equality with:

- patterns including `etl`  
- providers including `graphql`, `postgres`  
- storages including no-op backends  

**Why it hurts:** Truthful demotion of stubs **breaks CI** until tests change. Tests protect the lie.

**Target:** Assert **core** install sets + separate **stub intention** registry. Do not require fake providers to load as full apps unless gated.

---

### ST-006 — Phase-named tests

**Severity:** S3 · **Effort:** M

**Observation:** Names like `test_cqrs_phase5.py`, `test_mcp_phase3.py`, `test_resource_phase5.py` encode temporary program phases as permanent contracts.

**Target:** Rename to capability (`test_cqrs_schemas.py`, …) when touched; no new `phaseN` files.

---

## 3d. Code smell detail

### CS-001 — Layer bulk

**Severity:** S2 · **Metric**

Approx. Python LOC under `src/palm/`:

| Package | ~LOC |
|---------|-----:|
| runtimes (surfaces) | 22700 |
| common | 20500 |
| services | 11200 |
| patterns | 9900 |
| core | 7800 |
| app | 5000 |

**Use:** Track after system extract; surfaces and common should both fall or reclassify.

---

### CS-002 — Triple observability names

See **CF-001** / PD-018. Host exposes `event_plane_status`, `ops_status`, `control_plane_status`.  
Align with [EVENT-PLANE](docs/EVENT-PLANE.md) vocabulary (runtime vs host bus).

---

### CS-003 — Core leaves take concrete engines

**Severity:** S2 · **Related:** SD-001, SYSTEM-LOW-LEVEL P2

`ResourceLeaf` (and similar) take `ResourceEngine` type in **core**.  
Blocks a clean port without a core **protocol** for invoke.

**Target:** Small invoker protocol in core; engines and ports implement it.

---

### CS-004 — Definition forever-legacy shapes

**Severity:** S3

`from_dict` paths accept legacy shapes across definitions. Pre-1.0 can drop dead branches once fixtures update.

---

### CS-005 — Broad swallow / empty pass

See **CF-007**. Prefer explicit error or documented ignore.

---

## 4. Carry-forward (old era, still real)

These are **not** closed by the archive. Full text: [TECH-DEBT-ERA-0.45](docs/audit/TECH-DEBT-ERA-0.45.md).

| ID | Old | Title | Notes |
|----|-----|-------|-------|
| CF-001 | PD-018 | Overlapping observability vocabularies | Host vs runtime bus is clearer; magic strings may remain |
| CF-002 | PD-009 / PD-010 | Host composition residual | Host smaller than 1170 LOC; watch god-object creep |
| CF-003 | PD-014 / PD-015 | Assist/MCP complexity + coverage | Product/surface debt |
| CF-004 | PD-016 | Large SSR explorer files | Surface debt; also SD-005 call sites |
| CF-005 | PD-022 / PD-030 | DB adapters + empty extras | Runner/provider maturity |
| CF-006 | PD-023 | Placeholders registered as installed | Gate experimental |
| CF-007 | PD-024 | Broad `except Exception` | Hygiene |
| CF-008 | PD-029 | `urlopen` scheme allowlist | Security hygiene |
| CF-009 | PD-005 | Complexity gate scope | Tooling |
| CF-010 | PD-017 | Runtimes coverage cold spots | Tests |
| CF-011 | PD-011 | Inbound mixed responsibilities | Host/work plane |
| CF-012 | PD-025–027 | Naming / magic numbers | Low priority |

**Closed in old era (do not reopen without new evidence):**  
PD-001–004, PD-006–008, PD-012, PD-013, PD-019–021, PD-028, PD-031, and theme-closed work through 0.55 — see archive roadmap tables.

---

## 5. 0.57 slice ↔ debt

| Slice | Closes or reduces |
|------:|-------------------|
| 0.57.1 | Archive + SD register + low-level + **STUBS / surface debt** |
| 0.57.2 | SD-002 (boundary ✅), SD-003 (SystemInstance), SD-006 ✅, SD-001 port type |
| 0.57.3 | SD-001 (port exists), SD-009 (start) |
| 0.57.4 | SD-004 |
| 0.57.5 | SD-001, SD-005, SD-009 (product rebind) |
| 0.57.6 | SD-002 deflate bulk ✅, SD-012 shims listed; SD-011 residual |
| 0.57.7 | SD-005 effects ✅ (`resume_job` on port); list residual; AGENTS no-shortcut |
| 0.57.8 | SD-012 import sweep — src/tests use palm.system; shim modules remain |
| parallel / soon | **ST-001…005** demote lying stubs; unfreeze tests |
| later | SU-002…008 bulk; SD-008 session; SD-010 STE; CF-* |

---

## 6. Accepted trade-offs (not defects)

- **Core purity** — absolute; never “fix” by importing product into core.  
- **Register downward** — absolute.  
- **Pre-1.0 breaks** — allowed when structure needs truth; record SD/CF, ship migration note if public API breaks.  
- **Archive era PD numbers** — frozen history; no renumber.

---

*Name the debt. Then pay it in order. Do not paper it.*
