# Migration — 0.55 Reactive Interests

**Theme:** [VISION-0.55](../vision/closed/VISION-0.55.md) · **ADR:** [025-reactive-interests](../adr/025-reactive-interests.md)

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

Operator inspect / Assist use **`waiting_on`** (interest rows). Prompt park projection also uses `waiting_on`.

Provider signal to open a nested park is **`nested_park: true`** on the invoke payload (was `waiting_for_child_wizard`). Pattern status is only **`WAITING_FOR_INPUT`** while parked — no separate `WAITING_FOR_CHILD` enum value.

## Law

| Verb | Interest | Action |
|------|----------|--------|
| **Start** | Trigger / inbound / schedule | WorkIntent → drain → new job |
| **Continue** | Wait interest on owner | resume / fail via matcher |

Do **not** encode resume as a WorkIntent kind. Do **not** reintroduce parent-resume from completers.

## Nested delivery (0.55.14+)

On child success, **WaitPlaneService** writes the child payload to the owner's
`meta.output_key`, closes the interest, then resumes. Resource phase does **not**
complete nested success by polling the child — open interest means wait for the
plane.

## Public API collapse (0.55.15)

Package root `palm.common.wait` is a **slim door** — not a barrel of internals.

| Prefer | Avoid / removed |
|--------|-----------------|
| `WaitPlaneService` / `bind_wait_plane_to_runtime` | `bind_wait_matcher_to_runtime` (deleted) |
| `plane.open_on_job` / `open_interest_on_job` | `open_tracked_wait` (deleted) |
| `palm.common.wait.matcher` / `.signals` / … | Re-exports of matcher, policy, deliver, stub from package root |
| `palm.common.wait.workload_stub` | `from palm.common.wait import open_workload_wait` |

Pure types stay on `palm.core.wait`. Operator present helpers remain on the package root.

## Kind-generic delivery (0.55.16)

On positive continue match, the plane calls **`deliver_wait_completion`** (registry), not a hardcoded nested helper.

| Use | API |
|-----|-----|
| Default nested write | still registered as `nested_wizard` |
| Custom kind/source | `register_wait_deliverer(name, fn, kind=… / source=… / matches=…)` |
| Module | `palm.common.wait.deliver` |

`deliver_nested_wizard_completion` remains as the nested implementation + unit-test helper.

## Nested park slash (post-0.55.12)

**Breaking for custom callers:** `set_child_wait` / `get_child_wait` / `clear_child_wait` are **gone**.

| Use | API |
|-----|-----|
| Park nested child | `open_nested_park(state, target_id=…, meta=…)` or `plane.open_on_job` |
| Read park | `nested_park_interest(state)` or `waiting_on` / interests list |
| Clear park | `clear_nested_park(state, target_id=…)` |

Module: `palm.patterns.wizard.bindings.resource.nested_park`.

### Three “waits” (naming)

| Name | Meaning | Home |
|------|---------|------|
| **Interest wait** | Continue plane park | `palm.wait.interests` / WaitPlaneService |
| **Nested park** | Wizard resource step parked on child | interest with `meta.source=nested_wizard` |
| **Invoke wait** | Blocking poll until job ready | `providers/palm/.../wait.py` (`wait_for_job`) — not interest |

## Upgrade checklist

- [ ] Nested custom parks: `open_nested_park` / `make_job_wait` + plane — **not** `set_child_wait`
- [ ] Remove any use of `ChildCompletionHook` or `resume_parent_after_child`
- [ ] Prefer `waiting_on` / `nested_park_interest` over deleted dual-key helpers
- [ ] Workload stub: `from palm.common.wait.workload_stub import open_workload_wait, emit_workload_*` (full engine → 0.56)
- [ ] Custom open/match: plane or `access.open_interest_*` — not deleted tracked/runtime_bind helpers
- [ ] Custom completion shape: `register_wait_deliverer` — do not edit `WaitPlaneService.resume_owner`
- [ ] No `resume_child_wait` / `ChildWaitHooks` / poll-based parent completion

## References

- [EVENT-PLANE](../EVENT-PLANE.md) · [WORK-DRAIN](../WORK-DRAIN.md) · [VISION-GROVE](../vision/VISION-GROVE.md) §4  
- [VISION-0.56](../vision/VISION-0.56.md) — consumes `kind=workload`
