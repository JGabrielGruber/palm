# VISION 0.65 — Outbox as the proof cut

**Status:** 🌱 **Theme open** — plan stamp `0.65.0` (José 2026-08-18).  
**ADR:** [034](../adr/034-supervised-start-walks-registration.md) **Proposed**  
**Migration:** [MIGRATION-0.65](../migrations/MIGRATION-0.65.md)  
**Map:** [PALM.md](../PALM.md) · [VISION-0.64](closed/VISION-0.64.md) (**closed**) · [ADR-033](../adr/033-one-walker.md) **Accepted** · cut note [structure-materialize-cut](../architecture/appendix/structure-materialize-cut.md)  
**Prior organ:** `work_drain` — first real capability.

Execution starts at `0.65.1`. This file is the plan. The after-compact scout stays so a new session does not re-harvest.

---

## Goal

**Outbox** proves the 0.64 home copies. Definition lists the name. A hand takes seats. Omit means it does not run. Old walkers die in the same cut as the hand.

If a cut shows `work_drain` still has costume, that work is **0.64**. Themes classify. They do not lock you out.

## Floor

- `system.background.start` walks registration. It does not name organs. [ADR-034](../adr/034-supervised-start-walks-registration.md).  
- `CapabilitySeats` can carry outbox ports. Assemble fills them.  
- Outbox is name + hand + omit on the same phenotypes as drain.  
- The old outbox walkers are gone, or José names residual.

## Growth

Same membership law for `journal` is **not** this floor. Skip-string polish and more organs may continue while the theme stays open.

## Locks (José 2026-08-18 — theme open)

| # | Lock |
|---|------|
| **1** | Invert `system.background.start` (and grow seats) as the **first** execute motion. Not a second `if want_outbox`. |
| **2** | Who lists `outbox`: same phenotypes as drain — `local.cli` / `server` / `all_in_one` / `worker` list; `local.embedded` / `mcp` omit. Master-only start is not packaging law. |

## Forbidden always

- Definition `requires`.  
- New private menu in the start phase.  
- Alias tests green for composition / recover AND / freelance catalog.  
- Host as a second outbox lifecycle (ADR-033).

## Not this theme

