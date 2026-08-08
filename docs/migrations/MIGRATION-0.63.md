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

## Residual

Multi-process shared claim CAS remains [SD-019](../../TECH-DEBT.md#sd-019) — not this theme’s subject.  
Pretenders not yet swallowed: kill-date under [SD-020](../../TECH-DEBT.md#sd-020) / theme residual.

## Product law (while theme open)

- Do not dig composition root for readiness.  
- Do not set “ready” outside the assemble path.  
- When admission is law on a path: **fail closed** is correct; soft-open is dual mode.
