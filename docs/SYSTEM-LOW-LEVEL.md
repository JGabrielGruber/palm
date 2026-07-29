# Palm System — low-level design (0.57)

**Status:** Normative for theme **0.57** execution.  
**Language:** ASD-STE100 Simplified Technical English.  
**Map (high level):** [PALM.md](PALM.md)  
**Plan:** [VISION-0.57.md](VISION-0.57.md) · **ADR:** [026-palm-system-layer.md](adr/026-palm-system-layer.md)  
**Debt:** [TECH-DEBT.md](../TECH-DEBT.md) (SD-*)

This file is the **low-level** definition.  
It names packages, ports, moves, and acceptance checks.  
It does not replace [PALM.md](PALM.md).

---

## 1. Goal of the low-level design

1. Make **system** a real place in the tree.  
2. Define **ExecutionPort** as the first effect contract.  
3. Order moves so Palm stays green.  
4. Bind debt IDs to concrete files.

---

## 2. Target package layout

### 2.1 New top-level: `palm.system`

```text
src/palm/system/
  __init__.py              # public: SystemInstance protocol, ports
  instance.py              # protocol / façade of a running Palm
  ports/
    __init__.py
    execution.py           # ExecutionPort protocol + types
  runtime/
    __init__.py
    base.py                # moved from common.runtimes.base (when ready)
    host.py                # system host protocol (replaces thin RuntimeHost)
    wiring.py              # scheduler resolve helpers (from common if system-owned)
    hooks/                 # runtime job hooks that are system
  planes/
    wait/                  # from common.wait (continue)
    work/                  # from common.work (start) — or keep stage moves
    workload/              # bootstrap + doctor glue (not runners)
  executions/              # DefinitionExecutor + plan submit (system-adjacent)
```

**Rules:**

- `palm.system` may import `palm.core`, `palm.definitions`, `palm.instances`, and **shared** libraries.  
- `palm.system` must **not** import `palm.services`, `palm.runtimes` (surfaces), or `palm.patterns` for types that force cycles.  
- Patterns receive **ports** (injected), not system package internals.  
- Product resolves a system instance and uses **ports**.

### 2.2 What stays `palm.common` (shared)

| Keep in common (shared) | Why |
|-------------------------|-----|
| `transforms/` | Reusable rules |
| `cqrs/` | Bus primitives |
| `persistence/` | Repos used by system + product |
| `storage/` | StorageFactory |
| `services/` | BaseService, errors |
| `exceptions.py` | Shared errors |
| `state/` | Schema binding helpers |
| `compensation/` | Registry + coordinator (review if system-adjacent later) |
| `operator/` | Presenters (watch bulk; not kernel) |
| `events/` | Outbox helpers (may follow system later) |

### 2.3 What moves to system (ordered)

| Move wave | From | To | Debt |
|-----------|------|-----|------|
| **A — boundary** | New package + re-export façades | `palm.system` | SD-002 start |
| **B — host contract** | `common/runtimes/host.py` | `system/.../host.py` or ports | SD-003 |
| **C — port** | new | `system/ports/execution.py` | SD-001 |
| **D — BaseRuntime** | `common/runtimes/base.py` | `system/runtime/base.py` | SD-002 |
| **E — planes** | `common/wait`, `common/work` | `system/planes/...` | SD-002 |
| **F — executions** | `common/executions` | `system/executions` | SD-002 |
| **G — workload glue** | `common/workload` | `system/planes/workload` | SD-009 |
| **H — classify** | `common/runtimes/server` | keep or `runtimes` | SD-011 |

**Compatibility:** During cutover, `palm.common.runtimes.base` may re-export from `palm.system` (list under SD-012).  
Remove re-exports before theme exit when guards allow.

### 2.4 `PalmKernel` and `ApplicationHost`

| Type | Stays | Role |
|------|-------|------|
| `palm.app.PalmKernel` | `palm.app` | Infra: storage, instance manager, **registry of system instances** |
| `ApplicationHost` | `palm.app.host` | Product wiring, CQRS, profiles, recovery |
| Concrete surfaces | `palm.runtimes.*` | Thin; subclass or wrap system runtime |

`PalmKernel.create_runtime` builds a **system instance** (today `BaseRuntime`).  
Docstrings must say that (SD-006).

---

## 3. Execution port (v1 contract)

### 3.1 Protocol (normative sketch)

