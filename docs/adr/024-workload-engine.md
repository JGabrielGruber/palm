# ADR-024: WorkloadEngine and the workload plane

## Status

**Accepted** — July 2026 (canonical plan: [VISION-0.56](../VISION-0.56.md)).  
Supplements [ADR-022](022-neonroot-provider.md) and [ADR-023](023-hermetic-jobs.md); does not renumber them.

**Landed foundation (coherent cut):** pure `palm.core.workload` + `WorkloadLeaf` contract tests.  
Runners, CQRS, and neonroot adapter follow remaining 0.56 slices.

## Context

1. Palm extends via **providers** on ResourceEngine ([ADR-003](003-provider-apps.md)). NeonRoot was correctly introduced as a provider for 0.53 dogfood ([ADR-022](022-neonroot-provider.md)).
2. Hermetic jobs (0.54) proved definition graphs + isolated exec ([ADR-023](023-hermetic-jobs.md)), but **isolation ≠ data I/O**. Modeling every backend as “just another provider” does not scale to host/SSH/K8s/peer-Palm, warm workspaces, GPU placement, or Terraform-in-an-image.
3. Product surfaces in Palm are **CQRS-first** ([ADR-009](009-service-cqrs-contributors.md)). A new plane that only exposes a Python engine will be bypassed incorrectly by REST/MCP/Assist.
4. Reactive composition already uses the **orchestration event bus** ([EVENT-PLANE](../EVENT-PLANE.md)): `flow.session.*` / `job.*` → inbound triggers → new work. Workload terminal states must join that plane so **pipelines can follow workloads** without embedding graph logic in the engine.
5. Reactive interests ([ADR-025](025-reactive-interests.md) / 0.55) provide wait/resume; workloads emit lifecycle events and are waited on as `kind=workload`. Session watches ([VISION-SESSION-PLANE](../VISION-SESSION-PLANE.md)) attach later.
6. Unsafe but useful **host** execution must exist for dogfood and slim Compose, **default off**.

## Decision

### D1 — Workload plane and pure engine

Introduce a **workload plane** with pure core **`WorkloadEngine`** under **`palm/core/workload/`**:

- Operations: `start`/`place`, `exec`, `status`, `stop`/`collect`  
- Types: `WorkloadSpec`, `Workload`, `WorkloadResult`, `WorkloadHandle`, status enum  
- **`WorkloadRuntime` protocol** (the base contract) + registry in **core** (not common)  
- **No** imports of neonroot, docker, k8s, SSH SDKs in `palm/core/`

**Package layout (locked):**

| Layer | Path |
|-------|------|
| Engine + protocol | `palm/core/workload/` |
| Placement / ownership / event helpers | `palm/common/workload/` |
| Concrete adapters | `palm/runners/<name>/` (`host`, `neonroot`, `ssh`, `palm`, …) |
| CQRS product API | `palm/services/execution/workloads/` → `ExecutionService.workloads` |

v1 stays in this monorepo (no separate runners git repository). Optional install extras may split adapters later without moving the protocol out of core.

### D2 — Universal WorkloadSpec

All runtimes consume a **versioned, JSON-serializable Spec**. Runtimes adapt; they do not redefine the product language. Commands are **argv lists** (no shell strings in v1). Secrets are **refs**, not inline values in durable logs.

### D3 — Kinds and hermetic policy

Kinds: at least **`run`**, **`service`**, and **`workspace`** (warm exec; may be implemented as service).  
**Hermetic** is an **`isolation` policy** (`host` | `hermetic` | `best_effort`), not the engine name and not synonymous with NeonRoot.

### D4 — Hosts and placement

A small **host registry** describes places (`local`, ssh, peer palm, k8s context, …) with labels (e.g. GPU). Placement policy selects host + runtime; **fail closed** if none match. Host runtime is **never** auto-enabled to satisfy placement.

### D5 — NeonRoot is a runtime; façade is temporary

NeonRoot is a **WorkloadRuntime**. ResourceEngine may retain a **thin façade** (`provider: neonroot`) that delegates to **WorkloadExecutionService**/Engine for compatibility. Long-term conceptual model: runtime, not peer of `kv`/`rest`.

### D6 — Host runtime default off

Ship **host** WorkloadRuntime for dogfood; **disabled by default**; doctor warns when enabled. Unsupported as multi-tenant isolation.

### D7 — Providers consume; blueprints optional

Providers remain ResourceEngine backends. Optional **workload blueprints** on provider/resource definitions allow “materialize then speak.” **Consumption is always the provider interface.** WorkloadEngine does not implement SQL/HTTP business protocols.

### D8 — CQRS under **ExecutionService** (not a top-level WorkloadService)

Product entry is **`WorkloadExecutionService`** nested under the **execution** domain — peer of flows, processes, and providers:

```text
ExecutionService.workloads → WorkloadExecutionService
  palm/services/execution/workloads/
```

CQRS commands/queries/schemas register via the **execution** ServiceCqrsContributor path ([ADR-009](009-service-cqrs-contributors.md)), then REST/MCP/assist aliases/palm provider.

**Rationale:** Workloads are “how execution places isolated work,” the same family as provider invoke and flow sessions — not a Design-like product domain. A separate top-level service multiplies host wiring without benefit. Concrete isolation backends live in **`palm/runners/`**, not under the service package.

Application code paths **must not** call WorkloadEngine directly except tests, WorkloadLeaf contract harnesses, and carefully gated façades.

Minimum commands: `workload.start`, `workload.exec`, `workload.stop`.  
Minimum queries: `workload.get`, `workload.list`, `workload.hosts`, `workload.runtimes`.  
Support **idempotency_key** on start.

### D8b — WorkloadLeaf freezes the pattern contract with the engine

