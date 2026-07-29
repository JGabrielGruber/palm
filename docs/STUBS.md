# Palm — Intention stubs (not fake products)

**Status:** Live from **0.57.1** debt expansion.  
**Language:** ASD-STE100.  
**Debt:** [TECH-DEBT.md](../TECH-DEBT.md) ST-* · SD-013  
**Map:** [PALM.md](PALM.md)

---

## 1. Rule

Palm may **name a future capability** without shipping a lying implementation.

| Allowed | Forbidden |
|---------|-----------|
| Intention row here (purpose + maturity) | Return fake success that looks real |
| Gate: not in default install, or doctor `maturity=stub` | Register as healthy installed capability |
| Loud error on use (`NotImplemented`, clear message) | Silent no-op storage that “opens” |
| Tests for **intention registry** | Tests that freeze fake providers as required installs |

**Pre-1.0:** Prefer delete fake body + keep name in this file over keeping code that lies.

---

## 2. Intention catalog

### 2.1 Patterns

| Id | Purpose (keep) | Current body | Maturity | Debt |
|----|----------------|--------------|----------|------|
| **wizard** | Interactive human/agent flows | Full | **real** | — |
| **parallel** | Scoped branches + merge | Real | **real** | — |
| **pipeline** | Transform sequences | Real | **real** | — |
| **dag** | Resource/workload graph with deps | Real (v0) | **real** | port rebind SD-009 |
| **etl** | Extract → transform → load product pattern | Phase ticker only | **intention** | ST-003 |

**etl purpose (store this, not the ticker):**  
Declarative multi-stage data movement: extract from resources, transform, load to resources — composed with Palm job path and compensation later.

---

### 2.2 Providers (speak)

| Id | Purpose (keep) | Current body | Maturity | Debt |
|----|----------------|--------------|----------|------|
| **rest** | HTTP resource speak | Real | **real** | — |
| **kv** | Local key-value documents | Real | **real** | — |
| **file** | Local file resources | Real | **real** | — |
| **palm** | Palm-to-Palm speak | Real | **real** | SU/port paths |
| **graphql** | GraphQL API speak | Fake dict fetch | **intention** | ST-001 |
| **postgres** | Relational SQL speak | Fake dict fetch | **intention** | ST-001 |

**graphql purpose:** Schema-driven queries/mutations as resource actions.  
**postgres purpose:** SQL and relational resources as provider actions (not the storage backend).

---

### 2.3 Storages

| Id | Purpose (keep) | Current body | Maturity | Debt |
|----|----------------|--------------|----------|------|
| **memory** | Ephemeral process storage | Real | **real** | — |
| **filesystem** | Durable file-backed storage | Real | **real** | — |
| **postgres** | Durable SQL storage engine backend | No-op get/set | **intention** | ST-002 |
| **mongodb** | Durable document storage backend | Placeholder client | **intention** | ST-002 |

Do not confuse **provider postgres** (speak) with **storage postgres** (engine backend).

---

### 2.4 Transforms

| Id | Purpose (keep) | Current body | Maturity | Debt |
|----|----------------|--------------|----------|------|
| **parquet_load** | Load parquet into state | Always raises | **intention** | ST-004 |
| other builtins | See transform catalog | Real | **real** | — |

---

### 2.5 Runners (workload isolation)

| Id | Purpose | Maturity | Note |
|----|---------|----------|------|
| **host** | Run on host process/fs (unsafe) | real, default OFF | OK |
| **neonroot** | Container isolation | real | OK |
| **local** | Slim local runner path | check install | not a lie if wired |
| **ssh / palm / k8s** | Future placement | **intention** | not fake-installed |

---

### 2.6 Surfaces (product edges — not plugins)

Surfaces are **not** stubs of capability; they are **adapters**. Debt is **thickness** and **bypass**, not missing GraphQL.

| Surface | Purpose (keep) | Smell / debt |
|---------|----------------|--------------|
| **embedded** | In-process library runtime | Thin — good |
| **daemon** | Long-lived worker runtime | Thin — good |
| **server / REST** | HTTP product API | OK if via services |
| **server / Explorer SSR** | Human operator UI | SU-001 bypass · SU-002 size |
| **server / WebSocket** | Live Assist / events | SU-007 |
| **MCP** | Agent tools / resources | SU-003 dual stack · SU-004 legacy names |
| **CLI** | Terminal operator | SU-005 legacy aliases |

**Portal (queued):** PWA client of Assist — intention only; do not fork a second drive loop.

---

## 3. Default install policy (target)

| Set | Contains |
|-----|----------|
| **Default install** | real maturity only |
| **Optional / extra** | real drivers when packaged |
| **Intention registry** | this file + doctor section `intentions` |
| **Never default** | fake-success providers, no-op storages, ticker-only patterns |

`tests/test_modular_apps.py` must follow this policy (ST-005).

---

## 4. How to add an intention

1. Add a row here with **purpose** and maturity **intention**.  
2. Add or update ST/SU debt if code still lies.  
3. Do not add a fake `fetch` that returns success.  
4. Prefer empty package + registry flag `installed=False` over a lying class.

---

*Store the purpose. Free Palm from the fake body.*
