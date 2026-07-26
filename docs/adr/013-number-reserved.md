# ADR-013 — number reserved (unused)

## Status

**Vacant** — July 2026 (documented in 0.52.5 / PD-020). This is **not** an architecture decision.

## Context

The ADR sequence in `docs/adr/` runs **001–012**, then **014** onward. Number **013** was never assigned to a record. The gap was flagged in the docs audit and TECH-DEBT **PD-020** as “discipline broken.”

## Decision

1. **Leave 013 empty.** Do not renumber 014–021 (or later) to close the gap — that would break every external link and git history reference.
2. **Do not invent a backdated decision** solely to occupy 013. Vacant numbers are honest; fake ADRs are not.
3. **New ADRs** take the next free integer after the highest existing file (today: after 021 → **022**), not 013.

## Consequences

- The index ([README.md](README.md)) lists 013 as vacant so scanners and humans stop treating it as missing work.
- PD-020’s “013 missing” item is satisfied by **explicit reservation**, not by rewriting history.

## Links

- [docs/adr/README.md](README.md)  
- [TECH-DEBT.md](../../TECH-DEBT.md) PD-020  
- [VISION-0.52](../VISION-0.52.md)  
