# Hermetic run directory + seed modes (0.54.5)

Palm schedules jobs; NeonRoot runs them. Workspaces are **tmpfs** (fast, disposable).
NeonRoot **0.2** adds `--seed-mode copy|bind`.

## Seed modes

| Mode | Behavior | When to use |
|------|----------|-------------|
| **`copy` (default)** | Seed copied into vault bare → clone to tmpfs. Hermetic. Use `--output` for host write-back. | CI, dogfood purity, named artifacts |
| **`bind`** | Host `--seed` path mounted as workspace root; writes hit host live. **Not hermetic.** No `--seed-exclude`. No vault commit of host tree. | Trusted local whole-tree write-back (e.g. CSS into `docs/`) |

Palm resource params: `seed_mode: "copy" | "bind"` (see `neonroot.contract`).

## Palm-owned run layout (0.54.8 helper)

When Palm should stage I/O for a job without seeding the whole monorepo:

```text
{data_dir}/palm/hermetic/runs/{run_id}/
  payload/     # code or linked project slice
  input/       # optional inputs
  output/      # job writes here
  meta.json    # image, command, digests (mirror of job state)
```

Python (thin helper, not a domain service)::

```python
from palm.providers.neonroot import create_run_dir, write_payload_file, remove_run_dir

run = create_run_dir(data_dir="data", meta={"purpose": "assist-run-code"})
write_payload_file(run, "main.py", "print('hi')\n")
params = run.neonroot_spawn_params(
    image="palm-ci",
    command=["python", "payload/main.py"],
    vault="palm-ci",
    seed_mode="bind",  # default
)
# → neonroot provider invoke spawn with params
# remove_run_dir(run)  # GC after success
```

| Actor | Action |
|-------|--------|
| Palm (before) | `create_run_dir` + payload; record paths in job state |
| NeonRoot | `spawn --seed …/runs/{id} --seed-mode bind` (or copy) |
| Job | Read payload/input; write output/ |
| Palm (after) | Read output/; optional promote; `remove_run_dir` |

**GC:** delete `runs/{run_id}` after success (or after TTL on failure). Never bind entire `data/palm/` (instances, secrets).

## Recipes

| Recipe | Mode |
|--------|------|
| `just docs-css-sandbox` | copy + `--output` styles/output.css |
| `just docs-css-bind` | bind `docs/` (live host write) |
| `just docs-build-sandbox` | git-archive copy + `--output` `_build` |

## Assist “run code” (horizon)

1. Create run dir under `data/palm/hermetic/runs/{id}/payload`  
2. Write supplied script (allowlisted)  
3. `neonroot.spawn` image + bind or copy that dir  
4. Capture stdout / `output/`  

No in-engine `exec`. Policy hardcodes image allowlists and max payload size.

## Vault vs product

| Place | Holds |
|-------|--------|
| NeonRoot vault (`.neonroot`) | Images; optional committed tool workspaces |
| Tmpfs workspace | Live job tree (default) |
| Palm job state | Handles, status, tails |
| Palm product storage / host paths | Only **promoted** outputs |

See [HERMETIC-JOBS.md](HERMETIC-JOBS.md) · [VISION-0.54](VISION-0.54.md) · NeonRoot 0.2 docs.
