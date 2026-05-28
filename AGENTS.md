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

## Architecture Rules

1. **Behavior Tree Engine** (`palm/core/behavior_tree/`)
   - Must remain **general-purpose** and independent of the Wizard domain.
   - No knowledge of RichContext, sessions, or user interaction.
   - All nodes must inherit from the proper abstract base (`BaseNode`, `LeafNode`, `CompositeNode`, or `DecoratorNode`).

2. **Wizard Layer** (`palm/core/wizard/`)
   - Responsible for user interaction semantics.
   - Must build on top of the Behavior Tree Engine.
   - Must not leak UI concerns into the core BT engine.

3. **Folder Structure Discipline**
   - One primary class per file for all Behavior Tree nodes.
   - Concrete nodes live under `tree/nodes/`.
   - Never create "god classes" or monolithic files.

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
- New Wizard functionality → implement as nodes or decorators in the wizard layer first.
- Always add corresponding tests for both the abstraction and the concrete implementation.

## Review Checklist (for agents and humans)

- Does this change respect SRP?
- Is the Behavior Tree engine still independent of wizards?
- Are abstractions properly used?
- Are new nodes placed in the correct location?
- Are tests included for both abstraction contract and implementation?

---

Last updated: May 2026
