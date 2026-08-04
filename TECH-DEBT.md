# Palm — Technical debt (live)

**Status:** Live register from **0.57.1**. Theme **0.61 Living-kernel vitality open** — eyes **0.61.1–0.61.2** landed (stamps when José exits slices); plane hub half-moves named **[SD-015](#sd-015)** · **[CS-006](#cs-006)** · **[CS-007](#cs-007)**. Theme debt **[CS-002](#cs-002)** · **[OD-001](#od-001)** still open · **[SD-007](#sd-007)** ✅ paid. [VISION-0.61](docs/VISION-0.61.md) · [ADR-030](docs/adr/030-system-vitality.md) **Proposed**. Theme **0.60** closed **0.60.9** — **[BI-013](#bi-013)** ✅. Theme **0.59** closed **0.59.8** — **[SD-014](#sd-014)** ✅ · residual **[BI-*](#bi-boot-impact-inventory)**. Theme **0.58** closed **0.58.20**. Theme **0.57** closed **0.57.14**. Surface seed [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md). Vitality seed [VISION-VITALITY](docs/VISION-VITALITY.md).  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [docs/PALM.md](docs/PALM.md) · **Low-level plan:** [docs/SYSTEM-LOW-LEVEL.md](docs/SYSTEM-LOW-LEVEL.md)  
**Theme (open vitality):** [docs/VISION-0.61.md](docs/VISION-0.61.md) · [ADR-030](docs/adr/030-system-vitality.md) **Proposed**  
**Theme (closed supervisor):** [docs/VISION-0.60.md](docs/VISION-0.60.md) · [ADR-029](docs/adr/029-system-supervisor.md) **Accepted** · [RELEASE-0.60.9](docs/releases/RELEASE-0.60.9.md)  
**Theme (closed boot):** [docs/VISION-0.59.md](docs/VISION-0.59.md) · [ADR-028](docs/adr/028-system-boot.md) **Accepted** · [RELEASE-0.59.8](docs/releases/RELEASE-0.59.8.md)  
**Theme (closed):** [docs/VISION-0.58.md](docs/VISION-0.58.md) · [ADR-027](docs/adr/027-session-plane.md) **Accepted** · [docs/VISION-0.57.md](docs/VISION-0.57.md) · [ADR-026](docs/adr/026-palm-system-layer.md) **Accepted**

---

## 1. How to use this file

| Rule | Meaning |
|------|---------|
| **This file is live** | Residual **BI-*** (after 0.59 boot); residual **SI-*** / **SU-***; surface deflation seed; CS/CF |
| **Archive is history** | [docs/audit/TECH-DEBT-ERA-0.45.md](docs/audit/TECH-DEBT-ERA-0.45.md) — PD-001… era |
| **IDs** | **SD-** system · **SU-** surface · **SI-** session impact · **BI-** boot impact (0.59) · **OD-** operate diagnosis · **ST-** stub · **CS-** smell · **CF-** carry from PD era |
| **Carry** | Still-real items from the old era use **CF-NNN** and link the old PD |
| **Stubs catalog** | Purpose without fake implementation: [docs/STUBS.md](docs/STUBS.md) |
| **Close** | Mark `✅ done` with theme patch; do not delete rows |
| **Victory path** | Name debt before workaround; fix by [PALM.md](docs/PALM.md) purpose, not by more dual paths. Theme law: [docs/VERSIONING.md](docs/VERSIONING.md) — break ugly, pay or name residual; do not ship permanent workarounds to close a theme |

**Add a row when:** you leave a shim, find an edge→engine bypass, discover a purpose lie, or ship a surface that bypasses product/ports.  
**Do not add:** fixed bugs that are not structural.

**SI-* purpose:** After analysis (0.58.0), list code/docs that **must change** when session becomes multi-instance system glue. Residual after 0.58.

**BI-* purpose:** During **0.59** boot theme, list tangles and breaks discovered while migrating to phase tables and modes. Each break row should note: **rule harvested?** · **true owner?** · **parked theme?** See [VISION-0.59](docs/VISION-0.59.md) §5 break/harvest.

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
| [SD-007](#sd-007) | Product `SystemService` vs system layer name | S3 | S | **0.61.4** Inspect rename | ✅ paid (aliases residual) |
| [SD-008](#sd-008) | Session plane has no system home | S2 | M | **0.58** | ✅ closed (0.58.20 exit) |
| [SD-009](#sd-009) | Workload dual bind (leaf engine + service) | S1 | M | 0.57.3–5, 0.57.12 | ✅ service path on port; leaves already port-driver |
| [SD-010](#sd-010) | STE rewrite backlog (legacy dense docs) | S4 | L | ongoing | open |
| [SD-011](#sd-011) | Server transport stack under `common.runtimes` | S2 | L | 0.57.13 | ✅ kits package (`palm.kits.server`) |
| [SD-012](#sd-012) | Cutover shims (fill as 0.57 moves) | S3 | — | 0.57.6–12 | ✅ deleted (0.57.12) |
| [SD-013](#sd-013) | Installed placeholders that lie (capability catalog) | S1 | M | 0.57.9 | ✅ gated (ST-001…005) |
| [SD-014](#sd-014) | No unified system boot phase table; composition not full truth | S2 | L | **0.59** | ✅ closed (0.59.8 exit) |
| [SD-015](#sd-015) | SystemPlanes open-codes wait/session/work install | S2 | M | **0.61** boy-scout | ✅ paid (definitions at edge) |
| [SD-016](#sd-016) | Ambient system-instance DI (seat DI incomplete) | S2 | L | **0.61**+ | open (boot engine seats + ensure_on; host residual) |

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
| [CS-002](#cs-002) | Triple observability names on host | S2 | M | **0.61** pay down (= CF-001) |
| [CS-003](#cs-003) | Core leaves take concrete engines (not protocols) | S2 | M | open |
| [CS-004](#cs-004) | Definition `from_dict` forever-legacy shapes | S3 | M | open |
| [CS-005](#cs-005) | Broad swallow `except` / empty `pass` in hot paths | S3 | M | open (= CF-007) |
| [CS-006](#cs-006) | Supervisor continuous wire is schedule prose | S3 | M | ✅ paid (definitions at edge) |
| [CS-007](#cs-007) | Vitality `lineage: adapter` schema residue | S4 | S | ✅ paid (coerce + no emit) |
| [CS-008](#cs-008) | Plane factories still close over full runtime | S3 | M | ✅ paid (InstallContext ports) |

### Operate diagnosis (OD)

| ID | Title | Sev | Effort | Status |
|----|-------|:---:|:------:|--------|
| [OD-001](#od-001) | Doctor as kernel eyes (not vitality) | S2 | M | open (eyes home landed; product still doctor) |

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

**Severity:** S3 · **Effort:** S · **Theme:** **0.61.4** · **Status:** ✅ **paid**

**Observation:** Product door was named `palm.services.system` / `SystemService`, colliding with the system layer and supervisor loop protocol.

**Paid (0.61.4):**
- Law home: **`palm.services.inspect` / `InspectService`**
- Composition service id: **`inspect`**
- Host / context door: **`host.inspect` / `ctx.inspect`**
- Assist / session / flows take **`inspect=`** (constructors accept temporary `system=` alias)

**Not the same as:**
- Supervisor continuous protocol **`SystemService`** (`palm.system.supervisor`) — loop contract; name kept ([ADR-030](docs/adr/030-system-vitality.md) D6).
- Wire paths / MCP tool group still labeled `system/*` / `palm_system_*` (operate transport; not product law).

**Residual aliases (drop later):** `palm.services.system` re-export · `SystemService = InspectService` · `host.system` / `ctx.system` / `assist.system` properties.

---

### SD-015 — SystemPlanes open-codes plane install

<a id="sd-015"></a>

**Severity:** S2 · **Effort:** M · **Theme:** **0.61** (boy-scout under registry extension)

**Observation:** After hub membership landed, install policy was moved into
`SystemPlanes.install_wait` / `install_session` / `install_work` as a **private
menu** of three concretes. Schedule is thin (`ensure_on` + `install`), but the
hub still **authors** each plane’s participation law. That violates
[AGENTS §1.1](AGENTS.md) / [PALM §9](docs/PALM.md) law 4 (registry extension /
OCP·DIP): definition at the edge; consumer walks definitions.

**Smell:** *menu relocation* (schedule → hub), not finished design.

**Progress (0.61 mid):**

| Landed | Still related |
|--------|---------------|
| `SystemPlanes` hub membership | — |
| Planes take collaborators, not full runtime bag | [CS-008](#cs-008) runtime closures in factories |
| Schedule only seats hub + `install` | — |
| **`PlaneDefinition` at edge** (`wait`/`session`/`work` `definition.py`) | Catalog lists defaults only |
| Hub **walks** definitions (`defn.install`); no open-coded attach prose | Thin `install_*` aliases remain |
| Bind helpers → `install_named` | — |

**Paid shape:**

```text
Plane definition (edge: wait / session / work package)
  → name, aliases, order, install(hub, runtime, ctx)
catalog.DEFAULT_PLANE_DEFINITIONS
  → which definitions join a default system
SystemPlanes.install
  → sort by order · call definition.install · membership via put
Schedule
  → ensure_on + install
```

**Related residual:** [CS-006](#cs-006) · [CS-008](#cs-008) · [SD-016](#sd-016) · ADR-030 D3 · [VISION-0.61](docs/VISION-0.61.md).

**Status:** ✅ **paid** (definitions at edge; hub walks catalog).

---

### SD-016 — Ambient system-instance DI (seat DI incomplete)

<a id="sd-016"></a>

**Severity:** S2 · **Effort:** L · **Theme:** **0.61**+ (structural)

**Observation:** Palm grew real seats (`execution`, `install`, planes, supervisor)
but call graphs still often take the whole system instance and dig. Planes were
the loud instance; the bug is system-wide (boot, host, surfaces).

**Law (target):** inject **interfaces** and **subsystems** — not ambient shell DI.  
[AGENTS §1.2](AGENTS.md) · [PALM §9](docs/PALM.md) law 18.

| Landed (0.61) | Still open |
|---------------|------------|
| `InstallInterface` / `SystemInstall` | Kill ambient digs in host/product/surfaces |
| `system.interfaces` + `system.subsystems` packages | Drop compat shims when callers migrated |
| `Subsystem` protocol | Seat-first APIs outside boot (product doors) |
| BootContext seats: engines + install/planes/supervisor | Progressive install bind (partial board earlier) |
| Schedule uses `ctx.shell` + published seats | Thin `*_to_runtime` bridges remain |
| `SystemPlanes.ensure_on` / `SystemSupervisor.ensure_on` | Host recovery / ApplicationHost bag digs |
| Phase **how** co-located on subject (`phase_*.py`); boot = order + catalog + walk | Host phase definitions (same pattern) |
| System phase catalog imports subject modules only | Drop remaining wire / `*_to_runtime` shims when quiet |

**Avoid:** rename theater only (`runtime` → `source`); `system.common` dump.

**Related:** [SD-015](#sd-015) · [CS-008](#cs-008) · [SU-*](#surface-debt-su).

**Status:** open (boot seat DI improved; host/surfaces residual).

---

### SD-008 — Session plane has no system home

**Severity:** S2 · **Effort:** M · **Status:** ✅ **closed at 0.58.20 exit**

**Observation:** System plane + product door shipped **0.58.0–0.58.20**: seat, multi-attach,
bind, job-path, inspect, Assist dogfood, WS/cookie bind, watches/fan-in, vocabulary,
**active focus**, **owner gate**, **SessionService**, **service/origin sessions**,
**BoundSurface**, **strict attribution**, **inherit-or-service**, **kit door**,
**session operate**, **product path rename** (SI-001/005), **docs/skill** (SI-012).
**ADR-027 Accepted.** Structure live; agents taught truth.

**Residual (not SD-008):** explorer bare (SI-010), thin handle names (SI-002), CLI slots
(SI-006), optional CQRS contributor (SI-007), job-meta cleanup (SI-016), surface compost
([VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md) · **SU-***).

**Impact list:** [SI-001+](#4b-session-impact-inventory-si--0580-analysis) (residual rows stay open).

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

**Severity:** S2 · **Effort:** L · **Status:** ✅ **closed at 0.59.8 exit**  
**Theme:** [VISION-0.59](docs/VISION-0.59.md) (**closed**) · [ADR-028](docs/adr/028-system-boot.md) **Accepted**  
**Release:** [RELEASE-0.59.8](docs/releases/RELEASE-0.59.8.md) · [MIGRATION-0.59](docs/migrations/MIGRATION-0.59.md)  
**Related:** CF-002 (host composition residual) · CompositionProfile (0.50) · ADR-017 (import seams) · SI-014 (plane-store framework — separate) · residual **[BI-*](#bi-boot-impact-inventory)**

**Named when:** Session plane work (0.58.1–0.58.3) forced a clear split: **plugins** vs **system planes** vs **surface bind**. The pain is not missing dynamic import — Palm already has Django-style `INSTALLED_*` + `autoload()`. The pain is **scattered boot** and **implicit order**.

**Paid (0.59.0–0.59.8):** host + system phase tables walked; composition membership truth; BootMode + `for_mode` dogfood; SystemLog seats; residual cleanup (fixture + dead spine). Residual work is **BI-*** only — not a re-open of this debt root.

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

#### Target (theme 0.59)

- Document and implement **host + system boot phase** schedules.  
- Make **CompositionProfile** (and settings) the truthful “what is installed” for product/surfaces/capabilities.  
- **Boot modes** (safe / test / dev / prod / shapes) as presets over axes.  
- Stub seats first; migrate; **break/harvest** isolation ([VISION-0.59](docs/VISION-0.59.md) §5).  
- Host stops growing parallel hard-coded `if` forests that ignore the profile.  
- Map + ADR-028; STE theme plan open at 0.59.0.

#### Agent note (after close)

**SD-014 is closed.** New system planes attach via **system schedule**, not plugin install lists.  
Plugins stay `INSTALLED_*` + registry. Residual boot tangles use **BI-*** kill conditions — do not re-open dual membership ORs or private start soup.

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

**Severity:** S2 · **Theme:** **0.61** (pay down)

See **CF-001** / PD-018. Host exposes `event_plane_status`, `ops_status`, `control_plane_status`.  
These must **not** remain the source of truth for living load.

**Target (0.61):** System **vitality** projection is living fold ([VISION-0.61](docs/VISION-0.61.md) · [ADR-030](docs/adr/030-system-vitality.md) D9). Host status thins, delegates, or deletes. Do not grow a fourth host status method as truth. Align residual bus vocabulary with [EVENT-PLANE](docs/EVENT-PLANE.md).

**Progress (0.61.1–0.61.2):** Projection + `project_top` exist on system. Host still exposes the triple; doctor/product still assemble outside vitality.

---

### CS-006 — Supervisor continuous wire is schedule prose

<a id="cs-006"></a>

**Severity:** S3 · **Effort:** M · **Named:** mid-**0.61** · **Status:** ✅ **paid**

**Paid shape:** `ContinuousServiceDefinition` + `ContinuousWireContext` at
`palm.system.supervisor.definition`; `SystemSupervisor.install` walks catalog;
schedule only `sup.install(runtime, options)`. Register law for work_drain /
outbox lives at the edge.

**Related:** [SD-015](#sd-015) · ADR-029.

---

### CS-007 — Vitality `lineage: adapter` schema residue

<a id="cs-007"></a>

**Severity:** S4 · **Effort:** S · **Named:** mid-**0.61** · **Status:** ✅ **paid**

**Paid:** Primary lineages are `native` | `sampled`. `LINEAGE_ADAPTER` is
legacy-only (`LEGACY_LINEAGES`); `SeatReport` coerces adapter → sampled.
`adapter_count` removed from structural summaries. Do not rebuild adapter maps.

**Related:** [OD-001](#od-001) · [VISION-0.61](docs/VISION-0.61.md) §6.3.

---

### CS-008 — Plane factories still close over full runtime

<a id="cs-008"></a>

**Severity:** S3 · **Effort:** M · **Named:** mid-**0.61** · **Status:** ✅ **paid**

**Paid (proper cut):** :class:`~palm.system.ports.install.InstallInterface` /
:class:`~palm.system.ports.install.SystemInstall` is a first-class seat peer of
:class:`~palm.system.ports.execution.ExecutionPort`. Boot phase
``system.install.bind`` calls :meth:`BaseRuntime.bind_system_install`.
Planes install takes the install interface;
:meth:`InstallContext.from_install` snapshots it — no bag scrape in definitions.
Continuous install uses the same board. Residual ambient DI: [SD-016](#sd-016).

**Related:** [SD-015](#sd-015) · [SD-016](#sd-016).

---

### OD-001 — Doctor as kernel eyes

<a id="od-001"></a>

**Severity:** S2 · **Effort:** M · **Theme:** **0.61**

**Observation:** `build_doctor_report` and plane `doctor_snapshot` assemble / invent health outside system vitality. Product and assist treat **doctor** as the operate physiology API. Lexicon and home are wrong for living load.

**Target:**

| Prefer | Avoid |
|--------|--------|
| **Vitality** system home + seat reports + projection | New `doctor_*` system contracts |
| **Inspect** presents top/vitality from projection | Doctor inventing counters as law |
| Doctor as **legacy verb** / anatomy packaging that **reads** vitality | Doctor as foundation for 0.61 |

**Related:** [CS-002](#cs-002) · [SD-007](#sd-007) · [VISION-0.61](docs/VISION-0.61.md) §5.1 · [ADR-030](docs/adr/030-system-vitality.md) D7.

**Progress (0.61.1–0.61.2):** System vitality is the observation home (seat walk +
projection). Doctor / product `SystemService` still assemble operate truth for
surfaces. Demote unpaid until Inspect presents projection ([SD-007](#sd-007)).

**Status:** open (named at **0.61.0**; partial pay on system side only).

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
| [SI-001](#si-001) | `session_id` forced equal to `instance_id` | product Assist | 0.58.6–12 · **0.58.19** | ✅ paths/envelopes (handles thin SI-002) |
| [SI-002](#si-002) | FlowSession / AssistSession are product-only “sessions” | product | 0.58.1–12 · exit seed | open → [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md) |
| [SI-003](#si-003) | ProcessInstance has no session owner link | instances / system | 0.58.4 | ✅ done |
| [SI-004](#si-004) | WS connection bind is surface-local only | server WS | 0.58.7 | ✅ done |
| [SI-005](#si-005) | MCP / palm_assist paths treat session as instance | MCP Assist | 0.58.6–8 · **0.58.17** · **0.58.19** | ✅ path/alias rename |
| [SI-006](#si-006) | CLI / REPL `active_assist_session_id` | CLI TUI | 0.58.3 · **0.58.17** | partial (BoundSurface truth; dual mirrors residual) |
| [SI-007](#si-007) | CQRS instance queries are the public “session” | host CQRS / kits | 0.58.8 partial | partial (`system/session`) |
| [SI-008](#si-008) | `flow.session.*` events lack real session subject | event plane | 0.58.4+8 | ✅ partial + filter |
| [SI-009](#si-009) | WorkloadOwner.session_id optional / unenforced | workload | 0.58.8 partial | partial (EventContext) |
| [SI-010](#si-010) | Explorer / REST drive instance without session bind | surfaces SU | later (SU-*) | open (named residual) |
| [SI-011](#si-011) | Composition / inbound start without session attribution | work plane edges | 0.58.13 · **0.58.16** | ✅ done (inherit-or-service) |
| [SI-012](#si-012) | Docs and skills say session ≡ flow instance | docs / MCP skill | **0.58.20** | ✅ taught (skill + MCP + wiki) |
| [SI-013](#si-013) | Session multi-attach + reverse index | system plane | 0.58.2 | ✅ done |
| [SI-014](#si-014) | Plane-store pattern not shared across planes | architecture | **ponder later** | open |
| [SI-015](#si-015) | Continue paths skip owner check when session bound | product / surfaces | 0.58.11 · **0.58.15** | ✅ done (strict attribution) |
| [SI-016](#si-016) | Surfaces invent dual context; walk facts on job meta | product / surfaces | **0.58.14** · **0.58.17** | partial (seat+dogfood ✅; job-meta cleanup residual) |

### SI-001 — product handles still named “session” for instance

**Where:** `FlowSession.session_id`, `AssistSession.session_id` (class attrs —
SI-002 thin), grammar path `…/instance/{id}` (was `…/session/{id}`).  
**Status:** ✅ **done at path/envelope level (0.58.19)** — product continue
segment is `instance` / `instance_id`; REST and command paths emit that shape;
legacy segment `session` still **parsed**. Public envelopes: `session_id` =
system subject, `instance_id` = continue.  
**Residual (thin):** product class field `FlowSession.session_id` may still
name the continue handle (SI-002); CLI `active_assist_session_id` slot name
(SI-006). Not a dual-path law risk.

### SI-002 — FlowSession / AssistSession product-only

**Where:** `services/execution/flows/session.py`, `services/assist/session.py`, `services/assist/sessions/`.  
**Impact:** Handles still useful for testing and CLI/assist verbs; they resolve
continue via **SessionService** when wired. Fields may still name continue as
`session_id` (pre-plane era).  
**Target (named, not paid in 0.58):** honest **walk** handles under BoundSurface,
or **cut** and rebuild when APIs/SDKs land — see
[VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md). Do not polish the lie forever.

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

**Where:** `runtimes/mcp/assist/*`, assist/flows grammar.  
**Status:** ✅ **done at 0.58.19** (+ door/rewrite **0.58.17**) — product paths
use `instance`; aliases `flows/instance-*` (legacy `flows/session-*` keys map
to instance paths); `{instance_id}` accepts legacy `session_id` param when
continue handle is absent; `system/session/{id}` remains system journey.  
**Residual:** none on path/alias; skill narrative → **SI-012** ✅ at **0.58.20**.

### SI-006 — CLI / REPL active session id

**Where:** `runtimes/cli/tui/*`, `runtimes/cli/shared/context.py`.  
**Impact:** **Partial (0.58.3 · 0.58.17):** `CliContext.bound_surface` is product
truth; `active_system_session_id` mirrors it. Product
`active_assist_session_id` may still be instance-shaped (SI-001). TUI prompt
still shows assist id.  
**Target:** Prompt / verbs prefer BoundSurface; drop dual mirrors after rename.

### SI-007 — CQRS instance queries as public session

**Where:** host CQRS, `kits/server/cqrs.py`, facades `get_instance`, flows session REST.  
**Impact:** **Partial (0.58.8 + 0.58.18):** operator paths via product door —
`system/session/{id}` · `/view` · `/waiting` · `/instances` · `/focus` ·
`/cancel` · `/cancel/all`. SessionService operate verbs (`focus`,
`cancel_owned`, `surface_view` v2). Full CQRS contributor + REST routes
optional residual.  
**Target:** Session inspect/operate first-class in operator catalog; instance remains job-path API.

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

**Where:** server explorer SSR, bare explorer instance routes (SU-* related).  
**Impact:** Operator UI can drive instance without BoundSurface bind. Dogfood MCP/CLI/WS
paths bind; explorer bulk not paid in 0.58.  
**Status:** **open residual (0.58.20 honesty)** — name for later surface / SU-* theme.
Not a dual-path law hole on dogfood surfaces.  
**Target:** Cookie / BoundSurface when explorer HTTP is next touched.

### SI-011 — Composition / inbound without session

**Where:** work-drain triggers, inbound composition, schedules.  
**Impact:** ✅ **done (0.58.16):** **inherit-or-service** — WorkIntent carries system
`session_id` from the signal when present; submit uses
`SessionService.enrich_reactive_start` (inherit parent walk, else
`work-drain:` / `schedule:` / `inbound:` service session). Never random outside
`sess-…` for reactive. Host `sess-svc-host` at runtime start (0.58.13).  
**Residual edge:** explorer bare paths (SI-010); product rename (SI-001). Workloads
inherit job session only (no separate workload session type).

### SI-012 — Docs and skills alias

**Where:** MCP skill, docs/MCP.md, mcp.txt/card, llms.txt, wiki.  
**Status:** ✅ **done at 0.58.20** — skill + operator card/guide + MCP.md + wiki concept
`session-plane` teach: `session_id` = system subject; `instance_id` = continue;
BoundSurface / SessionService; system paths `system/session/{id}`; soft-land legacy
param names. STE on touch.  
**Residual:** thin class field names stay SI-002; legacy prose in deep MCP history
tables may still say “session” for walks — prefer new wording on next touch.

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
**Residual:** ✅ **0.58.15 closed** — strict attribution: continue resolves owner
from plane or refuses bare orphan (`SessionAttributionError`); start requires
system session when plane ready; compat flag
`PALM_SESSION_STRICT_ATTRIBUTION=false`. Elevated inspect and user-plane
**impersonation** remain later seeds — not dual-own.

### SI-016 — Surfaces invent dual context; walk facts on job meta

**Where:** CLI dual `active_system_session_id` + `active_assist_session_id`; MCP/WS
private bind assembly; job metadata used as walk/surface store.  
**Impact:** **Partial (0.58.14 · 0.58.17):** product **BoundSurface** + session
context metadata API; kit `resolve_session_service` single door; CLI/WS hold
BoundSurface; MCP/WS dogfood no raw plane for product verbs.  
**Residual:** dual mirror fields on CLI until rename; job meta cleanup where
edges still stuff walk facts.  
**Target:** Surfaces hold one **BoundSurface**; walk/surface/attribution facts
on session record only ([VISION-0.58 §4.3–4.4](docs/VISION-0.58.md), ADR-027 D13–D14).

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
| 0.58.16 | Inherit-or-service reactive start ✅; SI-011 finished |
| **close plan** | [VISION-0.58 §6.2](docs/VISION-0.58.md) **0.58.14–0.58.20** + exit (docs locked) |
| 0.58.14 | BoundSurface + session context metadata ✅; SI-016 seat |
| 0.58.15 | Strict attribution ✅ — SI-015 residual closed |
| 0.58.17 | Single kit door + surface dogfood ✅; SI-005/006/016 partial |
| 0.58.18 | Session operate + surface_view v2 ✅; SI-007 partial (operator paths) |
| 0.58.19 | Product vocabulary rename SI-001/005 ✅ |
| **0.58.20** | Docs/skill SI-012 ✅ + residual honesty SI-010/SU-* |
| **0.58 exit** | SD-008 ✅; ADR-027 Accepted; VISION-SURFACE-DEFLATION named; stamp `0.58.20` |
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
- **Plugin self-register + `INSTALLED_*` autoload** — keep; not replaced by a second import framework (SD-014 / 0.59).  
- **Planes are not plugins** — system owns attach; do not put planes on install lists (SD-014 / 0.59).  
- **Break / harvest mid-boot** — mid-0.59 may red-fail legacy phenotypes; declared green bar only; spine sacred ([VISION-0.59](docs/VISION-0.59.md) §5).  
- **0.58 does not ship user impersonation** — D11 seed only; do not soften exclusive ownership for support UX.

---

## 4c. Boot impact inventory (BI-* · 0.59)

<a id="bi-boot-impact-inventory"></a>

**Purpose:** Discoveries and breaks while paying **SD-014**. Grow during the theme.  
**Method:** [VISION-0.59](docs/VISION-0.59.md) §5 · [ADR-028](docs/adr/028-system-boot.md) D8.

| ID | Observation (seed) | Class / note | Status |
|----|--------------------|--------------|--------|
| [BI-001](#bi-001) | Dual start graphs (host vs runtime) not fully walked | inventory + stubs | ✅ paid 0.59.4 (dual root → BI-003) |
| [BI-002](#bi-002) | CompositionProfile not sole membership truth | membership | ✅ paid 0.59.5 (surface bulk → BI-010) |
| [BI-003](#bi-003) | ServerContext vs ApplicationHost second root | dual root | **residual** (exit) |
| [BI-004](#bi-004) | Plugin ensure order vs plane attach order implicit | system schedule | partial ✅ walked; residual edge cases |
| [BI-005](#bi-005) | Job hooks assembled ad hoc in BaseRuntime.start | system phase | partial ✅ phase seat; residual body clarity |
| [BI-006](#bi-006) | Work drain / recover / projections capability OR logic | host schedule + modes | ✅ work_drain OR gone; mode forbid; outbox dual still BI-009-ish |
| [BI-007](#bi-007) | Tests construct hosts many ways (hard to pin mode) | test mode fixtures | **residual** (fixture + dogfood paid; suite not forced) |
| [BI-008](#bi-008) | doctor boot phases / mode | report seat | ✅ paid (tables · membership · last_walk) |
| [BI-009](#bi-009) | Settings vs profile vs options triple override | resolver table | **residual** |
| [BI-010](#bi-010) | Surface mount still special-cased | membership + deflation | **residual** bulk → surface deflation |
| [BI-011](#bi-011) | Accidental import-order “features” (fill as found) | harvest | residual bucket |
| [BI-012](#bi-012) | Rules stuck in surface/host that belong in system schedule | harvest | residual bucket |
| [BI-013](#bi-013) | Work **start** (WorkIntent drain) lives on host workplane | system work plane + supervisor | ✅ closed (0.60.9 exit) |
| BI-014 | `ensure_host_session` swallows Exception on system start | honesty | **residual** |
| [BI-015](#bi-015) | System log narrative (depth / modes / catalog) | seats ✅; catalog later | **residual** |

### BI-001 — Dual start graphs

**Observation:** Host and system start are real but not one documented schedule.  
**Progress (0.59.1):** Documented as one story in [BOOT-INVENTORY.md](docs/BOOT-INVENTORY.md).  
**Progress (0.59.2):** Locked tables + walker; early log seats.  
**Progress (0.59.3):** System schedule fully walked; boot owns handlers; runtime package init cleaned.  
**Progress (0.59.4):** Host schedule fully walked; host boot owns handlers; ApplicationHost thin handoff.  
**Progress (0.59.5):** Membership truth — composition sole gate; deployment feeds resolver only.  
**Pay residual:** dual root (BI-003).

### BI-002 — Composition membership truth

**Observation:** Profile fields exist; host still special-cases capability ORs and mounts.  
**Pay:** ✅ **0.59.5** — runtime gates read `composition` only; settings resolver may fold deployment
`enable_work_drain_service` into membership once; explicit composition wins; PhaseSkip
`composition_off:*`; `boot.start` / doctor `boot.membership` report phenotype.  
**Residual:** surface *bulk* / chrome special cases → BI-010 / surface deflation.

### BI-003 — Dual composition root

**Observation:** `ServerContext` lean path vs `ApplicationHost` (ADR-019 refined).  
**Pay:** only if boot schedule makes fold cheap; else residual after 0.59.

### BI-004 — Plugin ensure vs plane attach

**Observation:** `ensure_core_plugins` then engines then planes — order implicit in code.  
**Pay:** system schedule phase ids.

### BI-005 — Job hooks ad hoc

**Observation:** Hooks list built inline in `BaseRuntime.start`.  
**Pay:** named system phase; no global middleware merge.

### BI-006 — Capability OR logic

**Observation:** work_drain / recover / projections activated by mixed profile and deployment flags.  
**Progress (0.59.2):** mode may forbid recover / background drain.  
**Progress (0.59.5):** work_drain background is composition-only at gate (no OR); deployment
feeds resolver on settings path. Outbox remains available×activated (composition + role).  
**Pay residual:** remaining triple-override clarity → BI-009.

### BI-007 — Test host constructions

**Observation:** Many tests build hosts without a named mode.  
**Progress (0.59.6–.7):** `ApplicationHost.for_mode("test"|"safe"|shapes)`; `server_port`; conftest
`test_mode_host` / `safe_mode_host`; dogfood tests pin phenotype + spine.  
**Progress (0.59.8 residual cleanup):**
- Default integration fixture `host` → `for_mode("all_in_one", settings=fast_settings)` (named mode).
- Dead spine examples fixed: legacy `pattern="dag", options={"name": "quick"}` → one-step wizard
  helper `tests/helpers/flows.py` (DAG requires `nodes` since 0.54).
- Touched host CQRS / CLI / palm_app / job-board tests use spine helper or `for_mode`.
**Still open:** opportunistic migrate of remaining hand-built `ApplicationHost(...)` sites when
edited; not a full suite force. Kill condition: new integration tests prefer `for_mode` or the
shared fixtures; do not reintroduce dead `options={"name": "quick"}` DAGs.

### BI-008 — Doctor boot report

**Observation:** No phase/mode dump.  
**Progress (0.59.2):** `control_plane_status()["boot"]` — mode, modes_available, phase_tables.  
**Progress (0.59.5):** `boot.membership`.  
**Progress (0.59.6):** `boot.last_walk` (public `host.boot_walk`).  
**Pay residual:** none required for exit bar; richer catalog optional.

### BI-009 — Triple override

**Observation:** Settings, profile, and start options can disagree.  
**Pay:** resolver table documented and tested.

### BI-010 — Surface mount special cases

**Observation:** Surface mount not only `CompositionProfile.surfaces`.  
**Progress (0.59.5):** host schedule requires `deployment.server` **and** non-empty
`composition.surfaces`; factory already filters by `only=composition.surfaces`.  
**Pay residual:** chrome / dual-stack surface bulk → [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md).

### BI-011 / BI-012 — Harvest buckets

Fill concrete rows when breaks appear. Note **rule**, **true owner**, **parked theme**.

### BI-013 — Work start on host workplane

<a id="bi-013"></a>

**Observation:** Durable WorkIntent store and schedules live under `palm.system.planes.work`. Continuous drain, trigger wire, and inbound live under `palm.app.host.workplane`.  

**True owner:** System — work plane service + **supervisor** for continuous drain.  

**Theme:** [VISION-0.60](docs/VISION-0.60.md) · [ADR-029](docs/adr/029-system-supervisor.md) **Proposed**.  

**Pay:** `WorkPlaneService` · `runtime.work_plane` · supervised `work_drain` · inbound system contract · system job start · host coordinator deflate.  

**Progress (0.60.1–0.60.9):** `SystemSupervisor` · `WorkPlaneService` · system session attr · supervised work_drain + outbox · inbound under `planes.work` · host prefers plane/supervisor · lean BaseRuntime seats without host.  

**Residual:** host coordinator still wires product session enrich + definition catalog; host `WorkDrainService` fallback; ExecutionPort job-start expand optional; BI-003 ServerContext product wire separate.  

**Status:** ✅ **closed** at **0.60.9** theme exit.

---

### BI-015 — System log (ordered narrative)

<a id="bi-015"></a>

**Observation:** Domain buses + journal exist; process boot narrative was missing.  

**Progress (0.59.1a):** `palm.system.log` + host/system phase lines + ring + doctor tail.  
**Progress (0.59.2):** Walker **reuses** SystemLog; `BootMode` default levels; early seats `host.system_log` / `system.log.ready`.  
See [docs/SYSTEM-LOG.md](docs/SYSTEM-LOG.md).

**Residual:** richer operate catalog; optional JSON/file sink.  
**Status at 0.59 exit:** seats + mode levels dogfooded; catalog/sinks remain residual.  
**Not:** OpenTelemetry product; BT tick flood; replace journal.

---

## 7. Later theme seeds (not open VISION yet)

| Seed | Debt | Spirit |
|------|------|--------|
| **System vitality** | SD-007 · CS-002 · OD-001 · BI-015 · **SD-015** · CS-006…008 | **Opened as 0.61** — [VISION-0.61](docs/VISION-0.61.md) · seed essay [VISION-VITALITY](docs/VISION-VITALITY.md) |
| **Surface deflation** | SU-* · SI-002/006/010 | Compost with evidence after eyes — [VISION-SURFACE-DEFLATION](docs/VISION-SURFACE-DEFLATION.md) |
| **Plane-store framework** | SI-014 | Ponder only; per-plane stores first |
| **User plane + session impersonation** | D11 · SI-015 bare residual | Principal **acts as** owning session — not dual-own |
| **Delegate / team session membership** | growth | Shared walk under one owner session |
| **Workload remainder** | 0.56 queue | Full placement, cancel hooks, peer mesh |

**Closed (not a seed):** **System supervisor + work plane** — [BI-013](#bi-013) ✅ · [VISION-0.60](docs/VISION-0.60.md) closed.  

**Closed (not a seed):** **System boot** — [SD-014](#sd-014) ✅ · [VISION-0.59](docs/VISION-0.59.md) closed · residual **BI-***.

---

*Name the debt. Then pay it in order. Do not paper it.*
