"""0.59.1 — Boot inventory characterization (today's order + spine contracts).

Pins what ApplicationHost and BaseRuntime start do *now* so schedule migration
cannot drift silently. Not the future phase API — see docs/BOOT-INVENTORY.md.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from palm.app import ApplicationHost, DeploymentProfile
from palm.app.settings import PalmSettings
from palm.common.plugins import ensure_core_plugins
from palm.runtimes.embedded import EmbeddedRuntime
from palm.system.planes.session.plane import SessionPlaneService
from palm.system.planes.wait.plane import WaitPlaneService

# Provisional host phase order for ApplicationHost.start (0.59.1 inventory).
# Update with docs/BOOT-INVENTORY.md when the real walker lands.
HOST_START_PHASE_ORDER: tuple[str, ...] = (
    "kernel.bootstrap",
    "host.event",
    "system.spawn",
    "definitions.load",
    "product.wire",
    "surfaces.mount",
    "projections.attach",
    "recover",
)


@pytest.fixture
def spine_settings() -> PalmSettings:
    """Minimal host settings for spine boot (memory, no examples)."""
    return PalmSettings.for_tests(load_examples=False)


def test_host_start_phase_order_all_in_one(spine_settings: PalmSettings) -> None:
    """ApplicationHost.start walks a fixed collaborator order (collapsed profile)."""
    host = ApplicationHost(
        settings=spine_settings,
        profile=DeploymentProfile.all_in_one(),
    )
    seen: list[str] = []

    real_bootstrap = host._app.bootstrap
    real_spawn = host._spawner.spawn_runtimes
    real_load = host._app.load_definitions
    real_wire = host._wire_cqrs
    real_surface = host._start_server_surface
    real_proj = host._attach_projections
    real_recover = host._recovery.recover

    def track(name: str, fn: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            seen.append(name)
            return fn(*args, **kwargs)

        return wrapper

    host._app.bootstrap = track("kernel.bootstrap", real_bootstrap)  # type: ignore[method-assign]
    host._spawner.spawn_runtimes = track("system.spawn", real_spawn)  # type: ignore[method-assign]
    host._app.load_definitions = track("definitions.load", real_load)  # type: ignore[method-assign]
    host._wire_cqrs = track("product.wire", real_wire)  # type: ignore[method-assign]
    host._start_server_surface = track("surfaces.mount", real_surface)  # type: ignore[method-assign]
    host._attach_projections = track("projections.attach", real_proj)  # type: ignore[method-assign]
    host._recovery.recover = track("recover", real_recover)  # type: ignore[method-assign]

    orig_event_init = host._event.initialize

    def event_init_tracked() -> None:
        seen.append("host.event")
        return orig_event_init()

    host._event.initialize = event_init_tracked  # type: ignore[method-assign]

    try:
        host.start()
        assert host.is_started
        # Only the ordered core phases (background drain is post-ready optional).
        core = [p for p in seen if p in HOST_START_PHASE_ORDER]
        assert core == list(HOST_START_PHASE_ORDER)
    finally:
        host.shutdown()


def test_spine_host_post_start_contracts(spine_settings: PalmSettings) -> None:
    """Collapsed host exposes product doors + system planes (spine green bar)."""
    host = ApplicationHost(
        settings=spine_settings,
        profile=DeploymentProfile.all_in_one(),
    )
    host.start()
    try:
        assert host.is_started
        assert host.running_runtimes() == ["main"]
        rt = host.runtime()
        assert isinstance(rt, EmbeddedRuntime)
        assert rt.is_started
        assert isinstance(rt.wait_plane, WaitPlaneService)
        assert isinstance(rt.session_plane, SessionPlaneService)
        # Product services built from composition (all_in_one services).
        assert host.system is not None
        assert host.session is not None
        assert host.definitions is not None
        assert host.execution is not None
        # Composition membership partially authoritative today.
        assert "system" in host.composition.services
        assert "session" in host.composition.services
        assert host.composition.has("projections")
    finally:
        host.shutdown()


def test_system_start_alone_attaches_planes(spine_settings: PalmSettings) -> None:
    """BaseRuntime system schedule without host still attaches wait + session."""
    from palm.app.bootstrap import runtime_start_options

    rt = EmbeddedRuntime()
    rt.start(**runtime_start_options(spine_settings))
    try:
        assert rt.is_started
        assert isinstance(rt.wait_plane, WaitPlaneService)
        assert isinstance(rt.session_plane, SessionPlaneService)
        # Execution port structural surface
        assert hasattr(rt, "execution")
        assert rt.storage.is_initialized
    finally:
        rt.stop()


def test_ensure_core_plugins_idempotent() -> None:
    """Plugin ensure may run host + system + tests; must be safe to repeat."""
    ensure_core_plugins()
    ensure_core_plugins()
    # Second call is a no-op (module flag); registries still readable.
    from palm.common.patterns._registry import registered_builders

    assert "wizard" in registered_builders()


def test_host_start_idempotent(spine_settings: PalmSettings) -> None:
    """Second host.start() is a no-op (does not re-spawn)."""
    host = ApplicationHost(
        settings=spine_settings,
        profile=DeploymentProfile.all_in_one(),
    )
    host.start()
    try:
        host.start()
        assert host.running_runtimes() == ["main"]
    finally:
        host.shutdown()


def test_composition_services_gate_build(spine_settings: PalmSettings) -> None:
    """build_all honors composition.services (membership partial truth today)."""
    from palm.app.host.composition import CompositionProfile

    lean = CompositionProfile.embedded()
    host = ApplicationHost(
        settings=spine_settings,
        profile=DeploymentProfile.all_in_one(),
        composition=lean,
    )
    host.start()
    try:
        assert host.system is not None
        assert host.session is not None
        assert host.definitions is not None
        assert host.execution is not None
        # embedded CORE_SERVICES — no assist/design/analytics chrome
        assert host.assist is None
        assert host.design is None
        assert host.analytics is None
    finally:
        host.shutdown()


def test_inventory_constants_match_documented_count() -> None:
    """Guard: HOST_START_PHASE_ORDER length matches inventory table core steps."""
    # H1–H9 in BOOT-INVENTORY (bootstrap through recover); host.event is H2.
    assert len(HOST_START_PHASE_ORDER) == 8
    assert HOST_START_PHASE_ORDER[0] == "kernel.bootstrap"
    assert HOST_START_PHASE_ORDER[-1] == "recover"
