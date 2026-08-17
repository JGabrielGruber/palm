# Appendix — structure materialize cut (2026-08-17)

**Status:** Standing engineering note. **Not** a theme plan. **Not** a VISION rewrite.  
**Locked by José:** first unit and “no no-op.”  
**Code (2026-08-17):** `AssemblyDefinition.capabilities` + manager materialize of `work_drain`; host/mode/composition are no longer peer kings for that unit.  
**Stamp:** José closed **0.63** and opened **0.64** (2026-08-17).

**Read after compact:** this file → [structure-management.md](../c3-components/structure-management.md) → implement.  
Do not re-harvest the tree unless code contradicts this note.

**Map:** [PALM.md](../../PALM.md) · [TECH-DEBT SD-020 / SD-021 / SD-016](../../../TECH-DEBT.md) · present [VISION-0.64](../../vision/VISION-0.64.md) · seed [VISION-ASSEMBLY §0](../../vision/VISION-ASSEMBLY.md#0-progress-honesty-2026-08-08)

---

## 1. Situation (as-built)

Admission is real. Membership install is not.

| Layer | Built | Missing |
|-------|--------|---------|
| Core assembly | Reconciler: phase + places + admission. `tick` emits only `ENSURE_PLACE`. | No membership sections on `AssemblyDefinition`. |
| System assembly | Load DNA, refuse-check, place hands, publish fail-closed admission. | No `materialize`. Capabilities/surfaces are start kwargs for refuse only. |
| Boot / runtime | `InstallInterface` used by plane and supervisor **install**. | Phase catalogs still choose membership (planes, plugins, engines, outbox, drain). |
| Host | DNA **seed** at spawn (`PALM_ASSEMBLY_DNA_ID` → mode → composition inference). | After load, `CompositionProfile.has` is still the install king. `BootMode` still peer-gates drain/recover. |
| Product | Admission oath on assist + four execution façades. Does not assemble or set ready. | Constructors still take a runtime bag. No service takes `ExecutionPort`. |
| Surfaces | Transport + admission voice. | Not this cut (`SU-*`). |

Builtin DNA lists **no** `places_required` and **no** install set. The default assemble path can go READY without installing a unit.

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

## 3. Locked for the next implementation session

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
| Host composition king | `src/palm/app/host/composition.py` |
| Host drain gate | `src/palm/app/host/application_host.py`, `boot/host_schedule.py`, `boot/modes.py` |
| Bootstrap flag → cap | `src/palm/app/bootstrap.py` |

---

## 6. Explicit non-goals for the focused session

- Re-run a repo-wide harvest.
- Close 0.63 by more residual cartography.
- Invent a second admission path.
- Surface compost, MCP dual stack, explorer splits.
- Full SD-016 sweep.
- Provider / cache membership sources (local only).
