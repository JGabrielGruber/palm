"""Living Capabilities (0.51.1) — the resolver derives capabilities from settings.

Derived, **not yet gating**: 0.51.1 makes ``composition_profile_from_settings`` compute
``capabilities`` from the ``enable_*`` flags, pinned against today's effective wiring,
*before* any host machinery reads them (0.51.2+ switches each gate to
``composition.has(...)``). These tests are the safety net for that transition — they lock
the derivation so a later gate can't silently change what a shape wires. See VISION-0.51 /
ADR-020.
"""

from __future__ import annotations

from dataclasses import replace

from palm.app import ApplicationHost
from palm.app.bootstrap import composition_profile_from_settings
from palm.app.host.composition import (
    ALL_SERVICES,
    DEFAULT_CAPABILITIES,
    SERVER_SURFACES,
)
from palm.app.host.composition import CompositionProfile as CP
from palm.app.host.roles import DeploymentProfile
from palm.app.settings import PalmSettings
from palm.core.structure import CAPABILITY_OUTBOX, CAPABILITY_PROJECTIONS, CAPABILITY_WORK_DRAIN


def _caps(**overrides: object) -> frozenset[str]:
    """Derived capabilities for the light test settings with explicit flag overrides."""
    settings = PalmSettings.for_tests(load_examples=False).model_copy(update=overrides)
    return composition_profile_from_settings(settings).capabilities


# ── the derivation, pinned ───────────────────────────────────────────────────


def test_full_recovery_derives_exactly_default_capabilities() -> None:
    """full_recovery turns on compensation; with analytics + always-on
    workloads that is exactly DEFAULT_CAPABILITIES — the production-default shape.
    journal and projections are DNA, not composition seeds."""
    profile = composition_profile_from_settings(PalmSettings.for_tests(full_recovery=True))
    assert profile.capabilities == DEFAULT_CAPABILITIES
    assert DEFAULT_CAPABILITIES == frozenset(
        {
            "compensation",
            "analytics",
            "workloads",
        }
    )


def test_lean_test_settings_derive_the_always_on_capabilities_plus_analytics() -> None:
    """for_tests default (full_recovery=False): compensation + outbox off, analytics on,
    workloads always-on. journal and projections are DNA, not composition."""
    assert _caps() == frozenset({"analytics", "workloads"})


def test_each_flag_toggles_exactly_its_capability() -> None:
    assert "compensation" in _caps(enable_compensation=True)
    assert "compensation" not in _caps(enable_compensation=False)
    assert "outbox" not in _caps(enable_event_outbox=True)
    assert "outbox" not in _caps(enable_event_outbox=False)
    assert "webhook" in _caps(enable_webhook_dispatcher=True)
    assert "webhook" not in _caps(enable_webhook_dispatcher=False)
    assert "work_drain" not in _caps()
    assert "analytics" in _caps(analytics_enabled=True)
    assert "analytics" not in _caps(analytics_enabled=False)


def test_journal_is_not_a_composition_seed() -> None:
    """journal has no enable_* flag and is not a composition seed (0.67.7 DNA + hand)."""
    assert "journal" not in _caps()
    assert "journal" not in _caps(
        enable_compensation=False,
        enable_event_outbox=False,
        analytics_enabled=False,
    )


def test_projections_is_not_a_composition_seed() -> None:
    """projections has no enable_* flag and is not a composition seed (0.67.9 DNA + hand)."""
    assert "projections" not in _caps()
    assert "projections" not in _caps(
        enable_compensation=False,
        enable_event_outbox=False,
        analytics_enabled=False,
    )


# ── behaviour preservation ───────────────────────────────────────────────────


def test_resolver_preserves_services_and_surfaces() -> None:
    """0.51.1 touches only capabilities; services/surfaces stay all_in_one's."""
    profile = composition_profile_from_settings(PalmSettings.for_tests(load_examples=False))
    assert profile.services == ALL_SERVICES == CP.all_in_one().services
    assert profile.surfaces == SERVER_SURFACES == CP.all_in_one().surfaces


