# ARCHITECTURE.md

## High-Level Architecture (post 0.3.0-dev clean-core migration)

Palm follows a **layered architecture** with strict separation of concerns.

### Layers

1. **Behavior Tree Engine** (`palm/core/behavior_tree/`)
   - One of the two allowed general-purpose engines in `palm/core/`.
   - General-purpose, reusable Behavior Tree implementation.
   - Core abstractions: `BaseNode`, `LeafNode`, `CompositeNode`, `DecoratorNode`, `Blackboard`.
   - Completely independent of wizards, persistence, CLI, and the Orchestration Engine (orchestration may compose with it optionally via backends).

2. **Shared Core Primitives** (`palm/core/events.py`)
   - `Event` + `EventBus` — minimal, synchronous, in-memory observability bus.
   - Used by the Orchestration Engine today; available to the BT engine and future engines.
   - Lives at the `core/` package root so it can be shared without duplication.

3. **Orchestration Engine** (`palm/core/orchestration/`)
   - The second general-purpose engine in `palm/core/`.
   - Introduces `Orchestrator`, `Job` (with strict status machine + its own independent `Blackboard`), `OrchestrationMode` (Strategy), and the abstract `ExecutionBackend`.
   - **Only** `TestBackend` (pure, deterministic, zero external deps) is allowed as a concrete backend inside this package.
   - All other concrete backends live outside `palm/core/` under `palm/backends/` (e.g. `BehaviorTreeBackend` for composition with the BT engine).
   - Uses the shared EventBus for observability.
   - **Strict rule**: Zero imports from `palm/core/behavior_tree/` (or any domain code) inside `palm/core/orchestration/`.

4. **Legacy Reference Implementation** (`palm/cli/solid/legacy/`)
   - Contains the complete pre-0.3.0 wizard engine, models, persistence, orchestrator, workflow scaffolding, etc.
   - This is a **deprecated reference snapshot only**. It is preserved so the existing Solid CLI continues to work.
   - New code must **never** import from here.

5. **Interface Layer** (`palm/cli/solid/`)
   - The Solid Admin CLI (and future TUIs / servers).
   - Currently wires the legacy implementation. Will be updated as clean layers are built on the two core engines.

General utilities (`config/`, `utils/logging/`) and the base `PalmError` remain at the top level as cross-cutting concerns.

## Key Design Decisions

- **Behavior Tree as Foundation**: Chosen over a simple DAG or state machine because it provides superior support for complex control flow, composition, reusability, and conditional execution while maintaining clean tree semantics.
- **Orchestration Engine + Strategy Pattern**: Added in 0.3.0-dev as the second core engine. `OrchestrationMode` + `ExecutionBackend` (with `TestBackend` as the primary concrete) enable pluggable execution (test, embedded, process, future distributed) without modifying the `Orchestrator`.
- **TestBackend First**: The orchestration engine's own testability and the majority of its contract/edge tests are deliberately independent of the BT engine. `TestBackend` provides deterministic synthetic work descriptors.
- **Shared EventBus**: Minimal observability primitive at `core/events.py` so both engines (and future ones) have a consistent, replaceable event model.
- **Blackboard Pattern**: Adopted for decoupled data sharing across nodes (and still used by Jobs even when driven by TestBackend).
- **OOP Abstractions + SRP**: Strong use of abstract base classes and inheritance to enforce contracts and enable extensibility. Every class has one reason to change.
- **Strict Core Purity**: `palm/core/` contains only general-purpose engines + tiny shared primitives. Zero domain, CLI, or legacy coupling.

## Future Extensibility

Both engines in `palm.core` are intentionally general-purpose:

- Behavior Tree Engine supports complex control flow, interactive leaves, and composition.
- Orchestration Engine (with pluggable modes + backends) supports job lifecycle, concurrency strategies, and observability for any executable (including BT trees).

Together they enable:
- Non-interactive DAG workflows
- Automated ETL processes
- AI agent decision systems
- Rich interactive wizards (rebuilt cleanly on top of the two engines)
- Hybrid human + automated flows

Wizards remain the current primary business need, but the architecture is deliberately broader.

---

Last updated: May 2026 (Orchestration Engine v0.3.0-dev with TestBackend + core events)
