# VISION 0.59 — System Boot + Composition Truth

**Status:** 📋 **Theme open** · plan **0.59.0** · inventory **0.59.1** ✅ · system log plan **0.59.1a** ✅  
**Inventory:** [BOOT-INVENTORY.md](BOOT-INVENTORY.md)  
**System log plan:** [SYSTEM-LOG.md](SYSTEM-LOG.md) (observation seat — not a second theme)  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [PALM.md](PALM.md) — read first.  
**ADR:** [028-system-boot.md](adr/028-system-boot.md) **Proposed**.  
**Debt root:** [SD-014](../TECH-DEBT.md#sd-014) · host residual [CF-002](../TECH-DEBT.md) · impact **BI-*** · system log [BI-015](../TECH-DEBT.md#bi-015).  
**Prior closed:** [VISION-0.58](VISION-0.58.md) session · [VISION-0.57](VISION-0.57.md) system · composition skeleton [ADR-019](adr/019-composition-profiles.md).  
**Queue (not this theme):** [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) · workload remainder · Grove.  
**North star:** [VISION-GROVE](VISION-GROVE.md).

---

## 1. Goal

Give Palm a **true boot schedule** and **truthful composition**.

Today, boot order lives in imperative soup:

- `ApplicationHost.start`
- `BaseRuntime.start`
- dual roots and capability ORs

**Session** and **system** are named.  
**Membership** (`CompositionProfile`) is declared but not always the only switch.  
**Modes** (safe, test, dev, prod) do not exist as first-class boot control.

**Success:**

- One **documented** host schedule + system schedule.  
- Code **walks a phase table** (stub first, then real handlers).  
- **CompositionProfile** is membership truth for services, surfaces, capabilities.  
- **Boot modes** declare phenotypes; tests boot **by mode**.  
- Breaks during migration **harvest isolation** (BI-*).  
- Spine (job path) stays honest; residual chrome is named, not pretended.  
- **System log** (when seats land) shows ordered boot story without reading source ([SYSTEM-LOG](SYSTEM-LOG.md)).

This theme is **not** surface compost.  
This theme is **not** a second plugin autoload framework.  
This theme is **schedule + membership + eager stubs + break/harvest**.  
**System log** is **observation** for that work — not a separate product theme.

---

## 2. Why now

1. **0.57** named the system. **0.58** named session. Boot is still implicit.  
2. **SD-014** was named on purpose mid-session work — **later** has arrived.  
3. Rest after 0.58 is complete. The next structural lever is **control of start**.  
4. Good boot unlocks **test by shape**, **safe mode**, **prod vs dev**, and **trim with confidence**.  
5. Palm is **pre-1.0**. We may break accidental assembly. We must not paper over debt.

---

## 3. Non-goals

| Out of scope for 0.59 | Why |
|-----------------------|-----|
| Full surface purge (explorer/MCP dual stack) | [VISION-SURFACE-DEFLATION](VISION-SURFACE-DEFLATION.md) |
| Shared plane-store framework | SI-014; separate |
| Grove multi-Palm mesh | Needs local control first |
| Full workload placement remainder | Only boot edges |
| One global middleware list | HTTP ≠ job hooks ≠ plane law |
| Second dynamic-import framework | Keep `INSTALLED_*` + autoload |
| Planes on install lists | Planes are system, not plugins |
| Fake-success “full chrome always green” mid-theme | Declared green bar only (§5) |

---

## 4. Principles

Bind to [PALM.md](PALM.md) and ADR-028.

1. **Plugins** — `INSTALLED_*` declare *what*; packages register **downward**.  
2. **Planes are not plugins** — system owns attach order.  
3. **Composition chooses membership** — not the kernel schedule.  
4. **One composition root walks a phase table** — no private boot via import side effects.  
5. **Two schedules, one story** — host schedule + system schedule.  
6. **Keep stacks separate** — surface filters ≠ job hooks ≠ plane law ≠ event consumers.  
7. **Stub seats first** — full shape early; migrate into stubs.  
8. **Break for truth** — no long dual-path comfort.  
9. **Break / harvest** — when assembly fails, grab the **rule**, re-home it, isolate (§5).  
10. **STE** for theme docs.

**Spirit:** Smaller honest Palm beats large Palm held by god-wire.

---

## 5. Break / harvest posture

Palm may **not** stay fully green on every mid-theme commit.  
That is allowed. Silence and permanent shims are not.

### 5.1 End of theme (exit bar)

| Expect | Meaning |
|--------|---------|
| **Spine works** | Definition → pattern → job → effects → events on declared modes |
| **Boot controllable** | Phase table + modes real; doctor/tests can report them |
| **Membership truthful** | Profile drives services / surfaces / capabilities on migrated path |
| **Not every legacy path forever** | Dual roots and import-order “features” may die or move |
| **Chrome residual named** | Heavy surfaces may stay residual → surface deflation |

### 5.2 Mid-theme green bar

| Track | Mid-theme | Exit |
|-------|-----------|------|
| Spine (`safe` / `test` + core job path) | Green (or recover same slice) | Green |
| Declared dogfood mode | May lag 1–2 slices | Green |
| Legacy host constructions | May fail; BI-* required | Migrated, deleted, or residual named |
| Heavy surfaces | May fail; harvest rules only | Not required fully green |

**Each slice** states which modes are in the green bar.

### 5.3 Break classes

| Class | Response |
|-------|----------|
| **Accidental dependency** | Harvest isolation; explicit phase; do not restore import-order magic |
| **Misplaced rule** | Move rule to true owner (system / product / registry); thin the caller |
| **True owner** | Keep ownership; declare it as phase or membership |
| **Out of theme** | Map and park (BI-* → later theme) |
| **Spine regression** | Fix in-theme — do not re-litigate wait/session law |

### 5.4 Isolation harvest questions

1. What **rule** was this code enforcing?  
2. Does that rule **belong here**?  
3. Was the behavior only **emergent**? Promote or drop.  
4. Prefer **smaller honest mode** over dual-path chrome.

---

## 6. Target shape

### 6.1 Three axes (do not merge)

| Axis | Question |
|------|----------|
| **CompositionProfile** | *What* is installed? |
| **DeploymentProfile** | *Where* / which roles? |
| **Boot schedule + mode** | *Order* and *strictness*? |

### 6.2 Two schedules (illustrative — names lock after inventory)

```text
HOST SCHEDULE (ApplicationHost)
  H1  kernel bootstrap
  H2  host event / recorder
  H3  spawn system instance(s)  ──►  SYSTEM SCHEDULE
  H4  load definitions
  H5  wire CQRS / product services
  H6  mount surfaces
  H7  projections / outbox (capabilities)
  H8  recover / drain / background

SYSTEM SCHEDULE (BaseRuntime)
  S1  ensure_core_plugins
  S2  engines / storage
  S3  ports open
  S4  planes attach (wait, session, workload, …)
  S5  job hooks install
  S6  orchestration start
  S7  bind / ready
```

### 6.3 Boot modes (eager stubs)

| Mode | Intent |
|------|--------|
| **safe** | Minimal truth; CI isolation; no surfaces; no background drain |
| **test** | Deterministic host; recover off by default |
| **dev** | Full local dogfood |
| **prod** | Strict operate; declared surfaces only |
| **cli / mcp / worker / server** | Map existing composition presets |

Modes are **presets over the axes**, not a fourth god-object.

### 6.4 Package home (confirm in ADR / early slices)

| Concern | Candidate |
|---------|-----------|
| System phase ids + protocol | `palm.system.boot` |
| Host phase handlers | `palm.app.host.boot` |
| Mode presets | next to CompositionProfile / DeploymentProfile |

System schedule **must not** import product or surfaces.

---

## 7. Stub policy

- Stubs **remind intent**.  
- Do not fake success that hides a missing phase.  
- Prefer “not migrated” report over silent dual path.  
- Temporary dual path only with **slice id + kill condition** on a BI row.  
- Plan as if full implementation exists; migrate Palm into the seats.

---

## 8. Ordered work

Slices stay **one purpose each**. Numbers lock at execution time after 0.59.1 inventory.

| Order | Slice spirit | Result |
|------:|--------------|--------|
| **0** | Plan + map + ADR | This file, ADR-028 Proposed, PALM boot section, STATUS, BI-* seed — ✅ |
| **1** | Inventory + characterization | [BOOT-INVENTORY.md](BOOT-INVENTORY.md); `tests/test_boot_inventory_0_59.py`; green bar — ✅ **0.59.1** |
| **1a** | System log basic | [SYSTEM-LOG.md](SYSTEM-LOG.md) · `palm.system.log` · host+system phase lines — ✅ **0.59.1a** |
| **2** | Stub schedule + modes | Phase ids, walker, mode registry; **reuse SystemLog** (do not invent a second narrative) |
| **3** | System schedule v1 | `BaseRuntime.start` walks table (+ system log phase lines) |
| **4** | Host schedule v1 | `ApplicationHost.start` walks table (+ host log phase lines) |
| **5** | Composition membership truth | Profile is the switch (+ skip reasons in system log) |
| **6** | Mode dogfood | `safe` + `test` green in CI (+ level defaults) |
| **7** | dev / prod / shape presets | cli/mcp/worker/server mapped |
| **8+** | Residual BI-* | Harvest isolation; fold dual roots only if cheap |
| **exit** | ADR Accepted · SD-014 closed or residual named · stamp · system log shipped or BI-015 residual |

---

## 9. Impact inventory (BI-*)

Live rows live in [TECH-DEBT.md](../TECH-DEBT.md) **BI-***.  
Seed at open. Grow when discovery finds tangles.

Each break row should note: **rule harvested?** · **true owner?** · **parked theme?**

---

## 10. Success criteria

- [ ] Documented host + system boot schedule.  
- [ ] Code walks a phase table.  
- [ ] At least two real modes dogfooded (`safe`/`test` + one full).  
- [ ] CompositionProfile membership truth on migrated path.  
- [ ] Plugins still INSTALLED_*; planes not install-list items.  
- [ ] BI-* honest; SD-014 closed or residual re-homed.  
- [ ] Spine green; declared modes green; chrome residual named.  
- [ ] ADR-028 Accepted at exit.  
- [ ] Tests boot Palm by mode without private host internals.  
- [ ] System log planned ([SYSTEM-LOG](SYSTEM-LOG.md)); seats or residual **BI-015**.

---

## 11. How to update this file

- Mark slices done with ✅ and patch id.  
- Adjust phase names after inventory (keep spirit).  
- Do not paste a second full map — link [PALM.md](PALM.md).  
- At exit: status closed, release/migration links, residual debt.

---

## 12. Related

| Doc | Role |
|-----|------|
| [SD-014](../TECH-DEBT.md#sd-014) | Debt root |
| [ADR-019](adr/019-composition-profiles.md) | Composition axis |
| [ADR-018](adr/018-application-host-decomposition.md) | Host decomposition |
| [ADR-026](adr/026-palm-system-layer.md) | System layer |
| [ADR-027](adr/027-session-plane.md) | Session plane (closed) |
| [SYSTEM-LOW-LEVEL](SYSTEM-LOW-LEVEL.md) | System package map |
| [VERSIONING](VERSIONING.md) | Theme rhythm |
