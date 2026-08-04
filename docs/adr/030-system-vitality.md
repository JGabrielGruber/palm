# ADR-030 — System vitality (living-kernel observation)

**Status:** Accepted  
**Date:** 2026-08-03  
**Accepted:** 2026-08-04 (theme exit `0.61.13`)  
**Theme:** [VISION-0.61](../VISION-0.61.md) (**closed**)  
**Map:** [PALM.md](../PALM.md)  
**Seed:** [VISION-VITALITY](../VISION-VITALITY.md)  
**Debt:** [SD-007](../../TECH-DEBT.md#sd-007) ✅ · [CS-002](../../TECH-DEBT.md#cs-002) ✅ · [OD-001](../../TECH-DEBT.md#od-001) ✅ · residual [BI-015](../../TECH-DEBT.md#bi-015) · [SD-016](../../TECH-DEBT.md#sd-016)  
**Release:** [RELEASE-0.61.13](../releases/RELEASE-0.61.13.md) · [MIGRATION-0.61](../migrations/MIGRATION-0.61.md)  
**Related:** [ADR-026](026-palm-system-layer.md) · [ADR-028](028-system-boot.md) · [ADR-029](029-system-supervisor.md) · [ADR-025](025-reactive-interests.md) · [SYSTEM-LOG](../SYSTEM-LOG.md)

---

## Context

1. Palm has a complete local **system** shape for reactive work ([ADR-026](026-palm-system-layer.md) … [ADR-029](029-system-supervisor.md)): planes, supervisor, boot membership, system log.  
2. Operators and agents still learn health mainly from **doctor** reports and **host** status trees (`event_plane_status`, `ops_status`, `control_plane_status`).  
3. Those paths **assemble** numbers outside a single system observation home. They use mixed vocabularies (**CS-002**). Doctor is not the kernel (**OD-001**).  
4. Product **`SystemService`** collides in English with the system layer and with the supervisor continuous-loop protocol name (**SD-007**).  
5. Palm needs **physiology** of the living process: attached seats, load, emissions, bulk of what is loaded — Palm’s living **`top`**.  
6. Workarounds that keep dual truth “to ship thin” create more debt and kill growth. Pre-1.0 may break ugly shapes when homes are wrong.  
7. Theme exit is **José’s judgment** when eyes are proper — not empty checklist death ([VERSIONING.md](../VERSIONING.md) *Who decides*).

---

## Decision

### D1 — Vitality is system observation

Introduce **system vitality** as the kernel’s eyes on the living instance.

| Vitality is | Vitality is not |
|-------------|-----------------|
| Read-only observation of seats, emissions, optional process/bulk | A **plane** that starts or continues work |
| Owned by **`palm.system`** | Owned by product doctor or host status |
| Dynamic discovery of what is attached | Filesystem scan of the repo as physiology |
| Input to inspect / later homeostasis | Silent Design mutation authority |

### D2 — Home package

| Concern | Home |
|---------|------|
| Projection, registry, walk, seat-report types | **`palm.system.vitality`** |
| Product operate door | **`palm.services.inspect`** (`InspectService`) |
| Continuous loop contract | **`palm.system.supervisor`** (protocol name `SystemService` = supervised loop — **different** from product Inspect) |

Do not put vitality under product. Do not put product counters under system.

### D3 — Dynamic seat discovery

| Stable | Dynamic |
|--------|---------|
| Seat report **schema** (versioned fields) | Which seats are **attached** after start |
| Capability **ids** in the registry catalog | Which capabilities are **enabled** (composition / mode / maturity) |

Walk the live `SystemInstance` (and membership).  
Absent seat or capability → **absent / skipped**, not fake green.  
Do **not** hardcode a closed menu of package paths as health law.  
Do **not** treat heap reflection as the architecture of record.

**System planes:** :class:`~palm.system.planes.hub.SystemPlanes` is the living
seat that **consumes** individual planes (``put`` · ``install`` · ``detach`` ·
``names`` · ``get`` · ``status``) — same pattern as :class:`SystemSupervisor`
for continuous services. Hub owns install policy; boot schedule only seats the
hub and calls ``install``. Vitality expands plane seats from the live hub.
No private wait/session/work menu in vitality or the schedule.

### D4 — Seat report is the unit of truth

Each discovered seat contributes a **seat report** (versioned dict).  
Projection folds reports and emission samples into a **snapshot** with lineage (`capability_id`, `seat_id`, `lineage`).

| Prefer | Avoid |
|--------|--------|
| Native `seat_report` (name may lock in code) on seats | Permanent private `__dict__` scrape as law |
| Temporary **adapters** from old `status` / `doctor_snapshot` with `lineage: adapter` | Silent dual trees of the same counters |
| One write path for the fact on the owning seat | Product inventing parallel numbers |

### D5 — VitalityRegistry

Eyes grow via a **capability registry**, not a closed `if` forest in BaseRuntime.

| Capability role | Examples |
|-----------------|----------|
| Core observe | `seat_walk`, `emission_window` |
| Optional observe | `process_resources` (**installed 0.61.8**), `loaded_bulk` (**installed 0.61.9**), `system_log_tail`, `boot_membership` |
| Active tools | `benchmark` (**installed 0.61.10**, **off by default**), `monitor_agent` (intention) |

Projection law: iterate **enabled** capabilities → each returns a typed fragment → merge → snapshot.  
Capabilities do not own start/continue.  
Intention vs installed maturity applies when a tool is experimental.  
Tools that thrash must not be default-enabled on everyday `project()`.

**Progress (0.61.8):** `process_resources` body — stdlib `resource` + optional
`/proc/self/status`; units labeled; top folds light `process.summary`; not a
health grade.

**Progress (0.61.9):** `loaded_bulk` body — resolve attached seats only; type /
module LOC / public callables / composition cardinality; top folds light
`bulk.summary`; **visibility not shame**; not a full tree genome scan.

**Progress (0.61.10):** `benchmark` tool — `run_benchmark` / `sample_benchmark`;
recipes `idle` · `pulse` · `walk` · `log_fill`; nested observe-only projection
(before/after); pure `diff_load_points`; consumes projection (no second metric
law). Workload placement later.

**Progress (0.61.11):** Product present — `InspectService.benchmark` /
`present_benchmark`; CLI `palm benchmark` (and assist catalog thin pass-through).
Surfaces do not thrash or invent load counters; they call the inspect door.

**Progress (0.61.12):** CLI human units (MiB · ms) by default (`--raw` / `--json`
keep machine numbers). Recipes deepened: `work_cycle` (default — enqueue + tick
missing-flow intents on work plane; peak_pending in recipe story) and
`project_stress` (observe projection self-cost).

### D6 — Product door is Inspect

Rename product **`palm.services.system` / `SystemService`** to **`palm.services.inspect` / `InspectService`** (**SD-007**).

| Host / surface | Target |
|----------------|--------|
| `host.system` (product) | `host.inspect` (temporary alias OK while migrating) |
| Doctor / top / list / cancel | Methods on InspectService that **read** system vitality and CQRS |

**Progress (0.61.4):** law home + host door landed; import/host `system` aliases residual; wire `system/*` paths may stay until surface compost.

Supervisor continuous protocol keeps the name **SystemService** for loops. Document the distinction in PALM / this ADR.

### D7 — Doctor is legacy debt, not lexicon law

| Concept | Role |
|---------|------|
| **Vitality** | System-intrinsic physiology terms and fold |
| **Doctor** | Legacy diagnosis **verb** and report packaging (**OD-001**) |
| **Top** | Operator metaphor for the living load view |

New system contracts must **not** use `doctor_*` as the physiology API.  
Assist/MCP may keep a `doctor` **alias** if the body consumes vitality.  
`build_doctor_report` must not remain the place that invents living counters.

**Progress (0.61.6 / OD-001 ✅):** Product doctor envelope is
`kind=legacy_doctor` · `role=anatomy_packaging` · `eyes_law` + `operate_paths`.
Nests projection `top` / vitality pointer. Anatomy bag =
storage/registries/jobs/control_plane residual. Plane `doctor_snapshot` and
host control_plane remain named residual (seat report + **CS-002**).

### D8 — Emission identity

Aggregates that may later inform Design or probes carry:

```text
actor_kind · session subject · channel · kind · outcome · time
```

Core `actor_kind` set: `human`, `agent`, `probe`, `system`, `peer`, plus **`unknown`**.  
Prefer declared metadata. Do not reverse-engineer “bot vs human” from timing alone.  
Do not blend emitter classes into one unlabelled score for mutation-facing claims.

### D9 — Host status trees are not living law

Host `event_plane_status` / `ops_status` / `control_plane_status` (**CS-002**) must not remain the source of truth for living load.

| Prefer | Avoid |
|--------|--------|
| System vitality projection | Growing a fourth host status method as truth |
| Thin host façade that delegates | Frozen characterization tests blocking correct homes forever |

Break or thin host status when vitality replaces it. Name residual bridges.

**Progress (0.61.7 / CS-002 ✅):** Host bags stamped `role=host_packaging` ·
`eyes_law` · `operate_paths`. Single **`packaging_status()`** entry (control-plane
body). Triple methods are residual aliases. Characterization tests assert
domain key **supersets** + demotion (no frozen dual-truth equality as law).
Doctor/CLI treat host status as packaging residual only.

### D10 — Modes, cost, and forbidden magic

- Modes gate expensive capabilities (`safe` / `test` cheap by default).  
- No silent job mutation from vitality.  
- No shame scores that auto-condemn large modules (visibility ≠ guilt).  
- No second metrics write path for the same fact.  
- No vitality plane of start/continue law.

### D11 — Theme exit is José’s judgment

**Floor** (“eyes open”) is defined in [VISION-0.61](../VISION-0.61.md).  
Theme **exit** is when **José Gabriel Gruber** judges eyes proper, ADR Accepted, residual named, and declared green bars hold.  
Agents propose and implement. They do not close the theme by checklist alone.  
Do not force exit to satisfy empty process notes while ambition still has proper work under the same home.

**Project law (all themes):** [VERSIONING.md](../VERSIONING.md) theme discipline (*Who decides*) · [AGENTS.md](../../AGENTS.md) §6b — floor · growth · José’s exit; proper over workaround; ambition over empty process.

---

## Consequences

### Positive

- Palm can develop and operate with **living evidence**.  
- One home for physiology; product and surfaces stay thin presenters.  
- Registry room for tools (benchmark, monitor) without dual paths.  
- Doctor and host status stop defining kernel vocabulary.

### Trade-offs

- Inspect rename has blast radius (host, assist, MCP, Explorer).  
- Characterization tests that freeze host status JSON must move with law.  
- Temporary adapters create short-lived dual shapes until native seat reports land.

### Residual (expected)

- Full surface deflation (SU-*) remains a later seed.  
- Full BI-015 catalog/sinks may grow under vitality or stay residual.  
- Dream pieces (probes, homeostasis, Grove, genome) need eyes first.

---

## Implementation notes (non-normative)

Suggested early order: seat report + walk → projection + `seat_walk` → emission window → Inspect rename → optional caps and host compost.  
See [VISION-0.61](../VISION-0.61.md) §7.

---

## Status history

| Date | Status |
|------|--------|
| 2026-08-03 | **Proposed** with theme open `0.61.0` |
| 2026-08-04 | **Accepted** at theme exit `0.61.13` — José judged eyes proper |
