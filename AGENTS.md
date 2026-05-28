# AGENTS.md

## Purpose

This document serves as the **constitution** for any AI coding agent (Grok Build, Claude, Cursor, etc.) or human developer working on Palm. It defines the non-negotiable principles, architecture constraints, and patterns that must be respected.

All generated or modified code must comply with the rules stated here.

## Core Principles

- **Single Responsibility Principle (SRP)**: Every class, module, and function must have one, and only one, reason to change.
- **Separation of Concerns**: Clear boundaries between layers (Behavior Tree Engine, Wizard Domain, Persistence, CLI/UI).
- **Open/Closed Principle**: The system must be open for extension but closed for modification.
- **Testability**: All core logic must be unit-testable without side effects.
- **Explicit over Implicit**: Prefer clear, readable, and self-documenting code over clever shortcuts.

## Architecture Rules (updated 0.3.0-dev)

1. **Behavior Tree Engine** (`palm/core/behavior_tree/`)
   - One of the two general-purpose engines allowed in `palm/core/`.
   - Must remain completely independent of wizards, RichContext, sessions, persistence, CLI, and the Orchestration Engine (orchestration may optionally compose with it via backends).
   - No imports from `palm.cli.*` or legacy code allowed.

2. **Orchestration Engine** (`palm/core/orchestration/`)
   - The second general-purpose engine in `palm/core/`.
   - Uses the Strategy pattern (`OrchestrationMode` + nested `ExecutionBackend`).
   - Primary test backend is `TestBackend` (fast, deterministic, zero I/O/threads/BT dependency).
   - Introduces `Job`, `Orchestrator`, and shared `palm/core/events.py` (Event + EventBus).
   - Must remain completely independent of wizards, RichContext, sessions, persistence, and CLI.
   - **Only** the optional `BehaviorTreeBackend` + one integration test file may import from the BT engine.
   - No imports from `palm.cli.*` or legacy code allowed.

3. **Legacy Reference Code** (`palm/cli/solid/legacy/`)
   - Contains the old wizard implementation, models, persistence, orchestrator, etc.
   - This is a **deprecated historical snapshot**. It exists only to keep the Solid CLI working during the transition.
   - **Strict rule**: New code must never import anything from `palm.cli.solid.legacy.*` (except inside the legacy package itself for its own maintenance).

4. **Future Domain Layers**
   - New wizard (and other domain) functionality must be built on top of `palm.core.behavior_tree` and/or `palm.core.orchestration`.
   - They will live outside `palm/core/` (typically under `palm/` or a new clean package) and must follow the same independence rules as the engines.

5. **Folder Structure Discipline**
   - One primary class per file for all Behavior Tree nodes.
   - Concrete nodes live under `tree/nodes/`.
   - Never create "god classes" or monolithic files in core engines.

4. **Blackboard Usage**
   - All data sharing between nodes must go through the `Blackboard`.
   - Direct parameter passing between nodes is forbidden except for construction.

## Forbidden Patterns

- Monolithic classes handling multiple responsibilities.
- Putting CLI/UI logic (Rich, prompt_toolkit, etc.) inside core.
- Using `eval()`, dynamic code execution, or overly dynamic Python magic in core logic.
- Tight coupling between layers (core should not import from cli).

## When Adding New Features

- New Behavior Tree node → create dedicated file under `tree/nodes/`
- New Orchestration Engine component (Job, Mode, Backend, etc.) → create dedicated file under `orchestration/`
- New Wizard functionality → implement as nodes or decorators in the wizard layer first (on top of the two core engines).
- Always add corresponding tests for both the abstraction and the concrete implementation (use Abstract*Test pattern + TestBackend for orchestration).

## Review Checklist (for agents and humans)

- Does this change respect SRP?
- Is the Behavior Tree engine still independent of wizards and orchestration?
- Is the Orchestration Engine (including TestBackend) still independent of wizards, CLI, and legacy?
- Are abstractions properly used (Strategy for modes/backends)?
- Are new nodes / engine classes placed in the correct location?
- Are tests included for both abstraction contract and implementation?
- Does any new code in `palm/core/` import from `cli.*` or legacy? (Must not)

---

Last updated: May 2026 (Orchestration Engine + TestBackend + core/events added)
