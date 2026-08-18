# ADR-033 — Old wiring dies in the same cut

**Status:** Accepted  
**Date:** 2026-08-17 · **Accepted:** 2026-08-18  
**Theme:** [VISION-0.64](../vision/closed/VISION-0.64.md) (**closed**)  
**Map:** [PALM.md](../PALM.md)  
**Related:** [ADR-026](026-palm-system-layer.md) · [ADR-027](027-session-plane.md) · [ADR-028](028-system-boot.md) · [ADR-029](029-system-supervisor.md) · [ADR-032](032-organism-assembly.md)  
**Vault:** [principles §10](../architecture/principles.md) · [glossary](../architecture/glossary.md)

José accepted (2026-08-18). Theme closed.

---

## Context

1. Palm keeps **adding** doors and almost never **removes** the old wire. The tree grows. Two paths do one duty.  
2. That is the worry. Not a missing type name. Old host phases, coordinator pairs, unused helpers, and “boot window stays” sit next to the new seat. Tests green both. The next organ copies the pile.  
3. Bugs hide in the leftover: a later change updates one path. The other still runs. Start moves; stop stays. A helper names a branch nobody walks and looks like API.  
4. ADR-026 already says temporary shims must be debt-listed. ADR-027 already forbids long-lived dual paths. ADR-029 already gives the supervisor start/stop. Those records did not make us **delete** the host start window for `work_drain`. Listing is not removal.  
5. Theme **0.64** is the first copyable capability. Later hands will copy what we leave. If we leave old wiring, they will add more and never remove.  
6. Pre-1.0 may break the old wire. José names residual when a dual must stay for a while. Silence is not a stay.

**Code now (2026-08-17).** The host start window and the coordinator start/stop pair are **gone**. `system.background.start` is the one `work_drain` loop start. Host schedule ends at `host.ready`. Host shutdown freezes the supervisor seat, then `runtime.stop` stops it again.

**Admission is not this delete target.** Admission is the business-rule face ([VISION-0.64](../vision/closed/VISION-0.64.md)): business does not talk to system lower layers. Capability is the structure fact. 0.64 does the work (step 2). Changing that face (step 3) and its dependents (step 4 / [SD-020](../../TECH-DEBT.md#sd-020)) comes after copyable. Leaving the old face as a **second membership king** is old wiring. Product still digging engines is the old contract. Deleting the face before the hands exist is a prettier soft lock.

---

## Decision

### D1 — One walker per duty

A **duty** is one act: install, start, stop, apply, bind.

A **walker** is the live code that performs that duty. Something in `src/` must call it.

| Prefer | Avoid |
|--------|--------|
| One walker | Two schedules, two coordinators, or a helper plus the real fill |
| One **fill site** for install/register | Hand **and** host `if` **and** catalog freelance |
| Supervisor start/stop for continuous services | Host phase that names the same service again |

### D2 — Adding is half the cut. Removal is the other half.

A new door is not landed until the old walker is gone.

| Landed means | Not landed |
|--------------|------------|
| Old walker deleted, **or** listed as **named residual** | Old walker still walks “just in case” |
| Tests prove the **live** door | Tests green a dead name so CI stays quiet |

Named residual is honest leftover. It is not a second king.

### D3 — A pair is not half-moved

Start and stop are one owner. Attach and detach are one owner.

Do not delete `start` on packaging and keep `stop` there because shutdown still called it. If the system owns the pair, packaging talks to that seat. It does not keep one side of the pair.

### D4 — Host is not a second lifecycle

The host is the composition root. It seeds, binds product `submit` / `able`, and walks its own boot table.

It does **not** own start/stop of a system continuous service.  
`able` may stay false until `host.ready`. The loop may start earlier and idle. That is not a second start.

### D5 — An unwalked branch is not API

A private helper whose only job is to name a branch nobody walks is not a public contract.

Delete the helper and the branch, **or** add one test that walks the branch and own the law. Do not keep the name “for later.”

Lists exist only if something walks them.

---

## Consequences

### Positive

- The tree stops growing a second wire for each new seat.  
- The next organ copies **name + hand + one start owner**, not the old host pair.  
- Dual fill shows up as a broken test or a named residual, not as a quiet second loop.

### Negative / cost

- Mid-cut breakage when the old walker dies.  
- Named residuals must stay listed ([TECH-DEBT](../../TECH-DEBT.md) or the theme cut). Silence is not a stay.  
- Ops keys and chronicle may still say old names (`start_plane_running`, closed vision). Those are not second walkers.

### Neutral

- This ADR does not close 0.64. José still judges copyable.  
- This ADR does not invent definition `requires`. It does not land journal/outbox.  
- This ADR does not rewrite [ADR-032](032-organism-assembly.md) D2. The admission contract changes after the work.  
- Horizon speech stays assembly → tunnels → Grove.

---

## Alternatives considered

| Option | Why rejected |
|--------|----------------|
| Fold the law only into VISION-0.64 | Theme notes close. Later organs will not read a closed pile C. |
| Debt-list forever (ADR-026 only) | A listed dual that still walks is still two owners. Listing is not the cut. |
| Keep a host “boot window” after system start | That is the half-move. Idempotent start hides the second walker. |
| Keep unused helpers as slim doors | Tests freeze dead names. The next change treats the helper as contract. |

---

## Links

- [VISION-0.64](../vision/closed/VISION-0.64.md)  
- [WORK-DRAIN](../WORK-DRAIN.md)  
- [structure-materialize-cut](../architecture/appendix/structure-materialize-cut.md)  
