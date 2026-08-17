# Appendix — structure materialize cut (2026-08-17)

**Status:** Standing engineering note. **Not** a theme plan. **Not** a VISION rewrite.  
**Locked by José:** first unit and “no no-op.”  
**Code (2026-08-17):** `AssemblyDefinition.capabilities` + manager materialize of `work_drain`; host/mode/composition are no longer peer kings for that unit.  
**Stamp:** José closed **0.63** and opened **0.64** (2026-08-17).

**Read after compact:** [VISION-0.64 after compact](../../vision/VISION-0.64.md#after-compact-2026-08-17) → **this file §1 + §7** → implement.  
Do not re-harvest the tree unless code contradicts this note.

**Map:** [PALM.md](../../PALM.md) · [TECH-DEBT SD-020 / SD-021 / SD-016](../../../TECH-DEBT.md) · present [VISION-0.64](../../vision/VISION-0.64.md) · seed [VISION-ASSEMBLY §0](../../vision/VISION-ASSEMBLY.md#0-progress-honesty-2026-08-08)

---

## 1. Situation (as-built)

Admission is real. **`work_drain` membership install is real.** Other capabilities still live on composition.

| Layer | Built | Residual |
|-------|--------|----------|
| Core assembly | Reconciler + `AssemblyDefinition.capabilities`. Builtin DNA lists `work_drain` on cli/server/all_in_one/worker. | No DNA `requires` / start-fact vocabulary. Refuse token `background_drain` is a second name. |
| System assembly | Walker `apply_local_capabilities` loops `LOCAL_CAPABILITY_HANDS`. Hand takes `CapabilitySeats`. Assemble fills seats from `ctx` + install `work_plane`. | Journal / outbox / inbound are not hands. |
| Boot / runtime | `system.background.start` starts **registered** drain when start ports are bound. | Outbox still uses a start option. |
| Host | DNA seed at spawn. Start window reads supervisor service, not a host listed bag. Status reads `runtime.work_plane`. | `host.start_plane` thin alias. Flags still seed composition. `allow_background_drain` is serialize-only. |
| Product | Admission oath on assist + four execution façades. | Constructors still take a runtime bag. No service takes `ExecutionPort`. |
| Surfaces | Transport + admission voice. | Not this cut (`SU-*`). |

A new organ is still not only a DNA name + hand: seed flags and composition still *look* like membership. That is leftover honesty, not a second install king.

---

## 2. Classification (do not mix)

| Class | Meaning | Examples |
|-------|---------|----------|
| **Spine** | Sequential. One owner. Definition as install set. | Membership field on definition; manager apply; demote `composition.has` / `BootMode` on that unit. |
| **Same-cut** | After the interface is frozen. May parallel later. | Product `ExecutionPort` / session seat / drop `admission_gate()` fallback to the runtime. |
| **Named residual** | Leave named. | Cancel/stop, LIST/DESCRIBE, unit engine access, packaging env, doctor, `*_to_runtime`. |
| **Other theme** | Do not open here. | Surface deflation, plugin catalog as DNA, OS/workload place spawn as first unit, SD-019, Grove. |
| **Docs drift** | Do not treat as done. | Seed comments that DNA is king of **wiring**; `composition.py` as sole membership switch; vault skeleton. |

Isolated “fix SD-016 everywhere” or residual-ledger cleanup is a workaround. Product does not own structure.

---

## 3. Locked (landed) — first unit

| Decision | Lock |
|----------|------|
| First materialize unit | **`work_drain` under a `capabilities` section** (local source only). |
| No-op prove-out | **No.** Do not land `journal` (or similar always-on) only to prove the field. |
| Scope of first slice | Definition names capabilities → manager materializes **`work_drain`** → seed/mode/profile stop being peer kings **for that unit**. Admission stays fail-closed. |
| Surfaces | Out of cut. |
| Product seat DI (SD-016) | Boy-scout only on files this spine already touches. Not a second front. |

### 3.1 Why `work_drain`

It is already a triple king: settings flag → `MEMBERSHIP_CAPABILITY_SEEDS` → `composition.has("work_drain")` → host schedule → DNA `refuse:background_drain`.

Not first: default planes (always-on kernel), `ensure_core_plugins` (wide), always-on `journal` / `projections` / `workloads`, `outbox` (store vs loop vs node role).

### 3.2 Spine steps (sequential, one workspace)

1. Add local **capabilities** on `AssemblyDefinition` (frozenset of names). Builtin DNA **lists what the phenotype has**, not only what it refuses.
2. Manager **materializes** that set: register/start `work_drain` only if listed.
3. `composition.has("work_drain")` becomes a projection of the definition, or dies on that path.
4. `BootMode.allow_background_drain` stops being a peer OR.
5. Proof: drain starts iff DNA lists it (embedded vs cli/server).

Do not fan this out across worktrees. Shared types.

**After** this contract is in code, same-cut product seats may use parallel worktrees.

---

## 4. Theme routing

José stamped **0.64** (2026-08-17). The engineering cut in §3 does not change.

---

## 5. Code homes (start here)

| Concern | Path |
|---------|------|
| Definition | `src/palm/core/assembly/definition.py` |
| Reconciler | `src/palm/core/assembly/engine.py` (today: places + admission only) |
| Seed catalog | `src/palm/system/assembly/seed.py` (`MEMBERSHIP_CAPABILITY_SEEDS`) |
| Seat / assemble | `src/palm/system/assembly/seat.py`, `loop.py`, `phase_assemble.py` |
| Composition seed | `src/palm/app/host/composition.py` (still lists `work_drain`; not install) |
| Hands / walker | `src/palm/system/assembly/hands.py`, `materialize.py` |
| Host start window | `src/palm/app/host/boot/host_schedule.py` (`host.background.start_plane`) |
| System start | `src/palm/system/subsystems/supervisor/phase_background.py` |
| Freelance catalog | `src/palm/system/subsystems/supervisor/definition.py` (`DEFAULT_CONTINUOUS_DEFINITIONS` is outbox-only; `WORK_DRAIN_SERVICE` exists, wire does not walk it) |
| Bootstrap flag → cap | `src/palm/app/bootstrap.py` |

---

## 6. Explicit non-goals for the focused session

- Re-run a repo-wide harvest.
- Close 0.63 by more residual cartography.
- Invent a second admission path.
- Surface compost, MCP dual stack, explorer splits.
- Full SD-016 sweep.
- Provider / cache membership sources (local only).
- Invent DNA `requires` / install-port vocabulary.
- Land journal / outbox as a second organ before pile B is honest.

---

## 7. Next motion after compact

José locked this order (2026-08-17). Not a slice table. Not patch stamps.

**Landed:** DNA `capabilities` · walker · `CapabilitySeats` from `ctx` + board · start from registered service · no `host._work_drain_listed` · tests/status use `runtime.work_plane` · default wire catalog does not register `work_drain`. Commits `6e50fd6b`, `d1b3c23a`.

**Process:** explore agents in parallel. One implementer at a time. Do not fan `seed.py`, `hands.py`, `phase_assemble.py`, `definition.py` (supervisor) across writers.

| Pile | Do | Do not |
|------|----|--------|
| **A** | STATUS header (done if this file + VISION match). Delete `BootMode.allow_background_drain`. Collapse `dna_lists_work_drain` in seed. | Do not rewrite seed fold here if B3 is in flight. |
| **B1** | **Landed.** Default catalog is outbox-only. Hand registers `work_drain`. Unregister-on-unlist stays. | Do not put `work_drain` back on `DEFAULT_CONTINUOUS_DEFINITIONS`. |
| **B2** | Refuse `work_drain` against DNA capabilities, not `assembly_capabilities` from composition. | Do not invent a new refuse vocabulary. |
| **B3** | Stop writing `"work_drain"` on composition presets and `enable_work_drain_service` seed. Then drop `refuse:background_drain` if omit is enough. | Do not wipe `composition.has` for journal/outbox/projections. |
| **C** | Coordinator reads `runtime.work_plane`. Optional: publish assembly seat without `getattr(shell, "assembly")`. | Journal as second hand only after B. No DNA `requires`. |

**First act next session:** **B2** — refuse `work_drain` against DNA capabilities, not `assembly_capabilities` from composition. Then B3 can stop writing the name on composition / flag. Cheap A may ride if it does not share `seed.py` with B2.
