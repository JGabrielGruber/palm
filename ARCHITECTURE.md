# ARCHITECTURE.md

## High-Level Architecture (post 0.3.0-dev clean-core migration)

Palm follows a **layered architecture** with strict separation of concerns.

### Layers

1. **Behavior Tree Engine** (`palm/core/behavior_tree/`)
   - The **only** content allowed in `palm/core/`.
   - General-purpose, reusable Behavior Tree implementation.
   - Core abstractions: `BaseNode`, `LeafNode`, `CompositeNode`, `DecoratorNode`, `Blackboard`.
   - Completely independent of any business domain, wizards, persistence, or CLI.

2. **Legacy Reference Implementation** (`palm/cli/solid/legacy/`)
   - Contains the complete pre-0.3.0 wizard engine, models, persistence, orchestrator, workflow scaffolding, etc.
   - This is a **deprecated reference snapshot only**. It is preserved so the existing Solid CLI continues to work.
   - New code must **never** import from here.
   - Future clean domain layers (including the real "wizard on BT" implementation) will live elsewhere.

3. **Interface Layer** (`palm/cli/solid/`)
   - The Solid Admin CLI (and future TUIs / servers).
   - Currently wires the legacy implementation. Will be updated as clean layers are built on the BT engine.

General utilities (`config/`, `utils/logging/`) and the base `PalmError` remain at the top level as cross-cutting concerns.

## Key Design Decisions

- **Behavior Tree as Foundation**: Chosen over a simple DAG or state machine because it provides superior support for complex control flow, composition, reusability, and conditional execution while maintaining clean tree semantics.
- **Blackboard Pattern**: Adopted for decoupled data sharing across nodes.
- **OOP Abstractions**: Strong use of abstract base classes and inheritance to enforce contracts and enable extensibility.
- **Single Responsibility Principle**: Enforced at every layer to maximize maintainability and testability.

## Future Extensibility

The Behavior Tree Engine is intentionally general-purpose so it can support:
- Non-interactive DAG workflows
- Automated ETL processes
- AI agent decision systems
- Hybrid human + automated flows

Wizards are the current primary business need, but not the only intended use case.

---

Last updated: May 2026
