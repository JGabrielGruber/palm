"""NeonRoot provider (0.53.1 health · 0.53.2 spawn) — honest optional CLI."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from palm.core.registry import provider_registry
from palm.providers.neonroot.cli import NeonrootProbe, probe_neonroot
from palm.providers.neonroot.provider import NeonrootProvider
from palm.providers.neonroot.spawn import (
    build_spawn_argv,
    parse_spawn_params,
    run_spawn,
)


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


def test_parse_spawn_params_requires_image() -> None:
    with pytest.raises(ValueError, match="image"):
        parse_spawn_params({"command": ["true"]})


def test_parse_spawn_params_command_list() -> None:
    req = parse_spawn_params(
        {
            "image": "palm-ci",
            "command": ["just", "ci"],
            "vault": "palm-ci",
            "seed": "git-archive",
        }
    )
    assert req.image == "palm-ci"
    assert req.command == ("just", "ci")
    assert req.vault == "palm-ci"
    assert req.sandbox is True


def test_build_spawn_argv_sandbox_and_seed() -> None:
    req = parse_spawn_params(
        {
            "image": "palm-ci",
            "command": ["uv", "run", "python", "-c", "print(1)"],
            "vault": "palm-ci",
            "name": "palm-docs-build",
        }
    )
    argv = build_spawn_argv("/usr/bin/neonroot", req, seed_path="/tmp/seed")
    assert argv[:2] == ["/usr/bin/neonroot", "spawn"]
    assert "palm-docs-build" in argv
    assert "--image" in argv and "palm-ci" in argv
    assert "--vault" in argv and "palm-ci" in argv
    assert "--sandbox" in argv
    assert "--seed" in argv and "/tmp/seed" in argv
    assert "--" in argv
    assert argv[argv.index("--") + 1 :] == ["uv", "run", "python", "-c", "print(1)"]


def test_build_spawn_argv_seed_mode_bind() -> None:
    req = parse_spawn_params(
        {
            "image": "palm-docs",
            "command": ["true"],
            "seed": "/tmp/docs",
            "seed_mode": "bind",
        }
    )
    argv = build_spawn_argv("neonroot", req, seed_path="/tmp/docs")
    assert "--seed-mode" in argv
    assert "bind" in argv


def test_build_spawn_argv_exclude_and_output() -> None:
    req = parse_spawn_params(
        {
            "image": "palm-docs",
            "command": ["tailwindcss", "-i", "styles/input.css", "-o", "styles/output.css"],
            "seed_exclude": ["data/", ".venv/"],
            "outputs": [
                {"host": "docs/styles/output.css", "container": "styles/output.css"},
            ],
        }
    )
    root = Path("/repo")
    argv = build_spawn_argv(
        "neonroot",
        req,
        seed_path="/repo/docs",
        repo_root=root,
    )
    assert argv.count("--seed-exclude") == 2
    assert "data/" in argv and ".venv/" in argv
    assert "--output" in argv
    out_idx = argv.index("--output")
    assert argv[out_idx + 1].endswith("docs/styles/output.css:styles/output.css")


def test_parse_outputs_rejects_escape() -> None:
    with pytest.raises(ValueError, match="escape|relative"):
        parse_spawn_params(
            {
                "image": "x",
                "command": ["true"],
                "outputs": ["out.css:../etc/passwd"],
            }
        )


def test_build_spawn_argv_isolated_skips_sandbox_flag() -> None:
    req = parse_spawn_params(
        {
            "image": "ci",
            "command": ["true"],
            "isolated": True,
        }
    )
    argv = build_spawn_argv("neonroot", req, seed_path=None)
    assert "--isolated" in argv
    assert "--sandbox" not in argv


def test_spawn_missing_image(neonroot_provider: NeonrootProvider) -> None:
    result = neonroot_provider.invoke("spawn", params={"command": ["true"]})
    assert result.success is False
    assert "image" in (result.error or "").lower()


def test_spawn_success_via_mock(neonroot_provider: NeonrootProvider) -> None:
    payload = {
        "exit_code": 0,
        "duration_s": 0.1,
        "argv": ["neonroot", "spawn", "--image", "palm-ci", "--", "true"],
        "image": "palm-ci",
        "command": ["true"],
        "stdout_tail": "",
        "stderr_tail": "",
    }
    with patch("palm.providers.neonroot.provider.run_spawn", return_value=payload):
        result = neonroot_provider.invoke(
            "spawn",
            params={"image": "palm-ci", "command": ["true"]},
        )
    assert result.success is True
    assert result.data["exit_code"] == 0


def test_spawn_nonzero_exit_is_fail(neonroot_provider: NeonrootProvider) -> None:
    payload = {
        "exit_code": 2,
        "duration_s": 0.2,
        "argv": ["neonroot", "spawn", "--image", "palm-ci", "--", "false"],
        "image": "palm-ci",
        "command": ["false"],
        "stdout_tail": "",
        "stderr_tail": "boom",
    }
    with patch("palm.providers.neonroot.provider.run_spawn", return_value=payload):
        result = neonroot_provider.invoke(
            "spawn",
            params={"image": "palm-ci", "command": ["false"]},
        )
    assert result.success is False
    assert "exited 2" in (result.error or "")


def test_run_spawn_unavailable_raises() -> None:
    missing = NeonrootProbe(available=False, error="neonroot not found on PATH")
    with patch("palm.providers.neonroot.spawn.probe_neonroot", return_value=missing):
        with pytest.raises(RuntimeError, match="not found"):
            run_spawn({"image": "x", "command": ["true"]}, repo_root=Path.cwd())


def test_example_resource_definitions_shape() -> None:
    from examples.definitions.neonroot_runners import (
        NEONROOT_HEALTH,
        NEONROOT_SPAWN_DOCS_BUILD,
        NEONROOT_SPAWN_TRUE,
    )

    assert NEONROOT_HEALTH.provider == "neonroot"
    assert NEONROOT_HEALTH.action == "health"
    assert NEONROOT_SPAWN_TRUE.action == "spawn"
    assert NEONROOT_SPAWN_TRUE.params.get("seed") == "git-archive"
    assert NEONROOT_SPAWN_TRUE.params.get("command") == ["true"]
    assert "docs_build" in " ".join(NEONROOT_SPAWN_DOCS_BUILD.params.get("command") or [])


def test_resource_engine_invokes_neonroot_health(neonroot_provider: NeonrootProvider) -> None:
    """ResourceEngine path: definition-shaped invoke via provider=neonroot."""
    from palm.core.resource.engine import ResourceEngine

    engine = ResourceEngine()
    engine.initialize()
    # Engine resolves providers from registry; force our instance into the cache
    # so health can be mocked without a second connect race.
    engine._active["neonroot"] = neonroot_provider

    present = NeonrootProbe(
        available=True,
        path="/usr/bin/neonroot",
        version="NeonRoot 0.0.2",
    )
    with patch("palm.providers.neonroot.provider.probe_neonroot", return_value=present):
        result = engine.invoke(provider="neonroot", action="health", params={})
    assert result.success is True
    assert result.data["available"] is True