Admission / [SD-020](../../TECH-DEBT.md#sd-020). `journal` (same law, later). `inbound` (old pile). Drain leftovers: journal consumer also named `work_drain`, `start_plane_running`, host then `runtime.stop`.

Not the queue: `analytics`, `neonroot` (dogfood); `workloads` (engine).

## Guide slices (not a sealed contract)

| Slice | Intent |
|-------|--------|
| **0.65.0** | Plan + ADR-034 Proposed. |
| **0.65.1** | **Landed** — invert start + grow seats. Freelance outbox `may_start` still reads `enable_outbox_background` (named residual). |
| **0.65.2+** | **Landed** — hand + DNA list + kill freelance catalog, composition/seed, host recover AND, second host thread. Omit proof. |

Extend or merge when the home is the same.

## Debt

Pay the old outbox walkers in this theme. Leave admission / SD-020 named. Do not invent `requires`.

---

## After compact (2026-08-18)

**Read this block first.** Do not re-scout unless a cite is stale.

**Present:** Theme **open**. Floor **met**. José has **not** exited. Agent recommended **exit** (proof cut done; journal/webhook are later, not remainder). José asked what cleanup exists — **do it in a cheap thread**, then he exits or not.

**Process:** parent holds the contract. Parallel **read**. One **writer**. Short briefs. [AGENTS §1.1](../../src/palm/AGENTS.md).

**0.65.2 landed (uncommitted as of write):** `outbox` is name + hand + omit on the same phenotypes as drain. Freelance catalog is empty. Composition/seed do not write the name. Host recover does not start the loop. `enable_outbox_background` / `enable_outbox_service` gone. Host `OutboxBackgroundService` deleted. Store wire on the host path follows DNA listing; explicit `host.start(enable_event_outbox=…)` still wins.

**José (keep):** some knobs still live on **profile/settings**, not DNA. Membership is the definition list. Poll / recover-on-start / bare `enable_event_outbox` are packaging. Do not grow another `enable_*` king when journal copies the home.

### Cheap cleanup (next thread — not journal)

Do these if José says clean. Not exit. Not a new organ.

| Item | Why | Leave |
|------|-----|-------|
| Delete unused `OUTBOX_SERVICE` recipe | Freelance shape leftover. Hands call `register_outbox`. Drain already deleted `WORK_DRAIN_SERVICE`. | `register_outbox` / `OutboxLoopService` |
| `phase_outbox.py` module doc | Still says host spawn kings store from `composition.has` | Store phase itself |
| [TECH-DEBT](../../TECH-DEBT.md) **SD-021** progress line | Still names 0.63.28 composition king as live | The debt row; other caps still composition |
| Dead test kwargs `enable_outbox_service=False` | Field gone; pydantic `extra=ignore` swallows them | Gate tests themselves |
| Appendix [structure-materialize-cut](../architecture/appendix/structure-materialize-cut.md) freelance row / B1 | Still says catalog is outbox-only | Closed 0.64 chronicle elsewhere |

**Do not** rewrite closed visions / ADR-020 / MIGRATION-0.60 as “cleanup.” **Do not** accept ADR-034 or close the theme unless José exits.

**Keep (named, not cleanup):** bare `enable_event_outbox` (non-host store); poll numbers on the profile; `from_wire` alias; job-hook opportunistic drain; webhook still composition-gated.

**Not this theme:** admission / SD-020 · `journal` · `inbound` · webhook as an organ.

### Home to copy (`work_drain`)

| Piece | Live |
|-------|------|
| Listing | `StructureDefinition.capabilities` / `has_capability` — [definition.py](../../src/palm/core/structure/definition.py). Lists `work_drain` on `local.cli` / `server` / `all_in_one` / `worker`. Omits on `local.embedded` / `mcp`. No `requires`. |
| Walker | `apply_local_capabilities` loops `LOCAL_CAPABILITY_HANDS` — [materialize.py](../../src/palm/system/structure/materialize.py) · [hands.py](../../src/palm/system/structure/hands.py). Table: `work_drain` + `outbox`. |
| Hand | `apply_work_drain` / `apply_outbox`. Unlist → `supervisor.unregister`. Listed → `register_*`. |
| Seats | `CapabilitySeats` is `supervisor` + `work_plane` + optional `outbox_store` / `outbox_processor`. Assemble fills them then materializes — [phase_assemble.py](../../src/palm/system/structure/phase_assemble.py). |
| Start | After assemble: `system.background.start` walks registered services and asks `may_start` — [phase_background.py](../../src/palm/system/subsystems/supervisor/phase_background.py). Host schedule ends at ready. |
| Proof tests | [test_work_drain_materialize.py](../../tests/assembly/test_work_drain_materialize.py) · [test_outbox_materialize.py](../../tests/assembly/test_outbox_materialize.py) |

Name + hand **registers**. It does **not** start a second organ until start walks registration.

### Walkers that died with the hand (0.65.2)

| Walker | File | What it decided |
|--------|------|-----------------|
| `composition.has("outbox")` at spawn | [host_schedule.py](../../src/palm/app/host/boot/host_schedule.py) | Now DNA `has_capability("outbox")` |
| `composition.has` ∧ master ∧ `enable_outbox_service` | [recovery.py](../../src/palm/app/host/lifecycle/recovery.py) | Deleted. Loop starts with drain. |
| Host recover start / second thread | `recovery.py` (host `OutboxBackgroundService` deleted) | Recover no longer starts the loop |
| Freelance catalog | [supervisor/definition.py](../../src/palm/system/subsystems/supervisor/definition.py) `DEFAULT_CONTINUOUS_DEFINITIONS` | Empty. Hands register. |
| Seed + presets | [seed.py](../../src/palm/system/structure/seed.py) · [composition.py](../../src/palm/app/host/composition.py) | Do not write `outbox` |
| `enable_outbox_background` | was start king on the service | Gone |

Builtin DNA lists `outbox` on the same phenotypes as drain. Default assemble id `local.embedded` omits it.

**Keep and rehome:** store, processor, `OutboxLoopService`. Job-hook opportunistic drain is not membership. Poll numbers may stay packaging. `BootMode.recover_on_start` stays a mode — outbox must stop depending on that window.

### Freeze set (rewritten in 0.65.2 — do not alias)

Proof: [test_outbox_materialize.py](../../tests/assembly/test_outbox_materialize.py). Rewritten: composition king, living-capabilities AND, host recover, `test_outbox_supervisor_0_60_6`, lean embedded, membership seed, composition presets, vitality freelance walk. Worker/server assert supervisor `outbox`, not `host.outbox_service`.

---

## After this theme (not this file)

| Next | Where |
|------|--------|
| `journal` | Same membership law. Attach hand, not a loop. |
| `webhook` | After outbox is omit-enough. Do not invent definition `requires`. |
| `compensation` / `projections` | Attach / detach. Later. |
| Admission contract + [SD-020](../../TECH-DEBT.md#sd-020) | [VISION-ASSEMBLY](VISION-ASSEMBLY.md) remainder. After copyable. |
