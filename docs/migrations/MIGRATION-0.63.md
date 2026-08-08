# Migration — 0.63 Organism assembly

**Theme:** [VISION-0.63](../vision/VISION-0.63.md) (**open**) · **ADR:** [032](../adr/032-organism-assembly.md) **Proposed**  
**Map:** [PALM.md](../PALM.md) · seed [VISION-ASSEMBLY](../vision/VISION-ASSEMBLY.md)

Palm is pre-1.0. This theme introduces **assembly DNA**, **admission**, and **fail-closed** citizens.  
Impact is discovered as the gate rises. This file **grows** when paths break — do not invent dual hops to avoid updating it.

## Prefer (when seats exist)

| Goal | Use |
|------|-----|
| Structure decree | Assembly definition (DNA) loaded via seed or authority |
| Readiness for business that needs ground | **Admission** snapshot from assembly status |
| Choose shape at edge | Entry / mode / DNA id seed — not dual profile soup as king |
| Packaging | `PALM_*` storage, paths, ports, logs, pool widths (unchanged spirit) |
| Household assemble | Assembly control / loop — **not** product |

## Behavior changes (0.63.2)

| Was | Now |
|-----|-----|
| No assembly seat | System phase `system.assembly.assemble` after `system.ready` |
| No admission surface | `BaseRuntime.admission` / `runtime.assembly` after start |
| — | Default DNA `local.embedded` → usually `may_run_business=True` after start |
| — | `assembly_skip=True` leaves admission fail-closed (empty) |

## Behavior changes (0.63.3) — gate raised

| Was | Now |
|-----|-----|
| Work-plane `able` = system started only | `able` = started **and** `admission.may_run_business` |
| Drain/tick could run with no organism readiness | Fail closed: `tick` returns 0 until admission allows |
| — | Enqueue still accepted (work waits); continuous drain idles when not able |

## Behavior changes (0.63.4)

| Was | Now |
|-----|-----|
| `submit_flow` / `submit_process` only needed `is_started` | Also require `admission.may_run_business` or **`AdmissionRefusedError`** |
| No coherence guard | `just guard-assembly` · `tests/assembly/` |

Runtime doubles used with `DefinitionExecutor` must publish an `admission` snapshot (no silent bypass).

## Behavior changes (0.63.5)

| Was | Now |
|-----|-----|
| Always `local.embedded` default DNA | Host seeds DNA from **boot mode** or **composition** |
| — | `ApplicationHost.for_mode("cli")` → `local.cli`; `safe`/`test` → `local.embedded`; server/prod → `local.server` |
| — | Explicit `assembly_dna_id` / `assembly_definition` still wins |

### Break inventory (pretenders)

| Path | Status |
|------|--------|
| Work-plane tick / drain | **Gated** (0.63.3) |
| `submit_flow` / `submit_process` (executor) | **Gated** (0.63.4) |
| DNA id from real dogfood shapes | **Seeded** (0.63.5) — refuse not yet hard-enforced on membership |
| Assist / MCP packaging soft-ready | Open pretender |
| Host soft “definitions ready” dual flags | Open pretender (SD-020 remainder) |
| Composition dual structure after DNA load | Partial — seed map + env DNA seed (0.63.13); residual enable_* membership seeds (SD-021) |

## Expected direction of break (honest early)

| Was (glue) | Toward (law) |
|------------|--------------|
| Soft “definitions ready” / host flags | Admission from assembly status |
| Profile + BootMode as structure king | Seed → DNA; status after load |
| Citizen starts with half-host | Fail closed until assemble (**0.63.3+** gate) |
| Tests that bypass readiness | Coherence suite: fix or delete |

Citizen fail-closed lands in **0.63.3+**. Until then admission is published but not all paths enforce it.

## Settings / env

