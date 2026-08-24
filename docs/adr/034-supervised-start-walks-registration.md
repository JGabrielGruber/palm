# ADR-034 — Supervised start walks registration

**Status:** Accepted  
**Date:** 2026-08-18 · **Accepted:** 2026-08-18  
**Theme:** [VISION-0.65](../vision/closed/VISION-0.65.md) (**closed**)  
**Map:** [PALM.md](../PALM.md)  
**Related:** [ADR-033](033-one-walker.md) **Accepted** · [ADR-029](029-system-supervisor.md) **Accepted**  
**Law:** [AGENTS §1.1](../../src/palm/AGENTS.md)

José accepted (2026-08-18). Theme closed.

---

## Context

1. `work_drain` is copyable: definition lists the name; a hand registers; omit unregisters.  
2. `system.background.start` used to name organs (`if want_drain` / `if want_outbox`) and skip strings named `work_drain`. A second listed hand would not start unless this loop grew.  
3. [AGENTS §1.1](../../src/palm/AGENTS.md) says invert **before** the second organ. Do not add another `if`.  
4. ADR-033 already says one walker per duty and old wiring dies in the same cut. This record is the **start** invert: the walker must not be a private menu of names.  
5. At theme open, outbox still freelance-registered and still used `enable_outbox_background`. That option died with the hand (0.65.2).

## Decision

### D1 — The start phase walks registration

`system.background.start` walks **registered** supervisor services. It starts a service when that service **may start**. It does not name `work_drain` or `outbox`.

### D2 — Readiness lives on the service (or its register)

A service carries `may_start` (or an equivalent hook) given install seats and start options.  
`work_drain` may start when start ports are bound.  
`outbox` may start when it is registered (store + processor seats). There is no option king on that service.

### D3 — Skip reasons do not name one organ as the world

If nothing is registered: `none_registered`.  
If something is registered and nothing may start: `none_ready`.  
Do not keep `structure_off:work_drain` / `ports_off:work_drain` as the only skip language.

### D4 — Seats grow at the walker edge

`CapabilitySeats` may carry the ports a later hand needs (`outbox_store` / `outbox_processor`). Assemble fills seats from install. The start phase does not scrape a shell bag.

### D5 — Adding is half. Removal is the other half.

The outbox **hand** landed when `composition.has` at spawn, the freelance catalog, host recover start, the node-role AND, and the second host thread died. Host store wire follows DNA listing. Bare `enable_event_outbox` is named packaging. ADR-033.

## Consequences

### Positive

- A new organ is name + hand + omit. Start already walks.  
- Tests prove the live door. Drain-named skip strings stop being law.

### Negative / residual

- Bare `enable_event_outbox` was packaging (0.65 named). **0.68.4** composted it: wire skips `capability_off:outbox` when DNA omits.  
- Poll numbers and `outbox_recover_on_startup` stay on the profile.  
- Webhook membership is DNA (0.67.13). Journal is DNA attach (0.67.7).

### Forbidden

- A new `if want_<organ>` in `phase_background.py`.  
- Definition `requires`.  
- Alias tests green for the old skip strings.

## Alternatives considered

- Add `if want_outbox` and invert later — rejected (§1.1).  
- Start every registered service with no `may_start` — rejected while the freelance catalog still registered outbox.  
- Empty the freelance catalog before the hand — rejected as a half-cut (recover `start("outbox")` would have had nothing to start).

## Links

- [VISION-0.65](../vision/closed/VISION-0.65.md)  
- [VISION-0.64](../vision/closed/VISION-0.64.md)  
- [ADR-033](033-one-walker.md)
