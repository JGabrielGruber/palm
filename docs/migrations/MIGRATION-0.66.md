# Migration — 0.66 Admission sits on capabilities

**Theme:** [VISION-0.66](../vision/VISION-0.66.md) · **ADR:** [035](../adr/035-admission-sits-on-capabilities.md) **Proposed**  
**Map:** [PALM.md](../PALM.md)

Palm is pre-1.0. Plan stamp `0.66.0` does not break runtime. **0.66.1** adds snapshot fields with defaults.

## Prefer

| Goal | Use |
|------|-----|
| May business that needs ground run? | `admission.may_run_business` (unchanged) |
| Is this organ here? | `admission.has_capability(name)` / `admission.capabilities` |
| Membership install | Structure definition list + hand. Not the snapshot as walker. |

## Behavior / names that will change

| Was | Now (from 0.66.1) |
|-----|-------------------|
| Snapshot = five fields | Also `capabilities` (installed names, default empty) |
| Organ fact = dig `runtime.structure` or supervisor | Published gate `has_capability` |
| `to_dict()` five keys | Extra key `capabilities` (list). Old readers that pick known keys keep. |

`require_business_admission` still fail-closes only on `may_run_business`. `able` is not this theme.

Dependents that freeze `may_run_business` as the organ list stay until step 4 / [SD-020](../../TECH-DEBT.md#sd-020).
