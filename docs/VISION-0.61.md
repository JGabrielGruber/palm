# VISION 0.61 — Living-kernel vitality

**Status:** 📋 **Open** — plan **0.61.0** ✅ · seat walk **0.61.1** landed · projection **0.61.2** landed (stamps when José exits slices).  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [PALM.md](PALM.md) — read first.  
**ADR:** [030-system-vitality.md](adr/030-system-vitality.md) **Proposed**.  
**Seed:** [VISION-VITALITY](VISION-VITALITY.md) (opened as this theme).  
**Theme law:** [VERSIONING.md](VERSIONING.md) (floor · growth · exit judgment) · [AGENTS.md](../AGENTS.md) §6b.  
**Prior closed:** [VISION-0.60](VISION-0.60.md) supervisor + work plane · [VISION-0.59](VISION-0.59.md) boot · [VISION-0.58](VISION-0.58.md) session.  
**Debt:** Theme pay [SD-007](../TECH-DEBT.md#sd-007) · [CS-002](../TECH-DEBT.md#cs-002) · [OD-001](../TECH-DEBT.md#od-001) · [BI-015](../TECH-DEBT.md#bi-015).  
**Mid-theme residual (named for refactor):** [SD-015](../TECH-DEBT.md#sd-015) plane install menu · [CS-006](../TECH-DEBT.md#cs-006) supervisor wire · [CS-007](../TECH-DEBT.md#cs-007) adapter lineage residue · [CS-008](../TECH-DEBT.md#cs-008) runtime closures.  
**Queue later:** [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) · residual BI / SI / SU · Grove.  
**North star:** [VISION-GROVE](VISION-GROVE.md).

---

## 1. Goal

Give Palm **first-class eyes on the living process**.

Vitality is **system-intrinsic physiology**: load, seats, emissions, and bulk of what is attached.  
It is Palm’s living **`top`** — not a doctor bolt-on, not host status folklore.

| Piece | Role |
|-------|------|
| **Seat discovery** | Walk the live `SystemInstance` after start |
| **Seat report** | Versioned fragment each attached seat can emit |
| **Projection** | Read-only fold: discover → sample → window → snapshot |
| **Registry** | Named observe/tool capabilities that grow over time |
| **Inspect** | Product door that **presents** vitality (and other operate APIs) |
| **Doctor** | Legacy diagnosis verb/report — **debt**, not the kernel home |

**Host** stays packaging.  
**Planes** still carry start/continue.  
**Supervisor** still runs continuous loops.  
**Vitality only observes.**

### 1.1 Ambition and floor

| Concept | Meaning |
|---------|---------|
| **Floor** | Eyes open: dynamic walk, seat reports, projection + registry, inspect present, emission identity, doctor marked debt |
| **Growth line** | Theme may grow while José keeps it open — native reports, host status compost, optional caps, real tools |
| **Exit** | **José’s** judgment when eyes are proper and residual is honest — not empty checklist death |

Do not kill ambition to satisfy dead process notes.  
Do not ship permanent workarounds to stay “thin.”  
Break what is ugly. Pay debt when feasible. Name the rest.  
**Who decides:** José Gabriel Gruber — [VERSIONING.md](VERSIONING.md) *Who decides*.

### 1.2 Success (theme intent)

- A started system can answer: what seats are attached, what load they report, what emissions say, what is absent.  
- Truth lives in **system vitality**. Product only presents.  
- Doctor and host triple-status do **not** invent living counters as law.  
- Residual entropy is named. Spine stays green on declared modes.

This theme is **not** full surface compost.  
This theme is **not** Grove mesh.  
This theme is **not** silent Design mutation.

---

## 2. Why now

1. **Structure is live** (0.57–0.60): system, session, boot, supervisor, work plane, system log.  
2. Palm can answer **anatomy** questions. It cannot yet answer **physiology** with first-class honesty.  
3. Further growth without eyes is **blind** — tests stay green while heat and bulk compound.  
4. Product `SystemService` collides with the system layer (**SD-007**).  
5. Host `event_plane` / `ops` / `control_plane` status and doctor assembly are a **triple + diagnosis** mess (**CS-002**, **OD-001**).  
6. Surface deflation and residual BI need **evidence** of heat, not folklore.

**Thesis:** Stop working Palm only by intent and CI. Add proper eyes.

---

## 3. Non-goals (subject of other seeds — not forever bans)

| Out of this theme’s *subject* | Relation |
|-------------------------------|----------|
| Full surface purge (SU-*) | [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) — break only if it blocks eyes |
| Grove multi-Palm mesh | Needs eyes first; monitor-as-peer may rehearse later |
| Genome / full AST “own GC” | Later dogfood; never blend with living load score |
| Silent Design rewrite from vitals | Forbidden always (consent) |
| OTel product as Palm truth | Optional bridge later; not lineage law |
| User plane / impersonation | Separate seed |

**Forbidden always (layer law):**

- Vitality as a **plane** that starts or continues work.  
- Second write path for the same fact “for metrics only.”  
- Shame scores that auto-condemn large modules.  
- Fake green for absent seats.  
- Hardcoded vital menus that ignore composition / membership.  
- Workaround architecture as the path of record.

---

## 4. Principles

Bind to [PALM.md](PALM.md), [ADR-029](adr/029-system-supervisor.md), [ADR-028](adr/028-system-boot.md), and ADR-030.

1. **Vitality is system observation** — not product truth, not a plane of law.  
2. **Dynamic seat discovery** on the live instance; protocol is stable; menus are not hardcoded.  
3. **One fold** — seat report / emissions → projection → present.  
4. **Registry grows eyes** — same spirit as plugins; intention vs installed when experimental.  
5. **Proper lexicon** — vitality owns physiology terms; doctor does not define them.  
6. **Inspect presents** — rename product door (**SD-007**).  
7. **Break ugly** — dual status trees and doctor counter invention are debt; pay or name.  
8. **Emission identity** — partition by declared `actor_kind` or explicit `unknown`.  
9. **Modes gate cost** — `safe` / `test` stay cheap.  
10. **Visibility ≠ guilt** — show bulk and load; do not auto-condemn size.  
11. **STE** for theme docs.  
12. **Theme exit is José’s judgment** when eyes are proper.

**Spirit:** Proper self-knowledge beats a clever dashboard glued outside the kernel.

---

## 5. Lexicon

| Term | Meaning | Home |
|------|---------|------|
| **Vitality** | Living physiology of this process | `palm.system.vitality` |
| **Seat** | Attached piece on this instance | Discovered on instance |
| **Seat report** | Versioned self-report fragment | Protocol |
| **Projection** | Read-only snapshot fold | System |
| **Capability** | Named observe/tool in the registry | VitalityRegistry |
| **Top** | Living load view (summary + seats) | Present shape |
| **Inspect** | Product operate API door | `InspectService` |
| **Doctor** | Legacy diagnosis verb/report | Product; **debt** |
| **Emission identity** | Who caused the signal | Envelope on aggregates |

**Rule:** New system contracts speak **vitality / seat report / projection / top / inspect**.  
Do not invent more `doctor_*` as the system API.

### 5.1 Doctor debt

| Observation | Stance |
|-------------|--------|
| `build_doctor_report` invents health outside vitality | **OD-001** — not foundation |
| Plane `doctor_snapshot` | Transitional; migrate to seat report; retire dual names |
| Assist/MCP `doctor` alias | May keep the **verb**; body must **read** vitality |
| Host triple status | **CS-002** — do not grow; thin, delegate, or delete |

---

## 6. Target shape

### 6.1 Layers

```text
  PRODUCT — InspectService
    top · vitality snapshot · list/cancel · (legacy doctor → reads vitality)
            │ reads
  SYSTEM — palm.system.vitality
    VitalityProjection
    VitalityRegistry
    SeatReport protocol + discover walk
            │
  LIVING SEATS (discovered)
    planes · supervisor services · ports · system log · membership
```

### 6.2 Dynamic discovery

Seats are **not** a static product menu of packages.

| Layer | Static | Dynamic |
|-------|--------|---------|
| Report protocol / field names | Versioned contract | — |
| Capability registry ids | Intentional catalog | Enable by composition / mode |
| What is attached this process | — | Discover on live instance |
| Absent seat / capability | — | `absent` / `skipped` — never fake green |

```text
Composition + boot membership
        │
        ▼
Live SystemInstance graph
        │
        ▼
seat_walk → seat reports
        │
        ▼
VitalityProjection snapshot (lineage)
```

**Not dynamic:** filesystem package scan as physiology; heap scrape; always-green hardcoded service names.

**System planes:**  
:class:`~palm.system.planes.hub.SystemPlanes` — living seat that **consumes** members via ``put`` / ``install`` / ``get`` / ``detach`` / ``status`` (same shape as supervisor).  
Hub owns install policy (construct · wire collaborators · put). Boot schedule only seats the hub and calls ``install``. Runtime ``wait_plane`` / ``session_plane`` / ``work_plane`` **read from the hub**. Vitality probes ``planes`` and expands members from the live hub.

**Other discovery seeds:**  
`supervisor` (+ registered services), `execution` port, system log, boot last_walk / membership.  
New seats appear by **being attached** (or registered on supervisor).

### 6.3 Seat report (vitality-owned)

| Field | Meaning |
|-------|---------|
| `schema` | **`palm.seat_report/1`** (locked 0.61.1) |
| `seat_id` | Stable id for this attachment |
| `kind` | plane · supervisor · supervisor_service · port · log · boot · engine · other |
| `present` | bool |
| `state` | ok · degraded · absent · error · skipped |
| `load` | optional (usually empty in system — product interprets raw) |
| `notes` | short strings |
| `lineage` | `sampled` (normal) · `native` (legacy `adapter` coerced to sampled) |
| `meta` | `sample_source` + **`raw`** (uninterpreted public payload) |
| `sample_ts` | optional ISO sample time |

**Package (locked):** `palm.system.vitality`  
**Types:** `SeatReport` · `SeatReportable` · `SeatProbe` · `ProbeCatalog`  
**Walk:** `discover_seats` / `seat_walk` / `walk_result`  
**Plane seeds:** hub seat `planes` + members expanded from live :class:`SystemPlanes`  
**Other seeds:** `supervisor` · `execution` · `system_log` · `boot_membership`  
**Dynamic expansion:** plane members from hub · `supervisor.<service_name>` from registry

**Sample law (system vitality):** raw-dog the live system — call public methods / read public attrs; stash in `meta.raw` (`lineage: sampled`). Structural fields only (id, kind, present, state). **No adapter maps** in system. **Product present** interprets raw.  
Do **not** put vitality `seat_report` on simple seats — public API is enough.  
`lineage: native` = seat truly owns `seat_report()` (optional, when truth is internal).

### 6.4 Capability catalog (registry)

| Id | Role | Maturity (0.61.2) |
|----|------|-------------------|
| `seat_walk` | Discover + fold seat reports | **installed** · enabled |
| `emission_window` | Recent yield / wait heat / fail + actor partition | intention stub |
| `boot_membership` | Last walk / membership context | intention stub |
| `system_log_tail` | Operate tape sample (BI-015 neighbor) | intention stub |
| `process_resources` | RSS/CPU/threads (stdlib) | intention stub |
| `loaded_bulk` | Light size of attached seats/modules — visibility not shame | intention stub |
| `benchmark` / `monitor_agent` | Grow when ready | intention stubs |

**Locked (0.61.2):** `VitalityRegistry` · `VitalityCapability` · `CapabilityFragment` · `VitalityProjection` · snapshot schema **`palm.vitality_snapshot/1`**  
**API:** `project` / `project_top` / `project_seat_walk_only`  
Projection: iterate **enabled** capabilities → fragment → merge → snapshot with `capability_id` + seat lineage.  
Projection **receives** seat reports; it does not re-curate load fields.

### 6.5 Emission identity

`human` · `agent` · `probe` · `system` · `peer` · **`unknown`**

Prefer declared session/assist metadata. Do not guess bots from timing alone.

### 6.6 Package homes

| Concern | Home |
|---------|------|
| Vitality projection + registry | `palm.system.vitality` |
| Seat report protocol | same (types / helpers) |
| Product present door | `palm.services.inspect` (`InspectService`) |
| Continuous loop protocol | `palm.system.supervisor` (`SystemService` = loop contract — different concept) |
| Doctor report assembly | Legacy under kits/product — **consumer or compost** |

System vitality must not import product or surfaces.

---

## 7. Ordered work (guide — not a coffin)

Slices stay **one purpose each**. Numbers may merge, split, or extend.  
Theme stays open while José still needs proper eyes.

| Order | Slice spirit | Result |
|------:|--------------|--------|
| **0** | Plan + map + ADR | This file · ADR-030 Proposed · STATUS · debt rows · seed open — ✅ **0.61.0** |
| **1** | Seat report + dynamic walk | Protocol + discover; honest absent; adapters residue — **landed** — stamp when José exits |
| **2** | Projection + registry (`seat_walk`) | Snapshot with lineage; `project` / `project_top` — **landed** — stamp when José exits |
| **3** | Emission window + actor envelope | Partition or unknown; no second write path |
| **4** | InspectService rename | SD-007; host/assist/MCP doors; product SystemService not law |
| **5+** | Growth | Native reports; optional caps; host status compost; doctor thin; tools |
| **exit** | ADR Accepted · residual named · stamp · migration if needed | When **José** judges eyes proper |

---

## 8. Debt this theme pays or names

| Debt | Theme action |
|------|--------------|
| **SD-007** | Pay — product Inspect rename (unpaid) |
| **CS-002** | Pay down — host triple status not living truth (unpaid) |
| **OD-001** | Name + demote doctor as kernel eyes (system home landed; product still doctor) |
| **BI-015** | Use log as sample; deeper catalog may grow under vitality |
| Seat dual APIs | Prefer public API raw sample; native `seat_report` only when internal truth needs it |
| Host control_plane as law | Break for living load; bridge only temporary |

### 8.1 Residual from 0.61 plane / eyes cuts (refactor backlog)

Named so boy-scout and later slices do not pretend hub install is finished.

| Debt | What left | Refactor toward |
|------|-----------|-----------------|
| **[SD-015](../TECH-DEBT.md#sd-015)** | ~~open-coded install~~ → **paid** | `PlaneDefinition` at edge; hub walks catalog |
| **[CS-006](../TECH-DEBT.md#cs-006)** | ~~schedule prose~~ → **paid** | `ContinuousServiceDefinition`; `sup.install` |
| **[CS-007](../TECH-DEBT.md#cs-007)** | ~~adapter lineage~~ → **paid** | coerce → sampled; no `adapter_count` |
| **[CS-008](../TECH-DEBT.md#cs-008)** | ~~runtime closures~~ → **paid** | `SystemWire` + `InstallContext.from_wire` |

**Landed (not debt):** hub membership; collaborator `attach` (no full runtime on plane); schedule thin `install` call; vitality package + raw sample + projection + `seat_walk` capability; adapters deleted as maps.

**Not the subject:** full SU-* deflation, SI surface residue, BI-003 dual root — name residual; break only if they poison discovery.

**Rule:** If vitality needs a permanent workaround, **break the shape** or **open a debt row**. Do not ship the workaround as architecture.

---

## 9. Mid-theme green bar

| Track | Mid-theme | Floor / exit |
|-------|-----------|--------------|
| Spine (`safe` / `test` + job path) | Green (or recover same slice) | Green |
| Seat walk on lean phenotype | After slice 1 | Honest absent |
| Projection present | After slice 2 | Lineage visible |
| Emission window | After slice 3 | unknown explicit |
| Inspect rename | After slice 4 | No dual product name as law |
| Host status delete | May lag | Done or residual named |
| Heavy surfaces | May fail; harvest only | Not full green required |

Each slice states which modes are in the green bar.

---

## 10. Success criteria (floor)

- [x] Dynamic seat discovery on a live `SystemInstance`.  
- [x] Seat report protocol with vitality lexicon.  
- [x] `VitalityProjection` + registry; `seat_walk` installed (emission_window intention until 0.61.3).  
- [ ] Product inspect presents top/vitality from projection only.  
- [ ] `actor_kind` partition or explicit `unknown`.  
- [ ] InspectService rename path closed or alias residual named (SD-007).  
- [ ] Doctor marked debt; new truth not invented in doctor assembly.  
- [ ] Ugly dual paths broken or named — no silent workaround architecture.  
- [ ] PALM names vitality as system observation.  
- [ ] ADR-030 Accepted at exit.  
- [ ] Spine green on declared modes.

Growth beyond this floor may continue under **0.61** until exit.

---

## 11. How to update this file

- Mark slices done with ✅ and patch id.  
- Lock package paths and schema versions as they land.  
- Do not paste a second full map — link [PALM.md](PALM.md).  
- At exit: status closed, release/migration links, residual debt.

---

## 12. Related

| Doc | Role |
|-----|------|
| [PALM.md](PALM.md) | System map |
| [ADR-030](adr/030-system-vitality.md) | Vitality decisions |
| [VISION-VITALITY](VISION-VITALITY.md) | Queue seed (opened) |
| [ADR-029](adr/029-system-supervisor.md) | Supervisor + work plane |
| [ADR-028](adr/028-system-boot.md) | Boot · membership honesty |
| [SYSTEM-LOG](SYSTEM-LOG.md) | Process narrative |
| [TECH-DEBT.md](../TECH-DEBT.md) | SD-007 · CS-002 · OD-001 · BI-015 |
| [STATUS.md](../STATUS.md) | Active theme |
| [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) | Later surface compost |
| [VISION-GROVE](VISION-GROVE.md) | Horizon |

---

## 13. Spirit

> Vitality is Palm’s living self-knowledge — proper system eyes, dynamic seats, registry growth. Inspect presents. Doctor is leftover anatomy packaging, marked debt. Do not keep dual truth to stay thin. Break what is ugly. Pay what is feasible. Name the rest. Ambition outranks empty theme-kill notes. Dream waits for tool, but the theme may grow until the tool is real.

---

*Open the eyes. Then growth is not blind.*