Ship **WorkloadLeaf** (BT leaf) and **contract tests** (leaf + fake WorkloadRuntime + real WorkloadEngine) in the same implementation arc as the core engine (**0.56.1–0.56.2**). That defines how graphs wait, fail, cancel, and complete before multiple patterns invent divergent call shapes. Production leaves may later call `execution.workloads` CQRS; tests bind a narrow port/fake.

### D9 — Events and reactive composition

Emit public **`workload.started`**, **`workload.ready`**, **`workload.failed`**, **`workload.stopped`** on the **orchestration** event bus (same plane as job/flow events). Payloads stay small (ids, status, exit_code, owner, labels, host_id, artifact refs).

**WorkloadEngine does not start flows or pipelines.**  
Inbound/triggers/work-drain subscribe to `workload.*` and submit flows/pipelines — same pattern as `flow.session.succeeded`.

### D10 — Ownership and cancel

Workloads record owner (`job_id` and/or `instance_id` and/or `lease`). Cancel, compensation, and session teardown **must** stop workloads Palm started. `stop` is idempotent. Leaks are recorded for ops.

### D11 — Palm mesh via palm provider

**`runtime=palm`** delegates Spec to a peer Palm’s workload API (CQRS/REST), implemented through the **palm provider** (and allowlisted base URLs). Mesh hop count is bounded (`max_hops`, default 1). SSH is a separate runtime/host kind (default off, allowlist).

### D12 — Surfaces are not workload runtimes

`palm.runtimes` (CLI, server, daemon, MCP, embedded) remain **process surfaces**. They are not registered as WorkloadRuntimes and are not folded into WorkloadEngine.

### D13 — Extension model

New isolation backends = new packages under **`palm/runners/<name>/`** implementing core `WorkloadRuntime`.  
New “can we run X?” (GPU, terraform image, ruff, docs build) = Spec + image/command + placement labels — **not** new core engines.  
Do **not** put the protocol ABC in `common` (that is core); do **not** put driver clients in core.

## Consequences

### Positive

- Multi-decade extension path without core erosion  
- CQRS-consistent product surface under **execution** (like providers)  
- WorkloadLeaf contract tests lock pattern↔engine semantics early  
- Pipelines and GPU/terraform/mesh without special cases in the engine  
- Slim Compose (host optional) and strong hermetic CI (neonroot/k8s) coexist  
- Clear SRP: allocate / speak / orchestrate / react  

### Negative / costs

- Two extension axes (providers + runtimes) — mitigated by glossary and review checklist  
- Temporary dual path (neonroot provider façade) — mitigated by migration slices  
- More moving parts than “just shell neonroot” — required for safety and growth  

### Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Edges call engine directly | Execution.workloads + CQRS for product; leaf/engine contract tests |
| Top-level WorkloadService sprawl | Nest under ExecutionService like providers |
| Pattern API drift | WorkloadLeaf + contract tests with core engine |
| Host runtime left on in prod | Default off; doctor; hermetic policy rejects host |
| Event bus log floods | Caps, artifact refs, public catalog discipline |
| Mesh open relay | Allowlist peers; max_hops; auth |
| Placement surprise | Fail closed; explicit errors; no silent host enable |
| God execution.workloads service | Policy + placement only; engine owns lifecycle |

## Migration

1. Land engine + host (off) + neonroot adapter.  
2. Point façade `run_script`/`spawn` at service/engine.  
3. CQRS + REST + events + trigger dogfood.  
4. Blueprints + palm remote.  
5. Document MIGRATION-0.56; deprecate dual paths.  

Existing 0.54 definitions remain valid through façades until explicit deprecation.

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Only more ResourceEngine providers | No shared Spec/lifecycle; weak placement/ownership |
| RunnerEngine name alone | Undersells long-lived service/workspace |
| IsolationEngine | Vague; poor API gravity |
| RuntimeEngine including CLI/server | Category error with `palm.runtimes` |
| Engine starts pipelines internally | Violates SRP; duplicates inbound/triggers |
| Always-on host exec | Unsafe default |
| Separate ServiceEngine vs RunEngine | Two allocators for one problem |
| No CQRS (engine-only API) | Breaks Palm edge consistency; encourages bypasses |
| Top-level `services/workloads` domain | Duplicates execution; providers already live under execution |
| Engine without WorkloadLeaf tests | Patterns invent incompatible wait/cancel semantics |

## Compliance checklist (review / merge)

- [x] No neonroot/docker/k8s imports under `palm/core/`  
- [ ] Product start path uses **execution** CQRS (`workload.*`)  
- [x] WorkloadLeaf contract tests (engine + fake runtime) green  
- [x] Host runtime default off (settings + engine policy + doctor warn when on)  
- [x] Hermetic policy cannot select host (engine unit test)  
- [x] Cancel/compensation stops owned workloads (engine `stop_owned` + leaf contract test)  
- [x] `workload.*` events small (unit test); trigger path dogfood later  
- [ ] Provider blueprint does not skip provider for business I/O  
- [ ] Peer palm allowlisted  
- [x] Glossary updated (HERMETIC-JOBS / AGENTS)  

## References

- [VISION-0.56](../VISION-0.56.md) · [VISION-0.55](../VISION-0.55.md) · [VISION-0.54](../VISION-0.54.md) · [VISION-0.31](../VISION-0.31.md)  
- [ADR-003](003-provider-apps.md) · [ADR-009](009-service-cqrs-contributors.md) · [ADR-022](022-neonroot-provider.md) · [ADR-023](023-hermetic-jobs.md)  
- [HERMETIC-JOBS.md](../HERMETIC-JOBS.md) · [EVENT-PLANE.md](../EVENT-PLANE.md) · [AGENTS.md](../../AGENTS.md)
