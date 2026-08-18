# Migration — 0.65 Outbox as the proof cut

**Theme:** [VISION-0.65](../vision/VISION-0.65.md) (**open**) · **ADR:** [034](../adr/034-supervised-start-walks-registration.md) **Proposed**  
**Map:** [PALM.md](../PALM.md)

Palm is pre-1.0. This theme copies the 0.64 home onto **outbox**. Old walkers die in the same cut as the hand. No compatibility aliases.

Plan stamp `0.65.0` did not break runtime. **0.65.1** landed the skip-string break. **0.65.2** landed the hand + DNA + walker kill.

## Prefer

| Goal | Use |
|------|-----|
| Is outbox in this process? | Structure definition lists `outbox`. Omit means it does not run. |
| Register the service | Capability hand. Not composition. Not the freelance wire catalog. |
| Start the loop | `system.background.start` walks registration. Host does not start the loop. |

## Behavior / names that will break

| Was | Now (when the slice lands) |
|-----|----------------------------|
| `composition.has("outbox")` as membership | Definition list + omit |
| `DEFAULT_CONTINUOUS_DEFINITIONS` freelance `outbox` | Hand register / unregister |
| Host recover AND (master + `enable_outbox_service`) | Same start walker as drain |
| `structure_off:work_drain` / `ports_off:work_drain` skip | **0.65.1** — `none_registered` (nothing on supervisor) / `none_ready` (registered, nothing may start) |
| `enable_outbox_background` as start king | **Gone** — listed + registered starts |
| `enable_outbox_service` | **Gone** — not a start king |
| `host.outbox_service` | Read `runtime.outbox_store` / supervisor `outbox` |

Admission / [SD-020](../../TECH-DEBT.md#sd-020) is not this theme.
