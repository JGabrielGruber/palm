"""0.63.23 — work-plane able defaults fail closed; admission access helper."""

from __future__ import annotations

from unittest.mock import MagicMock

from palm.core.assembly import AdmissionSnapshot, AssemblyPhase
from palm.core.storage import StorageEngine
from palm.core.work import WorkIntent
from palm.system.assembly import (
    admission_source_from_runtime_resolver,
    require_business_admission,
)
from palm.system.assembly.inventory import GATED_PATHS, admission_inventory
from palm.system.subsystems.planes.work.plane import WorkPlaneService


def _memory_storage() -> StorageEngine:
    storage = StorageEngine()
    storage.initialize()
    storage.select("memory")
    return storage


def test_able_default_false_before_attach() -> None:
    plane = WorkPlaneService()
    assert plane.is_able() is False


def test_attach_without_able_fails_closed() -> None:
    plane = WorkPlaneService()
    submitted: list[str] = []
    plane.attach(
        storage=_memory_storage(),
        submit_flow=lambda f, _p: submitted.append(f),
        # able omitted → fail closed (0.63.23)
    )
    assert plane.is_able() is False
    plane.enqueue(WorkIntent(kind="run_flow", target="x"))
    assert plane.tick() == 0
    assert submitted == []


def test_set_able_none_fails_closed() -> None:
    plane = WorkPlaneService()
    plane.attach(
        storage=_memory_storage(),
        submit_flow=lambda _f, _p: None,
        able=lambda: True,
    )
    assert plane.is_able() is True
    plane.set_able(None)
    assert plane.is_able() is False


def test_attach_with_able_true_ticks() -> None:
    plane = WorkPlaneService()
    submitted: list[str] = []
    plane.attach(
        storage=_memory_storage(),
        submit_flow=lambda f, _p: submitted.append(f),
        able=lambda: True,
    )
    plane.enqueue(WorkIntent(kind="run_flow", target="my-flow"))
    assert plane.tick() == 1
    assert submitted == ["my-flow"]


def test_admission_source_from_runtime_resolver() -> None:
    ready = AdmissionSnapshot(
        may_run_business=True,
        phase=AssemblyPhase.READY,
        definition_id="local.embedded",
    )
    rt = MagicMock()
    rt.admission = ready
    resolve = MagicMock(return_value=rt)
    source = admission_source_from_runtime_resolver(resolve)
    snap = require_business_admission(source)
    assert snap.definition_id == "local.embedded"
    resolve.assert_called_with(None)


def test_inventory_marks_able_fail_closed() -> None:
    ids = {c["id"] for c in GATED_PATHS}
    assert "work_plane.able_fail_closed" in ids
    pretenders = {p["id"]: p for p in admission_inventory()["readiness_edges"]}
    assert pretenders["work_plane.able_default_open"]["status"] == "paid_0_63_23"
    assert pretenders["host.soft_definitions_ready"]["status"] == "named_0_63_23"
