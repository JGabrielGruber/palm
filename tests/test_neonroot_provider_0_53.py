"""NeonRoot provider scaffold (0.53.1) — health + honest optional CLI."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from palm.core.registry import provider_registry
from palm.providers.neonroot.cli import NeonrootProbe, probe_neonroot
from palm.providers.neonroot.provider import NeonrootProvider


@pytest.fixture
def neonroot_provider() -> NeonrootProvider:
    import palm.providers  # noqa: F401 — ensure autoload

    cls = provider_registry.get("neonroot")
    assert cls is NeonrootProvider
    p = cls(name="neonroot")
    p.connect()
    return p


def test_neonroot_registered_in_provider_registry() -> None:
    import palm.providers  # noqa: F401

    assert provider_registry.get("neonroot") is NeonrootProvider


def test_neonroot_app_manifest() -> None:
    import palm.providers  # noqa: F401
    from palm.common.providers._registry import get_provider_app

    app = get_provider_app("neonroot")
    assert app is not None
    assert app.name == "neonroot"
    assert "health" in app.actions
    assert "spawn" in app.actions


def test_describe_lists_health_and_spawn(neonroot_provider: NeonrootProvider) -> None:
    desc = neonroot_provider.describe()
    names = {a.name for a in desc.actions}
    assert "health" in names
    assert "spawn" in names


def test_spawn_not_yet_implemented(neonroot_provider: NeonrootProvider) -> None:
    result = neonroot_provider.invoke("spawn", params={"command": ["true"]})
    assert result.success is False
    assert result.error is not None
    assert "not implemented" in result.error.lower()


def test_health_invoke_when_missing(neonroot_provider: NeonrootProvider) -> None:
    missing = NeonrootProbe(available=False, error="neonroot not found on PATH")
    with patch("palm.providers.neonroot.provider.probe_neonroot", return_value=missing):
        result = neonroot_provider.invoke("health")
        h = neonroot_provider.health()
    assert result.success is False
    assert h.healthy is False
    assert "not found" in (h.message or "").lower() or "not found" in (result.error or "").lower()


def test_health_invoke_when_present(neonroot_provider: NeonrootProvider) -> None:
    present = NeonrootProbe(
        available=True,
        path="/usr/bin/neonroot",
        version="NeonRoot 0.0.2",
    )
    with patch("palm.providers.neonroot.provider.probe_neonroot", return_value=present):
        result = neonroot_provider.invoke("health")
        h = neonroot_provider.health()
    assert result.success is True
    assert result.data["available"] is True
    assert result.data["version"] == "NeonRoot 0.0.2"
    assert h.healthy is True


def test_probe_neonroot_live_smoke() -> None:
    """Smoke: if neonroot is on this machine, probe succeeds; otherwise honest miss."""
    probe = probe_neonroot()
    assert isinstance(probe.available, bool)
    if probe.available:
        assert probe.path
    else:
        assert probe.error
