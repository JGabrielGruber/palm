# Migration — 0.59 System boot + composition truth

**Theme:** [VISION-0.59](../VISION-0.59.md) (**closed**) · **ADR:** [028](../adr/028-system-boot.md) **Accepted**  
**Map:** [PALM.md](../PALM.md) · **Release:** [RELEASE-0.59.8](../releases/RELEASE-0.59.8.md)  
**Inventory:** [BOOT-INVENTORY.md](../BOOT-INVENTORY.md) · **Log:** [SYSTEM-LOG.md](../SYSTEM-LOG.md)

Palm is pre-1.0. This theme makes **start controllable** and **composition truthful**. Most apps keep working; tests and operators that assumed dual capability ORs or private start order need small updates.

## Prefer

| Goal | Use |
|------|-----|
| Boot a declared phenotype | `ApplicationHost.for_mode("test"\|"safe"\|"dev"\|shapes, …)` |
| CI / isolation | `for_mode("test")` or `for_mode("safe")` (+ `PalmSettings.for_tests`) |
| Server shape in tests | `for_mode("server"|"prod", server_port=0, settings=…)` |
| Inspect last boot walk | `host.boot_walk` / doctor `control_plane.boot.last_walk` |
| Membership report | `host.membership_snapshot()` / doctor `boot.membership` |

## Behavior changes (truthful)

| Was | Now |
|-----|-----|
| work_drain background on when composition **or** deployment said so | **Composition only** at the gate (0.59.5). Deployment may *feed* membership once via settings resolver; explicit `CompositionProfile` wins. |
| Recover / background always on for full hosts | **BootMode** may forbid (`safe`/`test`: recover off, background off) |
| Host / runtime start as imperative soup | **Phase tables** walked: `HOST_PHASES` / `SYSTEM_PHASES` |
| Surfaces mount if server role alone | Needs **deployment.server** and non-empty **composition.surfaces** |
| Silent dual paths | Prefer **PhaseSkip** with reason (`composition_off:*`, `mode_*`, `deployment.server_off`) |

## Tests

| Avoid | Prefer |
|-------|--------|
| `pattern="dag", options={"name": "quick"}` (dead since 0.54) | One-step wizard: `tests.helpers.flows.spine_wizard` / `complete_spine_job` |
| Anonymous full host forever | Default fixture `host` is `for_mode("all_in_one")`; lean: `test_mode_host` / `safe_mode_host` |

## Not broken by 0.59

| Area | Note |
|------|------|
| Job path / wait / session law | Unchanged verbs |
| `INSTALLED_*` plugins | Still plugins; planes still **not** install-list items |
| WorkIntent store / system `planes.work` | Still exists; **start** of continuous drain remains host workplane residual (**BI-013**) |
| Dual root `ServerContext` | Still residual (**BI-003**) |

## Residual after theme close

| Open | Kind |
|------|------|
| **BI-003** | Dual composition root (`ServerContext` vs host) |
| **BI-007** | Remaining hand-built hosts (fixture + dogfood paid; not full suite force) |
| **BI-009** | Settings / profile / options triple override clarity |
| **BI-010** | Surface chrome bulk → [VISION-SURFACE-DEFLATION](../VISION-SURFACE-DEFLATION.md) |
| **BI-013** | Work **start** on host workplane (may stay host-owned) |
| **BI-014** | `ensure_host_session` swallow Exception |
| **BI-015** | System log richer catalog / sinks |
| **BI-004 / BI-005** | Fine-grain plugin vs hooks narrative (schedules walk; residual docs/edge cases) |

See [TECH-DEBT.md](../../TECH-DEBT.md) **BI-***.
