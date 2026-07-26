"""Hermetic job contract + dogfood definitions (0.54.1-0.54.2)."""

from __future__ import annotations

import pytest

from palm.providers.neonroot.contract import (
    HERMETIC_JOB_SPAWN_FIELDS,
    hermetic_job_summary,
    validate_hermetic_job_params,
)


def test_validate_requires_image_and_command() -> None:
    with pytest.raises(ValueError, match="image"):
        validate_hermetic_job_params({"command": ["true"]})
    with pytest.raises(ValueError, match="command"):
        validate_hermetic_job_params({"image": "palm-ci"})


def test_validate_spawn_contract_shape() -> None:
    req = validate_hermetic_job_params(
        {
            "image": "palm-ci",
            "command": ["true"],
            "seed": "git-archive",
            "seed_exclude": ["data/", ".venv/"],
            "outputs": [{"host": "/tmp/out.txt", "container": "out.txt"}],
            "vault": "palm-ci",
            "sandbox": True,
        }
    )
    assert req.image == "palm-ci"
    assert req.command == ("true",)
    assert req.seed == "git-archive"
    assert "data/" in req.seed_exclude
    assert any(o.endswith("out.txt") for o in req.outputs)

    summary = hermetic_job_summary(req)
    assert summary["kind"] == "hermetic_job"
    assert summary["provider"] == "neonroot"
    assert set(summary["command"]) == {"true"}


def test_known_fields_documented() -> None:
    assert "image" in HERMETIC_JOB_SPAWN_FIELDS
    assert "command" in HERMETIC_JOB_SPAWN_FIELDS
    assert "outputs" in HERMETIC_JOB_SPAWN_FIELDS


def test_hermetic_job_smoke_definitions() -> None:
    from examples.definitions.hermetic_job_smoke import (
        HERMETIC_JOB_SMOKE_FLOW,
        HERMETIC_PREFLIGHT,
        HERMETIC_TRUE_JOB,
        register_definitions,
    )

    assert HERMETIC_PREFLIGHT.provider == "neonroot"
    assert HERMETIC_PREFLIGHT.action == "health"
    assert HERMETIC_TRUE_JOB.action == "spawn"
    assert HERMETIC_TRUE_JOB.params["image"] == "palm-ci"
    # Contract params validate
    validate_hermetic_job_params(dict(HERMETIC_TRUE_JOB.params))

    steps = HERMETIC_JOB_SMOKE_FLOW.options["steps"]
    assert [s["resource_ref"] for s in steps] == [
        "hermetic-preflight",
        "hermetic-true-job",
    ]
    # Only neonroot — purpose-test constraint
    assert all(
        r.provider == "neonroot" for r in (HERMETIC_PREFLIGHT, HERMETIC_TRUE_JOB)
    )

    class _Repo:
        def __init__(self) -> None:
            self.n = 0

        def save_resource(self, _r):
            self.n += 1

        def save_flow(self, _f):
            self.n += 1

        def save_process(self, _p):
            self.n += 1

    repo = _Repo()
    register_definitions(repo)
    # 2 resources + 2 flows + 2 processes (smoke wizard + dag)
    assert repo.n == 6
