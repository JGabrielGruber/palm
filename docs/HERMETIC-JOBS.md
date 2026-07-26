# Hermetic jobs (0.54)

**Purpose test:** Palm schedules work as **definitions**; foreign tools run only via
**NeonRoot** (tmpfs workspaces). See [VISION-0.54](VISION-0.54.md) · [ADR-023](adr/023-hermetic-jobs.md).

## Contract (resource node)

| Field | Provider / action | Role |
|-------|-------------------|------|
| provider | `neonroot` | Hermetic runner |
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

### Future: Assist “run code”

Pick an image, provide a payload/script, Palm stages + `neonroot.spawn`, return result —
builds on this contract (not in-engine `exec`). See VISION-0.54 horizon.

## Docs product domain

Optional Living Library business process → [VISION-0.55](VISION-0.55.md), not this theme.
