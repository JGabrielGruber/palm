# VISION 0.55 — Living Library dogfood domain (optional)

**Status:** 📋 **Queued** — after [VISION-0.54](VISION-0.54.md) hermetic jobs / DAG purpose test.  
**Theme:** Treat documentation as an **optional Palm business process** (analytics-shaped domain), not core platform.

> *Palm already runs hermetic jobs and graphs. 0.55 asks Palm to use them for its own canopy — as a guest domain.*

---

## Intent

| Do | Don’t |
|----|--------|
| Optional composition service **docs** when wanted | Force library product into every embed |
| Definitions pack: rebuild process, resources, corpora as **config** | Grow product code in `palm.common` |
| Use **neonroot** only for steps that need tools (CSS, generators) | Require neonroot for plain markdown pin |
| Use **kv** / general storage for pins if product needs live query | Invent a second storage engine for docs |
| Thin DocsService: status/get/trigger process | God service that owns NeonRoot + all generators |

---

## Depends on 0.54

- Hermetic job resource contract (neonroot)  
- Multi-step definition graph (wizard chain and/or **dag**)  
- Clear split: Palm graph vs tmpfs job  

---

## Slice sketch (lock at 0.55.0)

| Patch | Direction |
|-------|-----------|
| **0.55.0** | Plan + ADR (docs domain boundaries) |
| **0.55.1** | Definition pack: rebuild Living Library process |
| **0.55.2** | Optional DocsService (compose-in) |
| **0.55.3** | Assist/MCP progressive surface |
| **0.55.4** | Corpora as high-level steps (wiki, mcp inventory, …) |
| **0.55.5** | Edge export phenotype from product pin or host `_build` |

---

## Non-goals

- Making docs required for Palm core  
- Replacing 0.52 static `docs/` SOURCE  
- Full CMS  

---

*Dogfood the canopy after the engine proves it can run real work.* 🌴📚
