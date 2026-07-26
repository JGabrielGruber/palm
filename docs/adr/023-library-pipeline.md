# ADR-023: Library Pipeline — docs as a storage-backed Palm product (0.54)

## Status

**Accepted** — July 2026 (0.54.0; refined after Living Library + Sovereign Runners).  
Planned in [VISION-0.54](../VISION-0.54.md).  
Builds on [ADR-021](021-living-library.md), [ADR-022](022-neonroot-provider.md), [ADR-011](011-local-document-resources.md) (tiered KV).

## Context

0.52 introduced SOURCE / BUILD / SURFACE and a thin on-disk builder (`docs/_build`).  
0.53 made NeonRoot a provider so production of artifacts can be hermetic.  
Serving live docs by reading host `_build` would ignore Palm’s **storage engine** (including tiered hot/cold KV) and would not scale to API/SDK inventories as first-class products.

The product goal is broader than “run docs_build in a flow”: **revisioned documentation corpora** published into Palm, queried by a **DocsService**, optionally exported to static edge.

## Decision

1. **Live docs truth is storage, not disk.** Published library content lives under a `library/*` (name may refine) keyspace in Palm storage, preferring **tiered KV** when the host is durable. Git/`docs/` remains **SOURCE** for human prose and landing soul.

2. **Multi-corpus, multi-resource.** Wiki, API inventory, SDK surface, MCP catalog, ADRs, site assets are **distinct corpora**, each with its own publish resource(s). Tool **images** may be few; **resources** are many. Reject a single god resource/image that builds everything as the only path.

3. **DocsService** is a real service domain (`CompositionProfile` service name `"docs"` when wired): list/get/status over the current pin, and **rebuild** by submitting the Palm graph (pipeline/resources) — never by shelling `just` as dogfood.

4. **Pipeline pattern** sequences publish steps and **pins** `meta/current` (or equivalent) only after successful production for the scoped rebuild. Wizard optional later.

5. **Host `_build` / Cloudflare** are **export phenotypes**: optional materialization of a pin for static hosting (`neonroot --output` or a dedicated export step). They are not what DocsService reads for “live” docs.

6. **Horizon:** Postgres/Mongo/GraphQL real tests and pinned drivers use the **same** produce-under-neonroot grammar; out of scope for 0.54 implementation but explicitly enabled by this architecture ([TECH-DEBT](../../TECH-DEBT.md) PD-022).

## Consequences

- **Positive.** Live docs survive process restarts with durable storage; clean rebuild via new revision; Assist/API/SDK docs share one service; dogfood matches how Palm should manage any external product; adapter runners can copy the template.
- **Risk.** Key schema and pin races — mitigate with single-writer pin convention and tests on memory + filesystem backends.
- **Risk.** Scope creep into CMS — rebuild regenerates from SOURCE/generators; no multi-author edit-in-storage as SOURCE.
- **Bounded.** v0 may ship one corpus + DocsService stub + pipeline; more corpora follow in-theme.

## Alternatives considered

- **DocsService reads only `docs/_build`.** Rejected — bypasses storage, weak durability, wrong for multi-surface API.
- **AnalyticsService as docs store.** Rejected — analytics is BI rows; library is document/inventory product. Shared *vocabulary* (publish/pin) is fine; shared service is not SRP.
- **One neonroot spawn builds all corpora.** Rejected as the only design — allowed as an optional bulk resource later, not the architecture.
- **Shell just from a Palm step.** Rejected (ADR-022).

## References

- [VISION-0.54](../VISION-0.54.md) · [VISION-0.52](../VISION-0.52.md) · [VISION-0.53](../VISION-0.53.md)  
- [ADR-011](011-local-document-resources.md) · [ADR-021](021-living-library.md) · [ADR-022](022-neonroot-provider.md)  
