# Event plane — host vs runtime buses

**Status:** 0.45.5 contract · **0.55 Reactive Interests** (wait matcher + composition catalog)  
**See also:** [VISION-0.45](vision/closed/VISION-0.45.md) · [VISION-0.55](vision/closed/VISION-0.55.md) · [ADR-025](adr/025-reactive-interests.md) · [WORK-DRAIN](WORK-DRAIN.md) · [VISION-GROVE](vision/VISION-GROVE.md) §4

Palm runs **two** in-process `EventEngine` instances when `ApplicationHost` is started with a runtime:

| Bus | Property | Emits | Subscribers |
|-----|----------|-------|-------------|
| **Orchestration** | `runtime.event` | `job.*`, `flow.session.*`, `resource.changed`, `workload.*` (stub), … | Wait matcher, inbound, work-drain triggers, event journal, projections |
| **Host coordination** | `host.event` | `host.started`, `host.shutdown`, `host.webhook.delivered`, … | Host recorder, worker coordinator |

## Rule of thumb

**Anything that reacts to job, flow, wait, or workload lifecycle must subscribe to `runtime.event`.**  
Do not emit or assert orchestration events on `host.event` — unit tests that did masked the 0.45.4 server bug (empty event tail on `palm host server`).

```python
# Correct — orchestration bus
host.app.runtime().event.emit("job.completed", job_id="j-1", flow="quick", status="SUCCEEDED")

# Wrong for orchestration — host coordination bus only
host.event.emit("job.completed", job_id="j-1")
```

## Two verbs on one bus (0.55)

[Grove Law of Reactive Interests](vision/VISION-GROVE.md): completers speak of themselves; Palm **starts** or **continues** by matching interest.

| Verb | Interest | Reaction on `runtime.event` | Home |
|------|----------|-----------------------------|------|
| **Start** | Trigger (rule / inbound / schedule) | Enqueue **WorkIntent** → drain → new job | [WORK-DRAIN](WORK-DRAIN.md), `WorkPlaneService` |
| **Continue** | **Wait interest** on parked owner | **resume_job** / fail owner per policy | `palm.core.wait`, **`WaitPlaneService`** (`palm.common.wait`) |

Same event type may feed **both** paths (e.g. `flow.session.succeeded` can start a reaction flow *and* unpark a waiter). Do not merge resume into WorkIntent kinds.

```text
                    runtime.event
         (job.* · flow.session.* · resource.* · workload.*)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     Wait matcher                      Trigger path
     (open waits by target)            (TriggerRegistry / inbound)
              │                               │
              ▼                               ▼
     resume_job / fail                 WorkIntentStore → drain
     (owner job)                       → submit_flow (new job)
```

**Completers** emit self-lifecycle only (`job_id` / `workload_id`, status, small payload).  
**Waiters** open interest on owner state (`palm.wait.interests`) and park.  
**Palm** matches — nested jobs today; `workload` stub for 0.56.

## Wiring (ApplicationHost + BaseRuntime)

- `InboundBindingService` (`mode: internal`) → `_runtime_event_engine()`
- Work plane trigger subscriptions → system event engine / host rebind
- `OrchestrationEngine` → `runtime.event` (set at runtime bootstrap)
- **`WaitPlaneService`** → `runtime.event` via `BaseRuntime` (**always** wired; sole continue path; public door **0.55.15**) — [ADR-025](adr/025-reactive-interests.md)
- Event journal attach + outbox reliable delivery → `runtime.event` (host slot reads the journal object; does not intercept `host.event`)

When the runtime is not started, `_runtime_event_engine()` falls back to `host.event` (embedded/tests without full server profile).

## Session terminal events (0.45.5)

On terminal job status, `OrchestrationEngine` emits:

| Job status | Event |
|------------|-------|
| `SUCCEEDED` | `flow.session.succeeded` |
| `FAILED` | `flow.session.failed` |

Payload includes `job_id`, `status`, and `flow_id` / `flow` when present in job metadata. These power `on_flow` triggers **and** wait matching for nested jobs (`kind=job`).

Also emitted: `job.status_changed`, `job.completed` (terminal).

## Trigger ↔ wait composition catalog

| Event type | Start (trigger → WorkIntent) | Continue (wait interest) |
|------------|------------------------------|---------------------------|
| `job.completed` | Optional `on_event` / inbound | **Yes** — `kind=job`, `target_id=job_id` (status → outcome) |
| `job.status_changed` | Rare | **Yes** if status terminal |
| `flow.session.succeeded` | Common reaction trigger | **Yes** — job kind |
| `flow.session.failed` | Optional | **Yes** — fail owner per policy |
| `resource.changed` | Common analytics / reaction (`on_resource`) | No (unless a wait kind is added later) |
| `workload.started` | Optional `on_workload` | No |
| `workload.ready` | Optional `on_workload` | **Yes** — `kind=workload` |
| `workload.failed` | Optional `on_workload` | **Yes** — fail / leave policy |
| `workload.stopped` | **`on_workload` dogfood** (0.56.9) | **Yes** — terminal success (exit 0) |
| `workload.completed` | Legacy stub alias | **Yes** — terminal via status |
| `inbound.received` | Enqueue path | No |
| `work.intent.*` | Observability | No |

Public/composition sets: `palm.common.events.catalog` (`PUBLIC_EVENT_TYPES`, `COMPOSITION_EVENT_TYPES`).

### Wait interest (durable)

Owner job/instance state key **`palm.wait.interests`** (list). Shape: `kind`, `target_id`, `opened_at`, `policy.on_target_failed`, `meta`, `v`.  
Pure types: `palm.core.wait`. Continue plane: `WaitPlaneService` (package root); matcher/policy/stub as **submodules**. Completion delivery is pluggable via `register_wait_deliverer` / `deliver_wait_completion` (`palm.common.wait.deliver`, 0.55.16). Surfaces: `waiting_on` on inspect / list-waiting / doctor.

### Workload events (0.55.7 stub → 0.56 engine)

`WorkloadEngine` emits `workload.started|ready|failed|stopped` on `runtime.event` (small payloads).  
Wait matcher continues owners; work-drain **`on_workload`** triggers start new flows (e.g. `workload-followup`).  
Stub helpers remain in `palm.common.wait.workload_stub` for unit tests.

## Doctor / ops

`host.control_plane_status()["event_plane"]` and REST/MCP doctor reports expose which bus inbound and work-drain use.  
Doctor also reports **`reactive_interests`**: `wait_matcher_wired`, open wait counts, kinds, verbs `start` / `continue`.  
CLI `palm doctor` prints an **Event Plane** table when host-backed.

## Tests

Use `tests.helpers.event_plane.runtime_event_engine(host)` and `emit_orchestration_event(...)` — never `host.event.emit` for orchestration contract tests.  
Wait matcher / durability: `tests/test_wait_*.py`, `tests/test_workload_wait_stub_0_55_7.py`.
