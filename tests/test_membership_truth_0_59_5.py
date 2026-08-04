"""0.59.5 — CompositionProfile is membership truth on the migrated path.

- Runtime gates read ``composition.has`` / ``composition.surfaces`` / services only.
- Deployment may *feed* the settings resolver (server work-drain → capability);
  it is not a second OR at phase time.
- Explicit composition wins over deployment.
- Phase skips use ``composition_off:*`` / mode reasons visible in SystemLog.
"""

from __future__ import annotations

from dataclasses import replace

from palm.app.bootstrap import composition_profile_from_settings
from palm.app.host.application_host import ApplicationHost
from palm.app.host.composition import CompositionProfile as CP
from palm.app.host.roles import DeploymentProfile
from palm.app.settings import PalmSettings
from palm.system.log import get_system_log, reset_system_log_for_tests


def test_settings_resolver_folds_deployment_work_drain() -> None:
    """Server deployment feeds work_drain into membership when resolving from settings."""
    settings = PalmSettings.for_tests(load_examples=False)
    assert settings.enable_work_drain_service is False
    bare = composition_profile_from_settings(settings)
    assert "work_drain" not in bare.capabilities

    with_server = composition_profile_from_settings(
        settings, deployment=DeploymentProfile.server_only(port=0)
    )
    assert "work_drain" in with_server.capabilities


def test_server_profile_host_gains_work_drain_membership() -> None:
    """Host with server deployment + settings path has work_drain on composition."""
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost(
        settings=settings,
        profile=DeploymentProfile.server_only(port=0),
    )
    assert host.composition.has("work_drain")
    host.start()
    try:
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].outcome == "ok"
        assert host.work_drain is not None
        assert host.work_drain.is_running is True
    finally:
        host.shutdown()


def test_explicit_composition_wins_over_deployment_work_drain() -> None:
    """Explicit empty capabilities stay empty even when deployment would feed work_drain."""
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost(
        settings=settings,
        profile=DeploymentProfile.server_only(port=0),
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    assert not host.composition.has("work_drain")
    host.start()
    try:
        assert host._work_drain_background_enabled() is False
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].outcome == "skip"
        assert by_id["host.background.work_drain"].reason == "composition_off:work_drain"
    finally:
        host.shutdown()


def test_work_drain_gate_is_composition_only_not_or() -> None:
    """Deployment flag alone (without membership) does not enable background drain."""
    settings = PalmSettings.for_tests(load_examples=False)
    # Explicit composition omits work_drain; deployment still "wants" it.
    host = ApplicationHost(
        settings=settings,
        profile=replace(
            DeploymentProfile.all_in_one(),
            enable_work_drain_service=True,
        ),
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    host.start()
    try:
        assert host.profile.enable_work_drain_service is True
        assert host._work_drain_background_enabled() is False
    finally:
        host.shutdown()


def test_composition_capability_enables_work_drain_without_deployment_flag() -> None:
    """Membership on composition is enough (deployment flag is not a second AND)."""
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost(
        settings=settings,
        profile=DeploymentProfile.all_in_one(),  # enable_work_drain_service False
        composition=replace(CP.all_in_one(), capabilities=frozenset({"work_drain"})),
    )
    host.start()
    try:
        assert host._work_drain_background_enabled() is True
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].outcome == "ok"
    finally:
        host.shutdown()


def test_surfaces_skip_when_composition_has_none() -> None:
    """Server deployment + empty surfaces → composition_off:surfaces, not silent mount."""
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost(
        settings=settings,
        profile=DeploymentProfile.server_only(port=0),
        composition=replace(
            CP.server(),
            surfaces=(),
            capabilities=frozenset({"projections", "journal"}),
        ),
    )
    host.start()
    try:
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.surfaces.mount"].outcome == "skip"
        assert by_id["host.surfaces.mount"].reason == "composition_off:surfaces"
    finally:
        host.shutdown()


def test_projections_skip_reason_composition_off() -> None:
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost(
        settings=settings,
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    host.start()
    try:
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.projections.attach"].outcome == "skip"
        assert by_id["host.projections.attach"].reason == "composition_off:projections"
    finally:
        host.shutdown()


def test_boot_mode_test_skips_background_with_mode_reason() -> None:
    reset_system_log_for_tests()
    settings = PalmSettings.for_tests(load_examples=False)
    # test mode composition is embedded (no work_drain) + mode forbids background
    host = ApplicationHost(settings=settings, boot_mode="test")
    host.start()
    try:
        by_id = {w.phase: w for w in (host._last_boot_walk or [])}
        assert by_id["host.background.work_drain"].outcome == "skip"
        # mode forbids first
        assert by_id["host.background.work_drain"].reason == "mode_background_off"
        boot = host.control_plane_status()["boot"]
        assert boot["membership"]["services"]
        assert "capabilities" in boot["membership"]
    finally:
        host.shutdown()


def test_system_log_boot_start_carries_membership() -> None:
    """Lifecycle boot.start lists services/surfaces/capabilities (phenotype visible)."""
    reset_system_log_for_tests()
    settings = PalmSettings.for_tests(load_examples=False)
    host = ApplicationHost(
        settings=settings,
        profile=DeploymentProfile.all_in_one(),
    )
    host.start()
    try:
        slog = get_system_log()
        starts = [r for r in slog.recent() if r.event == "boot.start"]
        assert starts
        fields = starts[0].fields
        assert "inspect" in str(fields.get("services", ""))
        assert "capabilities" in fields
        assert host.membership_snapshot()["services"]
    finally:
        host.shutdown()


def test_membership_snapshot_matches_composition() -> None:
    host = ApplicationHost(
        settings=PalmSettings.for_tests(load_examples=False),
        composition=CP.embedded(),
    )
    snap = host.membership_snapshot()
    assert snap["services"] == list(CP.embedded().services)
    assert snap["surfaces"] == []
    assert snap["capabilities"] == []
