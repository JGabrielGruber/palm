# ADR-033 — One walker per duty

**Status:** Proposed  
**Date:** 2026-08-17  
**Theme:** [VISION-0.64](../vision/VISION-0.64.md) (**open**)  
**Map:** [PALM.md](../PALM.md)  
**Related:** [ADR-026](026-palm-system-layer.md) · [ADR-027](027-session-plane.md) · [ADR-028](028-system-boot.md) · [ADR-029](029-system-supervisor.md) · [ADR-032](032-organism-assembly.md)  
**Vault:** [principles §10](../architecture/principles.md) · [glossary](../architecture/glossary.md)

José accepts. This record stays **Proposed** until he locks.

---

## Context

1. Palm moves duties from **host packaging** onto **system seats** (supervisor, planes, structure hands).  
2. A new door often lands **next to** the old walker. Tests green both. The next organ copies the pair.  
3. That is how bugs hide: a later change updates one walker. The other still runs. Start moves; stop stays. A helper names a branch nobody walks and looks like API.  
4. ADR-026 already says temporary shims must be debt-listed. ADR-027 already forbids long-lived dual paths. ADR-029 already gives the supervisor start/stop. Those records did not stop a second host start window for `work_drain`.  
5. Theme **0.64** is the first copyable capability. Later hands (journal, outbox, …) will copy this shape. The law must outlive the theme note.  
6. Pre-1.0 may break the old walker. José names residual when a dual must stay for a while.

**Code now (2026-08-17).** `system.background.start` is the one `work_drain` loop start. Host schedule ends at `host.ready`. The host coordinator has no start/stop pair. Host shutdown freezes the supervisor seat, then `runtime.stop` stops it again.

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

### D2 — A new door is not landed until the old walker is gone

Landing the new path is half the cut.

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

- The next organ copies **name + hand + one start owner**.  
- Shutdown order stays honest: host may freeze the supervisor seat, then `runtime.stop` runs.  
- Dual fill shows up as a broken test or a named residual, not as a quiet second loop.

### Negative / cost

- Mid-cut breakage when the old walker dies.  
- Named residuals must stay listed ([TECH-DEBT](../../TECH-DEBT.md) or the theme cut). Silence is not a stay.  
- Ops keys and chronicle may still say old names (`start_plane_running`, closed vision). Those are not second walkers.

### Neutral

- This ADR does not close 0.64. José still judges copyable.  
- This ADR does not invent definition `requires`. It does not land journal/outbox.  
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

- [VISION-0.64](../vision/VISION-0.64.md)  
- [WORK-DRAIN](../WORK-DRAIN.md)  
- [structure-materialize-cut](../architecture/appendix/structure-materialize-cut.md)  
