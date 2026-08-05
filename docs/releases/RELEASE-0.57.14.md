# Release 0.57.14 — Palm System (theme close)

**Date:** 2026-07-29  
**Package version:** `0.57.14` (`palmengine`)  
**Theme:** [VISION-0.57](../vision/closed/VISION-0.57.md) · [ADR-026](../adr/026-palm-system-layer.md) **Accepted**  
**Map:** [PALM.md](../PALM.md) · [SYSTEM-LOW-LEVEL](../SYSTEM-LOW-LEVEL.md)  
**Migration:** [MIGRATION-0.57](../migrations/MIGRATION-0.57.md)  
**Previous stamp:** `0.54.10` (0.55–0.56 shipped as slice commits without embedded release)

---

## Highlights

Palm has a **named system layer** that matches the whole-organism map.

- **`palm.system`** — `BaseRuntime`, **ExecutionPort**, wait / work / workload **planes**, executions, job hooks  
- **`palm.kits`** — exposed surface kits; **`palm.kits.server`** is the HTTP transport kit home  
- **`palm.common`** — shared libraries only (no system dump, no cutover shims)  
- **Capability catalog truth** — default `INSTALLED_*` does not lie; intentions gated  
- **Same ports** for graphs (P2 invoker/driver) and product effects  

**0.57 is closed** for structure. Optional **SU-*** surface debt remains. Session is a **future theme**.

Also embedded (since last PyPI-shaped stamp):

- **0.55** Reactive Interests — start / continue law; WaitPlaneService  
- **0.56** Workload scout — WorkloadEngine + runners; product over port  

---

## Upgrade

```bash
pip install -U palmengine==0.57.14
# or from this repo:
uv sync
```

**Import cutover:** see [MIGRATION-0.57](../migrations/MIGRATION-0.57.md). Prefer:

```python
from palm.system import BaseRuntime  # system instance
# runtime.execution  → ExecutionPort
from palm.kits.server import ...     # was common.runtimes.server
```

---

## Breaking

Yes — package moves for system, planes, executions, and server kit. **No dual-path shims.** Pre-1.0 truth over comfort.

---

## Slice summary (0.57.0 → 0.57.14)

| Slice | Summary |
|-------|---------|
| 0.57.0 | Plan + PALM.md + ADR-026 |
| 0.57.1 | Debt archive + SYSTEM-LOW-LEVEL + SD register |
| 0.57.2 | `palm.system` boundary + ExecutionPort type |
| 0.57.3–5 | Port on runtime; product/graph rebind (P2) |
| 0.57.6 | Deflate BaseRuntime + planes into system |
| 0.57.7 | Edge policy; `resume_job` on port |
| 0.57.8 | Import sweep onto `palm.system` |
| 0.57.9 | Capability catalog truth |
| 0.57.10 | Living docs match code |
| 0.57.11 | Executions + job hooks under system; `list_jobs` |
| 0.57.12 | Delete shims; workload catalog on port |
| 0.57.13 | `palm.kits` + server kit |
| **0.57.14** | Theme exit — ADR Accepted, migration, version dump |

---

## Next

- Optional **SU-*** surface work (explorer, MCP, CLI weight)  
- **Session plane** theme when ready ([VISION-SESSION-PLANE](../vision/closed/VISION-SESSION-PLANE.md))  
- Grove / multi-Palm still north star ([VISION-GROVE](../vision/VISION-GROVE.md))  

*First name the tree. Then grow the branch.*
