# ADR-023: Library Pipeline — Palm owns the docs build graph (0.54)

## Status

**Accepted** — July 2026 (0.54.0 planning).  
Planned in [VISION-0.54](../VISION-0.54.md). Builds on [ADR-021](021-living-library.md) (Living Library) and [ADR-022](022-neonroot-provider.md) (NeonRoot provider).

## Context

0.52 established SOURCE / BUILD / SURFACE and a thin `docs_build.py`.  
0.53 made NeonRoot a Palm provider with hermetic `spawn`, seed exclude, and host `--output`.  
Just recipes already rebuild CSS and the library canopy inside `palm-docs`.

The remaining gap is **product-shaped dogfood**: a durable Palm definition that sequences those resource steps, so operators and Assist use the same grammar as any other flow — and so future adapter work (Postgres/Mongo) can copy the pattern.

## Decision

1. **Pattern:** ship the v0 “rebuild Living Library” definition as a **pipeline** (linear steps). Wizard optional later for interactive step selection.

2. **Steps are resources**, primarily `provider: neonroot` (health + spawn). Work units remain 0.52/0.53 scripts and Tailwind CLI **inside** tool images — Palm does not reimplement them in Python for dogfood cosplay.

3. **Host artifacts** via NeonRoot **`--output`** (success-only), mirrored in resource params / spawn provider fields — not whole-tree seed write-back.

4. **Dual metabolism:** `just docs-*` stays for humans; the Palm flow is a **peer**, documented side-by-side in LIBRARY / DEVELOPMENT.

5. **Failure honesty:** missing CLI, missing image, non-zero spawn exit → failed job/instance, not silent skip (tests may mock spawn).

6. **Horizon (out of scope for 0.54 code):** Postgres/Mongo/GraphQL real tests and pinned extras should use the **same** neonroot resource orchestration (dedicated test images, git-archive seed, pytest in sandbox). Capture in VISION-0.54 horizon + TECH-DEBT direction; implement in a later T7-themed minor.

## Consequences

- **Positive.** Dogfood exercises resources, definitions, Assist, and runners together; documents the template for external systems.
- **Risk.** Slow e2e without NeonRoot — mitigate with mocks + optional live markers.
- **Bounded.** No CMS; no adapter implementation in 0.54; no Cloudflare replacement.

## Alternatives considered

- **Wizard-first rebuild.** Rejected for v0 — extra UX surface; pipeline is enough to prove the graph.
- **Shell step calling just.** Rejected — fake dogfood (ADR-022).
- **Implement postgres tests in 0.54.** Deferred — needs images + driver pinning; library pipeline is the smaller truthful slice that unlocks the grammar.

## References

- [VISION-0.54](../VISION-0.54.md) · [VISION-0.53](../VISION-0.53.md) · [VISION-0.52](../VISION-0.52.md)  
- [TECH-DEBT.md](../../TECH-DEBT.md) PD-022, PD-023, PD-030  
