# DEVELOPMENT.md

## Development Workflow

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Key Commands

- Run the CLI: `python main.py` or `palm`
- Run tests: `pytest`
- Lint: `ruff check .`
- Format: `ruff format .`
- Type check: `mypy src`

## Adding New Behavior Tree Nodes

1. Decide the category: Leaf, Composite, or Decorator.
2. Create a new file under `src/palm/core/behavior_tree/nodes/`.
3. Inherit from the correct abstract base class.
4. Implement `tick(blackboard: Blackboard) -> NodeStatus`.
5. Add comprehensive tests (both abstraction contract and specific behavior).

## Testing Philosophy

- Test abstractions using abstract test classes.
- Test concrete implementations thoroughly.
- Include edge cases and breaking scenarios.

## Code Style

- Follow PEP 8 + Ruff rules.
- Use type hints everywhere.
- Prefer explicit code over clever code.
- One class per file for Behavior Tree nodes.

## Legacy Code & Deprecation (0.3.0-dev+)

All pre-clean-core wizard, models, persistence, orchestrator, and workflow code now lives in `src/palm/cli/solid/legacy/`.

- This is a **reference implementation only**.
- Never add new features or import from `palm.cli.solid.legacy.*` in new code (except inside the legacy package for its own maintenance).

## Pull Request / Agent Review Requirements

- Must not violate architecture layers (core = only general-purpose BT engine and future reusable engines).
- Must respect Single Responsibility Principle.
- Must include tests.
- Must update documentation if behavior changes.
- New code must never depend on anything under `palm.cli.solid.legacy`.

---

Last updated: May 2026 (0.3.0-dev clean-core migration)
```
