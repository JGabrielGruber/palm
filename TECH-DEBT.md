# Palm — Technical debt (live)

**Status:** Live register from **0.57.1**. Theme **0.57 closed** at **0.57.14**. Theme **0.58 Session plane open** — **SD-008** / **SI-*** active.  
**Also open (later theme):** **[SD-014](#sd-014)** system boot phases + composition truth (named mid-0.58).  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [docs/PALM.md](docs/PALM.md) · **Low-level plan:** [docs/SYSTEM-LOW-LEVEL.md](docs/SYSTEM-LOW-LEVEL.md)  
**Theme (open):** [docs/VISION-0.58.md](docs/VISION-0.58.md) · [ADR-027](docs/adr/027-session-plane.md) **Proposed**  
**Theme (closed):** [docs/VISION-0.57.md](docs/VISION-0.57.md) · [ADR-026](docs/adr/026-palm-system-layer.md) **Accepted**

---

## 1. How to use this file

| Rule | Meaning |
|------|---------|
| **This file is live** | Residual + **0.58** session work: SU-*, SD-008, **SI-***; later-theme **SD-014**; CS/CF |
| **Archive is history** | [docs/audit/TECH-DEBT-ERA-0.45.md](docs/audit/TECH-DEBT-ERA-0.45.md) — PD-001… era |
| **IDs** | **SD-** system · **SU-** surface · **SI-** session impact (chew later) · **ST-** stub · **CS-** smell · **CF-** carry from PD era |
| **Carry** | Still-real items from the old era use **CF-NNN** and link the old PD |
| **Stubs catalog** | Purpose without fake implementation: [docs/STUBS.md](docs/STUBS.md) |
| **Close** | Mark `✅ done` with theme patch; do not delete rows |
| **Victory path** | Name debt before workaround; fix by [PALM.md](docs/PALM.md) purpose, not by more dual paths |

**Add a row when:** you leave a shim, find an edge→engine bypass, discover a purpose lie, or ship a surface that bypasses product/ports.  
**Do not add:** fixed bugs that are not structural.

**SI-* purpose:** After analysis (0.58.0), list code/docs that **must change** when session becomes multi-instance system glue. Not all are 0.58 slices. Agents resume from SI rows without full chat context.

---

## 2. Master table (system debt)

| ID | Title | Sev | Effort | Theme slice | Status |
|----|-------|:---:|:------:|-------------|--------|
| [SD-001](#sd-001) | No unified execution port | S1 | L | 0.57.3–5, 0.57.11–12 | ✅ done (job + workload catalog on port) |
| [SD-002](#sd-002) | System mixed into `palm.common` | S1 | XL | 0.57.2–13 | ✅ system/kits extracted; common = shared libs |
| [SD-003](#sd-003) | `RuntimeHost` incomplete vs live runtime | S2 | M | 0.57.2–3, 0.57.12 | ✅ clarified (submit contract + execution) |
| [SD-004](#sd-004) | `PatternBuildContext` is an engine bag | S1 | M | 0.57.4 | ✅ done (execution + resolve helpers) |
| [SD-005](#sd-005) | Edge and product call engines by field | S2 | L | 0.57.5–7, 0.57.11–12 | ✅ done for known product edges |
| [SD-006](#sd-006) | `PalmKernel` name vs system instance | S3 | S | 0.57.2 docs + code | ✅ done (0.57.2) |
| [SD-007](#sd-007) | Product `SystemService` vs system layer name | S3 | S | docs / rename later | open |
| [SD-008](#sd-008) | Session plane has no system home | S2 | M | **0.58** | open (theme active) |
| [SD-009](#sd-009) | Workload dual bind (leaf engine + service) | S1 | M | 0.57.3–5, 0.57.12 | ✅ service path on port; leaves already port-driver |
| [SD-010](#sd-010) | STE rewrite backlog (legacy dense docs) | S4 | L | ongoing | open |
| [SD-011](#sd-011) | Server transport stack under `common.runtimes` | S2 | L | 0.57.13 | ✅ kits package (`palm.kits.server`) |
| [SD-012](#sd-012) | Cutover shims (fill as 0.57 moves) | S3 | — | 0.57.6–12 | ✅ deleted (0.57.12) |
| [SD-013](#sd-013) | Installed placeholders that lie (capability catalog) | S1 | M | 0.57.9 | ✅ gated (ST-001…005) |
| [SD-014](#sd-014) | No unified system boot phase table; composition not full truth | S2 | L | **later theme** (not 0.58) | open |

### Surface debt (SU)

| ID | Title | Sev | Effort | Status |
|----|-------|:---:|:------:|--------|
| [SU-001](#su-001) | Explorer SSR bypasses product (engine fields) | S2 | M | open |
| [SU-002](#su-002) | Explorer / forms god-files (size + mixed roles) | S2 | L | open |
| [SU-003](#su-003) | MCP dual stack (assist meta + domain tools + fat in_process) | S2 | L | open |
| [SU-004](#su-004) | MCP legacy module names still in tree | S3 | S | open |
| [SU-005](#su-005) | CLI legacy alias forest locks old phrases | S3 | M | open |
| [SU-006](#su-006) | Surface transport kit split (`common.runtimes.server` vs `runtimes.server`) | S2 | L | ✅ kit home (`palm.kits.server`) |
| [SU-007](#su-007) | WebSocket / Portal maturity vs dual frame homes | S3 | M | open |
| [SU-008](#su-008) | Surface weight vs thin-adapter law (~14k server LOC) | S2 | XL | open |

### Stub / intention debt (ST)

| ID | Title | Sev | Effort | Status |
|----|-------|:---:|:------:|--------|
| [ST-001](#st-001) | Fake-success providers (graphql, postgres) | S1 | S | ✅ gated 0.57.9 |
| [ST-002](#st-002) | No-op storage backends listed as installed | S1 | S | ✅ gated 0.57.9 |
| [ST-003](#st-003) | ETL pattern is a phase ticker (gated off install) | S2 | S | ✅ gated 0.57.9 |
| [ST-004](#st-004) | Transform `parquet_load` registered, always errors | S3 | XS | ✅ gated 0.57.9 |
| [ST-005](#st-005) | Tests freeze lying install sets (`test_modular_apps`) | S1 | S | ✅ fixed 0.57.9 |
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

**Residual:** none for the port contract itself (0.57.12 adds workload catalog methods).

**Why it hurt:** Every new effect picked a side or duplicated both.

**Target:** Graphs and product both call `execution` on the system instance — **met**.

---

### SD-002 — System mixed into `palm.common`

**Severity:** S1 · **Effort:** XL · **Slices:** 0.57.2 (boundary ✅), 0.57.6 (deflate ✅ bulk)

**Progress (0.57.6–0.57.13):** System-shaped code under `palm.system`; surface kit under `palm.kits`.

| Area | Canonical | Notes |
|------|-----------|-------|
| `BaseRuntime` + host/wiring/middleware hooks/schedulers | `palm.system.runtime` | SD-012 deleted |
| Wait / work / workload glue | `palm.system.planes.*` | SD-012 deleted |
| `executions/` + job hooks | `palm.system.executions` / `runtime.job_hooks` | wave F |
| Server transport kit | `palm.kits.server` | SD-011 ✅ 0.57.13 |
| `plans/` | `palm.common.plans` | shared DTO + PlanRegistry |
| transforms / cqrs / services base | `palm.common` | shared (stay) |

**Residual for this ID:** mostly closed; plans and shared libs intentionally remain in common.  
Session plane is a **future theme** (SD-008).  

**Target:** ✅ system vs shared vs kits visible in the tree.

---

### SD-003 — `RuntimeHost` incomplete

**Severity:** S2 · **Effort:** M

**Observation:** Protocol exposes `orchestration`, `event`, `resource`, `is_started`.  
Live `BaseRuntime` also has `workload`, `context`, `wait_plane`, auth, storage, executor.

**Progress (0.57.12):** `RuntimeHost` is the **submit contract** (orchestration + event +
resource + `execution` + `is_started`). Effects still go through `execution`.  
`SystemInstance` remains the edge-facing “ports only” contract.

**Why it was incomplete:** submit needs engines; edges must not type only engines.

**Target:** ✅ documented and typed honestly — not deleted (executor still needs it).

**Evidence:** `palm/system/runtime/host.py`; `palm/system/instance.py`.

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

**Progress (0.57.12):** Product workload list/doctor/stop_owned use the port.
Job list and effects already did. Known dual-field edges closed.

**Policy:** Product → port. Surfaces → product or thin system entry.  
**No new** `runtime.resource` / `runtime.orchestration.*` effect shortcuts
without adding a residual row here. Status: ✅ for catalogued sites.

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

**Observation:** `palm.services.system` is doctor/health/inspect product.  
**System layer** is the kernel shape. Same English word, two purposes.

**Not the same as:**
- **`InstanceManager`** (`palm.common.managers`) — infra cache over `InstanceRepository`, not a product service domain.
- There is **no** product “ManagerService” today.

**Target:** Speech: “product SystemService (ops/inspect)” vs “system layer”.  
Optional rename to `OpsService` / `InspectService` only if product API churn is worth it — not required for 0.57 exit.

---

### SD-008 — Session plane has no system home

**Severity:** S2 · **Effort:** M · **Status:** **open — theme 0.58 active** (plan **0.58.0**)

**Observation:** Product `session_id` field name still often means instance (SI-001 residual
path/handle rename). System plane + product door through **0.58.13**: seat, multi-attach,
bind, job-path, inspect, Assist dogfood, WS/cookie bind, watches/fan-in, vocabulary,
**active focus**, **owner gate**, **SessionService**, **service/origin sessions** (work drain
+ host). Residual: product URL/handle rename (SI-001), explorer bulk (SI-010), docs (SI-012),
bare-instance paths without a bound system session.  
Watch-first queue note: [VISION-SESSION-PLANE](docs/VISION-SESSION-PLANE.md) (**superseded**).

**Target:** [VISION-0.58](docs/VISION-0.58.md) · [ADR-027](docs/adr/027-session-plane.md) —  
Close at theme exit when residual SI honest; structure is live.

**Impact list:** [SI-001+](#4b-session-impact-inventory-si--0580-analysis) (not all paid in 0.58).

---

### SD-009 — Workload dual bind

**Severity:** S1 · **Effort:** M · **Slices:** 0.57.3–5, 0.57.12 · **Status:** ✅ done

**Observation:** Leaves used engine; product used service → engine.

**Resolution:** Leaves use port→driver (0.57.4). Product effects + list/doctor/
stop_owned use ExecutionPort (0.57.12). Engine remains inside the system instance.

---

### SD-010 — STE rewrite backlog

**Severity:** S4 · **Effort:** L

**Observation:** New map/theme text uses STE.  
ARCHITECTURE, README, many VISION files remain dense legacy.

**Target:** Rewrite when a file is touched for substance. No big-bang rewrite required for 0.57 exit.

---

### SD-011 — Server transport under `common.runtimes`

**Severity:** S2 · **Effort:** L · **Slice:** 0.57.13 · **Status:** ✅ done

**Observation:** Server glue lived under `palm.common.runtimes.server` as a parking lot.

**Why it was there:** no named place for multi-surface shared transport before kits.

**Resolution:**
- Package **`palm.kits`** — exposed kits, install-list truth (`INSTALLED_KITS`, `register_kit`).
- Server kit **`palm.kits.server`** — one implementation; all former common paths rebound.
- Surfaces (`palm.runtimes.server`) import the kit; composition roots stay in runtimes.
- Future kits (cli helpers, websocket transport, …) register the same way; intentions stay off install until real.

**Law retained:** one implementation per kit; not system; not anonymous common bulk.

---

### SD-012 — Cutover shims

**Severity:** S3 · **Status:** ✅ deleted (0.57.12)

Temporary re-export packages under `palm.common` (runtimes base/host, wait, work,
workload, executions, hooks) removed. Canonical imports are `palm.system.*`.  
`palm.common.runtimes` retains **only** `server/` kit + doctor contributor registry.

---

### SD-013 — Installed placeholders that lie

**Severity:** S1 · **Effort:** M · **Related:** ST-001…005, CF-006 (PD-023)  
**Status:** ✅ gated (0.57.9) — see ST rows

**Progress (0.57.9):** Default `INSTALLED_*` is truthful. Intention packages use
`INTENTION_*` lists + loud refusal on use. Modular tests assert install vs intention.

**Policy (normative):**

1. Keep **intention** (name + purpose) in [docs/STUBS.md](docs/STUBS.md).  
2. Do **not** keep a fake implementation that looks healthy.  
3. Gate experimental apps: not in default `INSTALLED_*`, or mark maturity `stub` and fail loudly on use.  
4. Tests assert **intention sets**, not “fake providers return data.”

**Residual:** Package trees for graphql/postgres/etl still exist (scaffolds). Full delete optional later.

---

### SD-014 — System boot phases + composition truth

**Severity:** S2 · **Effort:** L · **Status:** **open — later theme** (named mid-**0.58**, not paid in 0.58)  
**Related:** CF-002 (host composition residual) · CompositionProfile (0.50) · ADR-017 (import seams) · SI-014 (plane-store framework — separate)

**Named when:** Session plane work (0.58.1–0.58.3) forced a clear split: **plugins** vs **system planes** vs **surface bind**. The pain is not missing dynamic import — Palm already has Django-style `INSTALLED_*` + `autoload()`. The pain is **scattered boot** and **implicit order**.

#### Observation (stacked pains — do not merge into one wrong fix)

| Pain | What exists today | What is weak |
|------|-------------------|--------------|
| **Plugin catalog** | `INSTALLED_PATTERNS` / providers / storages / runners / kits / services + `autoload()` | Parallel `_apps.py` shapes; rare `depends_on`; order only by list |
| **Self-register** | Side-effect `register_*` on import into common registries (ADR-017) | Correct for **plugins**; wrong model for **planes** |
| **System planes** | wait / work / session / workload attach on `BaseRuntime.start` + host `wire_*` | No single **phase table**; each plane grows its own attach story |
| **Composition** | `CompositionProfile` (services / surfaces / capabilities) + `DeploymentProfile` | Declared, not fully the only “what is on” switch for host assembly |
| **Host wire** | `ApplicationHost.start` → spawn → `_wire_cqrs` → workplane `wire_*` … | Imperative scatter; god-wire risk (CF-002) |
| **Cross-cutting stacks** | Job hooks, wait/work planes, server principal middleware, event journal | Three+ shapes; do **not** collapse into one global middleware list |
| **Import hygiene** | ADR-017 sanctioned seams; plugins register downward | Residual deferred imports; composition-root still heavy |

#### Law to preserve (when a theme pays this)

1. **Plugins** — settings / `INSTALLED_*` declare *what*; packages **self-register downward** into registries.  
2. **System planes** — **not** plugins; **not** in `INSTALLED_*`. System runtime **owns attach order**.  
3. **Settings / composition** choose membership (services, surfaces, capabilities, installed apps). They do **not** replace the kernel schedule.  
4. **One composition root** walks a **boot phase table**; modules do not invent private boot order via import side effects.  
5. Keep stacks separate: surface request filters ≠ job hooks ≠ plane law (start/continue/place) ≠ event consumers.

#### Illustrative phase table (target spirit — not frozen API)

```text
1. storage select / engines construct
2. ports open (execution, …)
3. planes attach (wait, work, session, workload — fixed set)
4. job hooks install
5. ensure_core_plugins (INSTALLED_* autoload)
6. product services wire (CompositionProfile.services)
7. surfaces mount (CompositionProfile.surfaces + DeploymentProfile)
8. recover / drain / background start
```

Today steps 3–8 are real but **named only in code paths**, not as one documented schedule.

#### Non-goals (do not “fix” SD-014 with these)

- A second dynamic-import framework on top of `INSTALLED_*` autoload.  
- Putting session/wait/work into plugin install lists.  
- One global middleware list for HTTP + job tick + planes.  
- Shared plane-store framework as a gate (that is **SI-014**, ponder later).  
- Blocking **0.58** session bind/dogfood on this theme.

#### Target (later theme)

- Document and implement a **system boot phase** schedule (BaseRuntime + host).  
- Make **CompositionProfile** (and settings) the truthful “what is installed” for product/surfaces/capabilities.  
- Optional: thin shared `App` protocol for plugins only (`name`, register, optional depends).  
- Host stops growing parallel hard-coded `if` forests that ignore the profile.  
- Map/ADR when structure changes; STE theme plan when opened.

#### Agent note

Session plane (0.58) continues under **SD-008 / SI-***.  
When adding a **new system plane** before SD-014 is paid: attach in BaseRuntime start next to peers; do **not** invent a self-register plugin path.  
When adding a **plugin**: `INSTALLED_*` + registry; do **not** put it in the kernel phase table as a special case without cause.

---

## 3b. Surface debt detail

Surfaces must stay **thin** ([PALM.md](docs/PALM.md)). Today `palm.runtimes` is the largest tree (~22k LOC Python). Most weight is **server** (~14k) then **MCP** (~4.7k) then **CLI** (~3.8k). Embedded/daemon stay small.

### SU-001 — Explorer SSR bypasses product

**Severity:** S2 · **Effort:** M · **Related:** SD-005

**Observation (updated 0.57.7):** Explorer **effects** use the port
(`execution.invoke_resource`, `execution.resume_job`). Residual risk is
**bulk / mixed roles** (SU-002) and any new bypasses, not those two call sites.

**Why it still hurts:** Surface code remains thick; easy to re-introduce engine fields.

**Target:** Explorer → product services where possible; keep port-only for effects.

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

**Severity:** S2 · **Effort:** L · **Related:** SD-011 · **Status:** ✅ done (0.57.13)

**Observation:** Protocol lived under common; composition under runtimes — two homes for one HTTP story.

**Resolution:** Kit **`palm.kits.server`** owns protocol/routes/transport/SSR helpers.  
Surfaces under `palm.runtimes.server` stay thin composers. That split is intentional (kit vs surface).

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

**Severity:** S1 · **Effort:** S · **Status:** ✅ gated (0.57.9)

| Provider | Resolution |
|----------|------------|
| `graphql` | Not in `INSTALLED_PROVIDERS`; `fetch`/`connect` raise `NotImplementedError` |
| `postgres` | Same |

Listed in `INTENTION_PROVIDERS`. Purpose remains in STUBS.md.

---

### ST-002 — No-op storage backends

**Severity:** S1 · **Effort:** S · **Status:** ✅ gated (0.57.9)

| Backend | Resolution |
|---------|------------|
| `storages/postgres` | Not in `INSTALLED_STORAGES` (core only); I/O raises |
| `storages/mongodb` | Same |

Remain in `OPTIONAL_STORAGES` for lazy discovery; no silent fake durability.

---

### ST-003 — ETL pattern phase ticker

**Severity:** S2 · **Effort:** S · **Status:** ✅ gated (0.57.9)

**Resolution:** Not in `INSTALLED_PATTERNS`; listed in `INTENTION_PATTERNS`.  
Package remains for explicit import (tests may opt in). Purpose in STUBS.md.

---

### ST-004 — `parquet_load` always errors

**Severity:** S3 · **Effort:** XS · **Status:** ✅ gated (0.57.9)

**Resolution:** Not in `INSTALLED_TRANSFORMS` / not registered as builtin.  
Module may remain for future pyarrow work (`INTENTION_TRANSFORMS`).

---

### ST-005 — Tests freeze lying install sets

**Severity:** S1 · **Effort:** S · **Status:** ✅ fixed (0.57.9)

**Resolution:** `test_modular_apps` asserts truthful `INSTALLED_*` + separate `INTENTION_*` sets.

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
| CF-002 | PD-009 / PD-010 | Host composition residual | Host smaller than 1170 LOC; **structural fix → [SD-014](#sd-014)** (boot phases + composition truth) |
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

## 4b. Session impact inventory (SI-* · 0.58.0 analysis)

**Purpose:** Capture **what the session plane will break or rebind** so agents can chew later without chat context.  
**Law (0.58):** session ≠ instance ≠ job; multi-instance; system home; surfaces bind.  
**Not all SI rows are 0.58 must-close.** Pay when a slice touches that edge; otherwise leave open.

| ID | Title | Area | Theme touch | Status |
|----|-------|------|-------------|--------|
| [SI-001](#si-001) | `session_id` forced equal to `instance_id` | product Assist | 0.58.6–12 | partial (door live; path rename residual) |
| [SI-002](#si-002) | FlowSession / AssistSession are product-only “sessions” | product | 0.58.1–12 | open (handles OK; resolve via SessionService) |
| [SI-003](#si-003) | ProcessInstance has no session owner link | instances / system | 0.58.4 | ✅ done |
| [SI-004](#si-004) | WS connection bind is surface-local only | server WS | 0.58.7 | ✅ done |
| [SI-005](#si-005) | MCP / palm_assist paths treat session as instance | MCP Assist | 0.58.6–8 | partial (rewrite live) |
| [SI-006](#si-006) | CLI / REPL `active_assist_session_id` | CLI TUI | 0.58.3 partial · 0.58.6 | open |
| [SI-007](#si-007) | CQRS instance queries are the public “session” | host CQRS / kits | 0.58.8 partial | partial (`system/session`) |
| [SI-008](#si-008) | `flow.session.*` events lack real session subject | event plane | 0.58.4+8 | ✅ partial + filter |
| [SI-009](#si-009) | WorkloadOwner.session_id optional / unenforced | workload | 0.58.8 partial | partial (EventContext) |
| [SI-010](#si-010) | Explorer / REST drive instance without session bind | surfaces SU | later (SU-*) | open |
| [SI-011](#si-011) | Composition / inbound start without session attribution | work plane edges | 0.58.13 | partial (service sessions) |
| [SI-012](#si-012) | Docs and skills say session ≡ flow instance | docs / MCP skill | ongoing | open |
| [SI-013](#si-013) | Session multi-attach + reverse index | system plane | 0.58.2 | ✅ done |
| [SI-014](#si-014) | Plane-store pattern not shared across planes | architecture | **ponder later** | open |
| [SI-015](#si-015) | Continue paths skip owner check when session bound | product / surfaces | 0.58.11 | ✅ done (bare-instance residual → **0.58.15**) |
| [SI-016](#si-016) | Surfaces invent dual context; walk facts on job meta | product / surfaces | **0.58.14** | open (close-plan seat) |

### SI-001 — product handles still named “session” for instance

**Where:** `FlowSession.session_id`, `AssistSession.session_id`, grammar path
`…/session/{id}`, MCP tool param docs — internal product still keys continue by
an attribute/path named session.  
**Impact:** **Partial (0.58.9–12):** public envelopes use `session_id` = system
subject and `instance_id` = continue. Plane owns ``active_instance_id``;
product **SessionService** (0.58.12) is the surface door for resolve/gate/submit.
Residual: rename product handle fields and URL segments to `instance` (not a
prerequisite for correct surface operation).  
**Target:** Product APIs and paths name `instance_id` for continue; `session_id`
only for the system subject; product reads focus via SessionService → plane.

### SI-002 — FlowSession / AssistSession product-only

**Where:** `services/execution/flows/session.py`, `services/assist/session.py`, `services/assist/sessions/`.  
**Impact:** Handles are fine; they resolve continue via **SessionService**
(0.58.12) when wired, not invent plane truth.  
**Target:** Thin handles over product session + job path; verbs target a primary
instance for UX under the bound system session.

### SI-003 — ProcessInstance has no session owner

**Where:** `palm/instances/process_instance.py`, instance sync, `SessionOwnershipHook`.  
**Status:** ✅ **done** at **0.58.4** — first-class `session_id` (+ metadata fallback);
`build_instance_from_job` / update; `SessionOwnershipHook` attaches on submit when
job metadata carries `session_id`. Product paths must still **pass** the system
session id (Assist dogfood 0.58.6).

### SI-004 — WS bind is surface-local

**Where:** `runtimes/server/surfaces/websocket/session.py` (`op: bind`, conn bind state).  
**Status:** ✅ **done** at **0.58.7** (+ **0.58.9** vocabulary) — `op: bind` / hello /
dispatch resolve system session via plane; cookie-like transport
(`X-Palm-Session`, Cookie `palm_session`); bound snapshot uses `session_id` +
`instance_id`. REST create echoes system `session_id` + `Set-Cookie`.

### SI-005 — MCP / palm_assist session = instance

**Where:** `runtimes/mcp/assist/*`, assist grammar paths `session/{id}`.  
**Impact:** **Partial (0.58.6–8):** start dogfood + path rewrite when `sess-…` is
passed; `system/session/{id}` inspect path. Grammar still says `session` for
instance segments in URLs (name residual).  
**Target:** Skills/docs teach system vs instance; URL rename optional later.

### SI-006 — CLI / REPL active session id

**Where:** `runtimes/cli/tui/*`, `runtimes/cli/shared/context.py`.  
**Impact:** **Partial (0.58.3):** `active_system_session_id` + `bind_system_session()`
are first-class and distinct from product assist/instance. Product
`active_assist_session_id` may still be instance-shaped until Assist dogfood
(0.58.6). TUI prompt still shows assist id.  
**Target:** Prompt / verbs prefer system session; assist handle uses attach list.

### SI-007 — CQRS instance queries as public session

**Where:** host CQRS, `kits/server/cqrs.py`, facades `get_instance`, flows session REST.  
**Impact:** **Partial (0.58.8):** `dispatch_operator_path` supports
`system/session/{id}` · `/waiting` · `/instances` (plane inspect). Full CQRS
contributor + REST routes optional residual.  
**Target:** Session inspect first-class in operator catalog; instance remains job-path API.

### SI-008 — flow.session.* events

**Where:** orchestration terminal emit; `EventContext`; instance lifecycle events.  
**Status:** ✅ **partial (0.58.4 + 0.58.8)** — context/payload attribution +
`event_matches` / Events WS session filter. Event type names unchanged.

### SI-009 — WorkloadOwner.session_id

**Where:** `palm/core/workload/owner.py`, engine stop-by-owner filters.  
**Impact:** **Partial (0.58.8):** `BaseRuntime.start_workload` enriches owner from
active `EventContext` (session/job/instance) when missing. Explicit owner still
wins. Residual: leaves that never bind event context.  
**Target:** All job-path starts carry session on owner when metadata has it.

### SI-010 — Explorer / REST without session bind

**Where:** server explorer SSR, REST flow session routes (SU-001 related).  
**Impact:** Operator UI bypasses session glue.  
**Target:** Later surface paydown; cookie bind when HTTP is touched.

### SI-011 — Composition / inbound without session

**Where:** work-drain triggers, inbound composition, schedules.  
**Impact:** **Partial (0.58.13):** work-drain submit enriches with stable **service session**
`sess-svc-work-drain:{target}` via `SessionService.enrich_submit_body(origin=…)`.
Host well-known `sess-svc-host` opens at runtime start. Outside surfaces still bind
random `sess-…`. **No** dual “no session” law for automated start when plane ready.  
**Residual:** inbound/schedule-specific origin tags if payload never hits work-drain
enrich; explorer bare paths (SI-010); product rename (SI-001). Workloads inherit only
(no separate workload session type).  
**Target:** All automated start attributed; operator composition binds outside sessions.

### SI-012 — Docs and skills alias

**Where:** MCP skill, docs/MCP.md, wiki, examples that say session_id is instance.  
**Impact:** Agents re-learn the lie.  
**Target:** Update when dogfood lands; STE on touch.

### SI-013 — Session multi-attach not first-class yet

**Where:** `SessionStore` / `SessionPlaneService` (0.58.1–0.58.2).  
**Status:** ✅ **done** at **0.58.2** — `attach_instance` / `detach_instance` /
`session_for_instance`; reverse key `palm:session:by_instance:*`; one instance
→ one session (refuses dual attach). Store remains on StorageEngine.

### SI-014 — Shared plane-store framework

**Observation:** Wait, work, workload, session may each need stores.  
**Target:** **Ponder later** — not a 0.58 gate. Per-plane store first.

### SI-015 — Continue paths skip owner check when session is bound

**Where:** Product/MCP/WS continue with bound system `session_id` + `instance_id`.  
**Status:** ✅ **done** at **0.58.11** — plane `owns_instance` /
`require_owned_instance` / `InstanceNotOwnedError`; operator
`rewrite_system_session_continue` gates continue paths; flows/assist dispatch
gate when params carry system `session_id`; host
`require_session_owns_instance`; WS maps to `session_owner`. Path instance is
authoritative (not replaced by plane focus).  
**Law:** exclusive ownership + active = focus only
([VISION-0.58 §4.1](docs/VISION-0.58.md), [ADR-027](docs/adr/027-session-plane.md) D9–D11).  
**Residual:** bare `instance_id` with **no** bound system session still skips the
gate (legacy tooling / SI-001 surface bind incomplete). Elevated inspect and
user-plane **impersonation** remain later seeds — not dual-own.

---

## 5. 0.57 slice ↔ debt (closed theme)

| Slice | Closes or reduces |
|------:|-------------------|
| 0.57.1–14 | See closed theme; **SD-008** left open → **0.58** |
| later | SU-* bulk; SD-010 STE; CF-* |

## 5b. 0.58 slice ↔ debt

| Slice | Closes or reduces |
|------:|-------------------|
| 0.58.0 | Plan; SI inventory; SD-008 active (not closed) |
| 0.58.1 | SD-008 home (partial): plane + StorageEngine store + lifecycle |
| 0.58.2 | SI-013 multi-attach + reverse index ✅ |
| 0.58.3 | Bind law on plane + host + CLI; SI-006 partial; SI-001 still product |
| 0.58.4 | SI-003 ✅; SI-008 partial; job metadata + SessionOwnershipHook |
| 0.58.5 | Journey inspect / list_waiting ✅ |
| 0.58.6 | Assist dogfood: system session on submit |
| 0.58.7 | SI-004 ✅ WS/cookie bind; flow create name-vs-id fix |
| 0.58.8 | Watches/fan-in; SI-001/005/007/008/009 partial truth |
| 0.58.9 | Vocabulary slash: session_id=system, instance_id=continue; duals deleted |
| 0.58.10 | Plane active_instance_id; resolve prefers focus; ownership vs focus documented; SI-015 named |
| 0.58.11 | SI-015 owner gate ✅ (`require_owned_instance` + rewrite/product/WS) |
| 0.58.12 | Product SessionService surface door ✅; flows/assist/MCP rebind; SI-001/002 partial |
| 0.58.13 | Service/origin sessions ✅; SI-011 partial (work-drain + host); workloads inherit |
| **close plan** | [VISION-0.58 §6.2](docs/VISION-0.58.md) **0.58.14–0.58.20** + exit (docs locked) |
| 0.58.14 | BoundSurface + session context metadata (session owns surface context) |
| 0.58.15 | Strict attribution — kill SI-015 bare-instance residual |
| 0.58.16 | Inherit-or-service start — finish SI-011 |
| 0.58.17 | Single kit door + surface dogfood (SI-005/006) |
| 0.58.18 | Session operate + surface_view v2 (SI-007 partial) |
| 0.58.19 | Product vocabulary rename SI-001/005 |
| 0.58.20 | Docs/skill SI-012 + residual honesty SI-010/SU |
| theme exit | SD-008 close; ADR-027 Accept; residual SI honest |
| later (not 0.58) | SI-014 plane-store; D11 impersonation; full SU-001 explorer bulk |

---

## 6. Accepted trade-offs (not defects)

- **Core purity** — absolute; never “fix” by importing product into core.  
- **Register downward** — absolute (plugins into registries).  
- **Pre-1.0 breaks** — allowed when structure needs truth; record SD/SI/CF, ship migration note if public API breaks.  
- **Archive era PD numbers** — frozen history; no renumber.  
- **Session store without shared plane-store framework** — allowed (SI-014 later).  
- **Cookie-like bind** — transport only; not a second session model.  
- **Exclusive instance ownership** — one instance → one session; not dual-own for admin UX.  
- **Active instance is focus only** — not a foreign-session pass ([ADR-027](docs/adr/027-session-plane.md) D10).  
- **Plugin self-register + `INSTALLED_*` autoload** — keep; not replaced by a second import framework (SD-014).  
- **Planes are not plugins** — system owns attach; do not put planes on install lists (SD-014).  
- **0.58 does not pay SD-014** — name it; boot-phase theme later; session dogfood continues.  
- **0.58 does not ship user impersonation** — D11 seed only; do not soften D9 for support UX.

---

## 7. Later theme seeds (not open VISION yet)

| Seed | Debt | Spirit |
|------|------|--------|
| **System boot + composition truth** | [SD-014](#sd-014), CF-002 | One phase table; profile is membership truth; plugins vs planes stay split |
| **Session plane (active theme)** | SD-008, SI-* | Outside subject; multi-attach; bind; dogfood — [VISION-0.58](docs/VISION-0.58.md) |
| **Plane-store framework** | SI-014 | Ponder only; per-plane stores first |
| **User plane + session impersonation** | D11 · SI-015 bare residual | Principal **acts as** owning session (grant, audit, time-bound). **Not** dual-own instances. Support/admin maturity without dissolving ownership — [VISION-0.58 §7.1](docs/VISION-0.58.md) |
| **Delegate / team session membership** | growth | Shared walk under one owner session + many principals, or explicit delegate tokens — same exclusive attach graph |

---

*Name the debt. Then pay it in order. Do not paper it.*
