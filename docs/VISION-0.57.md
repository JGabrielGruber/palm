# VISION 0.57 — Palm System (name the kernel)

**Status:** 🚧 **In progress** — system work **0.57.0–0.57.12** landed; residual SD-011 kits classification, surface SU-*, theme exit docs remain.  
**Language:** ASD-STE100 Simplified Technical English.  
**Map:** [PALM.md](PALM.md) — read first.  
**Low-level:** [SYSTEM-LOW-LEVEL.md](SYSTEM-LOW-LEVEL.md)  
**Debt (live):** [TECH-DEBT.md](../TECH-DEBT.md) · archive [audit/TECH-DEBT-ERA-0.45.md](audit/TECH-DEBT-ERA-0.45.md)  
**ADR:** [026-palm-system-layer.md](adr/026-palm-system-layer.md).  
**North star:** [VISION-GROVE](VISION-GROVE.md).  
**Prior scout:** [VISION-0.56](VISION-0.56.md) workload foundation (direction only; rewrites allowed).

---

## 1. Goal

Give Palm a **true system layer** that matches the whole organism.

The full picture of Palm lives in [PALM.md](PALM.md):

- what Palm is for,
- the **job path** (definition → pattern → job → effects → events),
- core machines, plugins, product, surfaces,
- ports and planes as **consequences** of that path,
- honest gaps.

This theme makes the **code** match that map for:

- the running machine (engines + planes),
- the **ports** that graphs and product must share,
- the line between **system** and **shared** code.

**Success:** [PALM.md](PALM.md) stays true. The tree follows it.  
New work has a home. Workarounds stop being the default path.

This theme is **not** “add REST for workloads.”  
This theme is **structure**.  
This theme is **not** only the dual-path pain — it is the kernel of the whole named Palm.

---

## 2. Why now

1. Workload work showed a **split brain**: graphs bind engines; edges bind services.  
2. `palm.common` holds **system** and **shared** at once. It grows without purpose.  
3. Session has no clean home.  
4. `PalmKernel` names infra. It does not name the effect surface of a running Palm.  
5. Palm is **not** in production. We may break and rewrite. We must not paper over debt.

0.56 gave **direction**. That is enough for a scout.  
0.57 takes the **rare chance** to name and clean the wiring.

---

## 3. Non-goals

| Out of scope for 0.57 | Why |
|-----------------------|-----|
| Full Grove multi-Palm mesh | Later; needs local system first |
| Full session product UI | Session **home** yes; full plane theme later |
| Feature race for every workload runtime | Structure first; runners follow ports |
| Keep all old paths for compatibility | Pre-1.0; truth over comfort |
| Rewrite every legacy doc to STE in one pass | New + touched docs only |

---

## 4. Principles (bind to PALM.md)

See [PALM.md §5](PALM.md) for the full law list. Short form:

1. One purpose per module.  
2. Core stays pure.  
3. Register downward.  
4. Effects use **named ports**.  
5. Planes are **system**.  
6. Product is **userland**.  
7. Surfaces stay thin.  
8. Shared is not a dump.  
9. Same ports for graphs and product.  
10. Break for truth; record residual debt.

**Documentation:** All new theme text uses **Simplified Technical English**.

---

## 5. Target shape (high level)

```text
Surfaces  →  Product (services)  →  ports  →  System  →  Core
                ↑                              │
             Plugins register ─────────────────┘
Shared = libraries only (not system)
App host = boot and composition (not a second kernel API)
```

| Piece | Target |
|-------|--------|
| **System instance** | One object (or clear façade) that holds engines and exposes ports |
| **Execution port** | First port: resource + workload effects (and related job bind as needed) |
| **Planes** | Event, work, wait stay system-owned; session gets a seat |
| **Shared** | What remains after system leaves `common` |
| **Product** | Calls ports on a resolved system instance |
| **Patterns** | Build against ports, not engine bags |

Package path is **`palm.system`** (landed). Residual modules and shims are debt, not an open naming debate.  
The purpose is fixed here. The path is not holy.

---

## 6. Ordered work (high level)

Slices stay **one purpose each**. Numbers lock at execution time.

