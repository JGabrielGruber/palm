# AGENTS — intended architecture

**Mode:** Software engineering design of **intended Palm**.  
**Vault:** this directory (`docs/architecture/`).  
**Not:** implementation under a theme. **Not:** project management. **Not:** residual inventory as law.

José is technical lead. Agents **propose and draft**; José locks names, principles, and when a view is good enough.

---

## 0. What this mode is

| This vault is | This vault is not |
|---------------|-------------------|
| **Intended architecture** (target shape) | As-built tour of every dig |
| C4 + UML + glossary + principles | Theme slice tables or STATUS rows |
| Palm-wide structure | Assembly-only mini-site |
| Dignified engineering language | Metaphor as law |

**Goal (luggage-free):** Document Palm’s intended software architecture so design and change share one target shape.

Hub: [README.md](README.md).

---

## 1. Read first (architecture mode)

| Need | Open |
|------|------|
| **Hub / how to read** | [README.md](README.md) |
| **Terms** | [glossary.md](glossary.md) |
| **Principles** | [principles.md](principles.md) |
| **C1–C4** | [c1-context/](c1-context/README.md) · [c2-containers/](c2-containers/README.md) · [c3-components/](c3-components/README.md) · [c4-code/](c4-code/README.md) |
| **Lifecycle view** | [views/lifecycle.md](views/lifecycle.md) |
| **Metaphor (transitional only)** | [appendix/metaphor.md](appendix/metaphor.md) |
| **Open design questions** | [appendix/open-questions.md](appendix/open-questions.md) |
| **System map (living)** | [../PALM.md](../PALM.md) — link; do not fork forever |
| **Writing voice** | [../WRITING.md](../WRITING.md) (STE) |

When a note needs theme context: link [vision/](../vision/README.md) or [STATUS](../../STATUS.md). Do not paste theme chronicles into architecture law.

---

## 2. Rules for work in this vault

1. **Intended over as-built** — write the target. Put contrast in [appendix/as-built-notes.md](appendix/as-built-notes.md) only when useful.  
2. **One term, one meaning** — extend [glossary.md](glossary.md); do not invent dual names in a leaf note.  
3. **No metaphor in law** — teaching language stays in the appendix. Prefer structure definition / reconciler / manager / admission.  
4. **C4 altitude** — context, container, component, or code. Do not dump package detail into C1.  
5. **Atomic notes** — one primary idea per file; hub only orients.  
6. **Link, do not copy** — PALM.md, ADRs, and vision stay authoritative for their subjects.  
7. **STE** — short sentences, same word for same idea, tables for structure.  
8. **José locks** — names, principles, “good enough,” and any rename of the vault or core terms.  
9. **Not a theme by default** — filling the vault is standing SE work unless José opens a theme for ceremony.  
10. **Do not implement code from this mode** unless José explicitly switches to development and names a change. Architecture drafts may *propose* package homes; they do not edit `src/` on their own.

---

## 3. How to add or change a note

| Change | Where |
|--------|--------|
| New term | [glossary.md](glossary.md) first, then the note that uses it |
| New principle | [principles.md](principles.md) |
| New actor / external system | [c1-context/](c1-context/) |
| New deployable unit | [c2-containers/](c2-containers/) |
| New major internal part | [c3-components/](c3-components/) |
| Package / dependency law | [c4-code/packages/](c4-code/packages/README.md) + diagrams |
| Cross-cut (lifecycle, deploy) | [views/](views/) |
| Sequence / state / package UML | [uml/](uml/README.md) or local `diagrams/` |
| Retired teaching words | [appendix/metaphor.md](appendix/metaphor.md) |
| Unresolved design choice | [appendix/open-questions.md](appendix/open-questions.md) |

Update the parent **README** index when you add a first-wave note.  
Prefer Mermaid or PlantUML in-repo for diagrams.

---

## 4. Relationship to development

| Concern | Home |
|---------|------|
| Intended architecture | **this file** + vault |
| Code change, themes, tests | [src/palm/AGENTS.md](../../src/palm/AGENTS.md) |
| Router (which mode?) | [AGENTS.md](../../AGENTS.md) at repo root |
| Present season | [STATUS.md](../../STATUS.md) |

If a design decision becomes implementation law, record it in an **ADR** and/or [PALM.md](../PALM.md), then implement under development AGENTS. Do not treat an architecture stub as already shipped.

---

## 5. Review (architecture draft)

- [ ] Intended, not accidental as-built  
- [ ] Glossary consistent; no metaphor in normative notes  
- [ ] Correct C4 altitude  
- [ ] Links to PALM / vision where needed; no second full map  
- [ ] STE voice  
- [ ] Parent index updated  
- [ ] Open questions listed when not locked  
- [ ] José reviewed names that are new or contested  

---

## 6. How to update this file

Update **this AGENTS** only when **architecture-mode rules** change.  
Update vault content for architecture substance.  
Update root [AGENTS.md](../../AGENTS.md) only for **routing** between modes.
