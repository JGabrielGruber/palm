# Hermetic jobs (0.54)

**Purpose test:** Palm schedules work as **definitions**; foreign tools run only via
**NeonRoot** (tmpfs workspaces). See [VISION-0.54](vision/closed/VISION-0.54.md) · [ADR-023](adr/023-hermetic-jobs.md).

## Glossary (0.56 workload plane)

| Term | Meaning |
|------|---------|
| **Hermetic** | **Isolation policy** (`isolation=hermetic`) — not a synonym for NeonRoot |
| **WorkloadEngine** | Pure core lifecycle: start / exec / status / stop ([ADR-024](adr/024-workload-engine.md)) |
| **WorkloadRuntime** | Adapter (host, neonroot, ssh, palm, …) under `palm/runners/` |
| **WorkloadSpec** | Portable JSON intent (argv lists, image, isolation, placement) |
| **Provider** | ResourceEngine backend (kv, rest, …) — **speak**, not long-term isolation home |
| **NeonRoot** | **WorkloadRuntime** only (`palm.runners.neonroot`) — provider removed 0.56 |

Product path (0.56+): **allocate** with WorkloadEngine · **speak** with providers · **react** with events.  
Wait interest kind `workload` is already live from 0.55; engine emits `workload.*` lifecycle events.

## Contract (0.56+ — WorkloadSpec / neonroot **runtime**)

Isolation is **not** a ResourceEngine provider. Use:

| Surface | How |
|---------|-----|
| Wizard | `step_kind: workload` + Spec / sugar |
| DAG | node `workload: { kind, image, command, placement.runtime: neonroot, … }` |
| API | `ExecutionService.workloads` / CQRS `workload.*` |

### WorkloadSpec seed (portable)

| `seed` | Meaning |
|--------|---------|
| omitted + `isolation=hermetic` | `git_archive` |
| omitted + `best_effort` | `none` |
| `{type: none}` | no seed |
| `{type: git_archive}` | `git archive HEAD` |
| `{type: path, path, exclude?}` | host dir, copy seed |
| `{type: bind, path}` | live mount (not hermetic) |

Extras in `resources`: `vault`, `outputs`, `sandbox`, `isolated`, `keep`.  
`labels.name` → neonroot workspace name. Mapping: `palm.runners.neonroot.spec_map`.

### Legacy spawn param shape (tooling / contract tests)

Still validated by `palm.runners.neonroot.contract.validate_hermetic_job_params`
(`image`, `command`, `seed`, `seed_mode`, `outputs`, …). Prefer Spec in definitions.

Run-dir + bind notes: [HERMETIC-RUN-DIR.md](HERMETIC-RUN-DIR.md).

NeonRoot workspaces run on **tmpfs** (fast, disposable). Promote results with
`--output` or Palm post-steps — not whole-tree sync.

## Simple vs hermetic

| Kind | Example |
|------|---------|
| Plain Palm | `kv`, `file`, transforms, `rest` |
| Hermetic job | `neonroot` + `spawn` |

## Dogfood flows

```bash
palm flow start hermetic-job-smoke    # wizard resource chain (0.54.2)
palm flow start hermetic-job-dag      # linear DAG (0.54.3)
palm flow start hermetic-job-fanout   # preflight → A‖B → join (0.54.4)
palm flow start hermetic-ci-slice     # ruff → guard_core (0.54.6, non-docs)
```

Needs NeonRoot CLI; spawn steps need `just ci-image`.

### DAG definition shape (v0)

```yaml
pattern: dag
options:
  chain_implicit: false   # set true (default) to chain list order when deps empty
  nodes:
    - id: preflight
      resource_ref: hermetic-preflight
    - id: branch_a
      resource_ref: hermetic-true-job
      depends_on: [preflight]
    - id: branch_b
      resource_ref: hermetic-true-job
      depends_on: [preflight]
    - id: join
      resource_ref: hermetic-true-job
      depends_on: [branch_a, branch_b]
```

One ready node per tick (stable order among ready); state under `dag.*`.

### run-python (0.56) — Workload plane dogfood

Simple wizard on the **workload** contract (not a special resource loop)::

    palm flow start run-python
    # alias: palm flow start hermetic-run-code
    # host:  PALM_WORKLOAD_HOST_ENABLED=1
    # neonroot: CLI + palm-ci image

| Step | What happens |
|------|----------------|
| **runtime** | `auto` \| `host` \| `neonroot` — same Spec language, different placement |
| **code** | Python source for `python -c …` |
| **run** | `step_kind: workload` → WorkloadEngine → host or neonroot runtime |
| **result** | Display `exit_code` + stdout |

`auto` prefers neonroot when the CLI is present, else host (must be enabled).  
Heavy multi-file CI dogfood remains the hermetic job / DAG flows above.

### DAG ready-set (0.54.8)

Default ``drain_ready: true`` — one tick runs all currently ready nodes (sequential
invokes). Set ``drain_ready: false`` for one node per tick.

## Docs product domain

Optional Living Library business process → [VISION-0.55](vision/closed/VISION-0.55.md), not this theme.
