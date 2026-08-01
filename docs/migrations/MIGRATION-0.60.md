# Migration — 0.60 System supervisor + work plane

**Theme:** [VISION-0.60](../VISION-0.60.md) (**closed**) · **ADR:** [029](../adr/029-system-supervisor.md) **Accepted**  
**Map:** [PALM.md](../PALM.md) · **Release:** [RELEASE-0.60.9](../releases/RELEASE-0.60.9.md)

Palm is pre-1.0. This theme makes **reactive start and continuous services** live on the **system instance**. Host stays packaging.

## Prefer

| Goal | Use |
|------|-----|
| Enqueue / tick work without host | `runtime.work_plane.enqueue` / `.tick` |
| Continuous work drain | Supervisor service `work_drain` · option `enable_work_drain_service=True` · or host background (uses supervisor) |
| Continuous outbox | Supervisor `outbox` · option `enable_outbox_background=True` · host recover prefers supervisor when no webhooks |
| Reload triggers hostless | `work_plane.reload_from_repository(runtime.repository)` |
| Inbound bindings | `palm.system.planes.work.inbound` (host re-exports remain) |

## Behavior changes

| Was | Now |
|-----|-----|
| WorkIntent drain only on host workplane | **WorkPlaneService** on `runtime.work_plane`; host reuses it |
| Background drain host-only | **SystemSupervisor** + `system.background.start` (optional) |
| Outbox poll only host `OutboxBackgroundService` | **OutboxLoopService** registered when outbox wired; host may start supervisor |
| Reactive session enrich product-only | System default submit uses **session plane** (`session_attr`); host may rebind product enrich |
| Inbound only under `app.host.workplane` | Home **`palm.system.planes.work.inbound`** |
| No system continuous seat | **`runtime.supervisor`** after `system.supervisor.wire` |

## System start options (new / used)

| Option | Meaning |
|--------|---------|
| `enable_work_drain_service` | Start supervised `work_drain` at `system.background.start` |
| `enable_outbox_background` | Start supervised `outbox` at same phase |
| `allow_background_drain` | Master switch; `False` skips background phase |
| `work_drain_*` / `outbox_*` | Poll/depth/batch knobs for plane and outbox loop |

## Tests

| Prefer | Avoid |
|--------|--------|
| Hostless `BaseRuntime.start` + plane tick | Assuming only host `WorkDrainService` exists |
| Assert `runtime.supervisor.names()` | Private host drain thread as sole owner |

## Not broken by 0.60

| Area | Note |
|------|------|
| Wait / session law | Unchanged verbs |
| Host product CQRS / surfaces | Still packaging |
| Boot schedules (0.59) | Extended with supervisor + background seats |

## Residual after theme close

| Open | Kind |
|------|------|
| Host product wire for enrich/catalog | Thin residual on coordinator |
| Host `WorkDrainService` fallback | When no plane (rare) |
| **BI-003** | ServerContext product assembly (not plane seats) |
| ExecutionPort explicit `submit_flow` | Optional expand; plane uses executor path |
| Surface deflation | [VISION-SURFACE-DEFLATION](../VISION-SURFACE-DEFLATION.md) |
