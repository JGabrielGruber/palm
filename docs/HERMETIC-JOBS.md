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
| `seed_exclude` | no | list of paths/globs |
| `outputs` | no | success-only `host:container` maps |
| `vault` | no | vault name |
| `sandbox` / `isolated` | no | defaults sandbox on |
| `timeout` | no | seconds |

Python validation: `palm.providers.neonroot.contract.validate_hermetic_job_params`.

NeonRoot workspaces run on **tmpfs** (fast, disposable). Promote results with
`--output` or Palm post-steps — not whole-tree sync.

## Simple vs hermetic

| Kind | Example |
|------|---------|
| Plain Palm | `kv`, `file`, transforms, `rest` |
| Hermetic job | `neonroot` + `spawn` |

## Dogfood flow (0.54.2)

```bash
palm flow start hermetic-job-smoke
```

Steps: `neonroot-health` → `neonroot-spawn-true` (needs `just ci-image` for spawn).

## Docs product domain

Optional Living Library business process → [VISION-0.55](VISION-0.55.md), not this theme.
