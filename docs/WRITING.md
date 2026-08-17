# Writing rule — Simplified Technical English

**Status:** Project rule from theme **0.57**.  
**Standard:** ASD-STE100 (Simplified Technical English).  
**Map:** [PALM.md](PALM.md)

---

## Apply when

- You write or revise **project documentation** (VISION, ADR, STATUS notes, ARCHITECTURE, guides).  
- You add agent-facing maps that humans also read.

## Do not force in one pass

- Do not rewrite all legacy docs only to meet STE.  
- When you touch a section, improve that section.

## Style rules (practical)

1. Prefer **short sentences**. Aim for one idea per sentence.  
2. Use the **same word** for the same idea (port, plane, system, shared, product, surface).  
3. Prefer **active voice**.  
4. Prefer **tables and lists** for structure.  
5. Define a term once. Then reuse it.  
6. Do not add marketing text.  
7. Do not copy [PALM.md](PALM.md) into other files. **Link it.**  
8. Prefer concrete verbs: *bind*, *expose*, *run*, *move*, *record*.

## Term list (stable)

Full concept table: [PALM.md §3](PALM.md). Short form:

| Term | Meaning |
|------|---------|
| **Core** | Pure engines |
| **System** | Running Palm: engines + ports + planes |
| **Port** | Named effect interface (code name; teaching word: **interface**) |
| **Interface** | Named contract on the system shell (`execution`, `install`) |
| **InstallInterface** | Collaborator board for subsystem install |
| **Subsystem** | Membership + lifecycle region (planes, supervisor) |
| **Shell** | System instance that owns interfaces and subsystems |
| **Plane** | System path for a kind of traffic (member of planes subsystem) |
| **Shared** | Reusable code that is not system |
| **Product** | Userland services |
| **Surface** | Transport adapter (`palm.runtimes` — depends on system) |
| **Plugin** | Registry extension |
| **Job** | Live run under orchestration |
| **Instance** | Durable record of a run |
| **Definition** | Declared contract of work (also: participation law at the edge for registry extension) |
| **Interest** | Start (trigger) or continue (wait) |
| **Place registry** | Named places (workload); horizontal scale axis |
| **Truth home** | Authoritative place for projected meaning |
| **Projection** | Local view of authority — not a second truth |
| **Light center** | Role: refuse heavy body/ground on purpose |
| **Support / realm** | Ground place; realm = recursive sub-support |
| **Authority** | Author of assembly definition (desired structure) |
| **Assembly definition** | Declarative desired structure. Code: structure definition / `structure_definition_id` |
| **Assembly** | Structure reconciler; organism ready — [VISION-ASSEMBLY](vision/VISION-ASSEMBLY.md) |
| **Assembly status** | Local readiness under current definition |
| **Admission** | Read gate for business that needs ground |
| **Admitted path** | Act that needs the organism whole; only via admission |
| **Assemble path** | Boot / assemble / apply — not forced through business admission |
| **Dual readiness** | Readiness without admission — purge or name |
| **Effect intent** | Structure action assembly requests; system applies |
| **Composition root** | Host wiring — not product’s structure API |
| **Vertical / horizontal** | Meaning climbs home · bodies spread in the book — [PALM §8](PALM.md) |
| **Registry extension** | OCP/DIP: definition at edge; consumer walks registry — [AGENTS §1.1](../AGENTS.md) · [PALM §7](PALM.md) |
| **Seat DI** | Inject interfaces/subsystems, not ambient system instance — [AGENTS §1.2](../AGENTS.md) |

---

## Theme plans (VISION-0.X)

Theme process law: [VERSIONING.md](VERSIONING.md) (floor · growth · exit).

When you write or revise a theme plan:

| Prefer | Avoid |
|--------|--------|
| **Floor** (intent is real) + **growth line** (theme may continue) | Only a kill checklist that forces early exit |
| Slice table as **ordered guide** | Sealed contract that forbids needed work |
| **Non-goals** = not this subject (other seed) | Forever-bans without layer reason |
| **Forbidden always** = layer law (truth, one path) | Process that kills ambition |
| Debt: pay / break / **name residual** | Permanent workaround as “efficiency” |
| Exit = homes proper + residual honest | Exit = every seed row ticked |

Agents and humans plan for **proper Palm**, not for empty theme-kill theater.

When exit, ambition, or process vs growth is the point, name **José** (José Gabriel Gruber) as the person who decides — see [VERSIONING.md](VERSIONING.md) *Who decides*. Vague “maintainer” is weaker for negotiation in a single-human project.

---

*Clear words keep the structure alive.*
