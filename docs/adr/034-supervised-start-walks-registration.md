# ADR-034 — Supervised start walks registration

**Status:** Proposed  
**Date:** 2026-08-18  
**Theme:** [VISION-0.65](../vision/VISION-0.65.md)  
**Map:** [PALM.md](../PALM.md)  
**Related:** [ADR-033](033-one-walker.md) **Accepted** · [ADR-029](029-system-supervisor.md) **Accepted**  
**Law:** [AGENTS §1.1](../../src/palm/AGENTS.md)

José opened theme **0.65** (2026-08-18). Accept at exit.

---

## Context

1. `work_drain` is copyable: definition lists the name; a hand registers; omit unregisters.  
2. `system.background.start` still names organs (`if want_drain` / `if want_outbox`) and skip strings name `work_drain`. A second listed hand will not start unless this loop grows.  
3. [AGENTS §1.1](../../src/palm/AGENTS.md) says invert **before** the second organ. Do not add another `if`.  
4. ADR-033 already says one walker per duty and old wiring dies in the same cut. This record is the **start** invert: the walker must not be a private menu of names.  
5. Outbox still freelance-registers and still uses `enable_outbox_background`. That option is **named residual** until the outbox hand lands and the old walkers die.

## Decision

### D1 — The start phase walks registration

`system.background.start` walks **registered** supervisor services. It starts a service when that service **may start**. It does not name `work_drain` or `outbox`.

### D2 — Readiness lives on the service (or its register)

A service carries `may_start` (or an equivalent hook) given install seats and start options.  
`work_drain` may start when start ports are bound.  
Until the outbox hand lands, freelance `outbox` may start only when `enable_outbox_background` is true. That gate sits on the **service**, not in a phase `if name ==`.

### D3 — Skip reasons do not name one organ as the world

If nothing is registered: `none_registered`.  
If something is registered and nothing may start: `none_ready`.  
Do not keep `structure_off:work_drain` / `ports_off:work_drain` as the only skip language.

### D4 — Seats grow at the walker edge

`CapabilitySeats` may carry the ports a later hand needs (`outbox_store` / `outbox_processor`). Assemble fills seats from install. The start phase does not scrape a shell bag.

### D5 — Adding is half. Removal is the other half.

The outbox **hand** is not landed until `composition.has`, the freelance catalog, host recover start, the node-role AND, and the second host thread die — or José names residual. ADR-033.

## Consequences

### Positive

- A new organ is name + hand + omit. Start already walks.  
- Tests prove the live door. Drain-named skip strings stop being law.

### Negative / residual

- `enable_outbox_background` stays until the hand cut. Honest leftover. Not a second membership king for `work_drain`.  
- Host recover still starts outbox. That walker dies with the hand.

### Forbidden

- A new `if want_<organ>` in `phase_background.py`.  
- Definition `requires`.  
- Alias tests green for the old skip strings.

## Alternatives considered

- Add `if want_outbox` and invert later — rejected (§1.1).  
- Start every registered service with no `may_start` — rejected while the freelance catalog still registers outbox.  
- Empty the freelance catalog before the hand — rejected as a half-cut (recover `start("outbox")` would have nothing to start).

## Links

- [VISION-0.65](../vision/VISION-0.65.md)  
- [VISION-0.64](../vision/closed/VISION-0.64.md)  
- [ADR-033](033-one-walker.md)
