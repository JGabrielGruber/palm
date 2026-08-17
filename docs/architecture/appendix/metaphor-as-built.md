# Appendix — metaphor leftover (as-built census)

**Status:** Census of leftover 0.63 feudal language in code and living docs.  
**Not** architecture law. **Not** a rename until José locks a cut.  
**Date:** 2026-08-17.

Prefer engineering words in [glossary.md](../glossary.md) §2.  
Teaching map: [metaphor.md](metaphor.md).

---

## 1. Three registers — do not mix

| Register | Words | This leftover? |
|----------|--------|----------------|
| **0.63 feudal** | kingdom, citizen, household, pretender, peasants, oath, fealty, market day, DNA (as definition), steward, wall / tower, king / crown / decree (packaging as king), thumbs, corridor | **Yes.** Clean toward the glossary. |
| **Living Palm biology** | genome, phenotype, organism in PHILOSOPHY / Grove / composition | **No**, unless José says that register moves too. |
| **Intended places** | org / realm as recursive support; Grove crown | **No.** Different care. Keep. |

**Hand** is glossary law (capability walker). Do not treat it as feudal leftover.

**Assembly** / `Assembly*` / `palm.*.assembly` is **legacy package name**, not the feudal register. Same cleanup season is optional. It is a larger front.

---

## 2. Identifier families in `src/`

Sweep 2026-08-17. Concentrated in `palm.system.assembly` plus seed / doctor / observability.

**2026-08-17 identifier cuts:** inventory API + row ids + doctor / Assist labels; household types; place-book / residual-ledger → registry; then DNA / env → structure definition seed. `Assembly*` packages and the living-docs pass wait.

| Family | What code names today | Kind | Prefer |
|--------|------------------------|------|--------|
| **household** | **renamed** → module `structure_effects.py`; `StructureEffectPort`; `default_structure_effects`; row id `structure.effect_intents` | Public type + factory | Structure materialize / effect port |
| **kingdom** | **renamed** → `admission_inventory` / `admission_inventory_snapshot`; `role=admission_inventory` | Public inventory API | Admission inventory |
| **citizen** | **renamed** → `GATED_PATHS`; keys `gated_paths` / `gated_count` | Public constant + snapshot | Admitted paths |
| **pretender** | **renamed** → `READINESS_EDGES`; `open_residual_edges`; `paid_readiness_edges`; keys `readiness_edges` / `readiness_edge_count` | Public inventory API | Dual readiness / named residual |
| **DNA** | **renamed** → `resolve_builtin_definition`; `definition_id_*`; `structure_definition_id`; env `PALM_STRUCTURE_DEFINITION_ID`; ids `definition.seed` / `definition.refuse` | Public seed + env contract | Structure definition / seed |
| **oath** | **renamed** → `assist.published_admission`; `flows.published_admission`; `execution.product_facade_admission` | Inventory contract | Published admission on façades |
| **fealty** | **renamed** → `surface.host_port`; `surface.host_port_edge` | Inventory contract | Surface uses host / port, not kernel dig |
| **market day** | **renamed** → `host.packaging_start_continue*` | Inventory contract | Business start / continue doors |
| **tower** | **renamed** → `inventory.admission` | Inventory contract | Admission inventory (same map) |
| **king** | **renamed** → `host.outbox_composition_seed`; `inventory.exit_residual*` | Inventory contract | Seed / composition chooser |
| **place book / ledger** | **renamed** → `place_registry.py`; `InProcessPlaceRegistry`; `PlaceEffectPort`; `place_effect_port`; field `registry`; row ids `place_registry.*` / `inventory.exit_residual*` | Public type + inventory | Place registry |

**No identifier:** steward.  
**Comment / docstring only:** phenotype (on `BootMode` and definition shape), peasants, crown, decree, second wall.

`Assembly*` types: about 227 `src/` line hits. Packages: 9 files under `palm.core.assembly`, 16 under `palm.system.assembly`. Leave until José says the types move.

Inspect / MCP JSON already uses `admission`, `may_run_business`, `definition_id`. Tests lock the **inventory helpers**, not doctor copy.

---

## 3. Comments (cheap)

**2026-08-17:** comments and docstrings under `src/palm/` and `tests/` restated toward glossary words.

**2026-08-17 (later):** smallest identifier cut landed, then household types, then place-book / ledger → registry, then DNA / env → structure definition seed. Inventory tuple `id` / `law` / `intent` restated with the map above.

---

## 4. Operator-facing (small, public)

| Surface | String |
|---------|--------|
| CLI `doctor` | `Structure admission` · `gated paths` |
| Assist menu | `Admission is closed` |
| Packaging bag | copies `gated_count` / `readiness_edge_count` |

---

## 5. Living docs that still speak the feudal table

Architecture vault retired the words. These still teach them as law:

| Home | What it still says |
|------|--------------------|
| [VISION-ASSEMBLY.md](../../vision/VISION-ASSEMBLY.md) §4 + §6.4 | Citizen / household / pretender as **normative** terms |
| [PALM.md](../../PALM.md) (admission / household sentence) | Citizens, household, pretenders, market-day |
| [WRITING.md](../../WRITING.md) term list | Citizen, household, pretender, DNA |
| [ADR-032](../../adr/032-organism-assembly.md) | DNA, steward, household, pretenders, structure king |
| [STATUS.md](../../../STATUS.md) | DNA seed; fail-closed citizens |
| [TECH-DEBT.md](../../../TECH-DEBT.md) SD-020 | Dual readiness / pretenders |
| [MIGRATION-0.63.md](../../migrations/MIGRATION-0.63.md) + CHANGELOG 0.63 | Chronicle in feudal voice |

**Allowed teaching (leave unless a docs pass is named):**

- [PHILOSOPHY.md](../../../PHILOSOPHY.md) “On the kingdom”
- [VISION-0.63](../../vision/closed/VISION-0.63.md) (closed chronicle)
- [metaphor.md](metaphor.md) (this appendix)

Do not rewrite those in the same sitting as a code rename.

---

## 6. Suggested cuts (José locks)

| Cut | Scope |
|-----|--------|
| **Comments + inventory names** | `kingdom_*`, `GATED_CITIZENS`, `PRETENDER_*`, `HouseholdEffectPort` / `household.py`, inventory row ids, doctor / assist labels |
| **Household types** | **Locked 2026-08-17.** `HouseholdEffectPort` / `household.py` / `default_household_effects` → `StructureEffectPort` / `structure_effects.py` / `default_structure_effects`. No aliases. |
| **Place book / ledger** | **Locked 2026-08-17.** `PlaceBookEffectPort` / `place_book.py` / `InProcessPlaceBook` → `PlaceEffectPort` / `place_registry.py` / `InProcessPlaceRegistry`. Residual row `inventory.exit_residual*`. No aliases. |
| **DNA / env** | **Locked 2026-08-17.** `PALM_ASSEMBLY_DNA_ID` / `assembly_dna_id` / `resolve_builtin_dna` / `dna_id_*` / `dna.seed` → `PALM_STRUCTURE_DEFINITION_ID` / `structure_definition_id` / `resolve_builtin_definition` / `definition_id_*` / `definition.seed`. No aliases. |
| **Package / type rename** | `AssemblyDefinition`, `AssemblyEngine`, `palm.*.assembly` — own sitting |
| **Docs pass** | VISION-ASSEMBLY §4/§6.4, PALM, WRITING, ADR-032 — own sitting |
| **Biology register** | genome / phenotype in PHILOSOPHY — not this leftover |

Cleanup of this leftover does not close a theme by itself.
