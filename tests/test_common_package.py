"""Smoke tests for palm.common package layout."""

from __future__ import annotations


def test_common_public_api() -> None:
    from palm.common import (
        DefinitionExecutor,
        ExecutionPlan,
        InstancePersistenceHook,
        PlanRegistry,
        ProcessPlan,
        build_pattern,
    )

    assert DefinitionExecutor is not None
    assert ExecutionPlan is not None
    assert ProcessPlan is not None
    assert PlanRegistry is not None
    assert InstancePersistenceHook is not None
    assert callable(build_pattern)


def test_common_subpackage_imports() -> None:
    from palm.common.patterns import PatternBuildContext, build_pattern
    from palm.common.persistence import DefinitionRepository, InstanceRepository
    from palm.common.plans import ExecutionPlan, PlanRegistry, ProcessPlan
    from palm.system.executions import DefinitionExecutor
    from palm.system.runtime.job_hooks import InstancePersistenceHook

    assert InstancePersistenceHook.__name__ == "InstancePersistenceHook"
    assert DefinitionExecutor.__name__ == "DefinitionExecutor"
    assert DefinitionRepository.__name__ == "DefinitionRepository"
    assert InstanceRepository.__name__ == "InstanceRepository"
    assert PatternBuildContext.__name__ == "PatternBuildContext"
    assert ExecutionPlan.__name__ == "ExecutionPlan"
    assert ProcessPlan.__name__ == "ProcessPlan"
    assert PlanRegistry.__name__ == "PlanRegistry"
    assert callable(build_pattern)


def test_common_runtimes_is_not_system_shim() -> None:
    """common.runtimes keeps server kit + doctor registry only (SD-012 deleted)."""
    import palm.common.runtimes as cr

    assert hasattr(cr, "register_doctor_contributor")
    assert not hasattr(cr, "BaseRuntime")
