# ADR-026 — Palm system layer and module purposes

**Status:** Proposed  
**Date:** 2026-07-29  
**Theme:** [VISION-0.57](../VISION-0.57.md)  
**Map:** [PALM.md](../PALM.md)

---

## Context

Palm has a pure **core**, strong **plugins**, and a growing **product** surface.  
Coordination code landed in `palm.common` without a hard line between:

- **system** behavior (running engines, planes, effects), and  
- **shared** libraries (reusable glue).

Graphs bind **engines** through `PatternBuildContext`.  
Edges often bind **services** that call the same engines.  
Some edges still touch runtime fields.

Workload work made the fracture clear. Isolation is not “another provider invoke.”  
A CQRS-only policy for one capability does not fix the design.

We also lack one short document that states **what Palm is** as a system.

Palm is not in production. We may break structure for truth.

---

## Decision

1. **Adopt [PALM.md](../PALM.md)** as the canonical high-level system definition.  
   The map must describe the **whole organism** (job path, core machines, plugins, product, surfaces), not only the current structural pain.  
   An incomplete map is treated as a false map; update it when structure changes.  
2. **Split purpose:**
   - **System** — holds engines for a running Palm; exposes **ports**; runs **planes**.  
   - **Shared** — reusable code that is not system and not product.  
3. **Introduce named ports** for effects. The first port is the **execution port** (resource + workload at minimum; job drive as the system owns it).  
4. **Graphs and product bind the same ports.** Services and CQRS stay policy and transport over ports.  
5. **Do not** treat CQRS or `ExecutionService` as the only truth of the system.  
6. **Do not** keep “workload special / edges only” as the architecture.  
7. **The job path is the spine.** New features must state their place on that path.  
8. **Documentation** for this theme and later new docs uses **ASD-STE100 Simplified Technical English**.  
9. **Archive** the prior tech-debt era as history. Open a new residual debt register after the cutover starts.

Package paths may move in later slices. **Purposes in PALM.md are normative now.**

---

## Consequences

### Positive

- One place to look for Palm’s structure.  
- Clear home for session and other planes.  
- Workload and resource share one effect model.  
- `common` can shrink to true shared code.  
- Tests can fake **ports** without a full host.

### Negative / cost

- Package moves and rebinds cost work.  
- Temporary shims may exist during cutover (must be debt-listed).  
- Old dense docs lag until rewritten.

### Neutral

- `PalmKernel` remains a valid name for **infra boot** if docs tell that truth.  
- Core purity and register-downward stay unchanged.

---

## Alternatives considered

| Option | Why rejected |
|--------|----------------|
| CQRS-only unification | Graphs must not need the full bus for every leaf tick |
| ExecutionService as the only interface | Too heavy; host-shaped; not injectable for pure pattern tests |
| Port without system/shared split | Leaves the dump problem; session still homeless |
| Workload-only service force | Selective purity; hardens the dual path |
| Docs-only rename | Names without rebind lie again |

---

## Follow-up

- Execute [VISION-0.57](../VISION-0.57.md) slices.  
- Promote this ADR to **Accepted** when the system boundary and execution port land in code.  
- Update ARCHITECTURE and AGENTS to **link** PALM.md; avoid a second full map.

---

## References

- Peer design note on the missing runtime execution port (session discussion, 2026-07).  
- [ADR-002](002-pattern-apps-and-common-boundaries.md) common boundaries (partial; now refined).  
- [ADR-024](024-workload-engine.md) workload plane.  
- [ADR-025](025-reactive-interests.md) start / continue law.  
- [VISION-GROVE](../VISION-GROVE.md).
