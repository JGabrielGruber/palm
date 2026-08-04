# Migration — 0.61 Living-kernel vitality

**Theme:** [VISION-0.61](../VISION-0.61.md) (**closed**) · **ADR:** [030](../adr/030-system-vitality.md) **Accepted**  
**Map:** [PALM.md](../PALM.md) · **Release:** [RELEASE-0.61.13](../releases/RELEASE-0.61.13.md)

Palm is pre-1.0. This theme adds **system-intrinsic eyes** on the living process. Product and surfaces only **present**. Doctor and host status are demoted packaging.

## Prefer

| Goal | Use |
|------|-----|
| Living load / seats | System vitality projection — `project` / `project_top` · schema `palm.vitality_snapshot/1` |
| Product door | `host.inspect` / `InspectService` (`top`, `vitality`, `benchmark`) — not product `SystemService` as law |
| CLI / REPL | `palm top` · `palm benchmark [recipe]` (human units default; `--raw` / `--json`) |
| Process / bulk | Installed caps `process_resources` · `loaded_bulk` on everyday top |
| Load story | `palm benchmark` default recipe `work_cycle` (or `project_stress` · `log_fill` · …) |

## Behavior changes

| Was | Now |
|-----|-----|
| Doctor invents living counters | Doctor = **legacy anatomy** (`kind=legacy_doctor`); eyes via vitality / top |
| Host `event_plane` / `ops` / `control_plane` as load law | Host bags = **packaging residual** (`packaging_status`); living law = vitality |
| Product `SystemService` name collides with system layer | Product door = **`InspectService`** (`host.inspect`; `host.system` alias residual) |
| No first-class physiology home | **`palm.system.vitality`** — seat walk, projection, registry |
| Benchmark only as idea | **`benchmark` tool** (off everyday top); Inspect + CLI present |
| Host `WorkDrainService` fallback | **Removed** (neighbor residual) — plane only |
| Host vs host-less product post-build drift | Shared **`apply_product_packaging`** (BI-003 floor) |

## Product rename (SD-007)

| Prefer | Avoid as law |
|--------|----------------|
| `from palm.services.inspect import InspectService` | New code on product `SystemService` as the operate door |
| `host.inspect.top()` / `.vitality()` / `.benchmark(...)` | Inventing load counters in CLI or MCP |

Temporary `host.system` / import aliases may remain; they are residual, not the home.

## Tests

| Prefer | Avoid |
|--------|--------|
| Assert vitality projection / seat walk / top present | Freezing host status JSON equality as living law |
| Doctor envelope `legacy_doctor` + nested top | Doctor as physiology lexicon |

## Not broken by 0.61

| Area | Note |
|------|------|
| Planes / supervisor / session law | Unchanged verbs |
| Job path / CQRS | Product still presents via inspect |
| Work plane start | Separate residual (enrich/catalog host packaging) |

## Residual after theme close

| Open | Kind |
|------|------|
| **BI-015** | Richer system-log catalog / sinks |
| **SD-016** | Ambient seat DI residual (boy-scout) |
| Host enrich/catalog on workplane coordinator | Packaging (BI-013 residual) |
| BI-003 growth | Packaging as registry seats; not type-kill |
| `monitor_agent` | Intention / later continuous watch product |
| Surface deflation | [VISION-SURFACE-DEFLATION](../VISION-SURFACE-DEFLATION.md) |
