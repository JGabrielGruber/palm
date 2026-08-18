# Migration — 0.64 First capability

**Theme:** [VISION-0.64](../vision/closed/VISION-0.64.md) (**closed** at `0.64.0`) · **ADR:** [033](../adr/033-one-walker.md) **Accepted**  
**Map:** [PALM.md](../PALM.md)

Palm is pre-1.0. This theme made `work_drain` a real capability (name + hand + omit). Old wires died in the same cut. No compatibility aliases.

## Prefer

| Goal | Use |
|------|-----|
| Is drain in this process? | Structure definition lists `work_drain`. Omit means it does not run. |
| Register the service | Capability hand (`LOCAL_CAPABILITY_HANDS`). Not composition. Not the wire catalog. |
| Start the loop | `system.background.start` — supervisor has the service. Host does not start drain. |
| Queue unit | `WorkIntent` on the work plane. Explicit: `host.tick_work`. |

## Behavior / names that broke

| Was | Now |
|-----|-----|
| `PALM_ASSEMBLY_DNA_ID` / `assembly_definition_id` | `PALM_STRUCTURE_DEFINITION_ID` / `structure_definition_id` |
| `palm.*.assembly` · `Assembly*` types | `palm.*.structure` · `Structure*` |
| Composition / settings / `WORK_DRAIN_SERVICE` as kings | Definition list + hand. Those leftovers are gone. |
| Host `start_plane` / coordinator start-stop pair | One start: `system.background.start`. Host schedule ends at `host.ready`. |

Admission is still the business face. It does not yet sit on capability (assembly remainder). [SD-020](../../TECH-DEBT.md#sd-020) is not paid here.

Next organ (outbox) is [VISION-0.65](../vision/VISION-0.65.md) — not open.
