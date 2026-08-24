# Migration — 0.68 The great cleansing

**Theme:** [VISION-0.68](../vision/VISION-0.68.md) · **ADR:** none  
**Map:** [PALM.md](../PALM.md)

Palm is pre-1.0. Plan `0.68.0`. Package stays `0.67.0` until José exits. **0.68.1** drops the empty projections boot phase. **0.68.2** drops the runner `ready()` doctor register. **0.68.3** trims living docs that promised webhook POST. **0.68.4** DNA-skips outbox store wire (`capability_off:outbox`). **0.68.5** drops the empty `LocalRunnerApp.ready()` override. **0.68.6** drops the runner `ready()` call. **0.68.7** drops the write-only `RunnerApp` bag. **0.68.8** drops the empty `palm.common.runtimes` parking lot. Costume compost may drop further empty seats.

## Prefer

| Goal | Use |
|------|-----|
| Is this organ here (and is the organism ready)? | `require_capability(source, name)` ([MIGRATION-0.67](MIGRATION-0.67.md)) |
| May business that needs ground run? | `require_business_admission(source)` |
| Outbox store wire | DNA `has_capability("outbox")` — skip `capability_off:outbox` when omitted |
| Snapshot history on a job | `enable_state_snapshot` (packaging, still read) |

## Behavior / names that may change (from 0.68.1)

Execute will name the cut. Likely:

| Was | May become |
|-----|------------|
| Boot phase `host.projections.attach` | **Gone (0.68.1).** Membership attach is the DNA hand (0.67.9–0.67.10). Inventory retunes onto admission. |
| Runner `ready()` doctor register | **Gone (0.68.2).** Anatomy doctor samples runners via `workloads` (`WorkloadEngine.doctor`). No global contributor list. |
| Bare `BaseRuntime.start(enable_event_outbox=…)` | **Gone (0.68.4).** `system.outbox.wire` skips `capability_off:outbox` when DNA omits. Default `local.embedded` omits. |
| Living docs that promise webhook POST | **Honest (0.68.3).** Production does not POST. `on_before_publish` stays a test hook. |
| `LocalRunnerApp.ready()` empty override | **Gone (0.68.5).** Local has no override. |
| Runner `ready()` call | **Gone (0.68.6).** The call is gone. Pattern/Provider `ready()` stays. |
| Write-only `RunnerApp` bag | **Gone (0.68.7).** Autoload still registers `WorkloadRuntime` into `workload_runtime_registry`. Pattern/Provider apps stay. |
| Empty `palm.common.runtimes` | **Gone (0.68.8).** Canonical runtime is `palm.system.runtime`. Server kit is `palm.kits.server`. |

`enable_state_snapshot` stays packaging unless José includes it.

## Not this migration

- Outbox `on_before_publish` as production POST.  
- Workload spawn ([VISION-0.56](../vision/VISION-0.56.md)).  
- Host-less `ServerContext` dissolve.