| Order | Slice spirit | Result |
|------:|--------------|--------|
| **0** | Plan + map + ADR | [PALM.md](PALM.md), this file, ADR-026 — ✅ |
| **1** | Debt archive + low-level | Live SD register; era archive; [SYSTEM-LOW-LEVEL](SYSTEM-LOW-LEVEL.md) — ✅ **0.57.1** |
| **2** | Name the system boundary in code | `palm.system` package; system vs shared visible — ✅ **0.57.2** |
| **3** | Execution port v1 | Named interface on BaseRuntime — ✅ type+impl |
| **4** | Rebind graphs | P2 invoker/driver + port bridges — ✅ **0.57.4** |
| **5** | Rebind product | Effect methods on port — ✅ (list/doctor residual) |
| **6** | Deflate shared | BaseRuntime + planes under `palm.system`; SD-012 shims — ✅ **0.57.6** |
| **7** | Edge policy | No new engine shortcuts; list residual bypass as debt — ✅ **0.57.7** |
| **8+** | Debt cleanup | Import sweep, catalog truth, docs, wave F, shim delete — ✅ **0.57.8–12** |
| **exit** | Theme exit | Residual debt honest; ADR-026 Accepted; workload/session grow **on** the map |

**Rule:** Do not ship more dual-path policy (e.g. “workload only through CQRS”) as the main fix.

---

## 7. Relation to 0.56 and Grove

| Theme | Role |
|-------|------|
| **0.55** | Law of start / continue — keep |
| **0.56** | Workload **scout** — engine + leaf direction; may rewrite bindings |
| **0.57** | **System name and wiring** — main goal |
| **Session plane** | After system home exists ([VISION-SESSION-PLANE](VISION-SESSION-PLANE.md)) |
| **Grove** | Still the multi-Palm north star; local system is the floor |

---

## 8. Debt

| Register | Role |
|----------|------|
| [TECH-DEBT.md](../TECH-DEBT.md) | **Live** — SD-* system debt + CF-* carry-forward |
| [docs/audit/TECH-DEBT-ERA-0.45.md](audit/TECH-DEBT-ERA-0.45.md) | **Archive** — PD era history |

Add SD rows for shims and new bypasses. Do not reopen closed PD IDs without new evidence.

---

## 9. Risks

| Risk | Mitigation |
|------|------------|
| Theme too large | Hard slice order; one purpose per patch |
| Rename theater without ports | Port rebind is load-bearing; names alone fail review |
| `common` move thrash | Move by **purpose**, not by fashion |
| Context loss mid-theme | PALM.md is the short memory; keep it true |

---

## 10. Exit criteria

Theme **0.57** may close when:

1. [PALM.md](PALM.md) matches the code at layer purpose level.  
2. A **named execution port** exists. Graphs and product use it for resource and workload effects.  
3. System vs shared is **visible** (package and/or guard).  
4. New debt register exists; old era is archived.  
5. No new dual-path “special case” for the next capability.  
6. `just check` stays green on the path we touch.

---

## 11. Review and next

High-level map and spine are in use.  
**Next:** optional SD-011 multi-kit home (or classify in place); surface SU-* later;
theme exit as **docs + version dump** (slices stay separate commits). Session = **theme**, not residual.

---

## 12. Patch log

| Patch | What |
|-------|------|
| **0.57.0** | Plan + [PALM.md](PALM.md) + ADR-026 (map era) |
| **0.57.1** | Archive PD-era debt; live SD register; [SYSTEM-LOW-LEVEL](SYSTEM-LOW-LEVEL.md); AGENTS slim |
| **0.57.2–5** | `palm.system` boundary; ExecutionPort; product/graph rebind (P2) |
| **0.57.6** | Deflate: BaseRuntime + wait/work/workload → `palm.system`; SD-012 shims; `ensure_core_plugins` |
| **0.57.7** | Edge policy: `resume_job` on port; rebind SD-005 effect samples; no-shortcut law in AGENTS/PALM |
| **0.57.8** | SD-012 import sweep — src/tests import system |
| **0.57.9** | Capability catalog truth — INSTALLED_* vs INTENTION_* |
| **0.57.10** | Living docs/notes match code (kill pre-system dead notes) |
| **0.57.11** | Wave F: executions + job_hooks → system; `list_jobs` on ExecutionPort; SD-012 shims |
| **0.57.12** | Delete SD-012 shims; workload catalog on port; RuntimeHost = submit + execution |

---

*First name the tree. Then grow the branch.*
