# VISION 0.65 — Outbox as the proof cut

**Status:** ✅ **Theme closed** (José 2026-08-18) at `0.65.0`.  
**ADR:** [034](../../adr/034-supervised-start-walks-registration.md) **Accepted**  
**Migration:** [MIGRATION-0.65](../../migrations/MIGRATION-0.65.md)  
**Map:** [PALM.md](../../PALM.md) · [VISION-0.64](VISION-0.64.md) (**closed**) · [ADR-033](../../adr/033-one-walker.md) **Accepted** · cut note [structure-materialize-cut](../../architecture/appendix/structure-materialize-cut.md)  
**Prior organ:** `work_drain` — first real capability.

**Exit:** José closed the theme (2026-08-18). The home copies. No open minor.

---

## Goal

**Outbox** proves the 0.64 home copies. Definition lists the name. A hand takes seats. Omit means it does not run. Old walkers die in the same cut as the hand.

If a cut shows `work_drain` still has costume, that work is **0.64**. Themes classify. They do not lock you out.

## Floor

- `system.background.start` walks registration. It does not name organs. [ADR-034](../../adr/034-supervised-start-walks-registration.md).  
- `CapabilitySeats` can carry outbox ports. Assemble fills them.  
- Outbox is name + hand + omit on the same phenotypes as drain.  
- The old outbox walkers are gone.

**Floor met.** Costume leftover paid in 0.65.3–0.65.4.

## Growth

Same membership law for `journal` is **not** this floor. It is later.

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

Admission / [SD-020](../../../TECH-DEBT.md#sd-020). `journal` (same law, later). `inbound` (old pile). Drain leftovers: journal consumer also named `work_drain`, `start_plane_running`, host then `runtime.stop`.

Not the queue: `analytics`, `neonroot` (dogfood); `workloads` (engine).

## Guide slices (not a sealed contract)

| Slice | Intent |
|-------|--------|
| **0.65.0** | Plan + ADR-034 Proposed. |
| **0.65.1** | **Landed** — invert start + grow seats. |
| **0.65.2+** | **Landed** — hand + DNA list + kill freelance catalog, composition/seed, host recover AND, second host thread. Omit proof. |
| **0.65.3** | **Landed** — leftover cleanup (`OUTBOX_SERVICE`, docs, dead kwargs). |
| **0.65.4** | **Landed** — surface / comment costume (dead `host.outbox.processed`, stale master help). |
| **exit** | **Landed** — ADR-034 Accepted · stamp `0.65.0` |

## Debt

Old outbox walkers paid. Leave admission / SD-020 named. Do not invent `requires`.

---

## After compact (closed chronicle)

**Present:** Theme **closed**. Floor **met**. No open minor.

**Process:** parent holds the contract. Parallel **read**. One **writer**. Short briefs. [AGENTS §1.1](../../../src/palm/AGENTS.md).

**0.65.2 landed** (`9dbc8b5b`): `outbox` is name + hand + omit on the same phenotypes as drain. Freelance catalog is empty. Composition/seed do not write the name. Host recover does not start the loop. `enable_outbox_background` / `enable_outbox_service` gone. Host `OutboxBackgroundService` deleted. Store wire on the host path follows DNA listing; explicit `host.start(enable_event_outbox=…)` still wins.

**0.65.3 leftover:** unused `OUTBOX_SERVICE` deleted.

**0.65.4 leftover:** surface / comment costume paid.

**José (keep):** some knobs still live on **profile/settings**, not DNA. Membership is the definition list. Poll / recover-on-start / bare `enable_event_outbox` are packaging. Do not grow another `enable_*` king when journal copies the home.

**Keep (named, not this theme):** bare `enable_event_outbox` (non-host store); poll numbers on the profile; `from_wire` alias; job-hook opportunistic drain; webhook still composition-gated.

**Not this theme:** admission / SD-020 · `journal` · `inbound` · webhook as an organ.

### Home (`work_drain` + `outbox`)

| Piece | Live |
|-------|------|
| Listing | `StructureDefinition.capabilities` / `has_capability` — [definition.py](../../../src/palm/core/structure/definition.py). Lists both on `local.cli` / `server` / `all_in_one` / `worker`. Omits on `local.embedded` / `mcp`. No `requires`. |
| Walker | `apply_local_capabilities` loops `LOCAL_CAPABILITY_HANDS` — [materialize.py](../../../src/palm/system/structure/materialize.py) · [hands.py](../../../src/palm/system/structure/hands.py). Table: `work_drain` + `outbox`. |
| Hand | `apply_work_drain` / `apply_outbox`. Unlist → `supervisor.unregister`. Listed → `register_*`. |
| Seats | `CapabilitySeats` is `supervisor` + `work_plane` + optional `outbox_store` / `outbox_processor`. Assemble fills them then materializes — [phase_assemble.py](../../../src/palm/system/structure/phase_assemble.py). |
| Start | After assemble: `system.background.start` walks registered services and asks `may_start` — [phase_background.py](../../../src/palm/system/subsystems/supervisor/phase_background.py). Host schedule ends at ready. |
| Proof tests | [test_work_drain_materialize.py](../../../tests/assembly/test_work_drain_materialize.py) · [test_outbox_materialize.py](../../../tests/assembly/test_outbox_materialize.py) |

### Walkers that died with the hand (0.65.2)

| Walker | File | What it decided |
|--------|------|-----------------|
| `composition.has("outbox")` at spawn | [host_schedule.py](../../../src/palm/app/host/boot/host_schedule.py) | Now DNA `has_capability("outbox")` |
| `composition.has` ∧ master ∧ `enable_outbox_service` | [recovery.py](../../../src/palm/app/host/lifecycle/recovery.py) | Deleted. Loop starts with drain. |
| Host recover start / second thread | `recovery.py` (host `OutboxBackgroundService` deleted) | Recover no longer starts the loop |
| Freelance catalog | [supervisor/definition.py](../../../src/palm/system/subsystems/supervisor/definition.py) `DEFAULT_CONTINUOUS_DEFINITIONS` | Empty. Hands register. |
| Seed + presets | [seed.py](../../../src/palm/system/structure/seed.py) · [composition.py](../../../src/palm/app/host/composition.py) | Do not write `outbox` |
| `enable_outbox_background` | was start king on the service | Gone |

---

## After this theme (not this file)

| Next | Where |
|------|--------|
| `journal` | Same membership law. Attach hand, not a loop. Not open. |
| `webhook` | After outbox is omit-enough. Do not invent definition `requires`. |
| `compensation` / `projections` | Attach / detach. Later. |
| Admission contract + [SD-020](../../../TECH-DEBT.md#sd-020) | [VISION-ASSEMBLY](../VISION-ASSEMBLY.md) remainder. |
