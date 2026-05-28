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

## Pull Request / Agent Review Requirements

- Must not violate architecture layers.
- Must respect Single Responsibility Principle.
- Must include tests.
- Must update documentation if behavior changes.

---

Last updated: May 2026
```
