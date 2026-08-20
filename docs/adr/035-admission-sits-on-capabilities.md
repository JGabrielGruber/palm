# ADR-035 — Admission sits on installed capabilities

**Status:** Accepted  
**Date:** 2026-08-20 · **Accepted:** 2026-08-20  
**Theme:** [VISION-0.66](../vision/closed/VISION-0.66.md) (**closed**)  
**Map:** [PALM.md](../PALM.md)  
**Related:** [ADR-032](032-organism-assembly.md) **Accepted** · [ADR-033](033-one-walker.md) **Accepted** · [ADR-034](034-supervised-start-walks-registration.md) **Accepted**  
**Sequence:** [VISION-0.64](../vision/closed/VISION-0.64.md) steps 3–4

José accepted (2026-08-20). Theme closed. Snapshot publishes installed names. Step 4 dependents: [VISION-0.67](../vision/VISION-0.67.md).

---

## Context

1. Admission is the **business-rule face**: may this act run. Capability is the **structure fact**: is this organ here. [VISION-0.64](../vision/closed/VISION-0.64.md).  
2. 0.63 published a boolean wall (`may_run_business`). 0.64 / 0.65 made `work_drain` and `outbox` copyable (name + hand + omit).  
3. The published snapshot still has five fields: `may_run_business`, `phase`, `definition_id`, `definition_version`, `reasons`. Installed names live on `StructureSeat.materialized_capabilities`. Business that needs the fact still digs the seat or the supervisor.  
4. Leaving the old face as a second membership king is old wiring (ADR-033). Deleting the face before the hands existed was rejected. Hands exist now.  
5. `require_business_admission` only checks the bool. That stays until dependents move (step 4 / [SD-020](../../TECH-DEBT.md#sd-020)).

## Decision

### D1 — The snapshot publishes installed capabilities

`AdmissionSnapshot` carries `capabilities: frozenset[str]`. Default empty.  
`has_capability(name)` is the predicate. Same names as `StructureDefinition`.

The set is **installed** names: `StructureSeat.materialized_capabilities` after assemble materialize. Not DNA listed-but-not-installed. Not `LOCAL_CAPABILITY_HANDS`.

### D2 — Ready stays the short wall

`may_run_business` stays `phase is READY` and no block reasons and truth home up.  
Refuse still blocks assemble and appears in `reasons`. Do not invent a capability named `ready`.

### D3 — Admission reads. It does not walk.

The walker remains `apply_local_capabilities`. The engine remains places + truth home + phase. The seat copies installed names onto the snapshot it already publishes.

### D4 — Coerce and serialize keep the bool

`to_dict`, `_from_duck`, and `coerce_admission_snapshot` round-trip `capabilities`. New fields have defaults. Callers that only read `may_run_business` do not break.

### D5 — One published read is the floor proof

A product-shaped caller can ask `has_capability("work_drain")` on the gate (`runtime.admission`, injected `admission_source`, or coerced snapshot) without touching `runtime.structure`.

## Consequences

### Positive

- Business can learn organs without a lower-layer dig.  
- Drain and outbox already have hands; they become the first readers.  
- Step 4 can retune `able` / façades against a real fact instead of the wall.

### Negative / residual

- `require_business_admission` still only fail-closes on `may_run_business`.  
- Host `start_ports.able` is still `host._started` (named; not this ADR).  
- DNA list without a hand does not appear on the snapshot (honest omit of the walker).

### Forbidden

- Copy the hands table onto the snapshot.  
- Definition `requires`.  
- Land journal as a no-op organ.  
- Retune `able` or `require(organ)` before the snapshot exists.

## Alternatives considered

- Publish DNA `definition.capabilities` instead of installed names — rejected. Listed without install would lie.  
- New field names (`organs`, `membership`) — rejected. José locked `capabilities` / `has_capability` for coherence.  
- Change `require_business_admission` in the same cut — rejected. That is step 4.

## Links

- [VISION-0.66](../vision/closed/VISION-0.66.md)  
- [VISION-0.64](../vision/closed/VISION-0.64.md)  
- [VISION-ASSEMBLY](../vision/VISION-ASSEMBLY.md)  
- [glossary](../architecture/glossary.md) — admission · capability
