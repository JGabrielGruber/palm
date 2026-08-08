# ADR-032 — Organism assembly (DNA · admission · single readiness)

**Status:** Proposed  
**Date:** 2026-08-08  
**Theme:** [VISION-0.63](../vision/VISION-0.63.md) (**open** at `0.63.0`)  
**Seed law:** [VISION-ASSEMBLY](../vision/VISION-ASSEMBLY.md)  
**Map:** [PALM.md](../PALM.md)  
**Migration:** [MIGRATION-0.63](../migrations/MIGRATION-0.63.md)  
**Debt:** [SD-020](../../TECH-DEBT.md#sd-020) · [SD-021](../../TECH-DEBT.md#sd-021) · boy-scout [SD-016](../../TECH-DEBT.md#sd-016)  
**Related:** [ADR-026](026-palm-system-layer.md) · [ADR-028](028-system-boot.md) · [ADR-029](029-system-supervisor.md) · [ADR-030](030-system-vitality.md) · [ADR-031](031-multi-claimer-work-drain.md) · [ADR-019](019-composition-profiles.md)

---

## Context

1. Palm can **boot** a system and **run** business (flows, start, continue). Between them, structure readiness is still **glue**: profiles, host enrich, catalog load order, soft “definitions ready.”  
2. That glue multiplies when Palm scales past one process. The missing care is **organism ready** — named in [VISION-ASSEMBLY](../vision/VISION-ASSEMBLY.md).  
3. Prior seasons built the body: system layer, boot, supervisor, work/wait planes, vitality, capacity.  
4. **José** opened theme **0.63** to assemble Palm under one structure law: DNA, steward, admission gate, purge pretenders.  
5. Impact of fail-closed is **not fully known**. That is allowed. We raise the wall, measure breakage, admit citizens.  
6. Pre-1.0 may break ugly shapes. Theme exit is **José’s judgment** when readiness feels proper — not checklist theater.

---

## Decision

### D1 — Assembly is the structure reconciler

Between boot (machine lives) and business (jobs run), **assembly** owns desired structure:

| Piece | Duty |
|-------|------|
| **Assembly definition (DNA)** | Declarative desired structure |
| **Assembly engine** | Pure reconciler — no sockets, no OS spawn, no business jobs |
| **Assembly status** | Local readiness under the current definition |
| **System loop** | Load → tick → apply effect intents → observe → publish admission |
| **Admission** | Gate for business that needs ground |

Assembly is **not** a second job orchestrator.  
Orchestration, work plane claim law, and ExecutionPort subjects stay.

### D2 — One admission gate (fail closed)

| Law | Meaning |
|-----|---------|
| **Citizens** | Acts that need the organism whole — only through admission |
| **Household** | Assemble path and what makes assemble possible — not forced through business admission |
| **Pretenders** | Soft-ready, dual catalog, host digs for structure — **break** until obey or die |
| **Fail closed** | Admission down → citizen start refused |
| **No dual king** | Host soft flags and profiles are not peer readiness law after DNA load |

Staging builds wall order. Staging does **not** mean permanent side doors for CI green.

### D3 — DNA is structure king; seed is chooser

| Prefer | Avoid |
|--------|--------|
| Entry / mode / env choose **which DNA** (or authority pointer) | Profile + BootMode + DNA as three structure kings forever |
| After load, assembly status is structure + readiness truth | Env capability toggles that rewrite membership as peer law |
| Profiles map **into** DNA seed | Profiles remain public dual structure |

**Env (`PALM_*`):** packaging (storage, paths, ports, logs, pool widths, secrets) **stays**. Structure toggles **seed or die**.

### D4 — First DNA is embedded

Floor proves **`local.embedded`** (name may lock): thin body from today’s embedded composition (core services, no surfaces, no drain membership as structure).

| Later (growth) | Role |
|----------------|------|
| `local.cli` | `palm` dogfood |
| `local.server` | `palm host server` dogfood |
| worker / light center / authority-pulled | Not floor |

`safe` / `test` share embedded structure unless a real structure split appears.

### D5 — Package homes

| Layer | Preferred home |
|-------|----------------|
| Pure | `palm.core.assembly` |
| System loop, admission, effect port, handlers | `palm.system.assembly` |

Core purity: no imports outside `palm.core`.  
Clients take **admission** (and domain ports), never assembly control, never composition root as structure API.  
Structure effects use **assembly effect port** — not `ExecutionPort`.

### D6 — Coherence suite is a truth instrument

| Prefer | Avoid |
|--------|--------|
| Negative tests: citizen must **not** run when admission down | Suite that only asserts happy green |
| Red after gate = pretender map | Soft-flag green that preserves dual mode |
| Guards for purity and “no second admission king” | Corridor police as permanent architecture |
| Fix or delete wrong bypass tests | Green bar that encodes the old lie |

Goal: know if we deliver **single truth**. Not vanity CI.

### D7 — Full-in on the law; staged on the purge

We go **full-in**: after DNA load, assembly is structure king.  
We go **staged**: first embedded + one citizen door + coherence suite; then swallow pretenders; then fatter DNA.

We do **not** half-in dual readiness as the long-term design.

### D8 — Plan for the unplanned

Theme allocates **unplanned reserve** slices for break inventory and unknown impact.  
Unknown is not a defect. Inventing dual paths to avoid unknown **is**.

### D9 — Exit is José’s judgment

When single readiness holds on owned paths, pretenders are purged or kill-dated, coherence suite defends the gate, residual is honest, and José feels the home is proper — he accepts this ADR and closes the theme.

---

## Consequences

### Positive

- One named organ for organism ready.  
- Fail-closed maps dual mode instead of hiding it.  
- DNA path enables later authority, places, and Grove without host glue as king.  
- Env remains useful for packaging without dual structure.

### Negative / cost

- Many green paths will **break** when the gate rises — intentional.  
- Profile/boot/env demotion is migration work (SD-021).  
- Tests and CI dogfood need coherence rewrite, not soft skips.  
- Floor DNA is thin; dogfood DNA must grow before daily `palm` feels native.

### Risks if ignored

- Bolt-on engine with host still structure king wastes the season.  
- Fail-open dual hops become permanent “checkpoints.”  
- Green-washing the suite re-encodes the lie.

---

## Alternatives considered

| Alternative | Why not |
|-------------|---------|
| Soft dual path “for compatibility” forever | Half-in; pretenders as architecture |
| Profiles remain structure king; DNA is labels | Dual truth; assembly is decoration |
| Start with server DNA only | Proves surfaces, not the organ; larger unknown |
| Product CommandBus sets ready | Wrong layer; product must not own reassemble |
| Infinite corridor guards without one gate | Rot; VISION-ASSEMBLY §6.4 refuses this |
| Full Grove / light-center DNA on floor | Wrong rung; body first under embedded |

---

## Status notes

- **0.63.0** — plan + this ADR **Proposed** · debt **SD-020** / **SD-021** named.  
- **0.63.1** — `palm.core.assembly` pure engine + types + tests (embedded DNA factory).  
- **0.63.2** — `palm.system.assembly` seat + loop + phase; shell `admission`; embedded assemble on start.  
- **0.63.3** — work-plane citizen gate: `able` = started ∧ admission; fail closed; pretender inventory named.  
- **0.63.4** — coherence suite + `guard-assembly`; `DefinitionExecutor` submit paths fail closed (`AdmissionRefusedError`).  
- **0.63.5** — builtin DNA catalog + seed map (mode/composition → decree); host spawn injects seed.  
- **0.63.6** — refuse vs membership; dual shape blocks admission.  
- **0.63.7** — vitality `assembly` seat presents admission + DNA.  
- **0.63.8** — kingdom inventory (gated vs pretender) · packaging nests admission.  
- **0.63.9** — create_cli_host seeds BootMode.cli / local.cli DNA.  
- **0.63.10** — inspect present nests admission on top/vitality.  
- **0.63.11** — in-process place book effect hands (ensure/release).  
- **0.63.12** — deployment profile seeds DNA + composition (run_host / palm host server).  
- **0.63.13** — env DNA seed (`PALM_ASSEMBLY_DNA_ID`); membership always for refuse; drain DNA king; SD-021 partial.  
- Next: OS place spawn · intents · residual enable_* membership seeds (**0.63.14+**).  
- Accept + theme close when José judges readiness proper.
