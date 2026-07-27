# Migration — 0.55 Reactive Interests

**Theme:** [VISION-0.55](../VISION-0.55.md) · **ADR:** [025-reactive-interests](../adr/025-reactive-interests.md)

## Breaking (post-theme cleanup)

| Removed | Replacement |
|---------|-------------|
| `ChildCompletionHook` (auto parent resume via child → parent) | `WaitMatcher` on `runtime.event` matching `palm.wait.interests` |
| `resume_parent_after_child` / inverted completer→waiter resume | Completers emit self-events only; matcher unparks |
| `ChildWaitHooks.resume_parent_after_child` | Dropped from pattern registry |
| `runtime.start(child_completion_hook=…)` | Option gone |
| `runtime.start(enable_wait_matcher=False)` | Matcher **always** wired on `BaseRuntime.start` |

Nested flows **must** open wait interest when parking (wizard `set_child_wait` does). Parks that only set legacy child-wait payload without interest will **not** auto-unpark.

## Additive surfaces (unchanged)

| Surface | Change |
|---------|--------|
| Inspect / session views | Optional **`waiting_on`** |
| List waiting / Assist catalog | **`waiting_on`** / **`waiting_on_summary`** |
| Doctor | **`reactive_interests`** |
| State key | **`palm.wait.interests`** |

Legacy **display** fields remain: `waiting_for_child`, `waiting_for_child_job_id` (UX, not unpark).

## Law

| Verb | Interest | Action |
|------|----------|--------|
| **Start** | Trigger / inbound / schedule | WorkIntent → drain → new job |
| **Continue** | Wait interest on owner | resume / fail via matcher |

Do **not** encode resume as a WorkIntent kind. Do **not** reintroduce parent-resume from completers.

## Nested state collapse (0.55.12)

| Before | After |
|--------|--------|
| Dual keys: `WizardKeys.WAITING_FOR_CHILD` **and** `palm.wait.interests` | **Interest only** for new parks (`meta.source=nested_wizard`) |
| `get_child_wait` read dual key | Projects from interest; **reads dual key only for pre-0.55.12 snapshots** |

Do not write `WAITING_FOR_CHILD` for new parks. Operator fields (`waiting_for_child` in prompts) remain as **projections** of interest.

### Three “waits” (naming)

| Name | Meaning | Home |
|------|---------|------|
| **Interest wait** | Continue plane park | `palm.wait.interests` / WaitPlaneService |
| **Child-wait UX** | Prompt/inspect fields | derived from interest via `get_child_wait` |
| **Invoke wait** | Blocking poll until job ready | `providers/palm/.../wait.py` (`wait_for_job`) — not interest |

## Upgrade checklist

- [ ] Nested custom parks call `open_wait_interest` / `make_job_wait` (or wizard `set_child_wait`)
- [ ] Remove any use of `ChildCompletionHook` or `resume_parent_after_child`
- [ ] Do not depend on `state[WAITING_FOR_CHILD]` for new parks — use `get_child_wait` or `waiting_on`
- [ ] Operators: `waiting_on` explains *why* parked; matcher continues when the target completes
- [ ] Workload stub: `open_workload_wait` + `emit_workload_*` (full engine → 0.56)

## References

- [EVENT-PLANE](../EVENT-PLANE.md) · [WORK-DRAIN](../WORK-DRAIN.md) · [VISION-GROVE](../VISION-GROVE.md) §4  
- [VISION-0.56](../VISION-0.56.md) — consumes `kind=workload`
