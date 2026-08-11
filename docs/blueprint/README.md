# Palm — intended architecture

**Role:** Software engineering **architecture description** of **intended Palm**.  
**Not:** project management (use [STATUS.md](../../STATUS.md) · themes · debt).  
**Not:** a tour of every as-built dig (optional later in [appendix/as-built-notes.md](appendix/as-built-notes.md)).

**Status:** Skeleton (2026-08-08). Fill notes over time. Empty leaves are intentional.

**Map:** [PALM.md](../PALM.md) · themes [vision/](../vision/README.md) · writing [WRITING.md](../WRITING.md)

---

## How to read

This vault uses **C4 altitudes** plus cross-cuts. Prefer **links** over copying PALM.md.

| Path | C4 / role |
|------|-----------|
| [c1-context/](c1-context/README.md) | Level 1 — system in the world |
| [c2-containers/](c2-containers/README.md) | Level 2 — process / deployable units |
| [c3-components/](c3-components/README.md) | Level 3 — major internal parts |
| [c4-code/](c4-code/README.md) | Level 4 — intended packages and dependency law |
| [views/](views/README.md) | Cross-cutting views (lifecycle, deployment, …) |
| [uml/](uml/README.md) | UML when C4 is not enough (sequence, state, package) |
| [glossary.md](glossary.md) | Engineering terms (one meaning each) |
| [principles.md](principles.md) | Architectural principles (intended) |
| [appendix/](appendix/README.md) | Metaphor, open questions, as-built contrast |

**Obsidian:** treat this tree as a vault spine. Wikilink notes; hub only orients.

**Diagrams:** store under each area’s `diagrams/` (or `uml/`). Prefer C4 for city map; UML for floor plans.

---

## What this is for

Palm needs a durable **intended** structure so seasons (including structure management / assembly) can be designed against something stable. Theme plans own **when**; this blueprint owns **how Palm is meant to be shaped**.

---

## Index (first wave)

| Note | Intent |
|------|--------|
| [glossary.md](glossary.md) | Clean language |
| [principles.md](principles.md) | Design laws |
| [c1-context/](c1-context/README.md) | Actors and external systems |
| [c2-containers/](c2-containers/README.md) | Palm process, storage, workers |
| [c3-components/](c3-components/README.md) | Structure management, boot, job path, planes, product, surfaces, host |
| [c4-code/packages/](c4-code/packages/README.md) | Package map |
| [views/lifecycle.md](views/lifecycle.md) | Boot → structure ready → business |
| [appendix/metaphor.md](appendix/metaphor.md) | Retired / teaching language |

Fill order suggestion: glossary · principles · c1 · lifecycle view · c3 structure management · c4 package law.