```python
# Conceptual — implement in 0.57.3 under palm.system.ports.execution

class ExecutionPort(Protocol):
    """Effects a started system instance may perform for graphs and product."""

    # --- resource / speak ---
    def invoke_resource(
        self,
        resource_ref: str,
        *,
        provider: str | None = None,
        action: str | None = None,
        params: dict[str, Any] | None = None,
        state: Any = None,
        resource_id: str | None = None,
    ) -> Any: ...

    # --- workload / isolate ---
    def start_workload(
        self,
        spec: Any,
        *,
        owner: Any = None,
        workload_id: str | None = None,
        idempotency_key: str | None = None,
        host_id: str | None = None,
    ) -> Any: ...

    def exec_workload(
        self,
        workload_id: str,
        command: list[str] | tuple[str, ...],
        *,
        timeout_s: float | None = None,
        env: dict[str, str] | None = None,
    ) -> Any: ...

    def stop_workload(self, workload_id: str, **kwargs: Any) -> Any: ...

    def workload_status(self, workload_id: str) -> Any: ...

    # --- job drive (system-owned; product may wrap) ---
    # v1 may expose a narrow JobPort or keep orchestration on the instance
    # until 0.57.5. Do not leave resource/workload on engines only.
```

### 3.2 Implementation

| Piece | Role |
|-------|------|
| `BaseRuntime` (system runtime) | Implements `ExecutionPort` by delegating to engines |
| Test doubles | Implement `ExecutionPort` without full host |
| `PatternBuildContext` | Holds `execution: ExecutionPort` (plus event/context if still needed) |
| `ProviderExecutionService` | `port.invoke_resource(...)` |
| `WorkloadExecutionService` | `port.start_workload` / `exec` / `stop` / `status` |

### 3.3 What is out of port v1

| Concern | Where |
|---------|--------|
| CQRS dispatch | Product / host |
| Authz policy | Product (then port) |
| Wait match | Wait plane (system), not execution port |
| Trigger drain | Work plane (system) |
| Definition catalog CRUD | Product definitions |

### 3.4 Job drive note

Definition submit and `resume_job` are system-owned.  
v1 may:

- **Option A:** methods on `ExecutionPort`, or  
- **Option B:** `SystemInstance.orchestration` / `JobPort` sibling.

**Prefer Option A or a clear `JobPort`** before theme exit so edges stop importing engine types.  
Record choice in 0.57.3 notes; update this file.

---

## 4. System instance protocol

```python
class SystemInstance(Protocol):
    """One started running Palm (today: BaseRuntime)."""

    @property
    def is_started(self) -> bool: ...

    @property
    def execution(self) -> ExecutionPort: ...

    # Planes (properties or attributes)
    # event bus for orchestration
    # wait_plane when attached
    # ...
```

`RuntimeHost` is **superseded** by `SystemInstance` + ports (SD-003).  
During cutover, `RuntimeHost` may remain as a structural subset for old type hints.

---

## 5. Classification of `palm.common` (today)

| Subpackage | System | Shared | Product/surface | Action |
|------------|:------:|:------:|:---------------:|--------|
| `runtimes/base`, wiring, hooks | ● | | | → system |
| `runtimes/host` | ● | | | → system ports |
| `runtimes/server` | | ◐ | ● | classify SD-011 |
| `runtimes/schedulers` | ● | | | → system |
| `wait` | ● | | | → system planes |
| `work` | ● | | | → system planes |
| `workload` | ● | | | → system planes |
| `executions` | ● | | | → system |
| `hooks` | ● | | | → system |
| `plans` | ● | | | → system (with executions) |
| `patterns` (materialize) | ◐ | ● | | keep shared registry glue; builders use port |
| `persistence` | | ● | | stay |
| `managers` | | ● | | stay (or system-adjacent) |
| `cqrs` | | ● | | stay |
| `transforms` | | ● | | stay |
| `events` | ◐ | ● | | outbox: shared; wire at system start |
| `compensation` | ◐ | ● | | stay shared until proven system |
| `operator` | | ● | ● | stay; not kernel |
| `resource` (common helpers) | | ● | | stay |
| `triggers` | ● | | | system / work plane |
| `surfaces` | | | ● | later with surfaces |
| `websocket` | | | ● | surface kit |
| `services` | | ● | | BaseService stay |
| `interactive_runtime` | ● | | | system or product assist helper — classify in 0.57.5 |
| `job_inspection`, `job_context` | ● | | | system-adjacent |

● = primary · ◐ = mixed

---

## 6. Rebind plan (graphs and product)

### 6.1 Graphs (0.57.4)

1. Add `execution: ExecutionPort | None` to build context.  
2. Builders pass port into patterns/leaves.  
3. `ResourceLeaf` / workload leaves call port methods.  
4. Keep engine fields only as deprecated shims (SD-012) until tests green.  
5. Remove engine fields from public build context.

**Core leaf note:** `ResourceLeaf` in `palm.core` today takes `ResourceEngine`.  
Options:

