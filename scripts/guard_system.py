#!/usr/bin/env python3
"""System layer purity guard — palm.system must not import product/surfaces/patterns."""

from __future__ import annotations

import sys
from pathlib import Path

# Forbidden outer layers (SYSTEM-LOW-LEVEL §2.1 / §7).
FORBIDDEN_PREFIXES = (
    "palm.services",
    "palm.runtimes",
    "palm.patterns",
    "palm.app",
)


def _is_forbidden(module: str | None) -> bool:
    if not module:
        return False
    for prefix in FORBIDDEN_PREFIXES:
        if module == prefix or module.startswith(prefix + "."):
            return True
    return False


def main() -> int:
    system_root = Path("src/palm/system")
    if not system_root.is_dir():
        print("palm.system package missing: src/palm/system")
        return 1

    violations: list[str] = []

    for py in sorted(system_root.rglob("*.py")):
        text = py.read_text(encoding="utf-8")
        rel = py.as_posix()
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if stripped.startswith("from "):
                # from palm.X import ...
                parts = stripped.split()
                if len(parts) >= 2 and parts[0] == "from":
                    mod = parts[1]
                    if _is_forbidden(mod):
                        violations.append(f"{rel}:{line_no}: {stripped}")
            elif stripped.startswith("import "):
                # import palm.X ...
                rest = stripped[len("import ") :].split("#", 1)[0]
                for chunk in rest.split(","):
                    name = chunk.strip().split(" as ", 1)[0].strip()
                    if _is_forbidden(name):
                        violations.append(f"{rel}:{line_no}: {stripped}")

    if violations:
        print("System layer purity violations:")
        print("\n".join(violations))
        return 1

    print("[OK] palm.system import rules respected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
