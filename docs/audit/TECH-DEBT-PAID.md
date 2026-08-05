# Palm — Technical debt (paid / closed detail)

**Status:** Archive of **paid and closed** debt detail. Not the live register.  
**Live open debt:** [TECH-DEBT.md](../../TECH-DEBT.md) (repo root).  
**Older PD era:** [TECH-DEBT-ERA-0.45.md](TECH-DEBT-ERA-0.45.md).  
**Language:** ASD-STE100 (practical).

Rows here are **history**. Do not treat them as open work.  
IDs stay stable for links from STATUS, VISION, and CHANGELOG.

---

### SD-004 — `PatternBuildContext` is an engine bag

<a id="sd-004"></a>

**Severity:** S1 · **Effort:** M · **Slice:** 0.57.4 · **Status:** ✅ done

**Observation:** Build context fields were raw engines only.

**Resolution:** Context carries `execution` plus optional engines for unit tests.  
Builders call `resolve_resource_invoker` / `resolve_workload_driver` (port first).  
Core leaves accept `ResourceInvoker` / `WorkloadDriver`. Engine fields remain for engine-only tests.

---


### SD-006 — `PalmKernel` name vs system instance

<a id="sd-006"></a>

**Severity:** S3 · **Effort:** S · **Status:** ✅ done (0.57.2)

**Observation:** `PalmKernel` is infra (storage, instance manager, runtime registry).  
Readers may think it is the effect kernel.

**Resolution:** Docstrings on `PalmKernel` and `create_runtime` state infra vs system instance.  
PALM.md and SYSTEM-LOW-LEVEL already draw the line. No rename required.

---


### SD-007 — Product `SystemService` vs system layer

<a id="sd-007"></a>

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


### SD-008 — Session plane has no system home

<a id="sd-008"></a>

**Severity:** S2 · **Effort:** M · **Status:** ✅ **closed at 0.58.20 exit**

**Observation:** System plane + product door shipped **0.58.0–0.58.20**: seat, multi-attach,
bind, job-path, inspect, Assist dogfood, WS/cookie bind, watches/fan-in, vocabulary,
**active focus**, **owner gate**, **SessionService**, **service/origin sessions**,
**BoundSurface**, **strict attribution**, **inherit-or-service**, **kit door**,
**session operate**, **product path rename** (SI-001/005), **docs/skill** (SI-012).
**ADR-027 Accepted.** Structure live; agents taught truth.

**Residual (not SD-008):** explorer bare (SI-010), thin handle names (SI-002), CLI slots
(SI-006), optional CQRS contributor (SI-007), job-meta cleanup (SI-016), surface compost
([VISION-SURFACE-DEFLATION](docs/vision/VISION-SURFACE-DEFLATION.md) · **SU-***).

