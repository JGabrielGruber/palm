# Migration — 0.67 Dependents require the organ

**Theme:** [VISION-0.67](../vision/VISION-0.67.md) · **ADR:** [036](../adr/036-require-capability.md) **Proposed**  
**Map:** [PALM.md](../PALM.md)

Palm is pre-1.0. Execute `0.67.7` landed journal as DNA list + attach hand. Package stays `0.66.0` until José exits. Additive: a new require beside the ready door.

## Prefer

| Goal | Use |
|------|-----|
| May business that needs ground run? | `require_business_admission(source)` (unchanged) |
| Is this organ here (and is the organism ready)? | `require_capability(source, name)` |
| Query without raise | `admission.has_capability(name)` |
| Work-plane drain query | install-board `able()` (ready then `work_drain`) |
| Wait / continue query | `admission_able()` / `may_run_business` |

## Behavior / names that will change

| Was | Now (from 0.67.1) |
|-----|-------------------|
| Organ require = dig structure or pretend ready is membership | `require_capability(source, name)` |
| Missing organ | `CapabilityRefusedError` after the ready wall |
| Missing organ on a surface | REST/MCP **409** `capability_refused`; CLI/SSR/WS brand (0.67.4) |

`require_business_admission` still fail-closes only on `may_run_business`. Existing call sites need no change.

`able` on the install board stays zero-arg. From 0.67.2 the default closure also reads `work_drain`. Wait uses a ready-only closure. From 0.67.3 host spawn injects drain `install_able` and ready `install_admission_able` (both include host `_started`). Decorators are not added.

From 0.67.4 surfaces speak `capability_refused` for the organ door. Ready-false stays `admission_refused`. Do not mix the codes.

From 0.67.5 `tick_schedules` (and host `tick_work` with `schedules=True`) uses the same drain able as `tick`. Ready without `work_drain` does not enqueue due schedules or advance `next_fire_at`. Direct `ScheduleRegistry.tick` stays a store helper.

From 0.67.6 vitality `work_cycle` drain proofs use `local.cli`. Embedded ready still enqueues; tick does not process.

From 0.67.7 `journal` membership is the structure definition list. Host attach follows `has_capability("journal")`. Composition omit does not hide a listed name. `local.embedded` and `local.worker` omit the organ. Do not treat `composition.has("journal")` as membership.