| Option | Trade-off |
|--------|-----------|
| **P1** Leaf stays on engine; port adapts at pattern layer | Core pure; dual types at edge of core |
| **P2** Leaf takes a small Protocol defined in core | Best long-term; core defines `ResourceInvoker` protocol |
| **P3** Leaf moves out of core | Large; avoid in 0.57 |

**Choose P2 if small:** core protocol for invoke only; system port implements it; engine implements it.  
**Choose P1** if P2 expands 0.57 too far — record as residual SD.

### 6.2 Product (0.57.5)

1. `ProviderExecutionService.invoke` → `runtime.execution.invoke_resource`.  
2. `WorkloadExecutionService` → `runtime.execution.*_workload`.  
3. Flow session resume → job port or orchestration via system instance API (not random edge fields).  
4. Update CQRS handlers only if they bypass services.

### 6.3 Edges (0.57.7)

1. Explorer SSR: go through product or execution port.  
2. `PalmKernel.invoke`-style helpers: port.  
3. palm provider local path: port.  
4. Any remaining site → SD-005 bullet.

---

## 7. Guards and enforcement

| Guard | Intent |
|-------|--------|
| `guard_core` | Unchanged: core purity |
| `guard_common` | Keep pattern ban; later **forbid new system modules in common** |
| New `guard_system` (optional 0.57.2+) | `palm.system` must not import services/runtimes/patterns |
| Import seams | ADR-017 still applies; new seams need comments |

**Rule for agents:** New effect APIs go on the port, not on a new `runtime.xyz` field for edges.

---

## 8. Slice acceptance (executable)

### 0.57.1 — Debt + low-level (this slice)

- [x] Old TECH-DEBT archived under `docs/audit/`  
- [x] Live `TECH-DEBT.md` with SD-*  
- [x] This low-level design exists  
- [x] VISION / STATUS point at live debt and this file  

### 0.57.2 — System boundary in code

- [ ] `palm.system` package exists with public `__init__`  
- [ ] `SystemInstance` and/or `ExecutionPort` module stubs (even if BaseRuntime not moved)  
- [ ] Docstrings: BaseRuntime is system instance  
- [ ] Guard or test: system package import rules  
- [ ] SD-012 lists any re-export shims  

### 0.57.3 — Execution port v1

- [ ] `ExecutionPort` implemented by BaseRuntime (or system runtime)  
- [ ] Unit tests with a fake port  
- [ ] Resource + workload methods real  

### 0.57.4 — Graphs rebind

- [ ] PatternBuildContext uses port  
- [ ] Wizard + dag (+ pipeline) resource/workload path use port  
- [ ] Tests green  

### 0.57.5 — Product rebind

- [ ] ExecutionService providers + workloads use port  
- [ ] No new service methods that take raw engines  

### 0.57.6 — Deflate common

- [ ] At least BaseRuntime + wait plane live under system **or** documented residual with SD-002 update  
- [ ] common classification matches reality  

### 0.57.7 — Edge policy

- [ ] SD-005 sample sites fixed or explicitly residual  
- [ ] AGENTS/PALM say no new engine shortcuts  

### Theme exit

- [ ] [VISION-0.57 §10](VISION-0.57.md) exit criteria  
- [ ] ADR-026 → Accepted  

---

## 9. Risks and decisions locked

| Decision | Lock |
|----------|------|
| Package name `palm.system` | Yes for 0.57 unless a blocker forces `palm.kernel` — then update PALM.md |
| Port name `ExecutionPort` | Yes for v1 |
| Break pre-1.0 | Yes |
| No CQRS-only unification | Yes |
| P1 vs P2 for ResourceLeaf | Prefer **P2** (core protocol); fall back P1 with SD note |
| Move all of common in one PR | **No** — waves A–H |

---

## 10. File index for implementers

| Concern | Start here |
|---------|------------|
| High-level map | [PALM.md](PALM.md) |
| This design | [SYSTEM-LOW-LEVEL.md](SYSTEM-LOW-LEVEL.md) |
| Debt | [TECH-DEBT.md](../TECH-DEBT.md) (SD/SU/ST/CS) |
| Intentions (no fake body) | [STUBS.md](STUBS.md) |
| Surfaces | Thin only; SU-* for bypass/bulk; samples in debt |
| Runtime today | `src/palm/common/runtimes/base.py` |
| Host protocol today | `src/palm/common/runtimes/host.py` |
| Build context | `src/palm/common/patterns/build_context.py` |
| Executor | `src/palm/common/executions/executor.py` |
| Provider product | `src/palm/services/execution/providers/service.py` |
| Workload product | `src/palm/services/execution/workloads/service.py` |
| Wait plane | `src/palm/common/wait/plane.py` |

---

*Low-level truth makes high-level law enforceable.*