def test_services_not_gated_by_capabilities_yet() -> None:
    """Service construction is settled by composition.services (0.50), not capabilities:
    a lean-capability host still builds every service."""
    host = ApplicationHost(settings=PalmSettings.for_tests(load_examples=False))
    host.start()
    try:
        # lean test settings derive {analytics, workloads} ...
        assert host.composition.capabilities == frozenset({"analytics", "workloads"})
        # ... yet every service is still built (services are a separate axis)
        for name in (
            "inspect",
            "session",
            "definitions",
            "execution",
            "assist",
            "design",
            "analytics",
        ):
            assert getattr(host, name) is not None
    finally:
        host.shutdown()


# ── 0.51.2: the first gates read the composition, not scattered flags ─────────


def test_compensation_gate_reads_composition_not_settings() -> None:
    """RecoveryCoordinator gates compensation on composition.has('compensation'); an
    explicit composition wins over settings.enable_compensation (which full_recovery sets)."""
    settings = PalmSettings.for_tests(full_recovery=True)  # enable_compensation=True

    with_cap = ApplicationHost(
        settings=settings,
        composition=replace(CP.all_in_one(), capabilities=frozenset({"compensation"})),
    )
    with_cap.start()
    try:
        assert with_cap._recovery.compensation is not None
    finally:
        with_cap.shutdown()

    without_cap = ApplicationHost(
        settings=settings,  # settings still enable compensation ...
        composition=replace(CP.all_in_one(), capabilities=frozenset()),  # ... composition omits it
    )
    without_cap.start()
    try:
        assert without_cap._recovery.compensation is None  # capability axis wins
    finally:
        without_cap.shutdown()


def test_webhook_gate_reads_composition_not_settings() -> None:
    """The webhook dispatcher is gated by composition.has('webhook'); settings.webhook_urls
    still configure it (refine, not bypass). Composition omitting 'webhook' wins over
    settings.enable_webhook_dispatcher."""
    settings = PalmSettings.for_tests(full_recovery=True).model_copy(
        update={
            "enable_webhook_dispatcher": True,
            "webhook_urls": ["https://example.test/hook"],
        }
    )

    with_cap = ApplicationHost(
        settings=settings,
        composition=replace(CP.all_in_one(), capabilities=frozenset({"webhook"})),
    )
    with_cap.start()
    try:
        assert with_cap._recovery._build_webhook_dispatcher() is not None
    finally:
        with_cap.shutdown()

    without_cap = ApplicationHost(
        settings=settings,  # settings still enable the dispatcher + provide urls ...
        composition=replace(CP.all_in_one(), capabilities=frozenset()),  # ... composition omits it
    )
    without_cap.start()
    try:
        assert without_cap._recovery._build_webhook_dispatcher() is None  # capability axis wins
    finally:
        without_cap.shutdown()


# ── 0.51.3: available (composition) and activated (deployment) ───────────────


