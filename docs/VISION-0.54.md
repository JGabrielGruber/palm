# VISION 0.54 — The Library Pipeline (Palm builds the canopy)

**Status:** 📋 **Queued** — opens after **0.53 Sovereign Runners** lands enough of the neonroot provider that hermetic steps are real.  
**Theme:** Build the Living Library with a **Palm pipeline / wizard / durable flow** — capability pressure on the engine, not a shell that calls `just`.  
**Depends on:** [VISION-0.52](VISION-0.52.md) (SOURCE / BUILD / SURFACE) · [VISION-0.53](VISION-0.53.md) (neonroot provider + tool images).  
**Not:** wrapping `just docs-build` in a Palm step and calling it dogfood.

> *0.52 named the library. 0.53 gave it honest hands. 0.54 teaches the hands a sequence.*

---

## Why after 0.53

Without sovereign runners, “Palm builds the docs” collapses to:

```text
Palm step → subprocess(["just", "docs-build"])
```

That exercises almost nothing of Palm’s value (resources, compensation, resume, Assist, multi-provider graph). With **0.53**:

```text
Palm pipeline
  → neonroot.spawn(palm-docs, docs_build)
  → neonroot.spawn(palm-docs, docs-css)     # optional
  → file / inventory checks
  → (later) publish hint / Assist handoff
```

Dogfood is **orchestration of isolation + artifacts**, not CLI cosplay.

---

## Intent (preview — refined at 0.54.0)

| Goal | Detail |
|------|--------|
| **Definition** | A published flow (pipeline or wizard) “Rebuild Living Library” |
| **Steps** | Resource steps via `neonroot` (+ maybe `file` for gates); reuse `scripts/docs_build.py` as the work unit inside the image |
| **Durability** | Instance resume if a long spawn is interrupted |
| **Surfaces** | CLI / Assist / optional Explorer — same operator loop |
| **Honesty** | Keep thin `just docs-build` for humans; Palm path is alternative metabolism, not a delete of 0.52 |

### Explicit non-goals (until 0.54.0 locks)

- Replacing Cloudflare with Palm hosting  
- Full DocsService CMS  
- Perfect efficiency (inefficiency is acceptable gym equipment)  
- Implementing before neonroot `spawn` is trustworthy  

---

## Slice sketch (to be locked at 0.54.0)

| Patch | Direction |
|-------|-----------|
| **0.54.0** | Plan + ADR (pipeline shape: pipeline pattern vs wizard vs hybrid) |
| **0.54.1** | Flow definition + resource steps calling neonroot |
| **0.54.2** | Characterization / e2e (sandbox or recorded) |
| **0.54.3** | Assist entry / operator UX |
| **0.54.4** | Compensation / failure semantics for failed spawns |
| **0.54.5** | Docs: LIBRARY + DEVELOPMENT — two metabolisms (just vs Palm) |

---

## Exit criteria (draft)

- A Palm definition can rebuild `docs/_build/deploy` via neonroot without the host needing Node.
- Documented difference vs `just docs-build`.
- No claim that “subprocess just” is the dogfood path.
- 0.52 builder remains the kernel of the work unit.

---

*The library grows. The runners isolate. The pipeline is Palm remembering how it tends itself.* 🌴📚
