# Migration — 0.57 Palm System

**Theme:** [VISION-0.57](../VISION-0.57.md) · **ADR:** [026-palm-system-layer](../adr/026-palm-system-layer.md)  
**Map:** [PALM.md](../PALM.md) · **Release:** [RELEASE-0.57.14](../releases/RELEASE-0.57.14.md)

Palm is pre-1.0. This theme **breaks import paths** for truth. There are no long-lived shims.

## Breaking — system home

| Was (removed or wrong home) | Use instead |
|-----------------------------|-------------|
| `palm.common.runtimes.base` / `BaseRuntime` | `palm.system` / `palm.system.runtime` |
| `palm.common.runtimes.host` / wiring / job hooks | `palm.system.runtime.*` |
| `palm.common.wait` plane service | `palm.system.planes.wait` (shared helpers may remain under `palm.common.wait` only if still shared DTOs — prefer system for runtime attach) |
| `palm.common.work` / work drain on runtime | `palm.system.planes.work` |
| `palm.common.workload` runtime bind | `palm.system.planes.workload` |
| `palm.common.executions` | `palm.system.executions` |
| Engine fields on edges for effects | **`runtime.execution`** (`ExecutionPort`) |

**Rule:** graphs and product call **ports**, not private engines.

## Breaking — kits

| Was | Use instead |
|-----|-------------|
| `palm.common.runtimes.server` | **`palm.kits.server`** |
| Server stack under `common` as “shared” | Surface kit package; install list `INSTALLED_KITS` |

Thin surface adapters stay in `palm.runtimes.*`. Kit infrastructure lives in `palm.kits`.

## Breaking — capability catalog truth

| Was | Now |
|-----|-----|
| Placeholder providers/storages/patterns in default `INSTALLED_*` | **Gated** — only real installs; intention stubs use `INTENTION_*` / explicit enable |

See [STUBS.md](../STUBS.md) and [TECH-DEBT.md](../../TECH-DEBT.md) ST-001…005.

## Not broken by 0.57

| Area | Note |
|------|------|
| Reactive law (0.55) | Unchanged — start / continue on `runtime.event` |
| Workload engine scout (0.56) | Engine + runners stay; **product list/doctor/stop** go through ExecutionPort |
| Session product | Still a **future theme** ([VISION-SESSION-PLANE](../VISION-SESSION-PLANE.md)); not a 0.57 residual |

## Product guidance

| Goal | Call |
|------|------|
| Start / stop / list jobs | ExecutionPort / product services over the port |
| Workload catalog / doctor rows | Port methods (not raw engine fields) |
| Resume parked job | `execution.resume_job` (on the port) |
| Server HTTP stack | `palm.kits.server` |

## Residual after theme close

| Open | Kind |
|------|------|
| **SU-*** surface debt (explorer, MCP dual stack, CLI aliases, surface weight) | Optional; not system law |
| **SD-008** session plane home | Future theme |
| **CS-*** / STE rewrite of old dense docs | Opportunistic |

Live register: [TECH-DEBT.md](../../TECH-DEBT.md).
