# Migration — 0.55 Reactive Interests

**Theme:** [VISION-0.55](../VISION-0.55.md) · **ADR:** [025-reactive-interests](../adr/025-reactive-interests.md)  
**Code version at theme close:** still `0.54.10` until an embedded 0.55 release; slices are logical `0.55.N` commits.

## Breaking?

**No required breaks** for typical operators or MCP clients. Changes are **additive** and dual-path safe.

## Additive surfaces

| Surface | Change |
|---------|--------|
| Inspect / session views | Optional **`waiting_on`**: list of open wait interests (`kind`, `target_id`, …) |
| List waiting / Assist catalog | Same fields + optional **`waiting_on_summary`** |
| Doctor | **`jobs.open_wait_*`**, **`reactive_interests`** (matcher wired, kinds, verbs) |
| Job/instance state | Key **`palm.wait.interests`** (JSON list) when parked on nested child or workload stub |

Legacy fields remain: `waiting_for_child`, `waiting_for_child_job_id`, etc.

## Behavioral notes

1. **Normative nested unpark** is `WaitMatcher` on `runtime.event` (completer self-events → resume owner). Nested wizards **open wait interest** when parking (`kind=job`).
2. **`ChildCompletionHook`** remains **on by default** as dual-path compat for parks without interest (pre-0.55.3 snapshots). It is a no-op if the matcher already unparked the parent. Disable with `runtime.start(child_completion_hook=False)`.
3. **Wait matcher** is on by default (`enable_wait_matcher=True`). Disable with `runtime.start(enable_wait_matcher=False)` for isolation tests only.
4. **Do not** encode resume as a WorkIntent kind — start vs continue stay separate ([EVENT-PLANE](../EVENT-PLANE.md), [WORK-DRAIN](../WORK-DRAIN.md)).

## Workload stub (not the 0.56 engine)

`workload.ready` / `workload.failed` / `workload.completed` events and `open_workload_wait` are a **socket** for 0.56. No full WorkloadEngine in 0.55.

## Upgrade checklist

- [ ] Clients may ignore `waiting_on` (optional).
- [ ] Persist/resume paths: instance snapshots already include blackboard keys — wait interests rehydrate on `resume_process`.
- [ ] Custom nested-flow parks should open wait interest (or keep relying on `ChildCompletionHook` until migrated).
- [ ] Operators: prefer doctor `reactive_interests` + list-waiting `waiting_on` to see *why* a job is parked.

## References

- [EVENT-PLANE](../EVENT-PLANE.md) · [WORK-DRAIN](../WORK-DRAIN.md) · [VISION-GROVE](../VISION-GROVE.md) §4  
- [VISION-0.56](../VISION-0.56.md) — consumes `kind=workload`
