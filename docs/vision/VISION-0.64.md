# VISION 0.64

**Status:** **Open** (2026-08-17). José closed **0.63**.  
**Map:** [PALM.md](../PALM.md) · vault [architecture/](../architecture/README.md) · seed [VISION-ASSEMBLY](VISION-ASSEMBLY.md)  
**Prior:** [VISION-0.63](closed/VISION-0.63.md) (closed) · [ADR-032](../adr/032-organism-assembly.md)

**This minor is `work_drain` as the first real capability** — the shape every later organ copies. Not a slice queue. Not host-owned drain. Not a private `if`.

| Law | Meaning |
|-----|---------|
| Structure definition lists the name | Membership |
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

**Commits:** `6e50fd6b` first capability (seats, names, no host drain) · `d1b3c23a` ctx seats, no host listed bag · B1 wire catalog no longer freelances `work_drain`. Master may be ahead of origin. Not pushed.

**Law that landed:** Structure definition lists the name. Walker loops `LOCAL_CAPABILITY_HANDS`. Hand takes `CapabilitySeats`. Assemble fills seats from boot `ctx` + install `work_plane`. Drain start is `system.background.start`. It reads `supervisor.get("work_drain")` (walker effect), not the definition again, not `host._work_drain_listed`. Host schedule ends at ready. The host does not start the loop again. Coordinator, tests, and status read `runtime.work_plane`. Default wire catalog does not register `work_drain`. Composition / flag do not write the name. Omit is enough. No host `start_plane` alias.

**Do not:** invent definition `requires` (the old DNA-requires idea); reuse VitalityRegistry for hands; open a 0.64 slice table; fan shared types across worktrees; start journal/outbox as a second organ until José says the home is copyable.

**Process:** parallel **read** (explore agents). One **writer** at a time. Parent keeps the contract short. `src/palm/AGENTS.md` §1.1 / §1.2.

### Next motion (ordered, not stamps)

| Pile | Job | Notes |
|------|-----|--------|
| **A** | **Landed** — dead costume gone | `allow_background_drain` deleted. Seed twins collapsed. `has_capability` / walker is enough. |
| **B1** | **Landed** — wire catalog does not freelance `work_drain` | Hand is the only register. Unregister-on-unlist stays for reassemble. |
| **B2** | **Landed** — refuse reads definition capabilities | Composition listing the name is not a refuse input. Omit is enough. |
| **B3** | **Landed** — composition / flag do not write `work_drain` | Presets, seed-map row, and the settings/deployment fold are gone. Omit is enough. `refuse:background_drain` is not a live wall. |
| **C** | **Landed** — no host/coordinator `start_plane` alias | Coordinator and status read `runtime.work_plane`. Host schedule ends at ready. Drain start is `system.background.start`. Assemble uses `shell.structure`. No `enable_work_drain_service`. Journal/outbox **hands** = exit proof, not cleanup. Definition `requires` — do not invent. |

A, B1–B3, C landed. Named leftovers paid: assemble uses `shell.structure`; settings/deployment have no `enable_work_drain_service`. Vitality default probes share `attr_resolver` (supervisor, execution, install, structure), `get_system_planes` (hub), and `first_resolver` for process log. Inventory `admission_inventory_snapshot` stays as eyes.

**Start next session:** José judges whether the organ is copyable. Journal as second organ only after that.
