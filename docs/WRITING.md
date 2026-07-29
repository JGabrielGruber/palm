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
| **Port** | Named effect interface |
| **Plane** | System path for a kind of traffic |
| **Shared** | Reusable code that is not system |
| **Product** | Userland services |
| **Surface** | Transport adapter |
| **Plugin** | Registry extension |
| **Job** | Live run under orchestration |
| **Instance** | Durable record of a run |
| **Definition** | Declared contract of work |
| **Interest** | Start (trigger) or continue (wait) |

---

*Clear words keep the structure alive.*
