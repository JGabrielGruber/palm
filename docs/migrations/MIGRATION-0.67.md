# Migration — 0.67 Dependents require the organ

**Theme:** [VISION-0.67](../vision/VISION-0.67.md) · **ADR:** [036](../adr/036-require-capability.md) **Proposed**  
**Map:** [PALM.md](../PALM.md)

Palm is pre-1.0. Execute `0.67.1` landed the sibling door. Package stays `0.66.0` until José exits. Additive: a new require beside the ready door.

## Prefer

| Goal | Use |
|------|-----|
| May business that needs ground run? | `require_business_admission(source)` (unchanged) |
| Is this organ here (and is the organism ready)? | `require_capability(source, name)` |
| Query without raise | `admission.has_capability(name)` / zero-arg `able()` |

## Behavior / names that will change

| Was | Now (from 0.67.1) |
|-----|-------------------|
| Organ require = dig structure or pretend ready is membership | `require_capability(source, name)` |
| Missing organ | `CapabilityRefusedError` after the ready wall |

`require_business_admission` still fail-closes only on `may_run_business`. Existing call sites need no change.

`able` on the install board stays zero-arg. Closures may read a name. Decorators are not added.
