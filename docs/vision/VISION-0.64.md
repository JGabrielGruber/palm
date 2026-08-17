# VISION 0.64

**Status:** **Open** (2026-08-17). José closed **0.63**.  
**Map:** [PALM.md](../PALM.md) · vault [architecture/](../architecture/README.md) · seed [VISION-ASSEMBLY](VISION-ASSEMBLY.md)  
**Prior:** [VISION-0.63](closed/VISION-0.63.md) (closed) · [ADR-032](../adr/032-organism-assembly.md)

**This minor is `work_drain` as the first real capability** — the shape every later organ copies. Not a slice queue. Not host-owned drain. Not a private `if`.

| Law | Meaning |
|-----|---------|
| DNA lists the name | Membership |
| Walker loops a table | New organ = name + hand |
| Hand takes **seats** | Supervisor + work plane. No shell bag |
| Plane is system | Attach / install board. Host does not stash or configure it |
| Start ports on the board | `submit` / `able`. Host binds product values at spawn |
| AGENTS §1.1 | A cut does not override this |

Cleanup of `host.work_drain` as owner, coordinator bag scrape, and tests that freeze that past is **in** this theme. Alias-to-keep-green is out.

No slice table. Residual: [TECH-DEBT.md](../../TECH-DEBT.md) · [structure-materialize-cut.md](../architecture/appendix/structure-materialize-cut.md).

**Exit:** José, when this organ is a home someone can copy.

---

## After compact (2026-08-17)

**Commits:** `6e50fd6b` first capability (seats, names, no host drain) · `d1b3c23a` ctx seats, no host listed bag. Master may be ahead of origin. Not pushed.

**Law that landed:** DNA lists the name. Walker loops `LOCAL_CAPABILITY_HANDS`. Hand takes `CapabilitySeats`. Assemble fills seats from boot `ctx` + install `work_plane`. Start reads `supervisor.get("work_drain")` (walker effect), not DNA again, not `host._work_drain_listed`. Tests and status learn `runtime.work_plane`.

**Do not:** invent DNA `requires`; reuse VitalityRegistry for hands; open a 0.64 slice table; fan shared types across worktrees; start journal/outbox as a second organ until pile B below is honest.

**Process:** parallel **read** (explore agents). One **writer** at a time. Parent keeps the contract short. `src/palm/AGENTS.md` §1.1 / §1.2.

### Next motion (ordered, not stamps)

| Pile | Job | Notes |
|------|-----|--------|
| **A** | Dead costume | STATUS still said “structure manager” in the header. Delete `allow_background_drain` (serialize only). Collapse `dna_lists_work_drain` in `seed.py` (walker / `has_capability` is enough). |
| **B1** | Wire must not freelance `work_drain` | `DEFAULT_CONTINUOUS_DEFINITIONS` registers at `supervisor.wire`; assemble then drops if unlisted. Hand is the only register. |
| **B2** | Refuse reads DNA, not composition caps | `assembly_capabilities` still copies composition into refuse. That is why composition still lists the name. |
| **B3** | Stop writing the name on composition / flag | After B2: drop preset `"work_drain"`, seed-map row, `enable_work_drain_service` fold. Then `refuse:background_drain` can die (omit is enough). |
| **C** | Later or optional | Coordinator `_start_plane` / `host.start_plane` alias. `getattr(shell, "assembly")` (seat the organ). Journal/outbox **hands** = exit proof, not cleanup. DNA `requires` — do not invent. |

A and B3 must not write `seed.py` at the same time. B is sequential (B1 → B2 → B3). Coordinator plane may sit beside B1 if files do not collide.

**Start next session:** cut [§7](../architecture/appendix/structure-materialize-cut.md#7-next-motion-after-compact) → census **B1** (who calls supervisor `install` / continuous catalog). Cheap A may land in the same motion.