def test_outbox_install_follows_dna_not_composition() -> None:
    """Outbox install follows DNA list, not composition write or the old recover AND."""
    settings = PalmSettings.for_tests(full_recovery=True)
    profile = DeploymentProfile.all_in_one()

    on = ApplicationHost(
        settings=settings,
        profile=profile,
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    on.start()
    try:
        assert not on.composition.has("outbox")
        rt = on.runtime()
        definition = rt.structure.definition
        assert definition is not None
        assert definition.has_capability(CAPABILITY_OUTBOX)
        assert CAPABILITY_OUTBOX in rt.structure.materialized_capabilities
        assert "outbox" in rt.supervisor.names()
        assert "outbox" in rt.supervisor.status()["running"]
    finally:
        on.shutdown()

    off = ApplicationHost(
        settings=settings,
        profile=profile,
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    off.start(structure_definition_id="local.embedded")
    try:
        rt = off.runtime()
        definition = rt.structure.definition
        assert definition is not None
        assert not definition.has_capability(CAPABILITY_OUTBOX)
        assert CAPABILITY_OUTBOX not in rt.structure.materialized_capabilities
        assert rt.supervisor is None or "outbox" not in rt.supervisor.names()
    finally:
        off.shutdown()


def test_work_drain_settings_side_routes_through_the_capability() -> None:
    """Drain install follows DNA list, not composition write or leftover flag."""
    settings = PalmSettings.for_tests(load_examples=False)
    profile = DeploymentProfile.all_in_one()

    on = ApplicationHost(
        settings=settings,
        profile=profile,
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    on.start()
    try:
        assert not on.composition.has("work_drain")
        rt = on.runtime()
        definition = rt.structure.definition
        assert definition is not None
        assert definition.has_capability(CAPABILITY_WORK_DRAIN)
        assert CAPABILITY_WORK_DRAIN in rt.structure.materialized_capabilities
        assert "work_drain" in rt.supervisor.names()
    finally:
        on.shutdown()

    off = ApplicationHost(
        settings=settings,
        profile=profile,
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    off.start(structure_definition_id="local.embedded")
    try:
        rt = off.runtime()
        definition = rt.structure.definition
        assert definition is not None
        assert not definition.has_capability(CAPABILITY_WORK_DRAIN)
        assert CAPABILITY_WORK_DRAIN not in rt.structure.materialized_capabilities
        assert rt.supervisor is None or "work_drain" not in rt.supervisor.names()
    finally:
        off.shutdown()


# ── 0.51.4: journal gated by the capability ──────────────────────────────────


def test_journal_gated_by_capability() -> None:
    """Journal wiring is gated by DNA ``has_capability('journal')`` (0.67.7).
    Default hosts list it on server/cli DNA; embedded omits it."""
    from palm.core.structure import CAPABILITY_JOURNAL

    default = ApplicationHost(settings=PalmSettings.for_tests(load_examples=False))
    default.start()
    try:
        assert default.admission.has_capability(CAPABILITY_JOURNAL)
        assert default.event_journal is not None
    finally:
        default.shutdown()

    lean = ApplicationHost(
        settings=PalmSettings.for_tests(load_examples=False),
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    lean.start(structure_definition_id="local.embedded")
    try:
        assert lean.event_journal is None  # DNA omit → no journal
    finally:
        lean.shutdown()


# ── 0.51.5: projections are a capability (the payoff — a lean ApplicationHost) ─


def test_projections_are_a_capability_lean_host_starts_without_them() -> None:
    """The projection layer is gated by DNA has_capability('projections'). Default hosts
    list it; lean “no projections” is embedded DNA, not empty composition on a server
    shape."""
    default = ApplicationHost(settings=PalmSettings.for_tests(load_examples=False))
    default.start()
    try:
        assert default.admission.has_capability(CAPABILITY_PROJECTIONS)
        assert default._instance_projection is not None
    finally:
        default.shutdown()

    lean = ApplicationHost(
        settings=PalmSettings.for_tests(load_examples=False),
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    lean.start(structure_definition_id="local.embedded")
    try:
        assert lean.is_started is True  # it assembles — the payoff of the theme
        assert not lean.admission.has_capability(CAPABILITY_PROJECTIONS)
        assert lean._instance_projection is None
        assert lean._job_board_projection is None
        assert lean._resource_projection is None
        assert lean.pattern_projection("wizard") is None
    finally:
        lean.shutdown()


def test_lean_host_serves_reads_direct_from_runtime() -> None:
    """0.51.6: a projection-less ApplicationHost serves reads via the standalone
    direct-from-runtime handlers — read-complete without a projection layer, and without
    dissolving ServerContext (see docs/SCOUT-0.51.6-serverctx-foldin.md). The reads return
    rather than raising "no handler for query"."""
    from palm.common.cqrs.query import GetJobStatusQuery, ListInstancesQuery, ListJobStatusQuery

    lean = ApplicationHost(
        settings=PalmSettings.for_tests(load_examples=False),
        composition=replace(CP.all_in_one(), capabilities=frozenset()),
    )
    lean.start(structure_definition_id="local.embedded")
    try:
        assert lean._instance_projection is None  # no projection layer ...
        # ... yet the read side works, served direct-from-runtime
        assert lean.ask(ListInstancesQuery(include_terminal=True)) == []
        assert lean.ask(ListJobStatusQuery()) == []
        assert lean.ask(GetJobStatusQuery(job_id="nope")) == {"found": False, "job_id": "nope"}
    finally:
        lean.shutdown()
