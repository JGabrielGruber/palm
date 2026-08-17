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

| Family | What code names today | Kind | Prefer |
|--------|------------------------|------|--------|
| **household** | module `household.py`; `HouseholdEffectPort`; `default_household_effects`; inventory id `household.structure_intents` | Public type + factory | Structure materialize / effect port |
| **kingdom** | `kingdom_map`; `kingdom_snapshot`; map `role=assembly_kingdom_inventory`; ids `kingdom.*` | Public inventory API | Admission inventory |
| **citizen** | `GATED_CITIZENS`; keys `gated_citizens` / `gated_count` | Public constant + snapshot | Admitted clients |
| **pretender** | `PRETENDER_EDGES`; `open_pretender_edges`; `paid_pretender_edges`; keys `pretender_edges` / `pretender_count` | Public inventory API | Dual readiness / named residual |
| **DNA** | `resolve_builtin_dna`; `dna_id_*`; `assembly_dna_id`; env `PALM_ASSEMBLY_DNA_ID`; ids `dna.seed` / `dna.refuse` | Public seed + env contract | Structure definition / seed |
| **oath** | ids `assist.admission_oath`; `flows.admission_oath`; `execution.product_facade_oath` | Inventory contract | Published admission on façades |
| **fealty** | ids `surface.fealty`; `surface.fealty_edge` | Inventory contract | Surface uses host / port, not kernel dig |
| **market day** | ids `host.packaging_market_day*` | Inventory contract | Business start / continue doors |
| **tower** | id `inventory.tower` | Inventory contract | Admission inventory (same map) |
| **king** | id `host.outbox_composition_king` | Inventory contract | Seed / composition chooser |

**No identifier:** steward.  
**Comment / docstring only:** phenotype (on `BootMode` and definition shape), peasants, crown, decree, second wall.

`Assembly*` types: about 227 `src/` line hits. Packages: 9 files under `palm.core.assembly`, 16 under `palm.system.assembly`. Leave until José says the types move.

Inspect / MCP JSON already uses `admission`, `may_run_business`, `definition_id`. Tests lock the **inventory helpers**, not doctor copy.

---

## 3. Comments (cheap)

**2026-08-17:** comments and docstrings under `src/palm/` and `tests/` restated toward glossary words. Identifiers unchanged.

Inventory **tuple data** (`GATED_CITIZENS` / `PRETENDER_EDGES` `id` / `law` / `intent`) still speaks feudal. That is the identifier sitting.

---

## 4. Operator-facing (small, public)

| Surface | String |
|---------|--------|
| CLI `doctor` | `Assembly (organism admission)` · `gated citizens` |
| Assist menu | `Organism admission is closed` |
| Packaging bag | copies `gated_count` / `pretender_count` |

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
| **Comments + inventory only; household types wait** | Same, but leave `HouseholdEffectPort` with `Assembly*` |
| **DNA / env** | `PALM_ASSEMBLY_DNA_ID`, `assembly_dna_id`, `resolve_builtin_dna` — public seed; own sitting |
| **Package / type rename** | `AssemblyDefinition`, `AssemblyEngine`, `palm.*.assembly` — own sitting |
| **Docs pass** | VISION-ASSEMBLY §4/§6.4, PALM, WRITING, ADR-032 — own sitting |
| **Biology register** | genome / phenotype in PHILOSOPHY — not this leftover |

Cleanup of this leftover does not close a theme by itself.
