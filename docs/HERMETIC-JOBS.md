# Hermetic jobs (0.54)

**Purpose test:** Palm schedules work as **definitions**; foreign tools run only via
**NeonRoot** (tmpfs workspaces). See [VISION-0.54](VISION-0.54.md) · [ADR-023](adr/023-hermetic-jobs.md).

## Glossary (0.56 workload plane)

| Term | Meaning |
|------|---------|
| **Hermetic** | **Isolation policy** (`isolation=hermetic`) — not a synonym for NeonRoot |
| **WorkloadEngine** | Pure core lifecycle: start / exec / status / stop ([ADR-024](adr/024-workload-engine.md)) |
| **WorkloadRuntime** | Adapter (host, neonroot, ssh, palm, …) under `palm/runners/` |
| **WorkloadSpec** | Portable JSON intent (argv lists, image, isolation, placement) |
| **Provider** | ResourceEngine backend (kv, rest, …) — **speak**, not long-term isolation home |
| **NeonRoot (today)** | Still a **provider** façade for 0.54 dogfood; becomes a **WorkloadRuntime** in 0.56 |

Product path (0.56+): **allocate** with WorkloadEngine · **speak** with providers · **react** with events.  
Wait interest kind `workload` is already live from 0.55; engine emits `workload.*` lifecycle events.

## Contract (resource node — 0.54 dogfood path)

| Field | Provider / action | Role |
|-------|-------------------|------|
| provider | `neonroot` | Hermetic runner (façade until workload runtime lands) |
| action | `health` \| `spawn` | Preflight or job |
| params | see below | Job specification |

### `spawn` params

| Param | Required | Notes |
|-------|----------|--------|
| `image` | yes | e.g. `palm-ci`, `palm-docs` |
| `command` | yes | argv list |
| `seed` | no (default `git-archive`) | `git-archive` \| path \| `none` |
| `seed_mode` | no (default `copy`) | `copy` (hermetic) \| `bind` (live host; NeonRoot 0.2+; needs path seed) |
| `seed_exclude` | no | list of paths/globs (**not** with `bind`) |
| `outputs` | no | success-only `host:container` maps (prefer with `copy`) |
| `vault` | no | vault name |
| `sandbox` / `isolated` | no | defaults sandbox on |
| `timeout` | no | seconds |

Run-dir + bind notes: [HERMETIC-RUN-DIR.md](HERMETIC-RUN-DIR.md).

Python validation: `palm.providers.neonroot.contract.validate_hermetic_job_params`.

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

### Assist run-code (0.54.9) — basic NeonRoot loop

Persisted wizard (like todo-builder). Textbook resource-action flow::

    palm flow start hermetic-run-code
    # or palm_assist(params={flow_id: "hermetic-run-code"})

| Step | What happens |
|------|----------------|
| **image** | Operator picks allowlisted NeonRoot image (`palm-ci` / `palm-docs`) |
| **code** | Operator writes `payload/main.py` content (`print(...)` for stdout) |
| **run** | Resource `hermetic-run-script` → `neonroot.run_script` (stage + spawn) |
| **remember_*** | Transform extracts `stdout` / `exit_code` into wizard memory |
| **result** | Display binds `{{ state.stdout }}` / `{{ state.exit_code }}` to the turn |
| **summary** | Confirm answers (includes full `run_result`) |

Staging uses [HERMETIC-RUN-DIR.md](HERMETIC-RUN-DIR.md). Not in-engine `exec`.  
**Definitions (v0):** flow + process + resource `hermetic-run-script`.  
**Later (optional):** multi-file projects, snippet catalog, `list_images`, saved artifacts.

### DAG ready-set (0.54.8)

Default ``drain_ready: true`` — one tick runs all currently ready nodes (sequential
invokes). Set ``drain_ready: false`` for one node per tick.

## Docs product domain

Optional Living Library business process → [VISION-0.55](VISION-0.55.md), not this theme.