| Kind | Stance |
|------|--------|
| Packaging (`PALM_STORAGE_*`, `PALM_DATA_DIR`, ports, log, workers, …) | **Keep** as packaging |
| Structure toggles that rewrite membership as peer law | Map into DNA seed or purge (SD-021) |
| DNA / mode seed (when introduced) | Chooses which definition loads |

## Behavior changes (0.63.13) — env structure seed (SD-021)

| Was | Now |
|-----|-----|
| No first-class env DNA chooser | **`PALM_ASSEMBLY_DNA_ID`** / `assembly_dna_id` seeds DNA (wins over mode/composition) |
| Caller `assembly_dna_id` skipped membership seed | Membership always seeded for refuse (dual shape fails closed) |
| Continuous drain only composition + boot mode | Also **DNA refuse** `background_drain` (structure king after load) |
| Structure env uncatalogued | `STRUCTURE_SEED_ENV` cartography in `palm.system.assembly.seed` |

`PALM_ENABLE_WORK_DRAIN_SERVICE` remains a **membership seed** at composition resolve — not a peer OR after DNA load.

## Behavior changes (0.63.14) — place spawn port

| Was | Now |
|-----|-----|
| ENSURE_PLACE only marked ledger ready | Optional **PlaceSpawnPort** runs first; ledger records outcome |
| No OS place contract | `os:` places **fail closed** without body handle (`os_spawn_not_configured`) |
| — | `RegisteredPlaceSpawn` routes exact id / prefix strategies |

Default remains in-process success (behavior-preserving for floor DNA with no `os:` places).

## Behavior changes (0.63.15) — household + OS process

| Was | Now |
|-----|-----|
| Default hands = place book only | **`HouseholdEffectPort`** — places + projection/policy/seed intents |
| `os:` only accept pre-supplied handle | **`OsProcessRegistry`** spawns `argv`/`command`; release terminates |
| Structure intents recorded no-op | Invalidate → `PROJECTION_FAILED`; refresh → `PROJECTION_LOADED`; policy re-checks refuse; seed finishes |

## Behavior changes (0.63.16) — workload place book

| Was | Now |
|-----|-----|
| No workload place strategy | **`workload:`** prefix via `WorkloadPlaceSpawn` / WorkloadEngine |
| Unbound place soft? | Fail closed: `workload_engine_not_bound` |
| — | `combined_structure_spawn_port` routes `os:` + `workload:` |

## Behavior changes (0.63.17) — host structure bind

| Was | Now |
|-----|-----|
| Default assemble seat = in-process place spawn only | **Combined** `os:` + `workload:` spawn on household hands |
| Workload engine only in tests | **`system.assembly.assemble`** binds shell `workload` when initialized |
| No opt-out | **`assembly_bind_workload=False`** keeps `workload:` fail-closed |
| — | Custom effect ports without place book are not clobbered |

Bare place ids still succeed in-process (fallback). DNA that requires `workload:` places can converge on the real host path after engines init.

## Behavior changes (0.63.18) — reassemble edges

| Was | Now |
|-----|-----|
| Same DNA READY short-circuit could leave stale refuse | Assemble clears refuse then re-checks membership |
| No named re-converge path | **`AssemblySeat.reassemble`** (omitted DNA → seat definition) |
| No force void of same-id READY | **`receive_definition(..., force=True)`** / **`engine.invalidate()`** |
| Place gone → invalidated | **`reassemble`** re-ensures places until ready or blocked |

Citizens stay fail-closed while phase is `invalidated` / `blocked`.

## Residual

Multi-process shared claim CAS remains [SD-019](../../TECH-DEBT.md#sd-019) — not this theme’s subject.  
Pretenders not yet swallowed: kill-date under [SD-020](../../TECH-DEBT.md#sd-020) / theme residual.

## Product law (while theme open)

- Do not dig composition root for readiness.  
- Do not set “ready” outside the assemble path.  
- When admission is law on a path: **fail closed** is correct; soft-open is dual mode.
