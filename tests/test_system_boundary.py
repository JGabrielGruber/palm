"""Architectural boundary tests for ``palm.system`` (0.57.2+)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

FORBIDDEN_PREFIXES = (
    "palm.services",
    "palm.runtimes",
    "palm.patterns",
    "palm.app",
)


def _system_root() -> Path:
    return Path(__file__).resolve().parents[1] / "src" / "palm" / "system"


def _is_forbidden(module: str | None) -> bool:
    if not module:
        return False
    for prefix in FORBIDDEN_PREFIXES:
        if module == prefix or module.startswith(prefix + "."):
            return True
    return False


def test_system_package_exists() -> None:
    root = _system_root()
    assert root.is_dir(), "palm.system package must exist"
    assert (root / "__init__.py").is_file()
    assert (root / "instance.py").is_file()
    assert (root / "ports" / "execution.py").is_file()


def test_system_has_no_product_surface_pattern_imports() -> None:
    """palm.system must not import services, runtimes surfaces, patterns, or app."""
    root = _system_root()
    violations: list[str] = []

    for path in sorted(root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        rel = path.relative_to(root.parents[1])
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if _is_forbidden(node.module):
                    violations.append(f"{rel}: from {node.module}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if _is_forbidden(alias.name):
                        violations.append(f"{rel}: import {alias.name}")

    assert not violations, "forbidden imports in palm.system:\n" + "\n".join(violations)


def test_public_exports() -> None:
    from palm.system import ExecutionPort, SystemInstance

    assert ExecutionPort is not None
    assert SystemInstance is not None


def test_base_runtime_is_system_instance_and_execution_port() -> None:
    from palm.common.runtimes.base import BaseRuntime
    from palm.system import ExecutionPort, SystemInstance

    runtime = BaseRuntime()
    assert isinstance(runtime, SystemInstance)
    assert isinstance(runtime, ExecutionPort)
    assert runtime.execution is runtime


def test_execution_port_fake_is_usable() -> None:
    """Test doubles can implement ExecutionPort without a full host."""
    from palm.system import ExecutionPort

    class FakePort:
        def invoke_resource(self, resource_ref: str, **kwargs: object) -> dict:
            return {"ref": resource_ref, "ok": True}

        def start_workload(self, spec: object, **kwargs: object) -> dict:
            return {"spec": spec, "status": "pending"}

        def exec_workload(
            self, workload_id: str, command: list[str] | tuple[str, ...], **kwargs: object
        ) -> dict:
            return {"id": workload_id, "command": list(command)}

        def stop_workload(self, workload_id: str, **kwargs: object) -> dict:
            return {"id": workload_id, "status": "stopped"}

        def workload_status(self, workload_id: str, *, refresh: bool = False) -> dict:
            return {"id": workload_id, "refresh": refresh}

    fake = FakePort()
    assert isinstance(fake, ExecutionPort)
    assert fake.invoke_resource("kv://x")["ok"] is True


@pytest.mark.parametrize(
    "name",
    ["invoke_resource", "start_workload", "exec_workload", "stop_workload", "workload_status"],
)
def test_execution_port_protocol_names(name: str) -> None:
    from palm.system.ports.execution import ExecutionPort

    assert hasattr(ExecutionPort, name)
