# Release 0.54.10 — Hermetic Jobs (theme close)

**Date:** 2026-07-26  
**Package version:** `0.54.10` (`palmengine`)  
**Theme:** [VISION-0.54](../vision/closed/VISION-0.54.md) · [ADR-023](../adr/023-hermetic-jobs.md)  
**Previous stamp:** `0.51.6` (debt/import/host work; 0.52–0.54 shipped as slice commits without embedded release)

---

## Highlights

Palm can run **definition-driven multi-step work** where foreign code only executes under **NeonRoot** — never in-engine `exec`.

- **Hermetic job contract** — spawn, seed, allowlist, run-dir staging  
- **DAG pattern v0** — resource nodes, dependencies, ready-set drain  
- **Dogfood flows** — smoke, fan-out, CI slice, Assist **run-code**  
- **Portal** — resource steps auto-advance; long NeonRoot runs wait out the session drive  

**0.54 is closed.** Next: [VISION-0.55](../vision/closed/VISION-0.55.md) **Session plane** (session lifecycle + multi-event subscriptions for Assist and dashboard). Docs product dogfood deferred past that.

---

## Upgrade

```bash
pip install -U palmengine==0.54.10
# or from this repo:
uv sync
```

**NeonRoot** (optional but required for hermetic dogfood): install CLI, `just ci-image` / `just docs-image` for allowlisted images.

```bash
palm flow start hermetic-run-code
# or Portal / palm_assist(params={flow_id: "hermetic-run-code"})
```

Use `print(...)` in run-code snippets; results land in `state.stdout` / summary.

---

## Breaking / migrations

No new MIGRATION for 0.54.10. Interim library product modules (if any local experiments from discarded 0.54 plan) remain removed — use static 0.52 docs tooling and 0.55+ session work.

---

## Slice summary (0.54.0 → 0.54.10)

| Slice | Summary |
|-------|---------|
| 0.54.0 | Replan; drop interim docs product stack |
| 0.54.1 | Contract + HERMETIC-JOBS.md |
| 0.54.2 | hermetic-job-smoke |
| 0.54.3 | DAG pattern v0 |
| 0.54.4 | hermetic-job-fanout |
| 0.54.5 | seed_mode + HERMETIC-RUN-DIR |
| 0.54.6 | hermetic-ci-slice |
| 0.54.7 | Purpose-test docs |
| 0.54.8 | drain_ready, run_dir, discover |
| 0.54.9 | hermetic-run-code + run_script |
| **0.54.10** | Dogfood complete; Portal resource auto-advance; **release** |

Full detail: [CHANGELOG.md](../../CHANGELOG.md) § 0.54.10.

---

## Verify

```bash
just docs-check
just check   # or just ci
uv run python -c "import palm; print(palm.__version__)"  # → 0.54.10
```