**Impact list:** [SI-001+](#4b-session-impact-inventory-si--0580-analysis) (residual rows stay open).

---


### SD-009 — Workload dual bind

<a id="sd-009"></a>

**Severity:** S1 · **Effort:** M · **Slices:** 0.57.3–5, 0.57.12 · **Status:** ✅ done

**Observation:** Leaves used engine; product used service → engine.

**Resolution:** Leaves use port→driver (0.57.4). Product effects + list/doctor/
stop_owned use ExecutionPort (0.57.12). Engine remains inside the system instance.

---


### SD-011 — Server transport under `common.runtimes`

<a id="sd-011"></a>

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

<a id="sd-012"></a>

**Severity:** S3 · **Status:** ✅ deleted (0.57.12)

Temporary re-export packages under `palm.common` (runtimes base/host, wait, work,
workload, executions, hooks) removed. Canonical imports are `palm.system.*`.  
`palm.common.runtimes` retains **only** `server/` kit + doctor contributor registry.

---


### SD-013 — Installed placeholders that lie

<a id="sd-013"></a>

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

<a id="sd-014"></a>

**Severity:** S2 · **Effort:** L · **Status:** ✅ **closed at 0.59.8 exit**  
**Theme:** [VISION-0.59](docs/vision/closed/VISION-0.59.md) (**closed**) · [ADR-028](docs/adr/028-system-boot.md) **Accepted**  
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
- Stub seats first; migrate; **break/harvest** isolation ([VISION-0.59](docs/vision/closed/VISION-0.59.md) §5).  
- Host stops growing parallel hard-coded `if` forests that ignore the profile.  
- Map + ADR-028; STE theme plan open at 0.59.0.

#### Agent note (after close)

**SD-014 is closed.** New system planes attach via **system schedule**, not plugin install lists.  
Plugins stay `INSTALLED_*` + registry. Residual boot tangles use **BI-*** kill conditions — do not re-open dual membership ORs or private start soup.

---

## 3b. Surface debt detail

Surfaces must stay **thin** ([PALM.md](docs/PALM.md)). Today `palm.runtimes` is the largest tree (~22k LOC Python). Most weight is **server** (~14k) then **MCP** (~4.7k) then **CLI** (~3.8k). Embedded/daemon stay small.


### SU-004 — MCP legacy module names

<a id="su-004"></a>

**Severity:** S3 · **Effort:** S · **Status:** ✅ **deleted**

**Observation:** Tiny re-export stubs still named as if they were eras:

- `mcp/tools.py` — “legacy tool registration”  
- `mcp/debug_tools.py`  
- `mcp/phase5_tools.py`

**Paid:** Empty stubs deleted (no importers). Domain tools live under `mcp/*/tools.py`; assist under `mcp/assist/`. No phase-era module names at the MCP package root.

---


### SU-006 — Surface transport kit split

<a id="su-006"></a>

**Severity:** S2 · **Effort:** L · **Related:** SD-011 · **Status:** ✅ done (0.57.13)

**Observation:** Protocol lived under common; composition under runtimes — two homes for one HTTP story.

**Resolution:** Kit **`palm.kits.server`** owns protocol/routes/transport/SSR helpers.  
Surfaces under `palm.runtimes.server` stay thin composers. That split is intentional (kit vs surface).

---


### ST-001 — Fake-success providers

<a id="st-001"></a>

**Severity:** S1 · **Effort:** S · **Status:** ✅ gated (0.57.9)

| Provider | Resolution |
|----------|------------|
| `graphql` | Not in `INSTALLED_PROVIDERS`; `fetch`/`connect` raise `NotImplementedError` |
| `postgres` | Same |

Listed in `INTENTION_PROVIDERS`. Purpose remains in STUBS.md.

---


### ST-002 — No-op storage backends

<a id="st-002"></a>

**Severity:** S1 · **Effort:** S · **Status:** ✅ gated (0.57.9)

| Backend | Resolution |
|---------|------------|
| `storages/postgres` | Not in `INSTALLED_STORAGES` (core only); I/O raises |
| `storages/mongodb` | Same |

Remain in `OPTIONAL_STORAGES` for lazy discovery; no silent fake durability.

---


### ST-003 — ETL pattern phase ticker

<a id="st-003"></a>

**Severity:** S2 · **Effort:** S · **Status:** ✅ gated (0.57.9)

**Resolution:** Not in `INSTALLED_PATTERNS`; listed in `INTENTION_PATTERNS`.  
Package remains for explicit import (tests may opt in). Purpose in STUBS.md.

---


### ST-004 — `parquet_load` always errors

<a id="st-004"></a>

**Severity:** S3 · **Effort:** XS · **Status:** ✅ gated (0.57.9)

**Resolution:** Not in `INSTALLED_TRANSFORMS` / not registered as builtin.  
Module may remain for future pyarrow work (`INTENTION_TRANSFORMS`).

---


### ST-005 — Tests freeze lying install sets

<a id="st-005"></a>

**Severity:** S1 · **Effort:** S · **Status:** ✅ fixed (0.57.9)

**Resolution:** `test_modular_apps` asserts truthful `INSTALLED_*` + separate `INTENTION_*` sets.

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

**Related:** [OD-001](#od-001) · [VISION-0.61](docs/vision/closed/VISION-0.61.md) §6.3.

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


### SI-001 — product handles still named “session” for instance

<a id="si-001"></a>

**Where:** `FlowSession.session_id`, `AssistSession.session_id` (class attrs —
SI-002 thin), grammar path `…/instance/{id}` (was `…/session/{id}`).  
**Status:** ✅ **done at path/envelope level (0.58.19)** — product continue
segment is `instance` / `instance_id`; REST and command paths emit that shape;
legacy segment `session` still **parsed**. Public envelopes: `session_id` =
system subject, `instance_id` = continue.  
**Residual (thin):** product class field `FlowSession.session_id` may still
name the continue handle (SI-002); CLI `active_assist_session_id` slot name
(SI-006). Not a dual-path law risk.


### SI-003 — ProcessInstance has no session owner

<a id="si-003"></a>

**Where:** `palm/instances/process_instance.py`, instance sync, `SessionOwnershipHook`.  
**Status:** ✅ **done** at **0.58.4** — first-class `session_id` (+ metadata fallback);
`build_instance_from_job` / update; `SessionOwnershipHook` attaches on submit when
job metadata carries `session_id`. Product paths must still **pass** the system
session id (Assist dogfood 0.58.6).


### SI-004 — WS bind is surface-local

<a id="si-004"></a>

**Where:** `runtimes/server/surfaces/websocket/session.py` (`op: bind`, conn bind state).  
**Status:** ✅ **done** at **0.58.7** (+ **0.58.9** vocabulary) — `op: bind` / hello /
dispatch resolve system session via plane; cookie-like transport
(`X-Palm-Session`, Cookie `palm_session`); bound snapshot uses `session_id` +
`instance_id`. REST create echoes system `session_id` + `Set-Cookie`.


### SI-005 — MCP / palm_assist session = instance

<a id="si-005"></a>

**Where:** `runtimes/mcp/assist/*`, assist/flows grammar.  
**Status:** ✅ **done at 0.58.19** (+ door/rewrite **0.58.17**) — product paths
use `instance`; aliases `flows/instance-*` (legacy `flows/session-*` keys map
to instance paths); `{instance_id}` accepts legacy `session_id` param when
continue handle is absent; `system/session/{id}` remains system journey.  
**Residual:** none on path/alias; skill narrative → **SI-012** ✅ at **0.58.20**.


### SI-008 — flow.session.* events

<a id="si-008"></a>

**Where:** orchestration terminal emit; `EventContext`; instance lifecycle events.  
**Status:** ✅ **partial (0.58.4 + 0.58.8)** — context/payload attribution +
`event_matches` / Events WS session filter. Event type names unchanged.


### SI-011 — Composition / inbound without session

<a id="si-011"></a>

**Where:** work-drain triggers, inbound composition, schedules.  
**Impact:** ✅ **done (0.58.16):** **inherit-or-service** — WorkIntent carries system
`session_id` from the signal when present; submit uses
`SessionService.enrich_reactive_start` (inherit parent walk, else
`work-drain:` / `schedule:` / `inbound:` service session). Never random outside
`sess-…` for reactive. Host `sess-svc-host` at runtime start (0.58.13).  
**Residual edge:** explorer bare paths (SI-010); product rename (SI-001). Workloads
inherit job session only (no separate workload session type).


### SI-012 — Docs and skills alias

<a id="si-012"></a>

**Where:** MCP skill, docs/MCP.md, mcp.txt/card, llms.txt, wiki.  
**Status:** ✅ **done at 0.58.20** — skill + operator card/guide + MCP.md + wiki concept
`session-plane` teach: `session_id` = system subject; `instance_id` = continue;
BoundSurface / SessionService; system paths `system/session/{id}`; soft-land legacy
param names. STE on touch.  
**Residual:** thin class field names stay SI-002; legacy prose in deep MCP history
tables may still say “session” for walks — prefer new wording on next touch.


### SI-013 — Session multi-attach not first-class yet

<a id="si-013"></a>

**Where:** `SessionStore` / `SessionPlaneService` (0.58.1–0.58.2).  
**Status:** ✅ **done** at **0.58.2** — `attach_instance` / `detach_instance` /
`session_for_instance`; reverse key `palm:session:by_instance:*`; one instance
→ one session (refuses dual attach). Store remains on StorageEngine.


### SI-015 — Continue paths skip owner check when session is bound

<a id="si-015"></a>

**Where:** Product/MCP/WS continue with bound system `session_id` + `instance_id`.  
**Status:** ✅ **done** at **0.58.11** — plane `owns_instance` /
`require_owned_instance` / `InstanceNotOwnedError`; operator
`rewrite_system_session_continue` gates continue paths; flows/assist dispatch
gate when params carry system `session_id`; host
`require_session_owns_instance`; WS maps to `session_owner`. Path instance is
authoritative (not replaced by plane focus).  
**Law:** exclusive ownership + active = focus only
([VISION-0.58 §4.1](docs/vision/closed/VISION-0.58.md), [ADR-027](docs/adr/027-session-plane.md) D9–D11).  
**Residual:** ✅ **0.58.15 closed** — strict attribution: continue resolves owner
from plane or refuses bare orphan (`SessionAttributionError`); start requires
system session when plane ready; compat flag
`PALM_SESSION_STRICT_ATTRIBUTION=false`. Elevated inspect and user-plane
**impersonation** remain later seeds — not dual-own.

### SD-001 — No unified execution port

<a id="sd-001"></a>

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

<a id="sd-002"></a>

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

<a id="sd-003"></a>

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

### SD-005 — Edge and product call engines by field

<a id="sd-005"></a>

**Severity:** S2 · **Effort:** L · **Slices:** 0.57.5, 0.57.7 (effects ✅)

**Progress (0.57.12):** Product workload list/doctor/stop_owned use the port.
Job list and effects already did. Known dual-field edges closed.

**Policy:** Product → port. Surfaces → product or thin system entry.  
**No new** `runtime.resource` / `runtime.orchestration.*` effect shortcuts
without adding a residual row here. Status: ✅ for catalogued sites.

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

**Related residual:** [CS-006](#cs-006) · [CS-008](#cs-008) · [SD-016](#sd-016) · ADR-030 D3 · [VISION-0.61](docs/vision/closed/VISION-0.61.md).

**Status:** ✅ **paid** (definitions at edge; hub walks catalog).

---

### SD-017 — WorkIntent claim not exclusive

<a id="sd-017"></a>

**Severity:** S1 · **Effort:** M · **Theme:** **0.62** floor ([VISION-0.62](docs/vision/closed/VISION-0.62.md) · [ADR-031](docs/adr/031-multi-claimer-work-drain.md))

**Observation:** `WorkIntentStore.claim_due` is read entry → set `status=claimed`.  
`WorkIntent` has no `claimed_by` / `lease_until`. No reclaim / visibility timeout.  
Two claimers can take the same intent or race the pending index and coalesce keys.

**Pay:** Exclusive `claim_due(..., claimer_id=)` · lease fields on core intent · `reclaim_expired` · owner-aware ack/fail when multi-claimer on · concurrent claim tests.  
In-process atomicity: store lock (or single-writer mutex). Same API at `workers=1`.

**Progress (0.62.1–0.62.3):** `WorkIntent.claimed_by` / `lease_until` · store `RLock` · exclusive `claim_due` · `reclaim_expired` · owner-aware `ack`/`fail` · plane `tick(claimer_id=…, reclaim=…)` · concurrent claim tests.  
**Do not:** Flip `work_drain_workers>1` as success before multi-worker growth (**SD-018**).

**Related:** [SD-018](#sd-018) · [SD-019](#sd-019) · [BI-013](#bi-013) (home closed; packaging residual).

**Status:** ✅ **paid** (0.62.1–0.62.3 floor).

---

### SD-018 — Work drain single-claimer by construction

<a id="sd-018"></a>

**Severity:** S2 · **Effort:** M · **Theme:** **0.62** growth

**Observation:** Continuous drain was one daemon thread (`palm-work-plane`): claim batch then serial `submit_flow`.  
QueuedScheduler was one job-drive worker; orchestration job map concurrency was unproven.

**Pay growth:** N drain workers (default **1**) under plane/supervisor; exclusive store only.  
Drive-path concurrent job drive: membership lock + exclusive drive + QueuedScheduler pool.

**Progress (0.62.4):** `work_drain_workers` (default 1) · plane starts N poll threads with distinct claimer ids · settings + install options · multi-worker background test.  
**Progress (0.62.5 residual named):** claim pool scale ≠ host-core job parallelism (GIL / patterns).  
**Progress (0.62.6):** `run_benchmark(..., workers=K)` multi-claimer `work_cycle` proof.  
**Progress (0.62.7):** orchestration `RLock` membership · `begin_drive` / `end_drive` exclusive per job · `drive_job` acquires · `QueuedScheduler(workers=N)` pool · settings `queued_workers` / `PALM_QUEUED_WORKERS` · concurrent submit + multi-worker drive tests. Product truth: multi-claimer improves **start-queue** throughput; Queued **N** improves **job-drive overlap** under I/O/wait — still not “all host cores for Python patterns” (workloads / processes).

**Related:** [SD-017](#sd-017) · supervisor continuous defs · vitality `work_cycle` 1 vs K · residual [SD-019](#sd-019).

**Status:** ✅ **paid** (drain N + drive pool + exclusive drive; GIL/host-core honesty remains product law).

---

### CS-002 — Triple observability names

<a id="cs-002"></a>

**Severity:** S2 · **Theme:** **0.61**

See **CF-001** / PD-018. Host exposes `event_plane_status`, `ops_status`, `control_plane_status`.  
These must **not** remain the source of truth for living load.

**Target (0.61):** System **vitality** projection is living fold ([VISION-0.61](docs/vision/closed/VISION-0.61.md) · [ADR-030](docs/adr/030-system-vitality.md) D9). Host status thins, delegates, or deletes. Do not grow a fourth host status method as truth. Align residual bus vocabulary with [EVENT-PLANE](docs/EVENT-PLANE.md).

**Progress (0.61.5):** Living fold is **`InspectService.top`** (system projection).

**Progress (0.61.7):** Host bags demoted — `role=host_packaging` · `eyes_law` ·
`operate_paths`. Single entry **`host.packaging_status()`** (same body as
control_plane). Triple methods remain **thin residual aliases**. Doctor nests
packaging only. Characterization tests no longer freeze dual-truth key equality
as law (superset + demotion stamps). CLI doctor labels ops/event-plane residual.

**Residual (named):** triple method names for consumers; nested event_plane/ops
inside packaging bag; bus string ids; `work_drain_background` alias; boot
membership inside packaging (anatomy, not seat law). Do not grow a fourth living
status method.

**Status:** ✅ **paid** (0.61.7) — host status is not living law; residual aliases named.

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

**Related:** [CS-002](#cs-002) · [SD-007](#sd-007) · [VISION-0.61](docs/vision/closed/VISION-0.61.md) §5.1 · [ADR-030](docs/adr/030-system-vitality.md) D7.

**Progress (0.61.5):** Product **`InspectService.top` / `.vitality`** present
**only** from system projection.

**Progress (0.61.6):** Doctor **demoted** — envelope `kind=legacy_doctor` ·
`role=anatomy_packaging` · `eyes_law` + `operate_paths` · nests projection
`top` / vitality pointer · nested `anatomy` bag. `build_doctor_report` is
anatomy packaging only (no seat invent). Verb may stay on assist/MCP/CLI.

**Residual (named, not unpaid eyes debt):** plane `doctor_snapshot` transitional
(toward seat report); host `control_plane` in packaging → **[CS-002](#cs-002)**;
flat packaging keys for consumers; wire `system/doctor` alias paths.

**Status:** ✅ **paid** (0.61.6) — doctor is not kernel eyes; residual packaging + CS-002/plane dual names named.

---

### SI-016 — Surfaces invent dual context; walk facts on job meta

<a id="si-016"></a>

**Where:** CLI dual `active_system_session_id` + `active_assist_session_id`; MCP/WS
private bind assembly; job metadata used as walk/surface store.  
**Impact:** **Partial (0.58.14 · 0.58.17):** product **BoundSurface** + session
context metadata API; kit `resolve_session_service` single door; CLI/WS hold
BoundSurface; MCP/WS dogfood no raw plane for product verbs.  
**Residual:** dual mirror fields on CLI until rename; job meta cleanup where
edges still stuff walk facts.  
**Target:** Surfaces hold one **BoundSurface**; walk/surface/attribution facts
on session record only ([VISION-0.58 §4.3–4.4](docs/vision/closed/VISION-0.58.md), ADR-027 D13–D14).

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
| **close plan** | [VISION-0.58 §6.2](docs/vision/closed/VISION-0.58.md) **0.58.14–0.58.20** + exit (docs locked) |
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
- **Break / harvest mid-boot** — mid-0.59 may red-fail legacy phenotypes; declared green bar only; spine sacred ([VISION-0.59](docs/vision/closed/VISION-0.59.md) §5).  
- **0.58 does not ship user impersonation** — D11 seed only; do not soften exclusive ownership for support UX.

---

## 4c. Boot impact inventory (BI-* · 0.59)

<a id="bi-boot-impact-inventory"></a>

**Purpose:** Discoveries and breaks while paying **SD-014**. Grow during the theme.  
**Method:** [VISION-0.59](docs/vision/closed/VISION-0.59.md) §5 · [ADR-028](docs/adr/028-system-boot.md) D8.

| ID | Observation (seed) | Class / note | Status |
|----|--------------------|--------------|--------|
| [BI-001](#bi-001) | Dual start graphs (host vs runtime) not fully walked | inventory + stubs | ✅ paid 0.59.4 (dual root → BI-003) |
| [BI-002](#bi-002) | CompositionProfile not sole membership truth | membership | ✅ paid 0.59.5 (surface bulk → BI-010) |
| [BI-003](#bi-003) | Product packaging dual path (types retained) | shared packaging | **residual** (growth: registry seats / enrich) |
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
| BI-014 | `ensure_host_session` swallows Exception on system start | honesty | ✅ paid (fail closed) |
| [BI-015](#bi-015) | System log narrative (depth / modes / catalog) | seats ✅; catalog later | **residual** |

### BI-001 — Dual start graphs

<a id="bi-001"></a>

**Observation:** Host and system start are real but not one documented schedule.  
**Progress (0.59.1):** Documented as one story in [BOOT-INVENTORY.md](docs/BOOT-INVENTORY.md).  
**Progress (0.59.2):** Locked tables + walker; early log seats.  
**Progress (0.59.3):** System schedule fully walked; boot owns handlers; runtime package init cleaned.  
**Progress (0.59.4):** Host schedule fully walked; host boot owns handlers; ApplicationHost thin handoff.  
**Progress (0.59.5):** Membership truth — composition sole gate; deployment feeds resolver only.  
**Pay residual:** BI-003 growth only (packaging seats / enrich); floor paid at 0.61.13.

### BI-002 — Composition membership truth

<a id="bi-002"></a>

**Observation:** Profile fields exist; host still special-cases capability ORs and mounts.  
**Pay:** ✅ **0.59.5** — runtime gates read `composition` only; settings resolver may fold deployment
`enable_work_drain_service` into membership once; explicit composition wins; PhaseSkip
`composition_off:*`; `boot.start` / doctor `boot.membership` report phenotype.  
**Residual:** surface *bulk* / chrome special cases → BI-010 / surface deflation.

### BI-004 — Plugin ensure vs plane attach

<a id="bi-004"></a>

**Observation:** `ensure_core_plugins` then engines then planes — order implicit in code.  
**Pay:** system schedule phase ids.

### BI-005 — Job hooks ad hoc

<a id="bi-005"></a>

**Observation:** Hooks list built inline in `BaseRuntime.start`.  
**Pay:** named system phase; no global middleware merge.

### BI-006 — Capability OR logic

<a id="bi-006"></a>

**Observation:** work_drain / recover / projections activated by mixed profile and deployment flags.  
**Progress (0.59.2):** mode may forbid recover / background drain.  
**Progress (0.59.5):** work_drain background is composition-only at gate (no OR); deployment
feeds resolver on settings path. Outbox remains available×activated (composition + role).  
**Pay residual:** remaining triple-override clarity → BI-009.

### BI-008 — Doctor boot report

<a id="bi-008"></a>

**Observation:** No phase/mode dump.  
**Progress (0.59.2):** `control_plane_status()["boot"]` — mode, modes_available, phase_tables.  
**Progress (0.59.5):** `boot.membership`.  
**Progress (0.59.6):** `boot.last_walk` (public `host.boot_walk`).  
**Pay residual:** none required for exit bar; richer catalog optional.

### BI-013 — Work start on host workplane

<a id="bi-013"></a>

**Observation:** Durable WorkIntent store and schedules live under `palm.system.planes.work`. Continuous drain, trigger wire, and inbound live under `palm.app.host.workplane`.  

**True owner:** System — work plane service + **supervisor** for continuous drain.  

**Theme:** [VISION-0.60](docs/vision/closed/VISION-0.60.md) · [ADR-029](docs/adr/029-system-supervisor.md) **Proposed**.  

**Pay:** `WorkPlaneService` · `runtime.work_plane` · supervised `work_drain` · inbound system contract · system job start · host coordinator deflate.  

**Progress (0.60.1–0.60.9):** `SystemSupervisor` · `WorkPlaneService` · system session attr · supervised work_drain + outbox · inbound under `planes.work` · host prefers plane/supervisor · lean BaseRuntime seats without host.  

**Residual:** host coordinator still wires product session enrich + definition catalog; ExecutionPort job-start expand optional; BI-003 ServerContext product wire separate.  

**Paid residual:** host `WorkDrainService` fallback removed — coordinator binds packaging onto system `work_plane` only (fail closed if unattached).  

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
