#!/usr/bin/env python3
"""Assembly coherence guard — run the fail-closed / single-truth suite (0.63.4).

This is a fitness instrument: failures mean dual mode or a broken gate, not
"make green by soft-open." See VISION-0.63 / VISION-ASSEMBLY §6.4.
"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests/assembly/",
        "tests/core/test_assembly_engine.py",
        "tests/test_assembly_system_0_63_2.py",
        "tests/test_assembly_gate_0_63_3.py",
        "--tb=short",
    ]
    print("🔒 Assembly coherence suite (fail-closed / single readiness)...")
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
