"""0.58.6 — Assist / flow dogfood: bind system session on start."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from palm.app import ApplicationHost, DeploymentProfile
from palm.app.settings import PalmSettings
from palm.services.assist.registry import scenario_by_id


@pytest.fixture
def dogfood_host() -> Iterator[ApplicationHost]:
    settings = PalmSettings.for_tests(load_examples=True)
    host = ApplicationHost(settings=settings, profile=DeploymentProfile.all_in_one())
    host.start()
    yield host
    host.shutdown()


def _operator_entry_flow_id() -> str:
    contrib = scenario_by_id("operator-entry")
    assert contrib is not None
    return str(contrib.flow_id)


def test_run_wizard_binds_system_session(dogfood_host: ApplicationHost) -> None:
    flows = dogfood_host.execution.flows
    flow_id = _operator_entry_flow_id()
    session = flows.run_wizard({"flow_name": flow_id, "by_id": True})
    meta = flows.get_instance_metadata(session.session_id)
    system_sid = meta.get("session_id")
    assert system_sid
    assert str(system_sid).startswith("sess-")
    assert str(system_sid) != session.session_id

    plane = dogfood_host.session_plane
    assert plane is not None
    owner = plane.session_for_instance(session.session_id)
    assert owner is not None
    assert owner.session_id == system_sid


def test_flow_create_returns_system_session_id(dogfood_host: ApplicationHost) -> None:
    flows = dogfood_host.execution.flows
    flow_id = _operator_entry_flow_id()
    created = flows.dispatch(["flows", flow_id, "create"], params={})
    assert created.get("session_id")
    assert created.get("instance_id") == created.get("session_id")
    assert created.get("system_session_id")
    assert str(created["system_session_id"]).startswith("sess-")
    assert created["system_session_id"] != created["session_id"]


def test_assist_start_exposes_system_session(dogfood_host: ApplicationHost) -> None:
    started = dogfood_host.assist.start_scenario("operator-entry", {})
    product_sid = started.get("session_id")
    assert product_sid
    system_sid = started.get("system_session_id")
    assert system_sid, f"expected system_session_id on envelope: {started.keys()}"
    assert str(system_sid).startswith("sess-")
    assert system_sid != product_sid
    assert started.get("instance_id") == product_sid
    refs = started.get("refs") or {}
    assert refs.get("system_session_id") == system_sid

    plane = dogfood_host.session_plane
    assert plane is not None
    assert plane.session_for_instance(str(product_sid)) is not None
    journey = plane.inspect(str(system_sid))
    assert product_sid in journey["instance_ids"]


def test_assist_start_reuses_explicit_system_session(dogfood_host: ApplicationHost) -> None:
    bind = dogfood_host.bind_session(surface="test")
    started = dogfood_host.assist.start_scenario(
        "operator-entry",
        {"system_session_id": bind.session_id},
    )
    assert started.get("system_session_id") == bind.session_id
    product_sid = started["session_id"]
    plane = dogfood_host.session_plane
    assert plane is not None
    assert product_sid in plane.list_instances(bind.session_id)
