# VISION 0.53 — Sovereign Runners (NeonRoot as a Palm provider)

**Status:** 🟢 **Open (0.53.0)** — plan + [ADR-022](adr/022-neonroot-provider.md).  
**Theme:** Make **hermetic execution** a first-class Palm capability: NeonRoot is not only a justfile habit for CI — it is a **provider** the resource engine can invoke.  
**Lineage:** ADR-016 (NeonRoot CI) · ADR-003 (provider apps) · Living Library BUILD (0.52) · composition capabilities (0.51).  
**Sequel:** **[VISION-0.54](VISION-0.54.md)** — Palm **pipeline** builds the Living Library *on* these runners (docs dogfood).

> *Register downward. Isolate honestly. Orchestrate the tools — do not become them.*

---

## True intent

Palm already knows how to talk to the outside world through **providers** (`rest`, `kv`, `file`, compositional **`palm`**, …). Separately, the project already runs **hermetic checks** via NeonRoot (`just ci-sandbox`, ADR-016): git-seeded sandboxes, thin images, no cloud required.

Those two stories have not met.

0.53 is the meeting:

| Today | 0.53 |
|-------|------|
| `just ci-sandbox` shells to NeonRoot | Palm **resource** `provider: neonroot` · `action: spawn` |
| `docs/node_modules` for Tailwind | Optional **`palm-docs` image** tools (provider can spawn the build) |
| “Hermetic” is operator folklore | Catalogued capability: health, images, spawn, results |
| Docs pipeline dogfood | **Deferred to 0.54** — needs runners first, or it fakes dogfood |

**Not this minor:** a Palm flow that only shells `just docs-build` and calls itself dogfood. That is 0.54’s *opposite* of the goal, and without a neonroot provider it is the only cheap lie available.

---

## Thesis

```
  Assist / wizard / pipeline / CLI
              ↓
     ResourceEngine  →  provider_registry["neonroot"]
              ↓
        neonroot spawn --sandbox --seed …
              ↓
     palm-ci | palm-docs | palm-audit  (tool phenotypes)
              ↓
     ruff · pytest · docs_build · tailwind · audit …
```

**NeonRoot is isolation metal. Palm is the story.**  
Same grammar as REST or the `palm` provider: `invoke(action, params)` → structured result + optional events.

### Tool phenotypes (images as resources)

| Image (working names) | Role | Host need |
|----------------------|------|-----------|
| **`palm-ci`** | already exists — ruff, pytest, guards, uv | none for checks |
| **`palm-docs`** | `docs_build.py` + Tailwind/Node *or* standalone CSS binary | no `docs/node_modules` required |
| **`palm-audit`** *(optional)* | radon, xenon, bandit, vulture | thin default workspace |

Workspace **profiles** (desk composition — not app CompositionProfile, but same spirit):

| Profile | Host | Images |
|---------|------|--------|
| Genome / edit | git + uv + runtime deps | — |
| Check | optional local tools | palm-ci |
| Docs canopy | optional | palm-docs |
| Full weight | everything local | optional |

Full-weight workspaces remain **first-class**. Images are the ideal default for tools, not a ban on fat laptops.

---

## Provider contract (locked by ADR-022)

### Package

`palm/providers/neonroot/` — ProviderApp layout ([PROVIDER-APPS](PROVIDER-APPS.md)):

- `provider.py` — `BaseProvider` (`invoke`, `describe`, `health`)
- `app.py` — `name = "neonroot"`, actions list, `ready()`
- `bindings/` as needed (resource contract first)
- Optional extra: `palmengine[neonroot]` or experimental gate if CLI missing (truth-seeking / PD-023)

### Actions (v0)

| Action | Params (sketch) | Result |
|--------|-----------------|--------|
| `health` | — | neonroot present, vaults/images reachable |
| `spawn` | `image`, `vault?`, `seed` (`git-archive` \| path), `command[]`, `env?` | exit code, stdout/stderr tails, duration |
| `image.ensure` / `image.build` | `name`, `containerfile?` | image id / status |
| `list_images` | `vault?` | catalog rows |

### ResourceDefinition examples

```text
# Hermetic Living Library build (no Palm pipeline yet — single resource step)
provider: neonroot
action: spawn
params:
  image: palm-docs   # or palm-ci if docs tools baked there
  seed: git-archive
  command: ["uv", "run", "python", "scripts/docs_build.py"]
```

```text
# Existing CI story, product-shaped
provider: neonroot
action: spawn
params:
  image: palm-ci
  seed: git-archive
  command: ["just", "ci"]
```

### Explicit non-goals (0.53)

- Reimplement containers inside `palm.core`
- Require NeonRoot for all Palm installs (optional provider / clear skip)
- Multi-cloud runner abstraction (k8s, Fly, GHA) — NeonRoot first; others later providers
- Full docs **pipeline** definition (0.54)
- DocsService CMS

---

## Slice sequence

| Patch | Slice | Notes |
|-------|--------|------|
| **0.53.0** | Plan — this VISION + ADR-022 | Theme open |
| **0.53.1** | Provider scaffold — `ProviderApp` + registry + `health` (honest fail if CLI missing) | Edge registration |
| **0.53.2** | `spawn` — git-archive seed + command; characterization tests (mock or neonroot-if-present) | Core verb |
| **0.53.3** | Resource bindings + one example definition / `examples/` | ResourceEngine path |
| **0.53.4** | `palm-docs` image (or extend palm-ci) + Tailwind-in-image path; `just docs-css-sandbox` | Thin workspace option |
| **0.53.5** | Wire just recipes through provider-friendly entrypoints (`docs-build-sandbox` stays; optional Palm CLI/resource) | Operator UX |
| **0.53.6** | Events + doctor surface (spawn lifecycle; neonroot section) | Observability |
| **0.53.7** | Assist / MCP path *(optional)* — “run hermetic check/build” via resource or thin assist alias | Operator loop |
| **0.53.8** | Composition note — optional capability or settings flag for neonroot availability | 0.51 grammar |

---

## Relationship to 0.52 and 0.54

```text
0.52 Living Library     SOURCE / thin BUILD / deploy canopy
         │
         ▼
0.53 Sovereign Runners  neonroot provider · tool images · hermetic spawn
         │
         ▼
0.54 Library Pipeline   Palm pipeline/wizard that *is* the docs build
                        (steps invoke neonroot + file + inventory — not just wrap just)
```

0.52’s `scripts/docs_build.py` **stays**. 0.53 teaches Palm to **run it hermetically**. 0.54 teaches Palm to **own the graph**.

---

## Exit criteria

- `neonroot` provider registered (optional install path documented).
- `health` + `spawn` work with characterization tests (skip or mock when NeonRoot absent in CI without the binary — policy in ADR).
- At least one resource definition or example runs `docs_build` or `ci` via the provider.
- Documented path to **no host `docs/node_modules`** for canopy CSS (image or committed CSS + image rebuild).
- STATUS / CHANGELOG / PROVIDER-APPS mention neonroot.
- 0.54 plan exists and is the sole owner of pipeline dogfood language (no fake dogfood in 0.53).

---

## Spirit check

- **Extension by registration** — not host god-object growth.  
- **Truth-seeking** — optional when NeonRoot missing; no silent fake hermetic.  
- **Early structure** — provider stub before every image is perfect.  
- **Enables 0.54** without stealing its theme.

---

*Isolation as a resource. Tools as phenotypes. Palm tells the story.* 🌴🔒
