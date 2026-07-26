# VISION 0.54 — Hermetic Jobs (definition-driven work)

**Status:** 🟢 **Landed (0.54.0–0.54.8)** — purpose-test theme closed. Prior library-product experiment discarded; docs domain → 0.55.  
**ADR:** [023-hermetic-jobs.md](adr/023-hermetic-jobs.md) (supersedes library-pipeline framing).  
**Depends on:** [VISION-0.53](VISION-0.53.md) Sovereign Runners (**landed**).  
**Sequel:** [VISION-0.55](VISION-0.55.md) — optional **docs dogfood domain** (Living Library as a Palm business process).

> *Does Palm fulfill its purpose?*  
> Business graphs are **definitions**. Foreign code and toolchains run in **NeonRoot** (tmpfs workspaces).  
> Palm does not `import` customer generators. Docs is a **later optional pack**, not the theme center.

---

## Why replan

The first 0.54 pass grew `common.library`, a domain `library` provider, and DocsService too early. That:

- thickened **common** with product DNA  
- mixed **platform** with **dogfood domain**  
- under-tested the real gap: **DAG / multi-step resource graphs** and **payload → runner**  

0.53 already gave honest hands (`neonroot` spawn, seed/exclude/output, images).  
0.54 must prove Palm can **orchestrate work** with those hands — not invent a docs CMS.

---

## True intent (purpose test)

| Claim | Proof in 0.54 |
|-------|----------------|
| Rules are definitions | At least one multi-step **flow/process** (resource graph) for hermetic work |
| No arbitrary code in engine | Heavy steps = **neonroot** only |
| Simple steps stay light | Pure Palm resources/transforms without isolation |
| Core stays general | No Living Library product in `common` |
| Optional domains later | DocsService / corpora → **0.55** |

Living Library **SOURCE/BUILD** from 0.52 (`docs/wiki`, `just docs-build`, palm-docs CSS) remains tooling.  
It is **not** the 0.54 platform feature set.

---

## Concepts

### A. Palm graph (business process)

Wizard resource chains today; **real `dag` pattern** is the growth target (currently a placeholder).

Nodes = resource invokes. Edges = order/deps. State = instance/job.

### B. Hermetic job (NeonRoot)

| NeonRoot | Role |
|----------|------|
| **Image** | Toolchain |
| **Workspace (tmpfs)** | Fast disposable work tree (seed → RAM → run → reap) |
| **Vault** | Images + optional committed workspaces |
| **spawn** | One-shot job; `--output` promotes artifacts |
| **bind** (planned) | Palm-owned host dir as live work tree — less copy when needed |

Palm stores **handles + status** in job state; not workspace trees in the engine.

### C. Two produce modes

| Mode | When |
|------|------|
| **In-process Palm** | kv, file, transforms, rest — no foreign runtime |
| **Hermetic** | Python/Node/DB tools — **only** via neonroot |

### D. Payload (later slices; don’t overbuild 0.54.0)

“Run this module/project” = payload **reference** (git-archive, path policy, later artifact id) → materialize/seed → neonroot.  
Security: allowlists, no free `eval`. Not the first slice.

### E. Palm-owned run layout (optional, when bind exists)

```text
{data_dir}/palm/hermetic/runs/{run_id}/
  payload/ | input/ | output/ | meta.json
```

Palm stages; NeonRoot bind/seeds; outputs explicit. Vault stays images + rare commits.

---

## Slice sequence

| Patch | Scope |
|-------|--------|
| **0.54.0** ✅ | Replan + ADR-023 rewrite; discard library/DocsService implementation |
| **0.54.1** ✅ | Hermetic job contract (`neonroot.contract`, [HERMETIC-JOBS.md](HERMETIC-JOBS.md)) + tests |
| **0.54.2** ✅ | Dogfood flow `hermetic-job-smoke` (neonroot only: preflight → spawn true) |
| **0.54.3** ✅ | **DAG pattern v0** — resource nodes, depends_on / implicit chain, one node per tick |
| **0.54.4** ✅ | DAG fan-out dogfood: `hermetic-job-fanout` (preflight → A‖B → join) |
| **0.54.5** ✅ | NeonRoot 0.2 `seed_mode` in contract + [HERMETIC-RUN-DIR.md](HERMETIC-RUN-DIR.md); `docs-css-bind` recipe |
| **0.54.6** ✅ | Second dogfood: `hermetic-ci-slice` (ruff → guard_core, neonroot only) |
| **0.54.7** ✅ | DEVELOPMENT + AGENTS purpose-test notes; Living Library product → 0.55 |
| **0.54.8** ✅ | Polish for 0.55: DAG `drain_ready`, `create_run_dir`, Assist discover starters |

---

## Explicit non-goals (0.54)

- DocsService / `services/docs`  
- `common.library` product store  
- `library` provider  
- Multi-corpus docs CMS  
- Whole-tree sync as product default  
- Implementing postgres adapters (horizon only)

---

## Horizon

| Theme | Content |
|-------|---------|
| **0.55** | Optional **docs dogfood domain** — Living Library as business process on hermetic jobs + kv; DocsService optional composition |
| **Assist “run code”** | Operator picks **image**, supplies **payload/code**, Palm stages + **neonroot.spawn**, returns stdout/artifacts — complex flow on this theme’s grammar (payload allowlists, not `exec` in-engine) |
| **Later** | Payload artifact registry; true parallel ready-set; adapter runners (PD-022); NeonRoot bind-mode + Palm run-dir |

---

## Exit criteria

- Prior docs-product 0.54 code **gone**; suite green  
- Written contract for hermetic job nodes  
- At least one **definition-only** multi-step hermetic flow (general providers)  
- DAG pattern **meaningfully less placeholder** than today  
- Second non-docs example or clear path  
- 0.55 vision named for docs domain  

---

## Spirit

Palm orchestrates. NeonRoot isolates (tmpfs-fast, disposable).  
Definitions are the business process.  
Docs inspires later — it does not own the engine.

*Purpose first. Dogfood second. Domain last.* 🌴
