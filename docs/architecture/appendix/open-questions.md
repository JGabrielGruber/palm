# Appendix — open questions

**Status:** Living. José locks answers.  
Record decisions in ADRs, [principles.md](../principles.md), or glossary when locked.

---

## Structure definition and membership

- Exact schema of membership sections (`plugins`, `products`, `surfaces`, `capabilities`, refuse, places)?  
- First capability or unit to materialize fully under definition (local compose prototype)?  
- How far does structure definition own bootstrap wire vs host seed still freelancing?  
- Package names: keep `assembly` in code or rename toward `structure`?

---

## Engine vs manager (mostly decided — confirm)

- **Intent:** reconciler (engine) in **core**; manager (seat, loop, hands, materialize, resolvers) in **system**.  
- Open: any pure types that must stay system-only? Any manager API surface on the shell beyond admission + structure effects?

---

## Membership source and Palm provider

- When does **membership source** appear on the definition (`local` only until then)?  
- What is a **definition package** (format, signing, version)?  
- Palm provider protocol for structure: which verbs, which home (support vs authority)?  
- Worker spawn: definition **cut** served by support — what is minimal cut?  
- **Cache / replicate** (provide → local store → local materialize): when is it in scope vs Grove/tunnels?

---

## Scale roles (orchestrator / support / worker)

- Confirm intended: thin orchestrator, support serves definitions/membership, worker uses — under structure definition, not freestyle.  
- Is “support serves custom plugins/products/surfaces” only via **provide definition packages**, or also runtime proxy? (Prefer provide + local materialize unless proxy is required.)

---

## Theme 0.63 exit

- How deep must **structure manager / materialize** be before José exits 0.63 vs admission-floor + named residual?  
- Is architecture vault fill a gate for exit, or parallel standing work?

---

## Package diagram (next SE step)

- First diagram: package families only, or include `core.assembly` / `system.assembly` split in v1?
