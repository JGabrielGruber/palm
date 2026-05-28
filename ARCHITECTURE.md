# ARCHITECTURE.md

## High-Level Architecture

Palm follows a **layered architecture** with strict separation of concerns.

### Layers

1. **Behavior Tree Engine** (`palm/core/behavior_tree/`)
   - General-purpose, reusable Behavior Tree implementation.
   - Core abstractions: `BaseNode`, `LeafNode`, `CompositeNode`, `DecoratorNode`, `Blackboard`.
   - Independent of any business domain.

2. **Domain Layer** (`palm/core/wizard/`)
   - Palm-specific business logic.
   - Uses the Behavior Tree Engine to implement interactive wizards.
   - Responsible for `RichContext`, session management, persistence, and user interaction semantics.

3. **Persistence Layer** (`palm/persistence/`)
   - Data storage concerns (currently SQLite).

4. **Interface Layer** (`palm/cli/`)
   - All user-facing interfaces (Solid CLI, future Textual TUI, WebSocket, etc.).

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
